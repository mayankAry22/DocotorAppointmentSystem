from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.conf import settings
from appointment.models import Customer, Doctor

@receiver(post_save, sender=Customer)
@receiver(post_save, sender=Doctor)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Welcome to Our Website'
        message = f'Hello {instance.first_name} {instance.last_name},\n\nWelcome to our website! Thank you for joining us.'
        from_email = settings.EMAIL_HOST_USER
        recipient_email = [instance.email]
    elif instance.is_active == False:
        subject = 'Account Deactivated'
        message = f'Hello {instance.first_name} {instance.last_name},\n\nYour account has been deactivated.'
        from_email = settings.EMAIL_HOST_USER
        recipient_email = [instance.email]
    elif instance.is_active == True:
        subject = 'Account Activated'
        message = f'Hello {instance.first_name} {instance.last_name},\n\nYour account has been activated.'
        from_email = settings.EMAIL_HOST_USER
        recipient_email = [instance.email]
        
    send_mail(subject, message, from_email, recipient_email)