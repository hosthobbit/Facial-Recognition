# AI Camera with Face Recognition and Interactive Speech

This project implements an AI camera system with face recognition capabilities and interactive speech features. The system can detect faces, recognize individuals, and engage in natural conversation including greetings and goodbyes.

## Features

- Real-time face detection using MediaPipe
- Face recognition with personalized greetings
- Dynamic conversation management (greetings and goodbyes)
- Support for multiple simultaneous faces
- Cooldown system for natural interaction timing

## Requirements

Install the required packages using:

```bash
pip install -r requirements.txt
```

## Setup

1. Clone this repository
2. Install dependencies
3. Set up your OpenAI API key in environment variables
4. Run the application:
   ```bash
   python main.py
   ```

## Configuration

- The system uses MediaPipe for robust face detection
- Face recognition is performed using face embeddings
- Speech generation uses OpenAI's API for natural language
- Interaction timing is managed through cooldown periods

## Usage

- The system will automatically detect and track faces in view
- New faces can be registered for recognition
- The AI will greet recognized individuals and say goodbye when they leave
- Multiple people can be tracked simultaneously

## Contributing

Feel free to submit issues and enhancement requests!