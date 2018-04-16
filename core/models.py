from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
import shortuuid

from nowmad.storage_backends import PublicMediaStorage

def default_id():
  return shortuuid.uuid()

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

class Status(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

class Place(models.Model):
    id = models.CharField(primary_key=True, max_length=200, default=default_id)
    place_id = models.CharField(max_length=200, blank=True)
    name = models.CharField(max_length=200, blank=True)
    address = models.CharField(max_length=400, blank=True)
    longitude = models.FloatField(blank=False, null=False, default=0)
    latitude = models.FloatField(blank=False, null=False, default=0)

    def __unicode__(self):
        return u"%s - %i - %i" % (self.name, self.longitude, self.latitude)

    def get_readonly_fields(self, request, obj=None):
        if obj: # obj is not None, so this is an edit
            return ['id',] # Return a list or tuple of readonly fields' names
        else: # This is an addition
            return []

class Review(models.Model):
    id = models.CharField(primary_key=True, max_length=200, default=default_id)
    short_description = models.CharField(max_length=200)
    information = models.CharField(max_length=500, blank=True)
    place = models.ForeignKey('Place', related_name='reviews', on_delete=models.CASCADE)
    status = models.CharField(max_length=200)
    categories = models.ManyToManyField('Category')
    pictures = models.ManyToManyField('Picture', blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_reviews', on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    public = models.BooleanField(default=False)
    link_1 = models.URLField(blank=True)
    link_2 = models.URLField(blank=True)

    class Meta:
        ordering = ('-creation_date',)

    def __unicode__(self):
        return self.short_description

    def get_readonly_fields(self, request, obj=None):
        if obj: # obj is not None, so this is an edit
            return ['id',] # Return a list or tuple of readonly fields' names
        else: # This is an addition
            return []

class Picture(models.Model):
    source = models.ImageField(max_length=200, upload_to='places', storage=PublicMediaStorage())
    caption = models.CharField(max_length=300, blank=True)

class InterestedPeople(models.Model):
    email = models.CharField(max_length=200, blank=True)

    def __unicode__(self):
        return self.email
