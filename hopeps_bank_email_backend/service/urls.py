from django.urls import path
from .views import SendEmailView

app_name = "service"

urlpatterns = [
    path('send-mail/', SendEmailView.as_view(), name="send-mail"),

]
