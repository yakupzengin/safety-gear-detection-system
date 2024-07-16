import cv2

class VideoProcessor:
    def __init__(self, video_path, output_path):
        self.video_path = video_path
        self.output_path = output_path
        self.cap = cv2.VideoCapture(video_path)

        # Check if the video file was successfully opened
        if not self.cap.isOpened():
            raise ValueError("Video not opened")

        # Get video properties
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = cv2.VideoWriter(self.output_path, fourcc, self.fps, (self.width, self.height))

    def release(self):
        # Release video capture and writer objects
        self.cap.release()
        self.out.release()
