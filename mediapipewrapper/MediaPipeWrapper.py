import json
from threading import Thread

import mediapipe as mp

from utils.Utils import Utils

import cv2


# This class is a wrapper for MediaPipe. Allows to capture motion using a camera in a new thread.
class MediaPipeWrapper(Thread):

    def __init__(self, camera=None, path=None):
        """
        Constructor for the class MediaPipeWrapper.
        :param camera: Index of the camera used by OpenCV.
        """
        super().__init__()

        # MediaPipe vars
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_pose = mp.solutions.pose

        # JSON data is stored here.
        self.data = {}

        # Array data is stored here
        self.list = []

        # CSV data is stored here.
        self.header = ""
        self.body = ""
        self.csv = ""

        # Webcam
        self.cap = None
        self.stopCam = False
        self.camera = camera
        self.path = path

        # Video output
        self.raw = None
        self.processed = None

    def capture(self, hide_output=False):
        """
        Capture the movements until a stop signal is received. This should be executed in a different thread.
        :return: None.
        """
        # Establish detection and tracking confidence
        with self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            # Current detected frame.
            frame_number = 0
            print(frame_number)
            # While the webcam is opened...
            while self.cap.isOpened() and not self.stopCam:
                # capture an image.
                success, image = self.cap.read()

                # Write frame in raw video.
                self.raw.write(image)

                # If not success reading image, ignore if webcam, or break if video.
                if not success:
                    print("Ignoring empty camera frame.")
                    self.stopCam = True
                    # If loading a video, use 'break' instead of 'continue'.
                    continue

                # To improve performance, optionally mark the image as not writeable to pass by reference.
                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                # Process the image using MediaPipe
                results = pose.process(image)

                # If a pose has been detected...
                if results.pose_landmarks is not None:
                    # store as json
                    self.data['frame ' + str(frame_number)] = {}
                    landmark_number = 0
                    for data_point in results.pose_landmarks.landmark:
                        self.data['frame ' + str(frame_number)][Utils.get_landmarks_list()[landmark_number]] = {}
                        self.data['frame ' + str(frame_number)][Utils.get_landmarks_list()[landmark_number]]['x'] = data_point.x
                        self.data['frame ' + str(frame_number)][Utils.get_landmarks_list()[landmark_number]]['y'] = data_point.y
                        self.data['frame ' + str(frame_number)][Utils.get_landmarks_list()[landmark_number]]['z'] = data_point.z
                        self.data['frame ' + str(frame_number)][Utils.get_landmarks_list()[landmark_number]][
                            'visibility'] = data_point.visibility
                        landmark_number += 1

                    frame_number += 1
                    # store as csv
                    for data_point in results.pose_landmarks.landmark:
                        self.body = self.body + str(data_point.x) + "; " + str(data_point.y) + "; " + str(
                            data_point.z) + "; " + str(data_point.visibility) + "; "
                    self.body = self.body[:-2]
                    self.body = self.body + "\n"

                    # store as list. Each element is a frame and contains in position 0 the name of the landmark,
                    # and in position 1 the x, y and x coordinates with the visibility.
                    x = []
                    y = []
                    z = []
                    v = []
                    for data_point in results.pose_landmarks.landmark:
                        x.append(data_point.x)
                        y.append(data_point.y)
                        z.append(data_point.z)
                        v.append(data_point.visibility)
                    frame = [x, y, z, v]
                    self.list.append(frame)

                # Draw the pose annotation on the image.
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                self.mp_drawing.draw_landmarks(
                    image,
                    results.pose_landmarks,
                    self.mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style())

                # Flip the image horizontally for a selfie-view display.
                if not hide_output:
                    cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))

                # Write frame in processed video.
                self.processed.write(image)

                # Recording and process finishes when 'esc' is pressed.
                if cv2.waitKey(5) & 0xFF == 27:
                    break
        self.processed.release()
        self.raw.release()
        pass

    def run(self, hide_output=False):
        """
        Start the capture of the movements using the camera selected when creating this object.
        :return: None.
        """
        # For webcam input. Here I have chosen 1 because that is the webcam I am using. Typically, it should be 0 or 1.
        # This can be changed to read from a video with testing purposes instead of webcam.
        if self.camera is None:
            self.cap = cv2.VideoCapture(self.path)
        else:
            self.cap = cv2.VideoCapture(self.camera, cv2.CAP_DSHOW)

        # Get width and height of camera captured images.
        frame_width = int(self.cap.get(3))
        frame_height = int(self.cap.get(4))
        size = (frame_width, frame_height)

        # Create a video writer to write all the frames here.
        self.raw = cv2.VideoWriter('original.mp4',
                                   cv2.VideoWriter_fourcc(*'MJPG'),
                                   10, size)

        self.processed = cv2.VideoWriter('processed.mp4',
                                         cv2.VideoWriter_fourcc(*'MJPG'),
                                         10, size)

        # We don't want to stop camera.
        self.stopCam = False

        self.capture(hide_output)

    def stop(self):
        """
        Stop the capture of the movements.
        :return: None
        """
        # Send signal to thread so it stops capturing.
        self.stopCam = True

        # Join thread.
        self.join()

        # Release the webcam.
        self.cap.release()

        # Export csv
        self.export_csv("../", "name.csv")

        pass

    def export_csv(self, file_path, file_name):
        """
        Export the captured movements into a csv file.
        :param file_name: Name of the exported file.
        :param file_path: Path where the file is going to be exported.
        :return: None
        """
        # The header of the csv file is created here so it is only created once.
        for landmark_name in Utils.get_landmarks_list():
            self.header = self.header + landmark_name + "_x; "
            self.header = self.header + landmark_name + "_y; "
            self.header = self.header + landmark_name + "_z; "
            self.header = self.header + landmark_name + "_visibility; "
        self.header = self.header[:-2]
        self.header = self.header + "\n"

        # Print csv
        self.csv = self.header + self.body
        with open(file_path + file_name, 'w') as f:
            f.write(self.csv)

    def export_json(self, file_path, file_name):
        """
        Export the captured movements into a json file.
        :param file_name: Name of the exported file.
        :param file_path: Path where the file is going to be exported.
        :return: None
        """
        with open(file_path + file_name, 'w') as f:
            json.dump(self.data, f, indent=4)

    def get_captured_data(self):
        """
        Get data captured by MediaPipe.
        :return: Data captured by MediaPipe in json format.
        """
        return self.data