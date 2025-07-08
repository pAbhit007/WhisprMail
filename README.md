

An automated email monitoring system that checks for job-related emails, summarizes them, and sends notifications via WhatsApp with both text and voice messages.

## Features

- Monitors Gmail inbox for job-related emails
- Categorizes emails into positive responses (congratulations) and rejections
- Generates daily summary
- Converts summary to voice message
- Sends both text and voice messages via WhatsApp
- Runs automatically every day at 9:00 AM
- Comprehensive logging system

## Prerequisites

- Python 3.7+
- Google Cloud Platform account
- Gmail account
- WhatsApp account
- Chrome browser (for WhatsApp Web)

## Setup

1. Install required packages:

   ```bash
   pip install -r requirements.txt
   ```

2. Set up Google Cloud Project:
   - Go to Google Cloud Console
   - Create a new project
   - Enable Gmail API
   - Create OAuth 2.0 credentials
   - Download credentials and save as `credentials.json` in the project root

3. Create a `.env` file in the project root with your WhatsApp number:

   ```env
   WHATSAPP_NUMBER=+1234567890  # Include country code
   ```

4. First-time setup:
   - Run the script: `python scheduler.py`
   - Complete Google OAuth authentication when prompted
   - Allow WhatsApp Web access when the browser opens

## Project Structure

```
WhisprMail/
├── requirements.txt
├── credentials.json
├── .env
├── scheduler.py          # Main scheduler
├── email_checker.py      # Gmail integration
├── voice_generator.py    # Text-to-speech
├── whatsapp_sender.py    # WhatsApp messaging
└── utils/
    └── logger.py        # Logging utility
```

## Running the Application

```bash
python scheduler.py
```

The application will run continuously and execute the email checking process daily at 9:00 AM.

## Logs

Logs are stored in the `logs` directory with daily rotation. Check these logs for monitoring the application's operation and troubleshooting.

## Note

- Keep the `token.pickle` file secure as it contains your Gmail access tokens
- Ensure your computer is running and connected to the internet at the scheduled time
- The WhatsApp number in .env should include the country code

## Error Handling

The application includes comprehensive error handling and logging. Check the logs in the `logs` directory for any issues.