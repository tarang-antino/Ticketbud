from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def send_review_email(email, types, context):
    # print("Hello")
    # context = {
    #     'name': name,
    #     'otp':otp

    # }
    print("---------------------------------------------", context)

    if types == "register":
        email_subject = 'Welcome'
        email_body = render_to_string('./event/templates/email_message_register.txt', context)
        # email_body=""
    elif types == "OTP":
        email_subject = 'Forgot Password'
        email_body = render_to_string('./event/templates/email_message.txt', context)
    elif types == "book-event":
        email_subject = 'Event Booked'
        email_body = render_to_string('./event/templates/email_message_bookevent.txt', context)
    elif types == "NewPass":
        email_subject = 'Password Updated'
        email_body = render_to_string('./event/templates/email_message_update.txt', context)
    elif types == "event-res":
        email_subject = 'Event Reschedule Requested'
        email_body = render_to_string('./event/templates/email_message_eventres.txt', context)
    elif types == "delete":
        email_subject = 'Event Booking Cancel Requested'
        email_body = render_to_string('./event/templates/email_message_delete.txt', context)
    elif types == "edit":
        email_subject = 'Profile Updated'
        email_body = render_to_string('./event/templates/email_message_edit.txt', context)

    # print("------------------------------------------------------------------------------------",email_body)
    # email_body="abcd"

    email = EmailMessage(
        email_subject, email_body,
        settings.DEFAULT_FROM_EMAIL, ["tarang.a@antino.io", email],
    )
    return email.send(fail_silently=False)
