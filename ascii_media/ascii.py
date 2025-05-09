import numpy as np
import cv2

# Gradient Modes
ASCII_GRADIENT_LD = " ░▒▓█"
ASCII_GRADIENT_SD = " ░▒▓▓█▒▓█▓▒▓█▓▓▒▒▒▒▓▒"
ASCII_GRADIENT_HD = "⣿▒▒▓▓█▓▓▒▒▒▒▓▓██▓▓▒▒▓▓█▒▒▓▓▒▒▒▒▓▓▓▒▒▓▓"
ASCII_GRADIENT_XHD = "⢿⠿⣿▒▒▓▓▓▒▒▓▓▒▒▓▒▒▓▓██▓▓▒▒▒▒██▒▒▓▓▒▒▓▓█▒▒▓▓▒▒▓▓▒▒"
ASCII_GRADIENT_1 = " ░▒▒▓▓█@#$%&*+=-.abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
ASCII_GRADIENT_2 = " ░▒▓█@#$%&*^()_+`-={}[]|:;\"'<>,.?/abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
ASCII_GRADIENT_3 = " ░▒▓█@#$%&*()_+=-|}{[]:;<>.,~`abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

def frame_to_ascii(frame, width=100, color=False, mode='HD'):
    height, original_width = frame.shape[:2]
    aspect_ratio = original_width / height
    new_height = int(width / aspect_ratio * 0.55)
    resized = cv2.resize(frame, (width, new_height), interpolation=cv2.INTER_AREA)

    ascii_frame = []

    # Select the appropriate gradient based on the mode
    if mode == 'LD':
        gradient = ASCII_GRADIENT_LD
    elif mode == 'SD':
        gradient = ASCII_GRADIENT_SD
    elif mode == 'XHD':
        gradient = ASCII_GRADIENT_XHD
    elif mode == '1':
        gradient = ASCII_GRADIENT_1
    elif mode == '2':
        gradient = ASCII_GRADIENT_2
    elif mode == '3':
        gradient = ASCII_GRADIENT_3
    else:
        gradient = ASCII_GRADIENT_HD  # Default mode is HD

    gradient_length = len(gradient)

    # Handle color
    if color:
        for row in resized:
            ascii_row = []
            for bgr in row:
                b, g, r = map(int, bgr)
                # Use the brightness value to select an appropriate character
                brightness = (r + g + b) / 3
                index = int((brightness / 255) * (gradient_length - 1))  # Map brightness to a gradient index
                char = gradient[index]  # Pick a character based on brightness
                ascii_row.append(f"\033[38;2;{r};{g};{b}m{char}\033[0m")
            ascii_frame.append("".join(ascii_row))
    else:
        # Convert to grayscale and normalize
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        min_val = np.min(gray)
        max_val = np.max(gray)
        stretched = (gray - min_val) * (255.0 / (max_val - min_val)) if max_val > min_val else gray

        for row in stretched:
            ascii_row = []
            for pixel in row:
                # Map pixel intensity to gradient characters based on gamma correction
                gamma_corrected = (pixel / 255.0) ** 0.6
                index = int(gamma_corrected * (gradient_length - 1))  # Use corrected intensity to choose character
                ascii_row.append(gradient[index])  # Pick the corresponding character from the gradient
            ascii_frame.append("".join(ascii_row))

    return "\n".join(ascii_frame)
