from django.db import models
# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    user = models.ForeignKey('accounts.User', blank=True, null=True, on_delete=models.CASCADE)
    pickup_day = models.CharField(max_length=10, blank=True, null=True)
    one_time_pickup = models.DateField(blank=True, null=True)
    account_balance = models.FloatField(default=0.00)
    suspension = models.BooleanField(default=False)
    suspension_start = models.DateField(blank=True, null=True)
    suspension_end = models.DateField(blank=True, null=True)
    zipcode = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    lat = models.FloatField(default=None, blank=True, null=True)
    lng = models.FloatField(default=None, blank=True, null=True)

