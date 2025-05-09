from setuptools import setup, find_packages

setup(
    name="ascii_media",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "opencv-python",
        "numpy",
        "requests",
        "keyboard",
        "soundfile",
        "asciichartpy",
        "yt-dlp",
        "pygame",
        "colorama",
        "termcolor",
        "Pillow",
        "moviepy",
        "ffmpeg-python",
        "mimetypes",
        "tempfile",

    ],
    entry_points={
        'console_scripts': [
            'ascii-media=ascii_media.__main__:main'

        ],
    },
)
