from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

class Category(models.Model):
    name = models.CharField(max_length=200)
    icon = models.URLField(max_length=200, blank=True, null=True)

class Location(models.Model):
    longitude = models.FloatField(blank=False, null=False, default=0)
    latitude = models.FloatField(blank=False, null=False, default=0)

    def __unicode__(self):
        return u"%i - %i" % (self.longitude, self.latitude)

class Review(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500, blank=True)
    location = models.ForeignKey('Location')
    categories = models.ManyToManyField('Category')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='first_reviewer')
    creation_date = models.DateField(auto_now_add=True)

    objects = models.Manager()

    def __unicode__(self):
            return self.title
