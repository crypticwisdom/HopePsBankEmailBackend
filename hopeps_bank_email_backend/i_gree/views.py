import secrets

import requests
from rest_framework.views import APIView
import http.client
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.conf import settings
import base64

# Create your views here.
# DOCUMENTATION: https://nibss.atlassian.net/wiki/external/1057980425/ZDZkMTlkMjFiMzAxNGY0MWFhN2Y3YWZhYTgyNTQwY2E

URL: str = "apitest.sandbox.nibss-plc.com.ng"
IDP_INITIATOR_URL: str = "https://idsandbox.nibss-plc.com.ng"
CHANNEL_CODE = {
    "01": "Mobile App", "02": "Customer Web Portal", "03": "Internal Web Portal", "05": "ATM", "06": "POS",
    "99": "NIBSS", "00": "Other"
}


# print(settings.CLIENT_ID, settings.CLIENT_SECRET, settings.MY_CALL_BACK)
"""
    The following is the list of channel codes available:
    01 - Mobile App, 02 - Customer Web Portal, 03 - Internal Web Portal, 05 - ATM
    06 - POS, 99 - NIBSS, 00 - Other
"""

class InitiatorView(APIView):
    permission_classes = []

    def get(self, request):
        try:
            print(settings.MY_CALL_BACK)
            url:str = f"{IDP_INITIATOR_URL}/oxauth/authorize.htm?scope=contact_info&acr_values=otp&response_type=code" \
                      f"&redirect_uri={settings.MY_CALL_BACK}&client_id={settings.CLIENT_ID}"

            return Response({"data": f"{url}"})
        except (Exception, ) as err:
            return Response({"detail": f"{err}"}, status=HTTP_400_BAD_REQUEST)


class CallBackURLView(APIView):
    permission_classes = []

    def get(self, request):
        try:

            authorization_code = request.GET.get("code", None)
            if "code" not in request.GET or not authorization_code:
                return Response({"data": "Invalid Authorization code"}, status=HTTP_400_BAD_REQUEST)

            to_base64 = base64.b64encode(bytes('cab7a23d-ee0c-4bae-a9bb-8f724f9f63b3:nVszV1eVtPd5oPvDEs3dxbg3XY6WxZTqPQ7QkKdt', 'utf-8'))
            base64_to_str = to_base64.decode('utf-8')

            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"Basic {base64_to_str}"
            }

            data = {
                "grant_type": "authorization_code",
                "code": f"{authorization_code}",
                "redirect_uri": "https://hopemail.tm-dev.xyz/i-gree/verify",
                "client_id": "cab7a23d-ee0c-4bae-a9bb-8f724f9f63b3"
            }

            exchange_auth_code = requests.post(url="https://idsandbox.nibss-plc.com.ng/oxauth/restv1/token",
                                               headers=headers, data=data)

            if exchange_auth_code.status_code == 200:
                access_token = exchange_auth_code.json()['access_token']
                headers1 = {
                    "Authorization": f"Bearer {access_token}",
                    "x-consumer-unique-id": f"02{secrets.token_urlsafe(10)}",
                    "x-consumer-custom-id": "cab7a23d-ee0c-4bae-a9bb-8f724f9f63b3"
                }
                dd = requests.post(url="https://apitest.nibss-plc.com.ng/bvnconsent/v1/getPartialDetailsWithBvn", headers=headers1, data={})

                if dd.status_code != 200:
                    return Response({"details": f"An error occurred, {dd.status_code} - {dd.text}"}, status=HTTP_400_BAD_REQUEST)

                return Response({"data": f"{dd.status_code}", "details": dd.json()})
            return Response({"data": f" Authorization Code: {authorization_code} ||| BASIC encoded-{to_base64} str-{base64_to_str} |||| {request.GET} || request: {exchange_auth_code} request_code {exchange_auth_code.status_code} :: request_text {exchange_auth_code.text} {exchange_auth_code.text} text-type '{type(exchange_auth_code.text)}' || request_content: {exchange_auth_code.content} content-type'{type(exchange_auth_code.content)}' || request_json '{exchange_auth_code.json()}' -type {type(exchange_auth_code.json())} |||||||||||||||| {exchange_auth_code.json()['access_token']}"})
        except (Exception, ) as err:
            return Response({"detail": f"{err}"}, status=HTTP_400_BAD_REQUEST)
