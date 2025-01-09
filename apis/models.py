from django.db import models


class Bin(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    color = models.CharField(max_length=50, null=True, blank=True)
    serial_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    current_level = models.IntegerField(default=0)
    current_weight = models.IntegerField(default=0)
    bin_height = models.IntegerField(default=0)
    pickups = models.ManyToManyField('Pickup', null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Pickup(models.Model):
    date = models.DateTimeField(auto_now=True)
    amount = models.IntegerField(default=0)
    cleared = models.BooleanField(default=False)

    def __str__(self):
        return f'id: {self.id}, amount: {self.amount}'

    class Meta:
        ordering = ['-date']
