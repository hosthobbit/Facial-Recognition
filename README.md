# AI Camera with Face Recognition and Interactive Speech

This project implements an AI camera system with face recognition capabilities and interactive speech features. The system can detect faces, recognize individuals, and engage in natural conversation including greetings and goodbyes.

## Features

- Real-time face detection using MediaPipe
- Face recognition with personalized greetings
- Dynamic conversation management (greetings and goodbyes)
- Support for multiple simultaneous faces
- Cooldown system for natural interaction timing

## System Requirements

- Python 3.8 or higher
- Webcam or USB camera
- Windows 10/11 or Linux (Ubuntu 20.04+)
- 4GB RAM minimum (8GB recommended)
- Internet connection for OpenAI API

## Required Dependencies

```plaintext
opencv-python>=4.8.0    # Computer vision and image processing
mediapipe>=0.10.0      # Face detection and mesh analysis
numpy>=1.24.0          # Numerical computations
openai>=0.28.0         # AI text generation
pyttsx3>=2.90          # Text-to-speech conversion
Pillow>=10.0.0         # Image processing
```

## Installation Instructions

1. **Set up Python Environment:**
   ```bash
   # Create a virtual environment (recommended)
   python -m venv venv

   # Activate virtual environment
   # On Windows:
   .\venv\Scripts\activate
   # On Linux/Mac:
   source venv/bin/activate
   ```

2. **Clone the Repository:**
   ```bash
   git clone https://github.com/hosthobbit/Facial-Recognition.git
   cd Facial-Recognition
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up OpenAI API:**
   - Get your API key from [OpenAI Platform](https://platform.openai.com)
   - Set the environment variable:
     ```bash
     # On Windows:
     setx OPENAI_API_KEY "your-api-key-here"
     # On Linux/Mac:
     export OPENAI_API_KEY="your-api-key-here"
     ```

5. **Configure Camera:**
   - Connect your webcam or USB camera
   - Ensure it's recognized by your system
   - Update camera index in config if needed (default is 0)

## Running the Application

1. **Start the Application:**
   ```bash
   python main.py
   ```

2. **First-time Setup:**
   - The system will create necessary directories for face data
   - Follow the prompts to train initial face recognition

3. **Using the System:**
   - Stand in front of the camera
   - The system will detect your face
   - For new faces, follow the training prompts
   - The AI will greet you and engage in conversation

## Troubleshooting

1. **Camera Issues:**
   - Check camera connection
   - Verify camera index in config
   - Ensure proper lighting

2. **Face Detection Problems:**
   - Maintain proper distance (2-6 feet)
   - Ensure good lighting
   - Face should be clearly visible

3. **Speech Issues:**
   - Check internet connection
   - Verify OpenAI API key
   - Check system audio settings

## Configuration Options

- Camera settings in `config.py`
- Face detection parameters in `face_detector.py`
- Speech settings in `speech_service.py`

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License - feel free to use and modify as needed.
