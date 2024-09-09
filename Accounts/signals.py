from allauth.account.signals import user_signed_up, user_logged_in
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.conf import settings
from .models import OtpToken
from django.core.mail import send_mail
from django.utils import timezone
User = get_user_model()

 
@receiver(post_save, sender=settings.AUTH_USER_MODEL) 
def create_token(sender, instance, created, **kwargs):
    if created:
        OtpToken.objects.create(user=instance, otp_expires_at=timezone.now() + timezone.timedelta(minutes=1))
        instance.is_active=False 
        instance.save()  
        # email credentials
        otp = OtpToken.objects.filter(user=instance).last()      
       
        subject="Email Verification"
        message = f"""
                                Hi {instance.username}, here is your OTP {otp.otp_code} 
                                it expires in 1 minute, use the url below to redirect back to the website
                                http://127.0.0.1:8000/verify-email/{instance.username}
                                
                                """
        sender = "salmathsalam1020@gmail.com"
        receiver = [instance.email, ]
        # Debugging
        print(f"Sending email to {receiver}")
        
        # send email
        send_mail(
                subject,
                message,
                sender,
                receiver,
                fail_silently=False,
            )
  

@receiver(user_signed_up)
def activate_user_on_signup(request, user, **kwargs):
    if user.is_active is False:
        user.is_active = True
        user.save()

@receiver(user_logged_in)
def activate_user_on_login(request, user, **kwargs):
    if user.is_active is False:
        user.is_active = True
        user.save()
