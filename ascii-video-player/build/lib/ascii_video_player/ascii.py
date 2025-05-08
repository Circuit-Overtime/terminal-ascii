import numpy as np

ASCII_GRADIENT = " ░▒▓█"

def frame_to_ascii(frame, width=100, color=False):
    height, original_width = frame.shape[:2]
    aspect_ratio = original_width / height
    new_height = int(width / aspect_ratio * 0.55)
    resized = cv2.resize(frame, (width, new_height), interpolation=cv2.INTER_AREA)

    ascii_frame = []
    gradient_length = len(ASCII_GRADIENT)

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
                ascii_row.append(ASCII_GRADIENT[index])
            ascii_frame.append("".join(ascii_row))

    return "\n".join(ascii_frame)
