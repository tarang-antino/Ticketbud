from django.template import Context
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings


def send_review_email(email,types,context):
    # print("Hello")
    # context = {
    #     'name': name,
    #     'otp':otp
        
    # }

    
    if types=="register":
        email_subject = 'Welcome'
        email_body = render_to_string('./event/templates/email_message_register.txt', context)
    elif types=="OTP":
        email_subject = 'Forgot Password'
        email_body = render_to_string('./event/templates/email_message.txt', context)
    elif types=="bookevent":
        email_subject = 'Event Booked'
        email_body = render_to_string('./event/templates/email_message_bookevent.txt', context)
    # print("------------------------------------------------------------------------------------",email_body)
    # email_body="abcd"

    email = EmailMessage(
        email_subject, email_body,
        settings.DEFAULT_FROM_EMAIL, ["tarang.a@antino.io",email],
    )
    return email.send(fail_silently=False)