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

            to_base64 = base64.b64encode(bytes('cab7a23d-ee0c-4bae-a9bb-8f724f9f63b3:zV1eVtPd5oPvDnVsEs3dxbg3XY6WxZTqPQ7QkKdt', 'utf-8'))
            base64_to_str = to_base64.decode('utf-8')

            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"Basic {base64_to_str}"
            }
            data = {
                "client_id": "cab7a23d-ee0c-4bae-a9bb-8f724f9f63b3",
                "code": f"{authorization_code}",
                "redirect_uri": "https://hopemail.tm-dev.xyz/i-gree/verify",
                "grant_type": "authorization_code",
            }

            exchange_auth_code = requests.post(url="https://idsandbox.nibss-plc.com.ng/oxauth/restv1/token",
                                               headers=headers, data=data)


            # print(authorization_code, request.GET)

            return Response({"data": f"{request.GET} || request: {exchange_auth_code} request_code {exchange_auth_code.status_code} :: request_text {exchange_auth_code.text}"})
        except (Exception, ) as err:
            return Response({"detail": f"{err}"}, status=HTTP_400_BAD_REQUEST)
