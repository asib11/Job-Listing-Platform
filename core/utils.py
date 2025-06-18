from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_welcome_email(user):

    subject = 'Welcome to Our Platform!'
    html_message = render_to_string('emails/welcome_email.html', {
        'user': user,
        'first_name': user.first_name
    })
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending welcome email: {str(e)}")
        return False


def send_password_reset_email(user, reset_url):
    subject = 'Reset Your Password'
    html_message = render_to_string('emails/password_reset_email.html', {
        'user': user,
        'reset_url': reset_url,
        'first_name': user.first_name,
        'valid_hours': 24  # Token validity period in hours
    })
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending password reset email: {str(e)}")
        return False
