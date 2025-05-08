import cv2
import numpy as np
import time
import sys
import os

# Ultra-smooth gradient of ASCII characters from dark to light (grayscale)
ASCII_GRADIENT = " ░▒▓█"

# Colors for colored output (simple ANSI escape codes for foreground colors)
COLOR_GRADIENT = [
    "\033[38;5;16m",  # Black
    "\033[38;5;232m",  # Dark Gray
    "\033[38;5;240m",  # Gray
    "\033[38;5;248m",  # Light Gray
    "\033[38;5;255m",  # White
]

def move_cursor_top():
    print("\033[H", end='')  # ANSI escape to move cursor to top-left

def hide_cursor():
    print("\033[?25l", end='')

def show_cursor():
    print("\033[?25h", end='')

def set_terminal_size(width, height):
    # Resize the terminal to fit the video dimensions
    os.system(f"resize -s {height} {width}")

def frame_to_ascii(frame, width=100, color=False):
    height, original_width = frame.shape
    aspect_ratio = original_width / height
    new_height = int(width / aspect_ratio * 0.55)  # Adjusted for character aspect ratio
    
    # High-quality resizing with anti-aliasing
    resized = cv2.resize(frame, (width, new_height), interpolation=cv2.INTER_AREA)
    
    # Contrast stretching for better detail visibility
    min_val = np.min(resized)
    max_val = np.max(resized)
    if max_val > min_val:
        stretched = (resized - min_val) * (255.0 / (max_val - min_val))
    else:
        stretched = resized
    
    # Create ASCII art with gradient mapping
    ascii_frame = []
    gradient_length = len(ASCII_GRADIENT)
    
    for row in stretched:
        ascii_row = []
        for pixel in row:
            # Map pixel to gradient with gamma correction for better perceptual accuracy
            gamma_corrected = (pixel / 255.0) ** 0.6
            index = min(int(gamma_corrected * gradient_length), gradient_length - 1)
            
            # For color, apply color gradient based on the brightness
            if color:
                color_code = COLOR_GRADIENT[index % len(COLOR_GRADIENT)]
                ascii_row.append(f"{color_code}{ASCII_GRADIENT[index]}\033[0m")
            else:
                ascii_row.append(ASCII_GRADIENT[index])
        ascii_frame.append("".join(ascii_row))
    
    return "\n".join(ascii_frame)

def play_video_ascii(video_path, color=False):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error opening video file")
        return

    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_delay = 1 / fps
    
    # Get terminal size and adjust accordingly
    terminal_width = os.get_terminal_size().columns - 1  # leave some space for margins
    terminal_height = os.get_terminal_size().lines - 1  # leave some space for margins
    set_terminal_size(terminal_width, terminal_height)

    hide_cursor()

    try:
        while True:
            frame_start = time.time()
            
            ret, frame = cap.read()
            if not ret:
                # Loop video
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            
            # Convert to grayscale and enhance details
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Apply adaptive histogram equalization for better contrast
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            enhanced = clahe.apply(gray)
            
            # Generate ASCII frame
            ascii_art = frame_to_ascii(enhanced, width=terminal_width, color=color)
            
            # Display
            move_cursor_top()  # Move cursor to top of terminal to avoid flickering
            print(ascii_art, end='')  # Print the ASCII art without clearing the screen
            
            # Maintain frame rate
            elapsed = time.time() - frame_start
            sleep_time = max(0, frame_delay - elapsed)
            time.sleep(sleep_time)
            
    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        show_cursor()

if __name__ == "__main__":
    color_flag = "-c" in sys.argv  # Check if -c flag is passed for color playback
    video_path = sys.argv[1] if len(sys.argv) > 1 else 'video_test.mp4'
    play_video_ascii(video_path, color=color_flag)
