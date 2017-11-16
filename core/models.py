from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

class Status(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

class Place(models.Model):
    name = models.CharField(max_length=200, blank=True)
    address = models.CharField(max_length=400, blank=True)
    longitude = models.FloatField(blank=False, null=False, default=0)
    latitude = models.FloatField(blank=False, null=False, default=0)

    def __unicode__(self):
        return u"%s - %i - %i" % (self.name, self.longitude, self.latitude)

class Review(models.Model):
    short_description = models.CharField(max_length=200)
    information = models.CharField(max_length=500, blank=True)
    place = models.ForeignKey('Place', related_name='reviews')
    status = models.CharField(max_length=200)
    categories = models.ManyToManyField('Category')
    pictures = models.ManyToManyField('Picture', blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_reviews')
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-creation_date',)

    def __unicode__(self):
        return self.short_description

class Picture(models.Model):
    source = models.ImageField(max_length=200, upload_to='places')
    caption = models.CharField(max_length=300, blank=True)

class InterestedPeople(models.Model):
    email = models.CharField(max_length=200, blank=True)

    def __unicode__(self):
        return self.email
