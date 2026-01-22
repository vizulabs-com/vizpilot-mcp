"""
Send sample emails to test email templates
Email Testing Specialist Implementation
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vizpilot_config.settings')
django.setup()

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from accounts.models import User, EmailVerificationToken
from subscriptions.models import Plan

def send_sample_verification_email(recipient_email):
    """Send sample verification email"""
    print(f"📧 Sending sample verification email to {recipient_email}...")
    
    # Create or get a test user
    user, created = User.objects.get_or_create(
        email='sample.user@example.com',
        defaults={
            'full_name': 'Sample User',
            'company': 'Sample Company',
        }
    )
    
    # Create a sample token
    token = EmailVerificationToken.objects.create(user=user)
    
    # Build verification URL
    verification_url = f"{settings.SITE_URL}/accounts/verify-email/{token.token}/"
    
    # Render email template
    html_message = render_to_string('emails/verify_email.html', {
        'user': user,
        'verification_url': verification_url,
        'site_name': 'VIZPILOT',
        'site_url': settings.SITE_URL,
    })
    
    # Send email
    try:
        send_mail(
            subject='[SAMPLE] Verify your VIZPILOT email address',
            message='This is a sample verification email. Please view in HTML.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            html_message=html_message,
            fail_silently=False,
        )
        print(f"✅ Verification email sent successfully to {recipient_email}")
        return True
    except Exception as e:
        print(f"❌ Error sending verification email: {e}")
        return False


def send_sample_welcome_email(recipient_email):
    """Send sample welcome email"""
    print(f"📧 Sending sample welcome email to {recipient_email}...")
    
    # Get or create a test user with subscription
    user, created = User.objects.get_or_create(
        email='sample.user@example.com',
        defaults={
            'full_name': 'Sample User',
            'company': 'Sample Company',
            'email_verified': True,
        }
    )
    
    # Get a plan for the user
    try:
        plan = Plan.objects.first()
        if plan and hasattr(user, 'subscription'):
            user.subscription.plan = plan
    except:
        pass
    
    # Render email template
    html_message = render_to_string('emails/welcome.html', {
        'user': user,
        'dashboard_url': f"{settings.SITE_URL}/dashboard/",
        'site_name': 'VIZPILOT',
        'site_url': settings.SITE_URL,
    })
    
    # Send email
    try:
        send_mail(
            subject='[SAMPLE] Welcome to VIZPILOT! 🚀',
            message='This is a sample welcome email. Please view in HTML.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            html_message=html_message,
            fail_silently=False,
        )
        print(f"✅ Welcome email sent successfully to {recipient_email}")
        return True
    except Exception as e:
        print(f"❌ Error sending welcome email: {e}")
        return False


if __name__ == '__main__':
    recipient = 'w.designer@gmail.com'
    
    print("=" * 60)
    print("📬 VIZPILOT Email Template Testing")
    print("=" * 60)
    print(f"Recipient: {recipient}")
    print(f"SMTP Host: {settings.EMAIL_HOST}")
    print(f"From: {settings.DEFAULT_FROM_EMAIL}")
    print("=" * 60)
    print()
    
    # Send verification email
    result1 = send_sample_verification_email(recipient)
    print()
    
    # Send welcome email
    result2 = send_sample_welcome_email(recipient)
    print()
    
    print("=" * 60)
    if result1 and result2:
        print("✅ All sample emails sent successfully!")
        print(f"📬 Check {recipient} inbox for 2 emails:")
        print("   1. [SAMPLE] Verify your VIZPILOT email address")
        print("   2. [SAMPLE] Welcome to VIZPILOT! 🚀")
    else:
        print("❌ Some emails failed to send. Check errors above.")
    print("=" * 60)
