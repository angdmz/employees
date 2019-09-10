from django.db import models

# Create your models here.
from business.models import Office


class OfficeLoad(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class OfficeLoaded(models.Model):
    office = models.ForeignKey(Office, on_delete=models.CASCADE, null=True, default=None, blank=True)
    load = models.ForeignKey(OfficeLoad, on_delete=models.CASCADE, null=True, default=None, blank=True)
