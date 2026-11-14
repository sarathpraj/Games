"""
14 - Alarm Clock
================
Set an alarm for a time of day. The terminal shows a live countdown
and rings (beeps) when the time arrives. Press Ctrl+C to cancel.

Concepts you'll practise:
  - The datetime module: datetime, time, timedelta
  - Parsing text into a time with strptime("%H:%M")
  - Date maths: if 07:00 has already passed today, the alarm is for tomorrow
  - time.sleep() to wait
  - print(..., end="\\r") to overwrite the same line (a live countdown)
  - Catching KeyboardInterrupt (Ctrl+C) to exit politely

Run:  python 14_alarm_clock.py

Challenges:
  1. Add snooze: after ringing, ask "Snooze 5 minutes? (y/n)".
  2. Allow several alarms at once (store them in a list).
  3. Play a sound file instead of a beep (you'll use pygame in project 18).
"""
import time
from datetime import datetime, timedelta


def ask_alarm_time():
    while True:
        text = input("Alarm time (24-hour HH:MM, e.g. 07:30 or 18:05): ").strip()
        try:
            return datetime.strptime(text, "%H:%M").time()
        except ValueError:
            print("  Please use the format HH:MM.")


def next_occurrence(alarm_time):
    """The next datetime when the clock shows alarm_time (today or tomorrow)."""
    now = datetime.now()
    target = datetime.combine(now.date(), alarm_time)
    if target <= now:
        target += timedelta(days=1)
    return target


def format_seconds(total_seconds):
    hours, remainder = divmod(total_seconds, 3600)   # divmod gives (quotient, remainder)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def ring(label, times=5):
    for _ in range(times):
        print(f"\a*** ALARM: {label.upper()} ***")   # \a = terminal bell (beep)
        time.sleep(1)


def main():
    print("=== Alarm Clock ===")
    alarm_time = ask_alarm_time()
    label = input("Alarm label [Wake up!]: ").strip() or "Wake up!"
    target = next_occurrence(alarm_time)
    print(f"\nAlarm set for {target:%A %H:%M}. Press Ctrl+C to cancel.\n")

    try:
        while True:
            seconds_left = int((target - datetime.now()).total_seconds())
            if seconds_left <= 0:
                break
            print(f"\r  Time left: {format_seconds(seconds_left)} ", end="", flush=True)
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nAlarm cancelled.")
        return

    print()
    ring(label)


if __name__ == "__main__":
    main()
