from django.shortcuts import render
from .utils import send_mail
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.conf import settings
import requests
from decouple import config


class SendEmailView(APIView):
    permission_classes = []

    def post(self, request):
        try:
            name, phone_number = request.data.get("name", None), request.data.get("phone_number", None)
            account_no, email_from = request.data.get("account_no", None), request.data.get("email_from", None)

            if not all([name, phone_number, account_no, email_from]):
                return Response(
                    {"detail": "Name, Email, Account Number and Phone Number of the receiver are required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            content = f"""
                <div>
                    <b>I <i>{name}</i>, would like to request for a debit card for my Hope PS Bank account.</b><br>
                    <br><br><br>
                    
                    <b>
                    Account Number: {account_no}<br>
                    Phone Number: {phone_number}<br>
                    Email: {email_from}
                    </b>
                </div>
            """
            print("got here ....")
            success, msg = send_mail(api_key=settings.API_KEY, content=content)
            print("came out clean ....")
            if success:
                return Response({"detail": f"Email Sent"})
            else:
                return Response({"detail": f"Email Sent"}, status=status.HTTP_400_BAD_REQUEST)

        except (Exception,) as err:
            return Response({"detail": f"{err}"})
