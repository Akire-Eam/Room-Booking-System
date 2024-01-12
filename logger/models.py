from django.db import models


# Create your models here.
class ActivityLog(models.Model):
    action = models.CharField(max_length=25, null=True, blank=False)
    log = models.CharField(max_length=2000, null=True, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=False)
