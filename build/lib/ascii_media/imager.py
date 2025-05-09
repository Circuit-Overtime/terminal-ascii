import time
import sys
import os
import argparse
import cv2
import keyboard
import requests
import mimetypes
import tempfile

from .ascii import frame_to_ascii
from .terminal import move_cursor_top, hide_cursor, show_cursor, set_terminal_size

VALID_IMAGE_MIME_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp", "image/bmp"}

def is_url(path):
    return path.startswith("http://") or path.startswith("https://")

def download_image(url):
    response = requests.get(url, stream=True)
    content_type = response.headers.get("Content-Type", "").lower()
    if content_type not in VALID_IMAGE_MIME_TYPES:
        raise ValueError(f"URL does not point to a valid image. Detected: {content_type}")
    
    extension = mimetypes.guess_extension(content_type) or ".jpg"
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=extension)
    for chunk in response.iter_content(chunk_size=8192):
        temp_file.write(chunk)
    temp_file.close()
    return temp_file.name

def open_image(image_path):
    return cv2.imread(image_path)

def get_image_dimensions(image):
    return image.shape[1], image.shape[0]  # width, height

def resize_image(image, width):
    height, width_original = image.shape[:2]
    aspect_ratio = width_original / height
    new_height = int(width / aspect_ratio)
    return cv2.resize(image, (width, new_height), interpolation=cv2.INTER_AREA)

def play_image_ascii(image_path, color=True, width=100, fit=True):
    temp_file = None

    if is_url(image_path):
        try:
            temp_file = download_image(image_path)
            image_path = temp_file
        except Exception as e:
            print(f"[Error] Could not download image: {e}", file=sys.stderr)
            return

    image = open_image(image_path)
    if image is None:
        print("[Error] Unable to read the image.", file=sys.stderr)
        return

    image_width, image_height = get_image_dimensions(image)
    aspect_ratio = image_width / image_height

    if fit:
        try:
            term_size = os.get_terminal_size()
            terminal_height = term_size.lines - 2
            adjusted_width = int((terminal_height / 0.55) * aspect_ratio)
            width = adjusted_width
            set_terminal_size(adjusted_width + 2, terminal_height + 2)
        except OSError:
            print("Warning: Could not fit to terminal. Using default width.", file=sys.stderr)

    hide_cursor()

    try:
        while True:
            if keyboard.is_pressed('q'):
                break

            if keyboard.is_pressed('p'):
                time.sleep(0.3)

            resized_image = resize_image(image, width)

            if color:
                ascii_art = frame_to_ascii(resized_image, width=width, color=True)
            else:
                gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
                enhanced_gray = clahe.apply(gray)
                ascii_art = frame_to_ascii(enhanced_gray, width=width, color=False)

            move_cursor_top()
            sys.stdout.write(ascii_art)
            sys.stdout.flush()

            time.sleep(0.1)

    except KeyboardInterrupt:
        pass
    finally:
        show_cursor()
        if temp_file:
            os.remove(temp_file)

def main():
    parser = argparse.ArgumentParser(description="Render an image as ASCII art in your terminal.")
    parser.add_argument("image_path", help="Path or URL to the image file")
    parser.add_argument("--nocolor", action="store_true", help="Disable colored ASCII output")
    parser.add_argument("--width", type=int, default=100, help="Set custom ASCII width")
    parser.add_argument("--fit", action="store_true", default=True, help="Fit ASCII to terminal size")

    args = parser.parse_args()
    play_image_ascii(
        image_path=args.image_path,
        color=not args.nocolor,
        width=args.width,
        fit=args.fit,
    )
