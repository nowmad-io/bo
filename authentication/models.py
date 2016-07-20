from django.utils.translation import ugettext_lazy as _
from django.db import models
from core.models import Location
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class travelUserManager(BaseUserManager):

    def create_user(self, email, first_name='', last_name='', location=None, date_of_birth=None, password=None):

        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
            first_name=first_name,
            last_name=last_name,
            location=location
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
            password=password,
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
    date_of_birth = models.DateField(blank=True, null=True)
    first_name = models.CharField(blank=True, max_length=30)
    last_name = models.CharField(blank=True,  max_length=30)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    location = models.ForeignKey(Location, blank=True, null=True)
    objects = travelUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

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
