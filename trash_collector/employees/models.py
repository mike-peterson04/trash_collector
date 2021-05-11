from django.db import models

# Create your models here.


class Employee(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey('accounts.User', blank=True, null=True, on_delete=models.CASCADE)
    area = models.CharField(max_length=15, blank=True, null=True)
    lat = models.FloatField(default=None, blank=True, null=True)
    lng = models.FloatField(default=None, blank=True, null=True)

