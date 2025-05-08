import time
from .video import open_video, get_video_fps, get_video_dimensions, read_frame
from .ascii import frame_to_ascii
from .terminal import move_cursor_top, hide_cursor, show_cursor, set_terminal_size

def play_video_ascii(video_path, color=False, width=100, loop=False, fit=True):
    cap = open_video(video_path)

    fps = get_video_fps(cap)
    frame_delay = 1 / fps

    video_width, video_height = get_video_dimensions(cap)
    aspect_ratio = video_width / video_height

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
            ret, frame = read_frame(cap)
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
