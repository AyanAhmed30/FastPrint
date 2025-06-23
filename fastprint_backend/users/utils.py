from django.core.mail import send_mail
from django.conf import settings

def send_verification_email(user, uidb64, token):
    link = f"http://localhost:8000/api/users/verify-email/{uidb64}/{token}/"
    subject = "Email Verification - FastPrintGuys"
    message = f"Hi {user.name},\n\nPlease verify your email using the following link:\n{link}"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)

def send_password_reset_email(user, uidb64, token):
    link = f"http://localhost:8000/api/users/reset-password/{uidb64}/{token}/"
    subject = "Reset Your Password - FastPrintGuys"
    message = f"Hi {user.name},\n\nClick below to reset your password:\n{link}"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
