import os
import sys

def move_cursor_top():
    print("\033[H", end='')

def hide_cursor():
    print("\033[?25l", end='')

def show_cursor():
    print("\033[?25h", end='')

def set_terminal_size(width, height):
    if sys.platform != "win32":
        os.system(f"resize -s {height} {width}")
