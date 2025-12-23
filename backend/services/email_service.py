import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Any
from backend.config import settings
from backend.models.lead import Lead, LeadFields
from datetime import datetime
import asyncio


class EmailService:
    """Email notification service using Gmail SMTP"""
    
    def __init__(self):
        self.smtp_host = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = settings.gmail_address
        self.sender_password = settings.app_password
    
    async def send_email(
        self,
        to_emails: List[str],
        subject: str,
        html_content: str,
        retry_count: int = 3
    ) -> bool:
        """
        Send email with retry logic
        
        Args:
            to_emails: List of recipient emails
            subject: Email subject
            html_content: HTML email content
            retry_count: Number of retries on failure
        
        Returns:
            True if sent successfully, False otherwise
        """
        for attempt in range(retry_count):
            try:
                # Create message
                message = MIMEMultipart("alternative")
                message["From"] = self.sender_email
                message["To"] = ", ".join(to_emails)
                message["Subject"] = subject
                
                # Attach HTML content
                html_part = MIMEText(html_content, "html")
                message.attach(html_part)
                
                # Send email
                await aiosmtplib.send(
                    message,
                    hostname=self.smtp_host,
                    port=self.smtp_port,
                    username=self.sender_email,
                    password=self.sender_password,
                    start_tls=True
                )
                
                print(f"Email sent successfully to {to_emails}")
                return True
                
            except Exception as e:
                print(f"Email send attempt {attempt + 1} failed: {e}")
                if attempt < retry_count - 1:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                else:
                    print(f"Failed to send email after {retry_count} attempts")
                    return False
        
        return False
    
    def create_hot_lead_email(
        self,
        lead: Lead,
        conversation_snippet: str,
        tenant_name: str
    ) -> str:
        """
        Create HTML email for hot lead notification
        
        Args:
            lead: Lead object
            conversation_snippet: Recent conversation
            tenant_name: Business name
        
        Returns:
            HTML email content
        """
        fields = lead.fields
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px 10px 0 0;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 24px;
        }}
        .badge {{
            display: inline-block;
            background: #ef4444;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 12px;
            margin-top: 10px;
        }}
        .content {{
            background: #f9fafb;
            padding: 30px;
            border-radius: 0 0 10px 10px;
        }}
        .field {{
            background: white;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
            border-left: 4px solid #667eea;
        }}
        .field-label {{
            font-weight: bold;
            color: #667eea;
            font-size: 12px;
            text-transform: uppercase;
        }}
        .field-value {{
            font-size: 16px;
            margin-top: 5px;
        }}
        .conversation {{
            background: white;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
            border: 1px solid #e5e7eb;
        }}
        .score {{
            text-align: center;
            font-size: 48px;
            font-weight: bold;
            color: #667eea;
            margin: 20px 0;
        }}
        .cta {{
            text-align: center;
            margin: 30px 0;
        }}
        .cta a {{
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 15px 30px;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔥 Hot Lead Alert!</h1>
        <div class="badge">SCORE: {lead.score}/100</div>
    </div>
    
    <div class="content">
        <p>A high-quality lead has been captured on {tenant_name}. Here are the details:</p>
        
        <div class="field">
            <div class="field-label">Name</div>
            <div class="field-value">{fields.name or 'Not provided'}</div>
        </div>
        
        <div class="field">
            <div class="field-label">Email</div>
            <div class="field-value">{fields.email or 'Not provided'}</div>
        </div>
        
        <div class="field">
            <div class="field-label">Phone</div>
            <div class="field-value">{fields.phone or 'Not provided'}</div>
        </div>
        
        <div class="field">
            <div class="field-label">Service Interest</div>
            <div class="field-value">{fields.service_interest or 'Not specified'}</div>
        </div>
        
        <div class="field">
            <div class="field-label">Budget</div>
            <div class="field-value">{fields.budget or 'Not specified'}</div>
        </div>
        
        <div class="field">
            <div class="field-label">Timeline</div>
            <div class="field-value">{fields.timeline or 'Not specified'}</div>
        </div>
        
        <h3>Recent Conversation:</h3>
        <div class="conversation">
            {conversation_snippet}
        </div>
        
        <p style="text-align: center; color: #6b7280; font-size: 14px;">
            Lead captured at {lead.created_at.strftime('%Y-%m-%d %H:%M:%S')} UTC
        </p>
    </div>
</body>
</html>
"""
        return html
    
    async def send_hot_lead_notification(
        self,
        lead: Lead,
        conversation_snippet: str,
        tenant_name: str,
        notification_emails: List[str]
    ) -> bool:
        """
        Send hot lead notification email
        
        Args:
            lead: Lead object
            conversation_snippet: Recent conversation
            tenant_name: Business name
            notification_emails: List of emails to notify
        
        Returns:
            True if sent successfully
        """
        subject = f"🔥 Hot Lead Alert: {lead.fields.name or 'New Lead'} (Score: {lead.score}/100)"
        html_content = self.create_hot_lead_email(lead, conversation_snippet, tenant_name)
        
        return await self.send_email(notification_emails, subject, html_content)


# Global email service instance
email_service = EmailService()
