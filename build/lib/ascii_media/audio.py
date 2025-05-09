import argparse
import os
import sys
import tempfile
import numpy as np
import asciichartpy
import soundfile as sf
from pytube import YouTube
import subprocess

def download_youtube_audio(url):
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True).first()
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, 'audio.mp4')
    stream.download(output_path=temp_dir, filename='audio.mp4')
    return temp_file

def extract_audio_data(file_path):
    data, samplerate = sf.read(file_path)
    if len(data.shape) > 1:
        data = data.mean(axis=1)  # Convert to mono by averaging channels
    return data

def plot_waveform(data, width=100):
    # Downsample data for plotting
    factor = max(1, len(data) // width)
    downsampled = data[::factor]
    chart = asciichartpy.plot(downsampled, {'height': 15})
    print(chart)

def main():
    parser = argparse.ArgumentParser(description="Visualize audio waveform as ASCII art.")
    parser.add_argument('source', help='Path to audio file or YouTube URL')
    args = parser.parse_args()

    if args.source.startswith('http'):
        print("Downloading audio from YouTube...")
        audio_path = download_youtube_audio(args.source)
    else:
        audio_path = args.source

    print("Extracting audio data...")
    data = extract_audio_data(audio_path)
    print("Rendering waveform:")
    plot_waveform(data)
