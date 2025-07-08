from gtts import gTTS
import os
from utils.logger import Logger
from datetime import datetime

class VoiceGenerator:
    def __init__(self):
        self.logger = Logger('VoiceGenerator')
        
        # Create audio directory if it doesn't exist
        if not os.path.exists('audio'):
            os.makedirs('audio')

    def generate_voice_message(self, text):
        """
        Convert text to speech and save as MP3
        Returns the path to the generated audio file
        """
        try:
            # Generate unique filename based on timestamp
            filename = f"audio/summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
            
            # Generate audio file
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(filename)
            
            self.logger.info(f'Voice message generated successfully: {filename}')
            return filename
            
        except Exception as e:
            self.logger.error(f'Error generating voice message: {str(e)}')
            raise