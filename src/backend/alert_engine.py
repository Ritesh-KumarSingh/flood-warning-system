"""
Alert Engine Module
Handles notification delivery via SMS, Email, and Push Notifications
"""

import os
from typing import List, Dict, Optional
from datetime import datetime
import json
from enum import Enum


class AlertChannel(Enum):
    """Alert delivery channels"""
    SMS = "sms"
    EMAIL = "email"
    PUSH = "push"
    ALL = "all"


class AlertEngine:
    """
    Alert delivery engine
    Sends notifications via multiple channels when flood risk is detected
    """
    
    def __init__(self, demo_mode: bool = True):
        """
        Initialize alert engine
        
        Args:
            demo_mode: If True, simulates sending (no actual API calls)
        """
        self.demo_mode = demo_mode
        self.alert_log = []
        
        # Twilio credentials (SMS)
        self.twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        self.twilio_auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        self.twilio_phone = os.environ.get('TWILIO_PHONE_NUMBER')
        
        # Email credentials
        self.smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.environ.get('SMTP_PORT', '587'))
        self.email_user = os.environ.get('EMAIL_USER')
        self.email_password = os.environ.get('EMAIL_PASSWORD')
        
        if demo_mode:
            print("🎭 Alert Engine in DEMO MODE (simulates sending)")
        else:
            print("🚀 Alert Engine in PRODUCTION MODE")
            if not self.twilio_account_sid:
                print("⚠️  Warning: Twilio credentials not set (SMS disabled)")
            if not self.email_user:
                print("⚠️  Warning: Email credentials not set (Email disabled)")
    
    def should_send_alert(self, risk_level: int, threshold: int = 1) -> bool:
        """
        Determine if alert should be sent based on risk level
        
        Args:
            risk_level: Current risk level (0-3)
            threshold: Minimum risk level to trigger alert (default: 1)
            
        Returns:
            True if alert should be sent
        """
        return risk_level >= threshold
    
    def send_alert(self, 
                   alert_data: Dict,
                   phone_numbers: Optional[List[str]] = None,
                   email_addresses: Optional[List[str]] = None,
                   channels: List[AlertChannel] = None) -> Dict:
        """
        Send alert via specified channels
        
        Args:
            alert_data: Alert information from risk assessment
            phone_numbers: List of phone numbers for SMS
            email_addresses: List of email addresses
            channels: List of delivery channels to use
            
        Returns:
            Delivery status report
        """
        if channels is None:
            channels = [AlertChannel.ALL]
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'risk_level': alert_data['risk_level'],
            'location': alert_data['location'],
            'deliveries': []
        }
        
        # Determine which channels to use
        send_sms = AlertChannel.SMS in channels or AlertChannel.ALL in channels
        send_email = AlertChannel.EMAIL in channels or AlertChannel.ALL in channels
        send_push = AlertChannel.PUSH in channels or AlertChannel.ALL in channels
        
        # Send SMS
        if send_sms and phone_numbers:
            sms_result = self._send_sms(alert_data, phone_numbers)
            results['deliveries'].append(sms_result)
        
        # Send Email
        if send_email and email_addresses:
            email_result = self._send_email(alert_data, email_addresses)
            results['deliveries'].append(email_result)
        
        # Send Push Notification
        if send_push:
            push_result = self._send_push_notification(alert_data)
            results['deliveries'].append(push_result)
        
        # Log the alert
        self.alert_log.append(results)
        
        return results
    
    def _send_sms(self, alert_data: Dict, phone_numbers: List[str]) -> Dict:
        """Send SMS alert via Twilio"""
        
        # Prepare message
        message = self._format_sms_message(alert_data)
        
        if self.demo_mode:
            print(f"\n📱 SIMULATING SMS to {len(phone_numbers)} recipient(s)")
            print(f"Message: {message[:100]}...")
            
            return {
                'channel': 'SMS',
                'status': 'simulated',
                'recipients': len(phone_numbers),
                'message': message,
                'timestamp': datetime.now().isoformat()
            }
        
        try:
            from twilio.rest import Client
            
            if not self.twilio_account_sid:
                raise ValueError("Twilio credentials not configured")
            
            client = Client(self.twilio_account_sid, self.twilio_auth_token)
            
            sent_count = 0
            failed_count = 0
            
            for phone in phone_numbers:
                try:
                    message_obj = client.messages.create(
                        body=message,
                        from_=self.twilio_phone,
                        to=phone
                    )
                    sent_count += 1
                    print(f"✅ SMS sent to {phone}: {message_obj.sid}")
                except Exception as e:
                    failed_count += 1
                    print(f"❌ Failed to send SMS to {phone}: {e}")
            
            return {
                'channel': 'SMS',
                'status': 'sent',
                'sent': sent_count,
                'failed': failed_count,
                'total': len(phone_numbers),
                'timestamp': datetime.now().isoformat()
            }
            
        except ImportError:
            print("⚠️  Twilio library not installed. Run: pip install twilio")
            return {'channel': 'SMS', 'status': 'error', 'message': 'Twilio not installed'}
        except Exception as e:
            print(f"❌ SMS Error: {e}")
            return {'channel': 'SMS', 'status': 'error', 'message': str(e)}
    
    def _send_email(self, alert_data: Dict, email_addresses: List[str]) -> Dict:
        """Send email alert"""
        
        subject = f"🚨 {alert_data['title']}"
        body = self._format_email_message(alert_data)
        
        if self.demo_mode:
            print(f"\n📧 SIMULATING EMAIL to {len(email_addresses)} recipient(s)")
            print(f"Subject: {subject}")
            print(f"Body preview: {body[:150]}...")
            
            return {
                'channel': 'EMAIL',
                'status': 'simulated',
                'recipients': len(email_addresses),
                'subject': subject,
                'timestamp': datetime.now().isoformat()
            }
        
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            
            if not self.email_user:
                raise ValueError("Email credentials not configured")
            
            sent_count = 0
            failed_count = 0
            
            # Create SMTP session
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_user, self.email_password)
                
                for email in email_addresses:
                    try:
                        msg = MIMEMultipart()
                        msg['From'] = self.email_user
                        msg['To'] = email
                        msg['Subject'] = subject
                        msg.attach(MIMEText(body, 'plain'))
                        
                        server.send_message(msg)
                        sent_count += 1
                        print(f"✅ Email sent to {email}")
                    except Exception as e:
                        failed_count += 1
                        print(f"❌ Failed to send email to {email}: {e}")
            
            return {
                'channel': 'EMAIL',
                'status': 'sent',
                'sent': sent_count,
                'failed': failed_count,
                'total': len(email_addresses),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Email Error: {e}")
            return {'channel': 'EMAIL', 'status': 'error', 'message': str(e)}
    
    def _send_push_notification(self, alert_data: Dict) -> Dict:
        """Send push notification (simulated)"""
        
        # In production, integrate with Firebase Cloud Messaging (FCM)
        # or Apple Push Notification Service (APNS)
        
        notification = {
            'title': alert_data['title'],
            'body': alert_data['message'][:200],
            'data': {
                'risk_level': alert_data['risk_level'],
                'location': alert_data['location']
            }
        }
        
        print(f"\n🔔 SIMULATING PUSH NOTIFICATION")
        print(f"Title: {notification['title']}")
        print(f"Body: {notification['body'][:100]}...")
        
        return {
            'channel': 'PUSH',
            'status': 'simulated',
            'notification': notification,
            'timestamp': datetime.now().isoformat()
        }
    
    def _format_sms_message(self, alert_data: Dict) -> str:
        """Format alert for SMS (160 characters)"""
        
        risk_labels = ['SAFE', 'WARNING', 'HIGH RISK', 'CRITICAL']
        risk = risk_labels[alert_data['risk_level']]
        
        # SMS must be concise (160 chars for single message)
        message = f"FLOOD ALERT: {risk} - {alert_data['location']}. "
        
        if alert_data['risk_level'] >= 3:
            message += "EVACUATE IMMEDIATELY! Call 112."
        elif alert_data['risk_level'] >= 2:
            message += "Prepare to evacuate. Stay alert."
        elif alert_data['risk_level'] >= 1:
            message += "Monitor updates. Prepare emergency kit."
        else:
            message += "No immediate danger. Stay informed."
        
        return message
    
    def _format_email_message(self, alert_data: Dict) -> str:
        """Format alert for email"""
        
        message = f"""
FLOOD EARLY WARNING ALERT

Location: {alert_data['location']}
Risk Level: {alert_data['risk_label']} (Level {alert_data['risk_level']})
Severity: {alert_data['severity']}
Timestamp: {alert_data['timestamp']}

{alert_data['message']}

RECOMMENDED ACTIONS:
"""
        
        for i, action in enumerate(alert_data['recommended_actions'], 1):
            message += f"{i}. {action}\n"
        
        if alert_data.get('emergency_contacts'):
            message += "\nEMERGENCY CONTACTS:\n"
            for service, number in alert_data['emergency_contacts'].items():
                message += f"- {service.replace('_', ' ').title()}: {number}\n"
        
        if alert_data.get('additional_info'):
            message += "\nCRITICAL CONDITIONS DETECTED:\n"
            for info in alert_data['additional_info']:
                message += f"- {info}\n"
        
        message += """
---
This is an automated alert from the AI-Based Flood Early Warning System.
Do not reply to this message.
"""
        
        return message
    
    def send_bulk_alerts(self, 
                        assessments: List[Dict],
                        contact_database: Dict) -> List[Dict]:
        """
        Send alerts for multiple locations
        
        Args:
            assessments: List of risk assessments
            contact_database: Dict mapping locations to contact lists
            
        Returns:
            List of delivery results
        """
        results = []
        
        for assessment in assessments:
            location = assessment['location']
            
            # Check if alert should be sent
            if self.should_send_alert(assessment['risk_level']):
                contacts = contact_database.get(location, {})
                
                result = self.send_alert(
                    assessment,
                    phone_numbers=contacts.get('phones', []),
                    email_addresses=contacts.get('emails', [])
                )
                
                results.append(result)
        
        return results
    
    def get_alert_log(self, limit: int = 10) -> List[Dict]:
        """Get recent alert log"""
        return self.alert_log[-limit:]
    
    def save_alert_log(self, filepath: str = "alert_log.json"):
        """Save alert log to file"""
        with open(filepath, 'w') as f:
            json.dump(self.alert_log, f, indent=2)
        print(f"✅ Alert log saved to {filepath}")


def demo_alert_engine():
    """Demonstrate alert engine functionality"""
    
    print("\n" + "="*70)
    print(" "*20 + "🚨 ALERT ENGINE DEMO")
    print("="*70 + "\n")
    
    # Initialize engine in demo mode
    engine = AlertEngine(demo_mode=True)
    
    # Example alert data (from risk assessment)
    alert_safe = {
        'timestamp': datetime.now().isoformat(),
        'location': 'Lucknow',
        'risk_level': 0,
        'risk_label': 'Safe',
        'risk_color': 'green',
        'severity': 'Low',
        'title': '✅ All Clear in Lucknow',
        'message': 'No flood risk detected. Weather conditions are normal.',
        'recommended_actions': [
            'Continue normal activities',
            'Stay updated on weather forecasts'
        ],
        'emergency_contacts': {}
    }
    
    alert_critical = {
        'timestamp': datetime.now().isoformat(),
        'location': 'Ayodhya',
        'risk_level': 3,
        'risk_label': 'Critical',
        'risk_color': 'red',
        'severity': 'Critical',
        'title': '🔴 CRITICAL FLOOD ALERT - AYODHYA',
        'message': 'CRITICAL FLOOD DANGER in Ayodhya! Evacuate immediately!',
        'recommended_actions': [
            '🚨 EVACUATE IMMEDIATELY to designated shelter',
            '🚨 Do NOT wait for further instructions',
            'Call emergency services: 112'
        ],
        'emergency_contacts': {
            'national_emergency': '112',
            'disaster_management': '1078'
        },
        'additional_info': [
            '🌧️ EXTREME rainfall: 340mm',
            '🌊 River at DANGER LEVEL: 13.2m'
        ]
    }
    
    # Test 1: Safe condition (should not send)
    print("TEST 1: Safe Condition")
    print("-"*70)
    if engine.should_send_alert(alert_safe['risk_level']):
        print("Would send alert (threshold: Warning+)")
    else:
        print("✅ No alert needed - conditions are safe")
    print()
    
    # Test 2: Critical condition (should send)
    print("TEST 2: Critical Condition")
    print("-"*70)
    if engine.should_send_alert(alert_critical['risk_level']):
        print("⚠️  Alert triggered! Sending to all channels...")
        
        result = engine.send_alert(
            alert_critical,
            phone_numbers=['+91-XXXXXXXXXX', '+91-YYYYYYYYYY'],
            email_addresses=['user1@example.com', 'user2@example.com'],
            channels=[AlertChannel.ALL]
        )
        
        print(f"\n📊 Delivery Report:")
        print(f"   Timestamp: {result['timestamp']}")
        print(f"   Location: {result['location']}")
        print(f"   Risk Level: {result['risk_level']}")
        print(f"   Channels used: {len(result['deliveries'])}")
    print()
    
    # Test 3: Bulk alerts
    print("TEST 3: Bulk Alert for Multiple Cities")
    print("-"*70)
    
    assessments = [alert_safe, alert_critical]
    contact_db = {
        'Lucknow': {
            'phones': ['+91-1111111111'],
            'emails': ['lucknow@example.com']
        },
        'Ayodhya': {
            'phones': ['+91-2222222222', '+91-3333333333'],
            'emails': ['ayodhya@example.com']
        }
    }
    
    results = engine.send_bulk_alerts(assessments, contact_db)
    print(f"\n✅ Bulk alerts processed: {len(results)} sent")
    
    # Show log
    print("\n" + "="*70)
    print("📋 ALERT LOG")
    print("="*70)
    log = engine.get_alert_log()
    for entry in log:
        print(f"\n[{entry['timestamp']}]")
        print(f"Location: {entry['location']}")
        print(f"Risk: {entry['risk_level']}")
        print(f"Deliveries: {len(entry['deliveries'])} channels")
    
    print("\n" + "="*70)
    print("✅ Alert Engine Demo Complete!")
    print("="*70 + "\n")


if __name__ == "__main__":
    demo_alert_engine()