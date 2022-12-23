from django.urls import path
from . import views

app_name = "I-Gree"

urlpatterns = [
    path('', views.InitiatorView.as_view(), name="index"),
    path('verify', views.CallBackURLView.as_view(), name="call-back-url"),
]
