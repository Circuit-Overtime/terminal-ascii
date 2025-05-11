import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

GRADIENT = "░▒▓█@#$%&*^()_+`-={}[]|:;\"'<>,.?/abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def load_test_image(image_path: str) -> np.ndarray:
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"[-] Test image not found at {image_path}")
    image = cv2.imread(image_path)
    return image


def image_to_ascii_image(img, width=320, font_size=6, output="ascii_output.png", colored=True):
    h, w = img.shape[:2]
    aspect_ratio = w / h
    new_height = int(width / aspect_ratio * 0.55)
    resized = cv2.resize(img, (width, new_height), interpolation=cv2.INTER_AREA)

    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    color = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)

    ascii_chars = GRADIENT
    grad_len = len(ascii_chars)

    try:
        font = ImageFont.truetype("DejaVuSansMono.ttf", font_size)
    except:
        font = ImageFont.load_default()

    bbox = font.getbbox("A")
    char_width, char_height = bbox[2] - bbox[0], bbox[3] - bbox[1]

    img_width = char_width * width
    img_height = char_height * new_height

    output_img = Image.new("RGB", (img_width, img_height), color=(0, 0, 0))
    draw = ImageDraw.Draw(output_img)

    for y in range(new_height):
        for x in range(width):
            brightness = gray[y, x] / 255.0
            index = int(brightness * (grad_len - 1))
            char = ascii_chars[index]
            if colored:
                r, g, b = color[y, x]
                draw.text((x * char_width, y * char_height), char, font=font, fill=(r, g, b))
            else:
                gray_value = int(brightness * 255)
                draw.text((x * char_width, y * char_height), char, font=font, fill=(gray_value, gray_value, gray_value))

    output_img.save(output)
    print(f"[+] ASCII image saved to {output}")


def main():
    test_image_path = "test4.jpg"  # Replace with the path to your test image
    image = load_test_image(test_image_path)
    colored = False  # Set to False for black-and-white output
    image_to_ascii_image(image, width=320, font_size=16, colored=colored)


if __name__ == "__main__":
    main()