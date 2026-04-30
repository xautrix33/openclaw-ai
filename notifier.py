import smtplib
import logging
from email.mime.text import MIMEText
from datetime import datetime

class Notifier:
    def __init__(self, email_config):
        self.email_config = email_config
        logging.basicConfig(level=logging.INFO, filename='notifications.log',
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def send_email(self, subject, message):
        try:
            msg = MIMEText(message)
            msg['Subject'] = subject
            msg['From'] = self.email_config['from_email']
            msg['To'] = self.email_config['to_email']

            with smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port']) as server:
                server.starttls()
                server.login(self.email_config['from_email'], self.email_config['password'])
                server.sendmail(self.email_config['from_email'], self.email_config['to_email'], msg.as_string())
            logging.info(f'Email sent: {subject}')
        except Exception as e:
            logging.error(f'Failed to send email: {subject} - {e}')

    def trade_entry(self, trade_details):
        subject = 'Trade Entry Alert'
        message = f'New trade entry:
\n{trade_details}'
        self.send_email(subject, message)

    def trade_exit(self, trade_details):
        subject = 'Trade Exit Alert'
        message = f'Trade exit:
\n{trade_details}'
        self.send_email(subject, message)

    def critical_error(self, error_message):
        subject = 'Critical Error Alert'
        message = f'Error occurred:
\n{error_message}'
        self.send_email(subject, message)

    def daily_summary(self, summary_data):
        subject = 'Daily Summary Report'
        message = f'Daily summary:
\n{summary_data}'
        self.send_email(subject, message)

    def fallback(self):
        logging.warning('Email notification failed, triggered fallback actions here.')

# Example Configuration
email_config = {
    'from_email': 'your_email@example.com',
    'to_email': 'recipient@example.com',
    'smtp_server': 'smtp.example.com',
    'smtp_port': 587,
    'password': 'your_password'
}

# Usage
notifier = Notifier(email_config)
notifier.trade_entry('Trade details here...')  # Call this where you handle trade entries
notifier.trade_exit('Trade exit details here...')  # Call this where you handle trade exits
notifier.critical_error('An error occurred!')  # Call this to log critical errors
notifier.daily_summary('Today’s summary report data here...')  # Call daily summaries