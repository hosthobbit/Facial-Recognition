import os
import sys
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_login import LoginManager, login_required, login_user, logout_user, UserMixin
from camera_manager import CameraManager
from face_detector import FaceDetector
from admin_interface import AdminInterface
from config_manager import ConfigManager
from speech_service import SpeechService
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

app = Flask(__name__)
app.secret_key = os.urandom(24)

config_manager = ConfigManager()
camera_manager = CameraManager()
face_detector = FaceDetector()
admin_interface = AdminInterface()
speech_service = SpeechService()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'

@login_manager.user_loader
def load_user(user_id):
    if admin_interface.get_user(user_id):
        return User(user_id)
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if admin_interface.authenticate(username, password):
            user = User(username)
            login_user(user)
            return redirect(url_for('admin'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/api/set_api_key', methods=['POST'])
@login_required
def set_api_key():
    try:
        data = request.get_json()
        if not data:
            logging.error('No data provided in request')
            return jsonify({'error': 'No data provided'}), 400
        api_key = data.get('api_key')
        if not api_key:
            logging.error('Empty API key provided')
            return jsonify({'error': 'API key is required'}), 400
        logging.info('Attempting to set API key...')
        if speech_service.set_api_key(api_key):
            logging.info('API key set successfully')
            return jsonify({
                'status': 'success',
                'message': 'API key saved and validated successfully'
            })
        else:
            logging.error('Failed to validate API key')
            return jsonify({
                'error': 'Failed to validate API key. Please check your key and try again.',
                'details': 'Check the server logs for more information'
            }), 400
    except Exception as e:
        logging.error(f'Error setting API key: {str(e)}')
        return jsonify({
            'error': 'An error occurred while setting the API key',
            'details': str(e)
        }), 500

@app.route('/api/face_detection', methods=['POST'])
def face_detection():
    try:
        frame = request.files['frame'].read()
        result = face_detector.process_frame(frame)
        if 'faces' in result:
            recognized_faces = {face['label'] for face in result['faces'] if face['label'] != 'Unknown'}
            speech_service.update_faces(recognized_faces)
        return jsonify(result)
    except Exception as e:
        logging.error(f'Face detection error: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/api/train', methods=['POST'])
@login_required
def train_face():
    try:
        if 'multipart/form-data' not in request.content_type:
            return jsonify({'error': 'Invalid content type. Expected multipart/form-data'}), 400
        label = request.form.get('label')
        if not label:
            return jsonify({'error': 'Label is required'}), 400
        images = request.files.getlist('images[]')
        if not images:
            return jsonify({'error': 'At least one image is required'}), 400
        image_data_list = []
        for image in images:
            if not image.filename:
                continue
            try:
                image_data = image.read()
                if image_data:
                    image_data_list.append(image_data)
            except Exception as e:
                logging.error(f'Error reading image file: {str(e)}')
                continue
        if not image_data_list:
            return jsonify({'error': 'No valid images were provided'}), 400
        result = face_detector.train_face_batch(image_data_list, label)
        return jsonify(result)
    except Exception as e:
        logging.error(f'Training error: {str(e)}')
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    try:
        camera_manager.initialize()
        app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        logging.error(f'Application startup error: {str(e)}')
        sys.exit(1)