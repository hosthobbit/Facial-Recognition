import os
import openai
import pyttsx3
import logging
import time
from typing import Dict, List, Optional, Set
from datetime import datetime, timedelta

class SpeechService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.engine = pyttsx3.init()
        self.known_faces = set()
        self.current_faces = set()
        self.last_welcome_times = {}
        self.welcome_cooldown = 3600
        self.goodbye_cooldown = 300
        self.last_goodbye_times = {}
        
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 1.0)
        
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
            self.logger.info('Loaded OpenAI API key from environment')

    def set_api_key(self, api_key: str):
        if not api_key:
            self.logger.error('Attempted to set empty API key')
            return False
            
        try:
            self.logger.info('Attempting to validate API key...')
            openai.api_key = api_key
            self.logger.info('API key set, attempting to list models...')
            
            try:
                models = openai.Model.list()
                self.logger.info(f'Successfully listed {len(models.data)} models')
            except Exception as e:
                self.logger.warning(f'Model listing failed, but continuing anyway: {str(e)}')
            
            self.openai_api_key = api_key
            self.logger.info('OpenAI API key set and validated successfully')
            return True
        except Exception as e:
            self.logger.error(f'Error validating API key: {str(e)}')
            self.logger.error(f'Error type: {type(e).__name__}')
            return False

    def update_faces(self, current_faces: Set[str]):
        self.logger.info(f'Current faces: {self.current_faces}')
        self.logger.info(f'New faces detected: {current_faces}')
        
        departed_faces = self.current_faces - current_faces
        for face in departed_faces:
            if self.can_say_goodbye(face):
                message = self.generate_goodbye_message(face)
                self.speak(message)
                self.last_goodbye_times[face] = datetime.now()
                self.logger.info(f'Said goodbye to {face}')
        
        new_faces = current_faces - self.current_faces
        self.logger.info(f'New faces to welcome: {new_faces}')
        
        for face in new_faces:
            if self.can_welcome(face):
                self.welcome_person(face, is_first_time=(face not in self.known_faces))
                self.last_welcome_times[face] = datetime.now()
                self.logger.info(f'Welcomed {face}')
        
        self.current_faces = current_faces
        self.known_faces.update(current_faces)
        self.logger.info(f'Updated current faces to: {self.current_faces}')

    def can_welcome(self, name: str) -> bool:
        if name not in self.last_welcome_times:
            return True
        last_welcome = self.last_welcome_times[name]
        time_since_last = (datetime.now() - last_welcome).total_seconds()
        can_welcome = time_since_last >= self.welcome_cooldown
        self.logger.info(f'Can welcome {name}? {can_welcome} (last welcome: {time_since_last}s ago)')
        return can_welcome

    def can_say_goodbye(self, name: str) -> bool:
        if name not in self.last_goodbye_times:
            return True
        last_goodbye = self.last_goodbye_times[name]
        time_since_last = (datetime.now() - last_goodbye).total_seconds()
        return time_since_last >= self.goodbye_cooldown

    def welcome_person(self, name: str, is_first_time: bool = False):
        try:
            message = self.generate_welcome_message(name, is_first_time)
            self.speak(message)
            self.logger.info(f'Welcomed {name} (first time: {is_first_time})')
        except Exception as e:
            self.logger.error(f'Error welcoming {name}: {str(e)}')
            self.speak(f'Welcome {name}!')

    def generate_welcome_message(self, name: str, is_first_time: bool = False) -> str:
        if not self.openai_api_key:
            self.logger.warning('No OpenAI API key set, using default welcome message')
            return f'Welcome {name}!'
            
        try:
            prompt = f'Generate a short, friendly welcome message for {name}'
            if is_first_time:
                prompt += ' who is using the system for the first time'
            else:
                prompt += ' who has returned'
            prompt += '. Make it witty and engaging but keep it under 20 words.'
            
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=[
                    {'role': 'system', 'content': 'You are a friendly AI assistant generating welcome messages.'},
                    {'role': 'user', 'content': prompt}
                ],
                max_tokens=50
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            self.logger.error(f'Error generating welcome message: {str(e)}')
            return f'Welcome {name}!'

    def generate_goodbye_message(self, name: str) -> str:
        if not self.openai_api_key:
            self.logger.warning('No OpenAI API key set, using default goodbye message')
            return f'Goodbye {name}, see you soon!'
            
        try:
            prompt = f'Generate a short, friendly goodbye message for {name}. Make it warm and personal but keep it under 20 words.'
            
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=[
                    {'role': 'system', 'content': 'You are a friendly AI assistant generating goodbye messages.'},
                    {'role': 'user', 'content': prompt}
                ],
                max_tokens=50
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            self.logger.error(f'Error generating goodbye message: {str(e)}')
            return f'Goodbye {name}, see you soon!'

    def speak(self, text: str):
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            self.logger.error(f'Error in text-to-speech: {str(e)}')