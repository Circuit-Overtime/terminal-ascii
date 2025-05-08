from setuptools import setup, find_packages

setup(
    name="ascii_video_player",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "opencv-python",
        "numpy"
    ],
    entry_points={
        'console_scripts': [
            'ascii-video=ascii_video_player.player:play_video_ascii',
        ],
    },
)
