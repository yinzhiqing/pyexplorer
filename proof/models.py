from django.db import models

# Create your models here.

class BtcRpc(models.Model):
    ip = models.GenericIPAddressField(default='127.0.0.1')
    port = models.PositiveIntegerField(default=9409)
    user = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
