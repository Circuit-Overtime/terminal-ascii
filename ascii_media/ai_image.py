import argparse
import requests
import sys
import os
import mimetypes
import tempfile
import cv2
import shutil
from .ascii import frame_to_ascii
from .terminal import move_cursor_top, hide_cursor, show_cursor, set_terminal_size

API_URL = "https://image.pollinations.ai/prompt/"
VALID_IMAGE_MIME_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp", "image/bmp"}

def fetch_image_from_api(prompt, model="flux-core", width=512, height=512, nologo=True, enhance=False):
    encoded_prompt = requests.utils.quote(prompt)
    url = f"{API_URL}{encoded_prompt}?width={width}&height={height}&nologo={str(nologo).lower()}&enhance={str(enhance).lower()}&model={model}"

    response = requests.get(url, timeout=300)  # long timeout
    if response.status_code == 200:
        # Write raw image data directly to a temp file
        temp = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        temp.write(response.content)
        temp.close()
        return temp.name  # Return path to the image
    else:
        raise Exception(f"Failed to fetch image: {response.status_code} - {response.text}")


def download_image(url):
    response = requests.get(url, stream=True)
    content_type = response.headers.get("Content-Type", "").lower()
    if content_type not in VALID_IMAGE_MIME_TYPES:
        raise ValueError(f"URL is not a valid image. Got: {content_type}")

    ext = mimetypes.guess_extension(content_type) or ".jpg"
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
    for chunk in response.iter_content(8192):
        temp.write(chunk)
    temp.close()
    return temp.name

def display_image_ascii(path, color=True, width=100, fit=True, mode="HD"):
    image = cv2.imread(path)
    if image is None:
        print("[Error] Could not load image.", file=sys.stderr)
        return

    if fit:
        try:
            term_size = os.get_terminal_size()
            terminal_height = term_size.lines - 2
            aspect = image.shape[1] / image.shape[0]
            width = int((terminal_height / 0.55) * aspect)
            set_terminal_size(width + 2, terminal_height + 2)
        except OSError:
            print("[Warning] Terminal sizing failed; using default width.", file=sys.stderr)

    resized = cv2.resize(image, (width, int(width / (image.shape[1] / image.shape[0]))), interpolation=cv2.INTER_AREA)
    if not color:
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        ascii_art = frame_to_ascii(gray, width=width, color=False, mode=mode)
    else:
        ascii_art = frame_to_ascii(resized, width=width, color=True, mode=mode)

    hide_cursor()
    try:
        move_cursor_top()
        sys.stdout.write(ascii_art)
        sys.stdout.flush()
    finally:
        show_cursor()
        os.remove(path)

def main(args):
    try:
        print(f"Generating image from prompt: {args.prompt}")
        image_path = fetch_image_from_api(
            prompt=args.prompt,
            model=args.model or "flux-core",
            width=args.width or 512,
            height=args.height or 512,
            nologo=args.nologo or True,
            enhance=args.enhance or False
        )

        if args.download:
            save_name = f"{args.prompt.replace(' ', '_')[:40]}.jpg"
            save_path = os.path.join(os.getcwd(), save_name)
            import shutil
            shutil.copyfile(image_path, save_path)
            os.remove(image_path)
            print(f"[Saved] Image saved as: {save_path}")
        else:
            display_image_ascii(image_path, color=not args.nocolor, width=args.width, fit=args.fit, mode=args.mode)

    except Exception as e:
        print(f"[Error] {e}", file=sys.stderr)

