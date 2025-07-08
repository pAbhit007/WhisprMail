import pywhatkit as pwk
import os
from utils.logger import Logger
from datetime import datetime, timedelta
import time

class WhatsAppSender:
    def __init__(self):
        self.logger = Logger('WhatsAppSender')

    def send_message(self, phone_number, message, audio_file=None):
        """
        Send text message and audio file (if provided) to specified WhatsApp number
        """
        try:
            # Ensure phone number is in correct format (with country code)
            if not phone_number.startswith('+91'):
                phone_number = '+91' + phone_number

            # Get current time for scheduling (2 minutes from now to allow browser to open)
            now = datetime.now()
            send_time = now + timedelta(minutes=2)
            
            # Send text message
            pwk.sendwhatmsg(
                phone_number,
                message,
                send_time.hour,
                send_time.minute
            )
            
            self.logger.info(f'Text message sent successfully to {phone_number}')
            
            # If audio file exists, send it
            if audio_file and os.path.exists(audio_file):
                # Wait for 30 seconds before sending audio
                time.sleep(30)
                pwk.sendwhats_image(
                    phone_number,
                    audio_file,
                    'Voice Summary',
                    wait_time=30
                )
                self.logger.info(f'Audio file sent successfully to {phone_number}')
                
        except Exception as e:
            self.logger.error(f'Error sending WhatsApp message: {str(e)}')
            raise