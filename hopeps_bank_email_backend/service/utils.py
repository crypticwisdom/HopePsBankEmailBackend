import requests

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings


def send_mail(api_key, content):
    try:

        message = Mail(
            from_email=f'{settings.EMAIL_FROM}',
            to_emails=f'{settings.EMAIL_TO}',
            subject='Debit card request',
            html_content=f'{content}'
        )

        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        # print(response.status_code)
        # print(response.body)
        # print(response.headers)
    except (Exception, ) as e:
        print(e)
        return False, f"{e}"
    else:
        return True, "Success"
