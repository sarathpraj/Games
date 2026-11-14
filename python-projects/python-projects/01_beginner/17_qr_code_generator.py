"""
17 - QR Code Generator
======================
Turn any text or link into a QR code image (PNG) you can scan with your phone.

This is your first project that needs a THIRD-PARTY library. Install it once:
    pip install "qrcode[pil]"

Concepts you'll practise:
  - Installing and importing a library with pip
  - Handling a missing library with try / except ImportError
  - Reading a library's options (version, error_correction, box_size, border)
  - Cleaning text so it's a safe filename

Run:  python 17_qr_code_generator.py

Challenges:
  1. Make a Wi-Fi QR code. The text format is:  WIFI:T:WPA;S:<network>;P:<password>;;
  2. Read a list of links from a CSV and create one QR code per row.
  3. Put a small logo in the middle (look up Pillow's Image.paste).
"""
from pathlib import Path

try:
    import qrcode
except ImportError:
    print('This project needs the "qrcode" library. Install it with:')
    print('    pip install "qrcode[pil]"')
    raise SystemExit(1)

OUTPUT_FOLDER = Path(__file__).parent


def safe_filename(text):
    """'My Website!' -> 'My_Website.png'"""
    cleaned = "".join(ch for ch in text if ch.isalnum() or ch in "-_ ").strip()
    return (cleaned or "qrcode").replace(" ", "_") + ".png"


def make_qr(data, filename, fill_color="black", back_color="white"):
    qr = qrcode.QRCode(
        version=None,                                        # None = smallest size that fits
        error_correction=qrcode.constants.ERROR_CORRECT_M,   # still scans if ~15% is damaged
        box_size=10,                                         # pixels per little square
        border=4,                                            # white margin (4 is the standard)
    )
    qr.add_data(data)
    qr.make(fit=True)
    image = qr.make_image(fill_color=fill_color, back_color=back_color)
    path = OUTPUT_FOLDER / filename
    image.save(path)
    return qr, path


def main():
    print("=== QR Code Generator ===")
    while True:
        data = input("\nText or link to encode (Enter to quit): ").strip()
        if not data:
            print("Bye!")
            break
        filename = safe_filename(input("File name [qrcode]: ").strip())
        colour = input("Colour, e.g. black, navy, darkgreen [black]: ").strip() or "black"

        try:
            qr, path = make_qr(data, filename, fill_color=colour)
        except ValueError:
            print(f"  '{colour}' isn't a colour I know. Try again with 'black'.")
            continue

        qr.print_ascii(invert=True)       # quick preview right in the terminal
        print(f"Saved: {path}")


if __name__ == "__main__":
    main()
