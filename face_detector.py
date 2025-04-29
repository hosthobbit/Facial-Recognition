import os
import cv2
import numpy as np
import logging
import mediapipe as mp
from typing import Dict, Any

class FaceDetector:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Initialize MediaPipe Face Detection
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(
            model_selection=1,
            min_detection_confidence=0.3
        )
        
        # Initialize MediaPipe Face Mesh
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=10,
            min_detection_confidence=0.3
        )
        
        # Initialize face recognition
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.trained = False
        self.faces_dir = 'faces'
        self.label_map = {}
        
        if not os.path.exists(self.faces_dir):
            os.makedirs(self.faces_dir)
        
        model_path = os.path.join(self.faces_dir, 'trained_model.yml')
        label_map_path = os.path.join(self.faces_dir, 'label_map.txt')
        if os.path.exists(model_path) and os.path.exists(label_map_path):
            self.recognizer.read(model_path)
            with open(label_map_path, 'r') as f:
                self.label_map = eval(f.read())
            self.trained = True

    def process_frame(self, frame_data: bytes) -> Dict[str, Any]:
        try:
            nparr = np.frombuffer(frame_data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            # Image preprocessing
            lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
            cl = clahe.apply(l)
            limg = cv2.merge((cl,a,b))
            frame = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
            
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.face_detection.process(rgb_frame)
            
            face_results = []
            if results.detections:
                for detection in results.detections:
                    bbox = detection.location_data.relative_bounding_box
                    h, w = frame.shape[:2]
                    x = int(bbox.xmin * w)
                    y = int(bbox.ymin * h)
                    width = int(bbox.width * w)
                    height = int(bbox.height * h)
                    
                    x = max(0, x)
                    y = max(0, y)
                    width = min(w - x, width)
                    height = min(h - y, height)
                    
                    face_info = {
                        'x': x,
                        'y': y,
                        'width': width,
                        'height': height,
                        'label': 'Unknown',
                        'confidence': detection.score[0]
                    }
                    
                    if self.trained:
                        face_roi = frame[y:y+height, x:x+width]
                        if face_roi.size > 0:
                            face_roi = cv2.resize(face_roi, (100, 100))
                            gray_face = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
                            gray_face = cv2.equalizeHist(gray_face)
                            
                            try:
                                label_id, confidence = self.recognizer.predict(gray_face)
                                if confidence < 100:
                                    face_info['label'] = self.label_map.get(label_id, 'Unknown')
                                    face_info['confidence'] = (100 - confidence) / 100
                            except Exception as e:
                                self.logger.error(f'Error in face recognition: {str(e)}')
                    
                    face_results.append(face_info)
            
            return {'faces': face_results}
            
        except Exception as e:
            self.logger.error(f'Frame processing error: {str(e)}')
            raise