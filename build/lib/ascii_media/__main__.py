import argparse
from . import imager, player, audio

def main():
    parser = argparse.ArgumentParser(prog='ascii-media', description="Render media as ASCII art in your terminal.")
    subparsers = parser.add_subparsers(dest='command', help='Sub-commands: image, video, audio')
    subparsers.required = True

    # Image subcommand
    image_parser = subparsers.add_parser('image', help='Render an image as ASCII art')
    image_parser.add_argument('image_path', help='Path to the image file or image URL')
    image_parser.add_argument('--nocolor', action='store_true', help='Disable colored ASCII output')
    image_parser.add_argument('--width', type=int, default=100, help='Set custom ASCII width')
    image_parser.add_argument('--fit', action='store_true', default=True, help='Fit ASCII to terminal size')

    # Video subcommand
    video_parser = subparsers.add_parser('video', help='Play a video as ASCII animation')
    video_parser.add_argument('video_path', help='Path to the video file')
    video_parser.add_argument('--nocolor', action='store_true', help='Disable colored ASCII output')
    video_parser.add_argument('--width', type=int, default=100, help='Set custom ASCII width')
    video_parser.add_argument('--loop', action='store_true', help='Loop the video')
    video_parser.add_argument('--fit', action='store_true', default=True, help='Fit ASCII to terminal size')

    # Audio subcommand
    audio_parser = subparsers.add_parser('audio', help='Visualize audio waveform as ASCII art')
    audio_parser.add_argument('source', help='Path to audio file or YouTube URL')

    args = parser.parse_args()

    if args.command == 'image':
        imager.play_image_ascii(
            image_path=args.image_path,
            color=not args.nocolor,
            width=args.width,
            fit=args.fit,
        )
    elif args.command == 'video':
        player.play_video_ascii(
            video_path=args.video_path,
            color=not args.nocolor,
            width=args.width,
            loop=args.loop,
            fit=args.fit,
        )
    elif args.command == 'audio':
        audio.main()
