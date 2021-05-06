from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Customer
# Create your views here.

# TODO: Create a function for each path created in customers/urls.py. Each will need a template as well.


def index(request):
    # The following line will get the logged-in in user (if there is one) within any view function
    user = request.user
    # It will be necessary while creating a customer/employee to assign the logged-in user as the user foreign key
    # This will allow you to later query the database using the logged-in user,
    # thereby finding the customer/employee profile that matches with the logged-in user.
    print(user)
    try:
        customer = Customer.objects.get(user=user.id)
        customer = {
            "customer": True
        }
    except:
        customer = {
            "customer": False
        }
    return render(request, 'customers/index.html', customer)


def pickup_day(request):
    user = request.user
    return render(request, 'customers/pickup_day.html')


def suspend(request):
    user = request.user
    return render(request, 'customers/suspend.html')


def account_info(request):
    user = request.user
    return render(request, 'customers/account_info.html')


def onboard(request):
    user = request.user
    if request.method == 'POST':
        user_id = user.id
        day = request.POST.get('day')
        name = request.POST.get('name')
        address = request.POST.get('address')
        zip = request.POST.get('zip')
        new_customer = Customer(name=name, user=user, pickup_day=day,address=address,zipcode=zip)
        new_customer.save()
        return HttpResponseRedirect(reverse('customers:index'))
    else:
        return render(request, 'customers/onboard.html')
