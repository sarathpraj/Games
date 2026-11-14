#!/usr/bin/env python3
"""
pipal_main.py — PiPal AI Desktop Robot
========================================
Hardware: Raspberry Pi Zero 2W
AI:       Claude Haiku (claude-haiku-4-5-20251001)
Display:  0.96" OLED SSD1306 (I2C, address 0x3C)
Motors:   2× TT motors via L298N driver
Audio:    USB sound card + USB mic + PAM8403 + 3W speaker
Input:    Push button on GPIO 17

WIRING SUMMARY
--------------
L298N:  IN1=GPIO18, IN2=GPIO23, IN3=GPIO24, IN4=GPIO25
OLED:   SDA=GPIO2,  SCL=GPIO3
Button: GPIO17 (other leg to GND)
OLED:   VCC=3.3V, GND, SDA=GPIO2, SCL=GPIO3

SETUP (run once on your Pi)
----------------------------
  sudo apt install -y espeak python3-pyaudio i2c-tools portaudio19-dev
  pip3 install anthropic SpeechRecognition luma.oled Pillow --break-system-packages
  export ANTHROPIC_API_KEY="sk-ant-your-key-here"

  # Find your USB mic device index:
  python3 -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())"
  # Set MIC_DEVICE_INDEX below to the index of your USB microphone.
"""

import os
import time
import random
import threading
import subprocess

# ── optional imports (gracefully degrade if not on a Pi) ─────────────────────
try:
    import RPi.GPIO as GPIO
    ON_PI = True
except ImportError:
    ON_PI = False
    print("[WARN] RPi.GPIO not found — running in simulation mode (no motors/button)")

try:
    from luma.core.interface.serial import i2c as I2C_serial
    from luma.oled.device import ssd1306
    from luma.core.render import canvas
    from PIL import ImageFont
    OLED_AVAILABLE = True
except ImportError:
    OLED_AVAILABLE = False
    print("[WARN] luma.oled not found — OLED face disabled")

import speech_recognition as sr
import anthropic

# ─────────────────────────────────────────────────────────────────────────────
#  CONFIGURATION  —  edit these to match your build
# ─────────────────────────────────────────────────────────────────────────────

# GPIO pin numbers (BCM mode)
M_L_IN1   = 18   # Left motor  — forward
M_L_IN2   = 23   # Left motor  — backward
M_R_IN3   = 24   # Right motor — forward
M_R_IN4   = 25   # Right motor — backward
BTN_PIN   = 17   # Wake button

# Audio
MIC_DEVICE_INDEX = 1    # Run list_microphone_names() to confirm index
LISTEN_TIMEOUT   = 6    # seconds to wait for speech before giving up
PHRASE_TIMEOUT   = 4    # max seconds of silence within a phrase

# Claude API
CLAUDE_MODEL   = "claude-haiku-4-5-20251001"
MAX_TOKENS     = 150    # keep responses short and snappy
MAX_HISTORY    = 20     # conversation turns to keep in memory

# Movement durations (seconds)
MOVE_DURATION  = 0.7
TURN_DURATION  = 0.45
DANCE_STEPS    = 4

# ─────────────────────────────────────────────────────────────────────────────
#  SYSTEM PROMPT
# ─────────────────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are PiPal, a cheerful AI desktop robot with wheels.
Keep ALL responses under 2 sentences and sound playful and curious.
When you want to physically move, embed ONE command (no more) in your response using this exact format:
  [MOVE:forward]  [MOVE:backward]  [MOVE:left]  [MOVE:right]  [MOVE:dance]
Example: "Sure! [MOVE:forward] Rolling over to check that out!"
If someone asks you to move or dance, always include a movement command.
Never explain what the brackets mean."""

# ─────────────────────────────────────────────────────────────────────────────
#  GPIO SETUP
# ─────────────────────────────────────────────────────────────────────────────

def setup_gpio():
    if not ON_PI:
        return
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    motor_pins = [M_L_IN1, M_L_IN2, M_R_IN3, M_R_IN4]
    for pin in motor_pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
    GPIO.setup(BTN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# ─────────────────────────────────────────────────────────────────────────────
#  MOTOR CONTROL
# ─────────────────────────────────────────────────────────────────────────────

def motors_stop():
    if not ON_PI:
        return
    for pin in [M_L_IN1, M_L_IN2, M_R_IN3, M_R_IN4]:
        GPIO.output(pin, GPIO.LOW)

def motors_forward():
    if not ON_PI:
        print("[MOTOR] Forward")
        return
    GPIO.output(M_L_IN1, GPIO.HIGH); GPIO.output(M_L_IN2, GPIO.LOW)
    GPIO.output(M_R_IN3, GPIO.HIGH); GPIO.output(M_R_IN4, GPIO.LOW)

def motors_backward():
    if not ON_PI:
        print("[MOTOR] Backward")
        return
    GPIO.output(M_L_IN1, GPIO.LOW);  GPIO.output(M_L_IN2, GPIO.HIGH)
    GPIO.output(M_R_IN3, GPIO.LOW);  GPIO.output(M_R_IN4, GPIO.HIGH)

def motors_turn_left():
    if not ON_PI:
        print("[MOTOR] Turn left")
        return
    GPIO.output(M_L_IN1, GPIO.LOW);  GPIO.output(M_L_IN2, GPIO.HIGH)
    GPIO.output(M_R_IN3, GPIO.HIGH); GPIO.output(M_R_IN4, GPIO.LOW)

def motors_turn_right():
    if not ON_PI:
        print("[MOTOR] Turn right")
        return
    GPIO.output(M_L_IN1, GPIO.HIGH); GPIO.output(M_L_IN2, GPIO.LOW)
    GPIO.output(M_R_IN3, GPIO.LOW);  GPIO.output(M_R_IN4, GPIO.HIGH)

def do_move(command):
    """Execute a parsed movement command from AI response."""
    moves = {
        "forward":  (motors_forward,   MOVE_DURATION),
        "backward": (motors_backward,  MOVE_DURATION),
        "left":     (motors_turn_left,  TURN_DURATION),
        "right":    (motors_turn_right, TURN_DURATION),
    }
    if command == "dance":
        print("[MOTOR] Dance!")
        for _ in range(DANCE_STEPS):
            motors_forward();    time.sleep(0.25)
            motors_backward();   time.sleep(0.25)
            motors_turn_left();  time.sleep(0.2)
            motors_turn_right(); time.sleep(0.2)
            motors_stop();       time.sleep(0.1)
    elif command in moves:
        fn, dur = moves[command]
        fn()
        time.sleep(dur)
        motors_stop()

def parse_and_execute_move(text):
    """Find [MOVE:xxx] in text, execute it, and return cleaned text."""
    import re
    match = re.search(r'\[MOVE:(\w+)\]', text, re.IGNORECASE)
    if match:
        cmd = match.group(1).lower()
        threading.Thread(target=do_move, args=(cmd,), daemon=True).start()
        text = re.sub(r'\[MOVE:\w+\]\s*', '', text, flags=re.IGNORECASE).strip()
    return text

# ─────────────────────────────────────────────────────────────────────────────
#  OLED FACE EXPRESSIONS
# ─────────────────────────────────────────────────────────────────────────────

oled_device = None

def setup_oled():
    global oled_device
    if not OLED_AVAILABLE:
        return
    try:
        serial = I2C_serial(port=1, address=0x3C)
        oled_device = ssd1306(serial)
        print("[OLED] Display initialised at 0x3C")
    except Exception as e:
        print(f"[OLED] Init failed: {e}")
        oled_device = None

def draw_face(expression="idle"):
    """
    Draw face on OLED. Expressions: idle, happy, listening, thinking, talking.
    OLED is 128×64 pixels, white-on-black.
    Left eye centred at (40, 25), Right eye at (88, 25).
    """
    if not OLED_AVAILABLE or oled_device is None:
        return

    with canvas(oled_device) as draw:
        if expression == "idle":
            # Normal open eyes + gentle smile
            draw.ellipse([20, 10, 60, 40], outline="white", fill="white")
            draw.ellipse([30, 18, 50, 32], outline="black", fill="black")   # left pupil
            draw.ellipse([68, 10, 108, 40], outline="white", fill="white")
            draw.ellipse([78, 18, 98, 32], outline="black", fill="black")   # right pupil
            draw.arc([30, 44, 98, 60], start=0, end=180, fill="white", width=2)

        elif expression == "happy":
            # Curved ^^ eyes + big smile
            draw.arc([20, 10, 60, 40], start=180, end=360, fill="white", width=3)
            draw.arc([68, 10, 108, 40], start=180, end=360, fill="white", width=3)
            draw.arc([20, 40, 108, 62], start=0, end=180, fill="white", width=3)

        elif expression == "listening":
            # Wide surprised eyes + flat mouth
            draw.ellipse([16, 6, 62, 42], outline="white", fill="white")
            draw.ellipse([28, 16, 50, 32], outline="black", fill="black")
            draw.ellipse([66, 6, 112, 42], outline="white", fill="white")
            draw.ellipse([78, 16, 100, 32], outline="black", fill="black")
            draw.line([44, 56, 84, 56], fill="white", width=2)

        elif expression == "thinking":
            # One squinted eye (line) + one open + diagonal mouth
            draw.ellipse([20, 10, 60, 40], outline="white", fill="white")
            draw.ellipse([30, 18, 50, 32], outline="black", fill="black")
            draw.line([68, 25, 108, 25], fill="white", width=5)             # squint
            draw.line([38, 52, 80, 58], fill="white", width=2)              # angled mouth

        elif expression == "talking":
            # Normal eyes + open circular mouth
            draw.ellipse([20, 8, 58, 38], outline="white", fill="white")
            draw.ellipse([29, 15, 49, 31], outline="black", fill="black")
            draw.ellipse([70, 8, 108, 38], outline="white", fill="white")
            draw.ellipse([79, 15, 99, 31], outline="black", fill="black")
            draw.ellipse([46, 44, 82, 62], outline="white", fill="white")   # open mouth
            draw.ellipse([51, 48, 77, 58], outline="black", fill="black")   # mouth interior

# ─────────────────────────────────────────────────────────────────────────────
#  IDLE ANIMATION (background thread)
# ─────────────────────────────────────────────────────────────────────────────

_idle_active = True
_current_expression = "idle"

def idle_animation_loop():
    """Occasionally blink or look around while idle."""
    while True:
        time.sleep(random.uniform(3, 7))
        if _current_expression != "idle":
            continue
        # Quick blink effect: briefly draw without eyes, then restore
        if OLED_AVAILABLE and oled_device is not None:
            try:
                with canvas(oled_device) as draw:
                    # Closed eyes (lines) + smile
                    draw.line([20, 25, 60, 25], fill="white", width=4)
                    draw.line([68, 25, 108, 25], fill="white", width=4)
                    draw.arc([30, 44, 98, 60], start=0, end=180, fill="white", width=2)
                time.sleep(0.12)
                draw_face("idle")
            except Exception:
                pass

def set_expression(expr):
    global _current_expression
    _current_expression = expr
    draw_face(expr)

# ─────────────────────────────────────────────────────────────────────────────
#  TEXT-TO-SPEECH
# ─────────────────────────────────────────────────────────────────────────────

def speak(text):
    """Speak text via espeak. Voice: en+m3 (male, friendly)."""
    if not text.strip():
        return
    print(f"[PIPAL] {text}")
    set_expression("talking")
    try:
        subprocess.run(
            ["espeak", "-v", "en+m3", "-s", "145", "-p", "58", text],
            check=True,
            timeout=30
        )
    except (subprocess.SubprocessError, FileNotFoundError) as e:
        print(f"[WARN] espeak failed: {e}")
    set_expression("idle")

# ─────────────────────────────────────────────────────────────────────────────
#  SPEECH RECOGNITION
# ─────────────────────────────────────────────────────────────────────────────

recognizer = sr.Recognizer()
recognizer.energy_threshold = 300   # lower = more sensitive
recognizer.dynamic_energy_threshold = True

def listen_for_speech():
    """
    Record from USB mic and return recognised text, or None on failure.
    If MIC_DEVICE_INDEX causes errors, try setting it to 0 or 2.
    """
    set_expression("listening")
    try:
        with sr.Microphone(device_index=MIC_DEVICE_INDEX) as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("[LISTEN] Listening...")
            audio = recognizer.listen(
                source,
                timeout=LISTEN_TIMEOUT,
                phrase_time_limit=PHRASE_TIMEOUT
            )
        print("[LISTEN] Processing speech...")
        set_expression("thinking")
        text = recognizer.recognize_google(audio)
        print(f"[HEARD] {text}")
        return text
    except sr.WaitTimeoutError:
        print("[LISTEN] Timed out — no speech detected")
        return None
    except sr.UnknownValueError:
        print("[LISTEN] Could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"[LISTEN] Google STT error: {e}")
        return None
    except Exception as e:
        print(f"[LISTEN] Unexpected error: {e}")
        return None
    finally:
        set_expression("idle")

# ─────────────────────────────────────────────────────────────────────────────
#  CLAUDE AI
# ─────────────────────────────────────────────────────────────────────────────

client      = anthropic.Anthropic()   # reads ANTHROPIC_API_KEY from env
history     = []                       # conversation memory

def ask_claude(user_text):
    """Send user message to Claude Haiku, return AI reply text."""
    history.append({"role": "user", "content": user_text})

    # Keep only the most recent turns to stay within context limits
    trimmed = history[-MAX_HISTORY:]

    set_expression("thinking")
    try:
        response = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=MAX_TOKENS,
            system=SYSTEM_PROMPT,
            messages=trimmed
        )
        reply = response.content[0].text.strip()
    except anthropic.APIConnectionError:
        reply = "Hmm, I can't reach the internet right now. Try again in a moment!"
    except anthropic.APIStatusError as e:
        reply = f"My brain got a hiccup — error {e.status_code}. Try again?"
    except Exception as e:
        reply = "Oops, something went wrong with my thinking circuits!"
        print(f"[ERROR] Claude API: {e}")

    history.append({"role": "assistant", "content": reply})
    return reply

# ─────────────────────────────────────────────────────────────────────────────
#  BUTTON HANDLING
# ─────────────────────────────────────────────────────────────────────────────

def wait_for_button():
    """Block until the wake button is pressed (GPIO LOW = pressed)."""
    if not ON_PI:
        print("[BUTTON] Press Enter to simulate button press...")
        input()
        return
    print("[WAIT] Press the wake button to talk to PiPal...")
    while GPIO.input(BTN_PIN) == GPIO.HIGH:
        time.sleep(0.05)
    # Debounce
    time.sleep(0.05)
    while GPIO.input(BTN_PIN) == GPIO.LOW:
        time.sleep(0.05)

# ─────────────────────────────────────────────────────────────────────────────
#  MAIN LOOP
# ─────────────────────────────────────────────────────────────────────────────

def main():
    print("=" * 50)
    print("  PiPal AI Robot — starting up")
    print("=" * 50)

    # Check API key
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("[ERROR] ANTHROPIC_API_KEY not set in environment.")
        print("  Run: export ANTHROPIC_API_KEY='sk-ant-...'")
        return

    setup_gpio()
    setup_oled()

    # Start idle blink animation in background
    blink_thread = threading.Thread(target=idle_animation_loop, daemon=True)
    blink_thread.start()

    # Greeting
    draw_face("happy")
    speak("Hi there! I'm PiPal. Press my button and let's chat!")
    draw_face("idle")

    try:
        while True:
            wait_for_button()

            # Play a short acknowledgment tone / feedback
            draw_face("listening")
            if ON_PI:
                subprocess.run(
                    ["espeak", "-v", "en+m3", "-s", "200", "mm"],
                    check=False, timeout=2
                )

            # Listen
            speech = listen_for_speech()
            if speech is None:
                draw_face("idle")
                speak("I didn't catch that — try again?")
                continue

            # Think
            draw_face("thinking")
            reply = ask_claude(speech)

            # Parse movement command before speaking
            clean_reply = parse_and_execute_move(reply)

            # Speak the cleaned reply
            speak(clean_reply)
            draw_face("idle")

    except KeyboardInterrupt:
        print("\n[EXIT] Shutting down PiPal...")
        speak("Bye! Until next time!")
    finally:
        draw_face("idle")
        if ON_PI:
            motors_stop()
            GPIO.cleanup()
        print("[EXIT] Cleanup complete.")

# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    main()
