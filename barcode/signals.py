import random
import string
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
from django.core.mail import send_mail, EmailMessage
import threading
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.models import User 

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)
    
    def run(self):
        try:
            self.email.send()
        except Exception as e:
            # Log the error or handle it accordingly
            print(f"Failed to send email: {e}")

               
@receiver(post_save, sender=User)
def send_user_mail(sender, instance, created, *args, **kwargs):
    if created:
        # Handle referral logic here
        try:
            
            
            email_template = "emails/register_email.html"
            c = {
                'user': instance.username,
                'user_email': instance.email,
                'sender_email': settings.EMAIL_HOST_USER,
            }
            
            renderer = render_to_string(email_template, c)
            mysender = EmailMessage(subject='Welcome Back!', body=renderer, to=[instance.email], from_email=settings.EMAIL_HOST_USER)
            mysender.content_subtype = "html"
            EmailThread(mysender).start()
             
        except instance.DoesNotExist:
            print("Invalid referral code")               

@receiver(post_save, sender=ContactMessage)
def contact_notification(sender, created, instance, **kwargs):
    if created:
        # Notify user when their profile is updated
        subject = 'New Contact Message'
        email_template = "emails/contact_email.html"
        c = {
            'user': instance.full_name,
            'user_email': instance.email,
            'sender_email': settings.EMAIL_HOST_USER,
        }
        
        renderer = render_to_string(email_template, c)
        mysender = EmailMessage(subject=subject, body=renderer, to=[instance.email], from_email=settings.EMAIL_HOST_USER)
        mysender.content_subtype = "html"
        EmailThread(mysender).start()   
            
@receiver(post_save, sender=NewsletterSubscriber)
def subscriber_notification(sender, instance, created, **kwargs):
    if created:
        # Notify staff when a new subscriber is added
        subject = 'New Subscriber Alert'
        message = "Welcome to ASCON, thank you for subscribing to our email. we hope you are having a nice day.. do enjoy the reast of your day"
        
        # Use Django's template rendering system to create the email content
        email_template = "emails/new_subscriber_email.html"
        c = {
            'user_email': instance.email,
            'sender_email': settings.EMAIL_HOST_USER,
            'message': message,  # Assuming there's a message field
        }
        
        renderer = render_to_string(email_template, c)
        mysender = EmailMessage(subject=subject, body=renderer, to=[instance.email], from_email=settings.EMAIL_HOST_USER)
        mysender.content_subtype = "html"
        EmailThread(mysender).start()
