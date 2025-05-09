# ASCII Media Renderer

`ascii-media` is a Python-based command-line tool that allows you to render media (images, videos, and audio) as ASCII art directly in your terminal. It also includes an AI-powered feature to generate ASCII art from text prompts.

## Features

- **Image Rendering**: Convert images into ASCII art with optional color support.
- **Video Playback**: Play videos as ASCII animations in your terminal.
- **Audio Visualization**: Visualize audio waveforms as ASCII art.
- **AI Image Generation**: Generate ASCII art from text prompts using AI models.
- **Terminal Fitting**: Automatically adjusts ASCII art to fit your terminal size.
- **Keyboard Controls**:
    - Press `q` to quit.
    - Press `p` to pause/resume.

## Installation

1. Clone the repository:
     ```bash
     git clone https://github.com/your-repo/ascii-media.git
     cd ascii-media
     ```

2. Install the required dependencies:
     ```bash
     pip install .
     ```

## Usage

Run the `ascii-media` command with one of the following subcommands:

### Image Rendering
Render an image as ASCII art:
```bash
ascii-media image <image_path_or_url> [--nocolor] [--width <width>] [--fit]
```

- `image_path_or_url`: Path to the image file or URL.
- `--nocolor`: Disable colored ASCII output.
- `--width`: Set custom ASCII width (default: 100).
- `--fit`: Fit ASCII art to terminal size (default: enabled).
- `--mode` : Selects the mode for the ascii-gradient.

    - ` --mode=LD`
    - ` --mode=SD`
    - ` --mode=HD (default)`
    - ` --mode=XHD`
    - ` --mode=1 `
    - ` --mode=2`
    - ` --mode=3`
    - ` --mode=256`


### Video Playback
Play a video as ASCII animation:
```bash
ascii-media video <video_path> [--nocolor] [--width <width>] [--loop] [--fit]
```

- `video_path`: Path to the video file.
- `--nocolor`: Disable colored ASCII output.
- `--width`: Set custom ASCII width (default: 100).
- `--loop`: Loop the video playback.
- `--fit`: Fit ASCII art to terminal size (default: enabled).

### Audio Visualization
Visualize an audio waveform as ASCII art:
```bash
ascii-media audio <source>
```

- `source`: Path to the audio file or YouTube URL.

### AI Image Generation
Generate ASCII art from a text prompt using AI:
```bash
ascii-media ai-image <prompt> [--model <model>] [--width <width>] [--height <height>] [--nologo] [--enhance] [--download] [--nocolor] [--fit]
```

- `prompt`: Text prompt for AI image generation.
- `--model`: AI model to use (default: `flux`).
- `--width`: Width of the generated image (default: 512).
- `--height`: Height of the generated image (default: 512).
- `--nologo`: Disable Pollinations logo overlay.
- `--enhance`: Enhance the prompt with more detail.
- `--download`: Download the generated image.
- `--nocolor`: Disable colored ASCII output.
- `--fit`: Fit ASCII art to terminal size (default: enabled).

## Examples

### Render an Image
```bash
ascii-media image example.jpg --width 80
```

### Play a Video
```bash
ascii-media video example.mp4 --nocolor --loop
```

### Visualize Audio
```bash
ascii-media audio example.mp3
```

### Generate AI Image
```bash
ascii-media ai-image "A futuristic cityscape" --enhance --width 256 --height 256
```

## Keyboard Controls

- **`q`**: Quit the current operation.
- **`p`**: Pause or resume playback.

## Dependencies

The project relies on the following Python libraries:
- `opencv-python`
- `numpy`
- `requests`
- `keyboard`
- `soundfile`
- `asciichartpy`
- `yt-dlp`
- `pygame`
- `colorama`
- `termcolor`


Install them automatically using the `setup.py` file.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
