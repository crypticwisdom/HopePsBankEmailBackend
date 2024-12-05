from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('service/', include('service.urls')),
    path('i-gree/', include('i_gree.urls')),
]
