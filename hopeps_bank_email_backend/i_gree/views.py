from rest_framework.views import APIView
import http.client
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.conf import settings

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
            print(request.GET)
            # authorization_code = request.GET.get("code", None)
            # if "code" not in request.GET or not authorization_code:
            #     return Response({"data": "Invalid Authorization code"}, status=HTTP_400_BAD_REQUEST)
            #
            # print(authorization_code, request.GET)
            return Response({"data": f""})
        except (Exception, ) as err:
            return Response({"detail": f"{err}"}, status=HTTP_400_BAD_REQUEST)

