import schedule
import time
import os
from dotenv import load_dotenv
from email_checker import EmailChecker
from voice_generator import VoiceGenerator
from whatsapp_sender import WhatsAppSender
from utils.logger import Logger

class EmailAlertScheduler:
    def __init__(self):
        self.logger = Logger('EmailAlertScheduler')
        load_dotenv()  # Load environment variables
        
        # Initialize components
        self.email_checker = EmailChecker()
        self.voice_generator = VoiceGenerator()
        self.whatsapp_sender = WhatsAppSender()
        
        # Get WhatsApp number from environment variable
        self.whatsapp_number = os.getenv('WHATSAPP_NUMBER')
        if not self.whatsapp_number:
            raise ValueError("WHATSAPP_NUMBER environment variable not set")

    def process_daily_emails(self):
        """
        Main function to process emails and send alerts
        """
        try:
            self.logger.info("Starting daily email processing")
            
            # Get email summary
            result = self.email_checker.get_email_summary()
            self.logger.debug(f"Raw result from get_email_summary: {result}")
            if not isinstance(result, tuple) or len(result) != 2:
                self.logger.error(f"Expected 2 values from get_email_summary, got: {len(result) if isinstance(result, tuple) else type(result)}")
                return
            category_counts, summary = result
            self.logger.debug(f"category_counts: {category_counts}")
            self.logger.debug(f"summary: {summary}")
            
            # Generate voice message if there are relevant emails
            audio_file = None
            if category_counts and any(count > 0 for count in category_counts.values() if isinstance(count, int)):
                self.logger.debug("Relevant emails found, generating voice message.")
                audio_file = self.voice_generator.generate_voice_message(summary)
            else:
                self.logger.debug("No relevant emails found, skipping voice message generation.")
            
            # Send WhatsApp message
            self.logger.debug(f"Sending WhatsApp message to {self.whatsapp_number}")
            self.whatsapp_sender.send_message(
                self.whatsapp_number,
                summary,
                audio_file
            )
            
            self.logger.info("Daily email processing completed successfully")
            
        except Exception as e:
            self.logger.error(f"Error in daily email processing: {str(e)}")

    def start(self):
        """
        Start the scheduler
        """
        try:
            # Schedule the job to run daily at 16:15 (4:15 PM)
            schedule.every().day.at("16:39").do(self.process_daily_emails)
            
            self.logger.info("Scheduler started. Will run daily at 16:29 (4:29 PM)")
            
            # Keep the script running
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
                
        except Exception as e:
            self.logger.error(f"Error in scheduler: {str(e)}")
            raise

if __name__ == "__main__":
    scheduler = EmailAlertScheduler()
    scheduler.start()