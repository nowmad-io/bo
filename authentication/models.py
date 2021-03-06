from django.conf import settings
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
import urllib.request

from nowmad.storage_backends import PublicMediaStorage

class travelUserManager(BaseUserManager):
    def create_user(self, email, first_name='', last_name='', picture=None, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            picture=picture
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, first_name, last_name, picture=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            first_name=first_name,
            last_name=last_name,
            picture=picture,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class travelUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(blank=True, max_length=30)
    last_name = models.CharField(blank=True,  max_length=30)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    public_default = models.BooleanField(default=False)
    picture = models.URLField(blank=True, null=True)
    objects = travelUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_first_name(self):
        # The user is identified by their email address
        return self.first_name

    def get_last_name(self):
        # The user is identified by their email address
        return self.last_name

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def get_sid(self):
        # The user is identified by their email address
        return self.sid

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_perms(self, perm_list, obj=None):
        "Does the user have all permissions?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def get_friends(self):
        return self.friends.all()

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
