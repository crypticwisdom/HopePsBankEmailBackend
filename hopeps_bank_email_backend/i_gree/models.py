from django.db import models

# Create your models here.

IDP_FLOW_STATUS = (
    ("completed", "Completed"),
    ("failed", "Failed"),
    ("pending", "Pending"),
)

class IdpUserSessionModel(models.Model):
    unique_id = models.CharField(max_length=20, null=True, blank=True)
    first_name = models.CharField(max_length=20, null=True, blank=True)
    surname = models.CharField(max_length=20, null=True, blank=True)
    middle_name = models.CharField(max_length=20, null=True, blank=True)
    enroll_user_name = models.CharField(max_length=20, null=True, blank=True)
    channel_code = models.CharField(max_length=3, null=True, blank=True, default="02")
    authorization_code = models.CharField(max_length=300, null=True, blank=True)
    access_token = models.CharField(max_length=300, null=True, blank=True)
    status = models.CharField(max_length=20, choices=IDP_FLOW_STATUS, default="pending")
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.first_name} {self.surname} - {self.status}"