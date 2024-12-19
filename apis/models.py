from django.db import models


class Bin(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    serial_number = models.CharField(max_length=50, null=True, blank=True)
    current_level = models.IntegerField(default=0)
    current_weight = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Pickup(models.Model):
    bin = models.ForeignKey(Bin, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.bin.name
