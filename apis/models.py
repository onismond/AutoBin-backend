import uuid
from django.db import models
from users.models import User


class Bin(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    owner = models.ForeignKey(User, related_name='bin', on_delete=models.CASCADE, null=True, blank=True)
    color = models.CharField(max_length=50, null=True, blank=True)
    serial_number = models.CharField(max_length=50, null=True, blank=True)
    current_level = models.IntegerField(default=100)
    current_weight = models.IntegerField(default=0)
    bin_height = models.IntegerField(default=100)
    pickups = models.ManyToManyField('Pickup', related_name='bin', blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


    class Meta:
        ordering = ['-id']


class Pickup(models.Model):
    amount = models.FloatField(default=0.0)
    cleared = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'id: {self.id}, amount: {self.amount}'

    class Meta:
        ordering = ['-date']


class Transaction(models.Model):
    serial_number = models.UUIDField(default=uuid.uuid4, editable=False)
    amount = models.FloatField(default=0.0)
    cleared = models.BooleanField(default=False)
    contact = models.CharField(max_length=15, null=True, blank=True)
    pickups = models.ManyToManyField(Pickup, related_name='transaction', blank=True)
    date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, related_name='transactions', on_delete=models.CASCADE, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'id: {self.id}, amount: {self.amount}'

    class Meta:
        ordering = ['-date']