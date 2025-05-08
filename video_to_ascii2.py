import cv2
import numpy as np
import time
import sys
import os
import argparse

ASCII_GRADIENT = " ░▒▓█"

def move_cursor_top():
    print("\033[H", end='')

def hide_cursor():
    print("\033[?25l", end='')

def show_cursor():
    print("\033[?25h", end='')

def set_terminal_size(width, height):
    if sys.platform != "win32":
        os.system(f"resize -s {height} {width}")

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

def play_video_ascii(video_path, color=False, width=100, loop=False, fit=True):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error opening video file: {video_path}")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 25
    frame_delay = 1 / fps

    # Get original video dimensions
    video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    aspect_ratio = video_width / video_height

    # If fit mode is enabled, override width to fit terminal height
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
            frame_start = time.time()
            ret, frame = cap.read()
            if not ret:
                if loop:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    continue
                else:
                    break

            if color:
                ascii_art = frame_to_ascii(frame, width=width, color=True)
            else:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
                enhanced_gray = clahe.apply(gray)
                ascii_art = frame_to_ascii(enhanced_gray, width=width, color=False)

            move_cursor_top()
            sys.stdout.write(ascii_art)
            sys.stdout.flush()

            elapsed = time.time() - frame_start
            sleep_time = frame_delay - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)

    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        show_cursor()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Play a video as ASCII art in your terminal.")
    parser.add_argument("video", help="Path to the video file")
    parser.add_argument("-c", "--color", action="store_true", help="Enable full color mode")
    parser.add_argument("--fit", default=True, action="store_true", help="Auto-resize terminal to fit full video height")
    parser.add_argument("--width", type=int, default=100, help="Width of ASCII output (default: 100)")
    parser.add_argument("-l", "--loop", action="store_true", help="Loop video playback")
    parser.add_argument("-f", "--help", action="store_true", help="Display help information")
    args = parser.parse_args()

    play_video_ascii(args.video, color=args.color, width=args.width, loop=args.loop, fit=args.fit)
