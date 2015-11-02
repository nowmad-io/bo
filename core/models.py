from django.db import models


# Create your models here.
class Location(models.Model):
    longitude = models.FloatField(blank=False, null=False, default=0)
    latitude = models.FloatField(blank=False, null=False, default=0)
