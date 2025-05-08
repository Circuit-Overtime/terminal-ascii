import cv2

def open_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Error opening video file: {video_path}")
    return cap

def get_video_fps(cap):
    fps = cap.get(cv2.CAP_PROP_FPS)
    return fps if fps > 0 else 25

def get_video_dimensions(cap):
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    return width, height

def read_frame(cap):
    ret, frame = cap.read()
    return ret, frame
