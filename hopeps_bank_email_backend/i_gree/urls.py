from django.urls import path
from . import views

app_name = "I-Gree"

urlpatterns = [
    path('', views.InitiatorView.as_view(), name="i-gree"),
    path('verify', views.CallBackURLHandlerView.as_view(), name="call-back-url"),
]
