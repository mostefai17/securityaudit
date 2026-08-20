from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.shortcuts import get_object_or_404


# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)

class AuditReport(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='audit_reports')
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    score = models.FloatField()

