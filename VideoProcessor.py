import cv2
from mediapipewrapper.MediaPipeWrapper import MediaPipeWrapper


class VideoProcessor:

    def __init__(self, path=None):
        # Reference to video.
        self.video_path = path
        self.video = None
        self.video_width = None
        self.video_height = None
        self.num_frames = None
        self.duration = None
        self.frames_per_second = None
        self.data = {}

        # Media pipe wrapper
        self.mediapipe_wrapper = None

        # If path is provided.
        if path is not None:
            self.load_video(self.video_path)

    def __del__(self):
        if self.video is not None and self.video.isOpened():
            self.video.release()

    def load_video(self, path):
        # Load video.
        self.video_path = path
        self.video = cv2.VideoCapture(path)

        if not self.video.isOpened():
            raise ValueError("Unable to open video source", self.video)

        # Get width and height of the video.
        self.video_width = self.video.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.video_height = self.video.get(cv2.CAP_PROP_FRAME_HEIGHT)

        # Get num frames, duration and frames per second.
        self.num_frames = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
        self.frames_per_second = self.video.get(cv2.CAP_PROP_FPS)
        self.duration = round(self.num_frames / self.frames_per_second)
        print("Num. Frames:", self.num_frames)
        print("Frames per Second (fps):", self.frames_per_second)
        print("Duration (s):", self.duration)

    def get_frame(self):
        if self.video is not None and self.video.isOpened():
            ret, frame = self.video.read()
            if ret:
                # To improve performance, optionally mark the image as not writeable to pass by reference.
                frame.flags.writeable = False
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Return a boolean success flag and the current frame converted to BGR
                return ret, frame
            else:
                return ret, None
        else:
            return False, None

    def get_current_frame_number(self):
        if self.video is not None and self.video.isOpened():
            return self.video.get(cv2.CAP_PROP_POS_FRAMES)
        else:
            return 0

    def set_to_frame(self, frame):
        self.video.set(cv2.CAP_PROP_POS_FRAMES, frame)

    def process_full_video_mediapipe(self):
        self.mediapipe_wrapper = MediaPipeWrapper(None, self.video_path)

        self.mediapipe_wrapper.run(True)

        return self.mediapipe_wrapper.get_captured_data()
