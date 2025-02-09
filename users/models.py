from django.utils import timezone
from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils.html import mark_safe

ROLES = (
    ("user", "User"),
    ("collector", "Collector"),
)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser, PermissionsMixin):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, unique=True)
    contact = models.CharField(max_length=15, unique=True)
    username = models.CharField(max_length=25, null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    address_updated_at = models.DateTimeField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatar', null=True, blank=True)
    phone_verification_code = models.CharField(max_length=15, null=True, blank=True)
    password_change_verification_code = models.CharField(max_length=15, null=True, blank=True)
    role = models.CharField(max_length=15, choices=ROLES, default=ROLES[0][0])
    # transactions = models.ManyToManyField(Transaction, related_name='user', blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'password', 'contact']

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def set_collector_location(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        self.address_updated_at = timezone.now()
        self.save()

