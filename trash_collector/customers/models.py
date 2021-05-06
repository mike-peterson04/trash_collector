from django.db import models
# Create your models here.

# TODO: Finish customer model by adding necessary properties to fulfill user stories


class Customer(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey('accounts.User', blank=True, null=True, on_delete=models.CASCADE)
    pickup_day = models.CharField(max_length=10)
    one_time_pickup = models.DateField()
    account_balance = models.FloatField()
    suspension_start_stop = models.BooleanField()
    zipcode = models.CharField(max_length=15)
    address = models.CharField(max_length=50)

