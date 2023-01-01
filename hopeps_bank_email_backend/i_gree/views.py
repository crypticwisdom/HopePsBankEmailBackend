import secrets
from django.shortcuts import redirect, render
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from django.conf import settings
import base64
from i_gree.models import IdpUserSessionModel
from .utils import encrypt_text, decrypt_text

# Create your views here.
# DOCUMENTATION: https://nibss.atlassian.net/wiki/external/1057980425/ZDZkMTlkMjFiMzAxNGY0MWFhN2Y3YWZhYTgyNTQwY2E

IDP_INITIATOR_URL: str = "https://idsandbox.nibss-plc.com.ng"
CHANNEL_CODE = {
    "01": "Mobile App", "02": "Customer Web Portal", "03": "Internal Web Portal", "05": "ATM", "06": "POS",
    "99": "NIBSS", "00": "Other"
}

class InitiatorView(APIView):
    permission_classes = []

    def get(self, request):
        try:
            url:str = f"{settings.IDP_INITIATOR_URL}/oxauth/authorize.htm?scope=profile&acr_values=otp&response_type=code" \
                      f"&redirect_uri={settings.MY_CALL_BACK}&client_id={settings.CLIENT_ID}"
            return Response({"detail": f"{url}"})
        except (Exception, ) as err:
            return Response({"detail": f"{err}"}, status=HTTP_400_BAD_REQUEST)


class CallBackURLHandlerView(APIView):
    permission_classes = []

    def get(self, request):
        try:
            authorization_code = request.GET.get("code", None)
            if "code" not in request.GET or not authorization_code:
                error_message: str = "Authorization code not found."
                return redirect(f"{settings.FRONTEND_REDIRECT_URL}?error_message={error_message}")

            # Converting ClientID:ClientSecret to base64. (READ) -> [https://en.wikipedia.org/wiki/Basic_access_authentication#:~:text=In%20basic%20HTTP%20authentication%2C%20a,joined%20by%20a%20single%20colon%20%3A%20.]
            to_base64 = base64.b64encode(bytes(f'{settings.CLIENT_ID}:{settings.CLIENT_SECRET}', 'utf-8'))
            # Decode the encoded base64 to string format.
            base64_to_str = to_base64.decode('utf-8')

            # Header
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"Basic {base64_to_str}"
            }

            data = {
                "grant_type": "authorization_code",
                "code": f"{authorization_code}",
                "redirect_uri": f"{settings.MY_CALL_BACK}",
                "client_id": f"{settings.CLIENT_ID}"
            }
            # Make request to exchange authorization token for an access token.
            exchange_auth_code = requests.post(url=f"{settings.GET_ACCESS_TOKEN_URL}",
                                               headers=headers, data=data)

            if exchange_auth_code.status_code == 200:
                unique_id = secrets.token_urlsafe(10)
                access_token = exchange_auth_code.json()['access_token']
                headers1 = {
                    "Authorization": f"Bearer {access_token}",
                    "x-consumer-unique-id": f"02{unique_id}",
                    "x-consumer-custom-id": f"{settings.CLIENT_ID}"
                }
                # Make request to get the resource owner's (User) details.
                get_bvn_details = requests.post(url=f"{settings.GET_BVN_DETAIL_URL}", headers=headers1, data={})

                if get_bvn_details.status_code != 200:
                    error_message: str = f"An error occurred while trying to fetch the resource owner's details. " \
                                         f"It returned status_code '{get_bvn_details.status_code}' " \
                                         f"and message - '{get_bvn_details.text}'."
                    return redirect(f"{settings.FRONTEND_REDIRECT_URL}?error_message={error_message}")

                response = get_bvn_details.json()[0]

                # Save user's detail
                # session = IdpUserSessionModel.objects.create(
                #     unique_id=unique_id, first_name=response['first_name'], surname=response['surname'],
                #     middle_name=response['middle_name'], enroll_user_name=response['enroll_user_name'],
                #     authorization_code=encrypt_text(authorization_code), access_token=encrypt_text(access_token),
                #     status="completed"
                # )
                msg: str = ""
                y = "sa"
                for key, value in response:
                    msg += f"{key}={value}&"
                    y="reee"
                # Remove the last '&' at the end of the message
                msg = msg[:len(msg) - 1]
                return redirect(f"{settings.FRONTEND_REDIRECT_URL}?{msg}")

            error_message: str = f"An error occurred while exchanging an Authorization Code for an Access Token. Response " \
                          f"returned a status_code - {exchange_auth_code.status_code} with message - {exchange_auth_code.text}"
            return redirect(f"{settings.FRONTEND_REDIRECT_URL}?error_message={error_message}")

        except (Exception, ) as err:
            return redirect(f"{settings.FRONTEND_REDIRECT_URL}?error_message={err}&msg={msg}&response={response['first_name']}&y={y}")
