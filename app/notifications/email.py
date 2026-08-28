import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import os

logger = logging.getLogger(__name__)

class EmailService:
    @staticmethod
    def send_alert_email(to_email, subject, html_content):
        """
        Sends an HTML email via SMTP.
        Configuration should be loaded from environment variables in production.
        """
        smtp_host = os.environ.get('SMTP_HOST', 'smtp.mailtrap.io')
        smtp_port = int(os.environ.get('SMTP_PORT', 2525))
        smtp_user = os.environ.get('SMTP_USER', 'mock_user')
        smtp_pass = os.environ.get('SMTP_PASS', 'mock_pass')
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = "alerts@dataflownexus.com"
        msg['To'] = to_email
        
        part = MIMEText(html_content, 'html')
        msg.attach(part)
        
        try:
            # Using a context manager for the SMTP connection
            with smtplib.SMTP(smtp_host, smtp_port) as server:
                if smtp_user and smtp_pass:
                    server.login(smtp_user, smtp_pass)
                server.sendmail(msg['From'], [msg['To']], msg.as_string())
                
            logger.info(f"Alert email sent to {to_email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}")
            return False
