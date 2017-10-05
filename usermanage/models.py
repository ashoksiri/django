# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.core import validators
import datetime
from django.utils import timezone as timezone


class Clients (models.Model):
	id                  = models.AutoField (primary_key=True)
	organization_name   = models.CharField (max_length=50)
	address             = models.CharField (max_length=300, blank=True, null=True)
	contact_number      = models.CharField (max_length=20)
	phone_number        = models.CharField (max_length=20, blank=True, null=True)
	email               = models.EmailField()
	row_status          = models.CharField (max_length=2, default=1)
	requested_by        = models.CharField (max_length=10)
	created_time        = models.DateTimeField (default=datetime.datetime.now())
	modified_time       = models.DateTimeField (default=datetime.datetime.now() )


class UserManager(BaseUserManager):
    # use_in_migrations = True

    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = Users(username=username, email=email,is_staff=is_staff, is_active=True, is_superuser=is_superuser, created_time=datetime.datetime.now(), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False,**extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password, True, True,**extra_fields)


class Users(AbstractUser):
    pass
    id                      =   models.AutoField(primary_key=True)
    username                =   models.CharField(
                                    _('username'),
                                    max_length=150,
                                    unique=True,
                                    help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
                                    validators=[validators.RegexValidator(r'^[\w.@+-]+$',
                                                                                                          _('Enter a valid username. '
                                                                                                            'This value may contain only letters, numbers '
                                                                                                            'and @/./+/-/_ characters.'), 'invalid'),
                                                                                ],
                                    error_messages={
                                        'unique': _("A user with that username already exists."),
                                    },
                                )
    first_name              =   models.CharField(_('first name'), max_length=30, blank=True)
    last_name               =   models.CharField(_('last name'), max_length=30, blank=True)
    email                   =   models.EmailField(_('email address'), blank=True, null=True)
    age                     =   models.DateField (blank=True, null=True)
    gender                  =   models.CharField (blank=True, null=True, max_length=10)
    mobile_number           =   models.CharField (blank=True, null=True, max_length=10)
    status                  =   models.IntegerField (default=False)
    user_type               =   models.CharField(max_length=10, default='user')
    is_preferences_active   =   models.IntegerField(default=False)
    row_status              =   models.BooleanField(default=True)
    requested_by            =   models.CharField(blank=True, null=True, max_length=10)
    is_staff                =   models.BooleanField(
                                    _('staff status'),
                                    default=False,
                                    help_text=_('Designates whether the user can log into this admin site.'),
                                )
    is_active               =   models.BooleanField(
                                    _('active'),
                                    default=True,
                                    help_text=_(
                                        'Designates whether this user should be treated as active. '
                                        'Unselect this instead of deleting accounts.'
                                    ),
                                )
    created_time            =   models.DateTimeField (_ ('date created'), default=timezone.now)
    modified_time           =   models.DateTimeField (_ ('date updated'), default=timezone.now)
    clients                 =   models.ForeignKey(Clients)

    objects                 = UserManager()

    EMAIL_FIELD             = 'email'
    USERNAME_FIELD          = 'username'
    REQUIRED_FIELDS         = ['email']

    #
    # class Meta:
    #     verbose_name = _('user')
    #     verbose_name_plural = _('users')
    #     abstract = True
    #
    # def get_full_name(self):
    #     """
    #     Returns the first_name plus the last_name, with a space in between.
    #     """
    #     full_name = '%s %s' % (self.first_name, self.last_name)
    #     return full_name.strip()
    #
    # def get_short_name(self):
    #     "Returns the short name for the user."
    #     return self.first_name


class Countries (models.Model):
    id              = models.AutoField (primary_key=True)
    country_name    = models.CharField (max_length=20, unique=True)
    created_time    = models.DateTimeField (default=datetime.datetime.now ())
    modified_time   = models.DateTimeField (default=datetime.datetime.now ())


class States (models.Model):
	id              = models.AutoField (primary_key=True)
	state_name      = models.CharField (max_length=20, unique=True)
	created_time    = models.DateTimeField (default=timezone.now)
	modified_time   = models.DateTimeField (default=timezone.now)
	countries       = models.ForeignKey (Countries)


class Cities (models.Model):
	id              = models.AutoField (primary_key=True, unique=True)
	city_name       = models.CharField (max_length=20)
	created_time    = models.DateTimeField (default=timezone.now)
	modified_time   = models.DateTimeField (default=timezone.now)
	states          = models.ForeignKey (States)

class Keywords(models.Model):
    id              = models.AutoField (primary_key=True)
    keyword         = models.CharField (max_length=50)
    created_time    = models.DateTimeField (default=timezone.now)
    modified_time   = models.DateTimeField (default=timezone.now)
    status          = models.IntegerField(default=True)
    source_type     = models.CharField(max_length=15, blank=True, null=True)
    clients         = models.ForeignKey (Clients, default=1)

class Preferences (models.Model):
    id              = models.AutoField (primary_key=True)
    start_date      = models.DateField()
    end_date        = models.DateField()
    created_time    = models.DateTimeField (default=timezone.now)
    modified_time   = models.DateTimeField (default=timezone.now)
    requested_by    = models.CharField (max_length=10, null = True, blank = True)
    row_status	    = models.CharField(max_length=10, null=True)
    keywords        = models.ForeignKey (Keywords)
    users           = models.ForeignKey (Users)

class Channel_page_sources (models.Model):
    id              = models.AutoField (primary_key=True)
    source_type     = models.CharField (max_length=50)
    channel_page    = models.CharField (max_length=100)
    created_time    = models.DateTimeField (default=timezone.now)
    modified_time   = models.DateTimeField (default=timezone.now)
    row_status      = models.CharField (max_length=10, blank=True, null=True)
    requested_by    = models.CharField (max_length=10, blank=True, null=True)
    clients         = models.ForeignKey (Clients)
    status = models.IntegerField(default=True)