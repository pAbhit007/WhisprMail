import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle
from datetime import datetime, timedelta
from utils.logger import Logger
import base64
from email.mime.text import MIMEText
import re
import google.generativeai as genai

class EmailChecker:
    def __init__(self):
        self.logger = Logger('EmailChecker')
        self.SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
        self.creds = None
        self.service = None
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')  # Add your Gemini API key to .env
        self.initialize_service()

    def initialize_service(self):
        """Initialize the Gmail API service."""
        try:
            # The file token.pickle stores the user's access and refresh tokens
            if os.path.exists('token.pickle'):
                with open('token.pickle', 'rb') as token:
                    self.creds = pickle.load(token)
                    
            # If there are no (valid) credentials available, let the user log in
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials.json', self.SCOPES)
                    self.creds = flow.run_local_server(port=0)
                
                # Save the credentials for the next run
                with open('token.pickle', 'wb') as token:
                    pickle.dump(self.creds, token)

            self.service = build('gmail', 'v1', credentials=self.creds)
            self.logger.info('Gmail service initialized successfully')
        except Exception as e:
            self.logger.error(f'Error initializing Gmail service: {str(e)}')
            raise

    def classify_email_with_gemini(self, email_text):
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY not set in environment variables.")
        genai.configure(api_key=self.gemini_api_key)
        model = genai.GenerativeModel('gemini-2.0-flash-lite')
        prompt = (
            "Classify the following email into one of these categories: "
            "Promotion, Important, Advertisement, Social, Updates, Forums, Spam, Job Offer, Job Rejection, Other. "
            "Return only the category name. Email:\n"
            f"{email_text}"
        )
        try:
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            self.logger.error(f'Gemini classification error: {str(e)}')
            return "Other"

    def get_email_summary(self):
        """
        Check emails from the last 24 hours and categorize them using Gemini.
        Returns a tuple of (category_counts, summary_text)
        """
        try:
            # Calculate time 24 hours ago in epoch format
            time_24h_ago = int((datetime.now() - timedelta(days=1)).timestamp())
            
            # Search query for emails in the last 24 hours
            query = f'after:{time_24h_ago}'
            
            # Get messages
            results = self.service.users().messages().list(
                userId='me', q=query).execute()
            messages = results.get('messages', [])

            if not messages:
                summary = "No new emails in the last 24 hours."
                return {"None": 0}, summary

            category_counts = {}
            category_subjects = {}

            for message in messages:
                msg = self.service.users().messages().get(
                    userId='me', id=message['id']).execute()
                
                subject = ''
                for header in msg['payload']['headers']:
                    if header['name'] == 'Subject':
                        subject = header['value']
                        break

                # Get email body
                if 'parts' in msg['payload']:
                    parts = msg['payload']['parts']
                    data = parts[0]['body'].get('data', '')
                else:
                    data = msg['payload']['body'].get('data', '')
                
                try:
                    text = base64.urlsafe_b64decode(data).decode('utf-8')
                except Exception:
                    text = ''

                # Use Gemini to classify
                category = self.classify_email_with_gemini(text)
                if category not in category_counts:
                    category_counts[category] = 0
                category_counts[category] += 1
                category_subjects.setdefault(category, []).append(subject)

            # Create summary
            summary = f"Email Summary for {datetime.now().strftime('%Y-%m-%d')}:\n\n"
            for cat, count in category_counts.items():
                summary += f"{cat}: {count}\n"
                for subj in category_subjects[cat]:
                    summary += f"  • {subj}\n"
            if not category_counts:
                summary += "No relevant emails found in the last 24 hours."

            return category_counts, summary

        except Exception as e:
            self.logger.error(f'Error checking emails: {str(e)}')
            raise