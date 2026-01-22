#!/usr/bin/env python
"""
Send Professional Email Design Samples
Sends 6 sample emails (3 verification + 3 welcome) to PO for review
"""
import os
import django
import sys

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vizpilot_config.settings')
django.setup()

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from accounts.models import User
from subscriptions.models import Plan

def send_sample_emails():
    """Send all 6 professional email design samples"""
    
    # Get or create sample user
    user, created = User.objects.get_or_create(
        email='w.designer@gmail.com',
        defaults={
            'full_name': 'Seed Ahmed',
            'is_active': True,
            'email_verified': False
        }
    )
    
    # Get or create a plan
    plan, _ = Plan.objects.get_or_create(
        slug='professional',
        defaults={
            'name': 'Professional',
            'tier': 'pro',
            'price_monthly': 2900,  # $29.00
            'price_yearly': 29000,  # $290.00
            'limits': {
                'technologies': 5,
                'daily_views': 1000,
                'api_requests_daily': 1000,
                'team_seats': 1
            },
            'features': ['API Access', 'Protocol Library', 'IDE Integration']
        }
    )
    
    # Create sample subscription if needed
    if not hasattr(user, 'subscription') or user.subscription is None:
        from subscriptions.models import Subscription
        from datetime import datetime, timedelta
        from django.utils import timezone
        
        now = timezone.now()
        Subscription.objects.get_or_create(
            user=user,
            defaults={
                'plan': plan,
                'status': 'trialing',
                'billing_cycle': 'monthly',
                'current_period_start': now,
                'current_period_end': now + timedelta(days=14),
                'usage_reset_at': now + timedelta(days=14)
            }
        )
        user.refresh_from_db()
    
    # Sample data for templates
    context = {
        'user': user,
        'verification_url': 'https://vizpilot.vizulabs.com/verify/sample-token-abc123',
        'dashboard_url': 'https://vizpilot.vizulabs.com/dashboard/',
        'site_url': 'https://vizpilot.vizulabs.com'
    }
    
    # Add subscription data if available
    if hasattr(user, 'subscription') and user.subscription:
        context['user'].subscription.plan.api_requests_per_day = user.subscription.plan.limits.get('api_requests_daily', 1000)
        context['user'].subscription.plan.technology_limit = user.subscription.plan.limits.get('technologies', 5)
    
    recipient = 'w.designer@gmail.com'
    from_email = settings.DEFAULT_FROM_EMAIL
    
    emails_sent = []
    
    # Send Verification Email Options
    verification_options = [
        ('verify_email_option1.html', 'Option 1: Classic Professional'),
        ('verify_email_option2.html', 'Option 2: Minimal Clean'),
        ('verify_email_option3.html', 'Option 3: Modern Corporate'),
    ]
    
    print("\n" + "="*60)
    print("SENDING VERIFICATION EMAIL SAMPLES")
    print("="*60 + "\n")
    
    for template, description in verification_options:
        try:
            html_content = render_to_string(f'emails/{template}', context)
            subject = f'[SAMPLE - {description}] Verify your VIZPILOT email'
            
            send_mail(
                subject=subject,
                message='Please view this email in HTML format.',
                from_email=from_email,
                recipient_list=[recipient],
                html_message=html_content,
                fail_silently=False,
            )
            
            print(f"✅ Sent: {description}")
            print(f"   Subject: {subject}")
            print(f"   Template: {template}\n")
            emails_sent.append(description)
            
        except Exception as e:
            print(f"❌ Failed to send {description}: {str(e)}\n")
    
    # Send Welcome Email Options
    welcome_options = [
        ('welcome_option1.html', 'Option 1: Classic Professional'),
        ('welcome_option2.html', 'Option 2: Minimal Clean'),
        ('welcome_option3.html', 'Option 3: Modern Corporate'),
    ]
    
    print("\n" + "="*60)
    print("SENDING WELCOME EMAIL SAMPLES")
    print("="*60 + "\n")
    
    for template, description in welcome_options:
        try:
            html_content = render_to_string(f'emails/{template}', context)
            subject = f'[SAMPLE - {description}] Welcome to VIZPILOT'
            
            send_mail(
                subject=subject,
                message='Please view this email in HTML format.',
                from_email=from_email,
                recipient_list=[recipient],
                html_message=html_content,
                fail_silently=False,
            )
            
            print(f"✅ Sent: {description}")
            print(f"   Subject: {subject}")
            print(f"   Template: {template}\n")
            emails_sent.append(description)
            
        except Exception as e:
            print(f"❌ Failed to send {description}: {str(e)}\n")
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"\n✅ Successfully sent {len(emails_sent)}/6 sample emails")
    print(f"📧 Recipient: {recipient}")
    print(f"📬 From: {from_email}")
    print("\n" + "="*60)
    print("NEXT STEPS")
    print("="*60)
    print("\n1. Check inbox: w.designer@gmail.com")
    print("2. Review all 6 email designs")
    print("3. Choose preferred option for each email type")
    print("4. Provide feedback to Ahmed Yousif (Orchestrator)")
    print("\nDesign Options:")
    print("  • Option 1: Classic Professional (Indigo header, clean layout)")
    print("  • Option 2: Minimal Clean (Black & white, minimalist)")
    print("  • Option 3: Modern Corporate (Gradient accent, structured)")
    print("\n" + "="*60 + "\n")

if __name__ == '__main__':
    send_sample_emails()
