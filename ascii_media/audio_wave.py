import yt_dlp
import argparse
import os
import sys
import tempfile
import numpy as np
import asciichartpy
import soundfile as sf
import pygame
import threading
import time
import termcolor
import keyboard
from colorama import init as colorama_init, Fore, Style

colorama_init()

def download_youtube_audio(url):
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, 'audio.wav')

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': temp_file.replace('.wav', '.%(ext)s'),
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    for file in os.listdir(temp_dir):
        if file.endswith('.wav'):
            return os.path.join(temp_dir, file)

    raise FileNotFoundError("WAV file not found after download.")

def extract_audio_data(file_path):
    data, samplerate = sf.read(file_path)
    if len(data.shape) > 1:
        data = data.mean(axis=1)
    return data

def get_colorized_chart(data):
    chart = asciichartpy.plot(data, {'height': 15})
    colored_chart = ""
    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
    lines = chart.splitlines()
    for i, line in enumerate(lines):
        color = colors[i % len(colors)]
        colored_chart += color + line + Style.RESET_ALL + "\n"
    return colored_chart

def animate_waveform(data, width=100, fps=15, duration=0):
    chunk_size = int(len(data) / (fps * duration)) if duration > 0 else int(len(data) / 100)
    i = 0
    paused = False

    while i < len(data):
        if keyboard.is_pressed('q'):
            pygame.mixer.music.stop()
            break
        elif keyboard.is_pressed('p'):
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
                paused = True
        elif keyboard.is_pressed('r'):
            if paused:
                pygame.mixer.music.unpause()
                paused = False

        if not paused:
            os.system('cls' if os.name == 'nt' else 'clear')
            chunk = data[i:i + chunk_size]
            downsampled = chunk[::max(1, len(chunk) // width)]
            print(get_colorized_chart(downsampled))
            i += chunk_size
            time.sleep(1 / fps)
        else:
            time.sleep(0.1)

def play_audio(filepath):
    pygame.mixer.init()
    pygame.mixer.music.load(filepath)
    pygame.mixer.music.play()

def main(args):
    if args.source.startswith('http'):
        print("Downloading audio from YouTube...")
        audio_path = download_youtube_audio(args.source)
    else:
        audio_path = args.source

    print("Extracting audio data...")
    data = extract_audio_data(audio_path)

    print("Starting playback and animation...")
    threading.Thread(target=play_audio, args=(audio_path,), daemon=True).start()
    animate_waveform(data, width=120, fps=60, duration=60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ASCII Audio Waveform Visualizer")
    parser.add_argument("source", help="Path to audio file or YouTube URL")
    args = parser.parse_args()
    main(args)
