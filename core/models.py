from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class Location(models.Model):
    longitude = models.FloatField(blank=False, null=False, default=0)
    latitude = models.FloatField(blank=False, null=False, default=0)
    def __unicode__(self):
        return u"%i - %i" % (self.longitude, self.latitude)

class Category(models.Model):
    class Meta:
        ordering = ['name']
        verbose_name = _('user')

    name = models.CharField(max_length=30)


class Review(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    location = models.ForeignKey('Location')
    privacy = models.IntegerField()
    category = models.ManyToManyField(Category, blank=True)

    #the who fields
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='first_reviewer')
    creation_date = models.DateField(auto_now_add=True)

    def __unicode__(self):
            return self.title
