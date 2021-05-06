from django.db import models
# Create your models here.

# TODO: Finish customer model by adding necessary properties to fulfill user stories


class Customer(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey('accounts.User', blank=True, null=True, on_delete=models.CASCADE)
    pickup_day = models.CharField(max_length=10,blank=True, null=True)
    one_time_pickup = models.DateField(blank=True, null=True)
    account_balance = models.FloatField(default=0.00)
    suspension = models.BooleanField(default=False)
    suspension_end = models.DateField(blank=True, null=True)
    zipcode = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)

