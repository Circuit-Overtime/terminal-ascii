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
    # print(f"Used Graident: {gradient}")
    if color:
        for row in resized:
            ascii_row = []
            for bgr in row:
                b, g, r = map(int, bgr)
                char = "█"
                ascii_row.append(f"\033[38;2;{r};{g};{b}m{char}\033[0m")
            ascii_frame.append("".join(ascii_row))
    else:
        min_val = np.min(resized)
        max_val = np.max(resized)
        stretched = (resized - min_val) * (255.0 / (max_val - min_val)) if max_val > min_val else resized

        for row in stretched:
            ascii_row = []
            for pixel in row:
                gamma_corrected = (pixel / 255.0) ** 0.6
                index = min(int(gamma_corrected * gradient_length), gradient_length - 1)
                ascii_row.append(gradient[index])
            ascii_frame.append("".join(ascii_row))

    return "\n".join(ascii_frame)
