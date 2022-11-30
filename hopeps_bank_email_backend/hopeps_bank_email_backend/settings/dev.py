from .base import *
print("******************* Running on Development Environment *********************")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^-gcdl5u%c41=tz)$-k&if@)ofdmqnolz_5*$^x&%+8%0i-4!!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["hopepsbank.com", "www.hopepsbank.com", "hopepsbank.com", "127.0.0.1", "localhost"]


CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://localhost:8080",
    "https://www.hopepsbank.com"
]

# CORS_ALLOW_ALL_ORIGINS = True

API_KEY = config("API_KEY", None)
EMAIL_TO = config("EMAIL_TO", None)
EMAIL_FROM = config("EMAIL_FROM", None)


print(API_KEY, EMAIL_FROM, EMAIL_TO)
