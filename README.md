# AI Camera System

An intelligent camera system that uses facial recognition and natural language processing to interact with people in real-time.

## Features

- **Real-time Face Detection**: Uses MediaPipe for robust face detection
- **Face Recognition**: Identifies known individuals using OpenCV's LBPH Face Recognizer
- **Dynamic Interaction**: 
  - Greets new people as they appear
  - Says goodbye when people leave
  - Recognizes multiple people simultaneously
  - Maintains conversation context for each person
- **Natural Language Generation**: Uses OpenAI GPT-3.5 to generate natural, contextual responses
- **Admin Interface**: Web interface for system management and training
- **Voice Synthesis**: Text-to-speech for verbal interaction

## Requirements

- Python 3.11+
- OpenCV
- MediaPipe
- Flask
- OpenAI API key
- pyttsx3 for text-to-speech

## Installation

1. Clone the repository:
```bash
git clone https://github.com/hosthobbit/Facial-Recognition.git
cd Facial-Recognition
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install flask flask-login opencv-python mediapipe pyttsx3 openai
```

4. Set up your OpenAI API key through the admin interface or environment variable:
```bash
export OPENAI_API_KEY=your-api-key-here
```

## Usage

1. Start the application:
```bash
python main.py
```

2. Access the web interface:
- Main interface: http://localhost:5000
- Admin interface: http://localhost:5000/admin

3. Train face recognition:
- Log in to the admin interface
- Upload photos of people to train the system
- Add labels (names) for each person

## Features in Detail

### Face Detection and Recognition
- Uses MediaPipe for accurate face detection
- Supports multiple faces simultaneously
- LBPH Face Recognizer for reliable face recognition
- Automatic face tracking and identification

### Interactive Greetings
- Welcomes new people when they appear
- Generates personalized greetings using GPT-3.5
- Maintains cooldown periods to avoid repetitive greetings
- Says goodbye when people leave the frame

### Admin Interface
- Secure login system
- Face training interface
- OpenAI API key configuration
- System monitoring and management

## Configuration

- Face detection sensitivity can be adjusted in `face_detector.py`
- Greeting cooldown periods can be modified in `speech_service.py`
- Web interface settings in `main.py`

## Troubleshooting

### Common Issues

1. **OpenAI API Key Issues**
   - Ensure your API key is valid
   - Check the API key is properly set in the admin interface
   - Verify API key permissions and credits

2. **Face Recognition Issues**
   - Ensure good lighting conditions
   - Train with multiple angles of each face
   - Adjust detection confidence thresholds if needed

3. **Speech Issues**
   - Check system audio settings
   - Verify pyttsx3 installation
   - Adjust speech rate and volume in settings

## Contributing

Contributions are welcome! Please feel free to submit pull requests.

## License

MIT License

## Acknowledgments

- OpenAI for GPT-3.5
- Google for MediaPipe
- OpenCV community
- Flask framework