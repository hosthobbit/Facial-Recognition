import cv2
import logging

class CameraManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.camera = None
        self.initialized = False

    def initialize(self):
        """Initialize the camera"""
        try:
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                raise Exception('Failed to open camera')
            self.initialized = True
            self.logger.info('Camera initialized successfully')
        except Exception as e:
            self.logger.error(f'Error initializing camera: {str(e)}')
            raise

    def get_frame(self):
        """Get a frame from the camera"""
        if not self.initialized:
            raise Exception('Camera not initialized')
        ret, frame = self.camera.read()
        if not ret:
            raise Exception('Failed to capture frame')
        return frame

    def release(self):
        """Release the camera"""
        if self.camera:
            self.camera.release()
            self.initialized = False
            self.logger.info('Camera released')