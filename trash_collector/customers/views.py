from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Customer
import datetime

# Create your views here.

# TODO: Create a function for each path created in customers/urls.py. Each will need a template as well.


def index(request):
    # The following line will get the logged-in in user (if there is one) within any view function
    user = request.user
    # It will be necessary while creating a customer/employee to assign the logged-in user as the user foreign key
    # This will allow you to later query the database using the logged-in user,
    # thereby finding the customer/employee profile that matches with the logged-in user.
    print(user)
    context = context_gen(user)

    return render(request, 'customers/index.html', context)


def pickup_day(request):
    user = request.user
    context = context_gen(user)
    if request.method == 'POST':
        context['customer'].one_time_pickup = request.POST.get('date')
        context['customer'].save()
        return HttpResponseRedirect(reverse('customers:pickup_day'))
    return render(request, 'customers/pickup_day.html', context)


def suspend(request):
    user = request.user
    context = context_gen(user)
    if context['customer'].suspension:
        return render(request, 'customers/resume.html', context)
    if request.method == 'POST':
        context['customer'].suspension_start = request.POST.get('start_date')
        context['customer'].suspension_end = request.POST.get('end_date')
        context['customer'].suspension = True
        date_check = context['customer'].suspension_start.split('-')
        count = 0
        for x in date_check:
            date_check[count] = int(x)
            count += 1
        if datetime.datetime(date_check[0], date_check[1], date_check[2]) > datetime.datetime.now():
            context['customer'].suspension = False
        else:
            context['customer'].suspension = True
        context['customer'].save()
        return HttpResponseRedirect(reverse('customers:resume'))
    return render(request, 'customers/suspend.html', context)


def resume(request):
    user = request.user
    context = context_gen(user)
    if request.method == 'POST':
        context['customer'].suspension_start = None
        context['customer'].suspension_end = None
        context['customer'].suspension = False
        context['customer'].save()
        return HttpResponseRedirect(reverse('customers:suspend'))
    return render(request, 'customers/resume.html', context)


def account_info(request):
    user = request.user
    context = context_gen(user)
    if request.method == 'POST':
        context['customer'].pickup_day = request.POST.get('day')
        context['customer'].name = request.POST.get('name')
        context['customer'].address = request.POST.get('address')
        context['customer'].zipcode = request.POST.get('zip')
        context['customer'].save()
        return HttpResponseRedirect(reverse('customers:index'))
    return render(request, 'customers/account_info.html', context)


def onboard(request):
    user = request.user
    if request.method == 'POST':
        user_id = user.id
        day = request.POST.get('day')
        name = request.POST.get('name')
        address = request.POST.get('address')
        zip = request.POST.get('zip')
        new_customer = Customer(name=name, user=user, pickup_day=day, address=address, zipcode=zip)
        new_customer.save()
        return HttpResponseRedirect(reverse('customers:index'))
    else:
        return render(request, 'customers/onboard.html')


def context_gen(user):
    try:
        customer = Customer.objects.get(user=user.id)
        context = {
            "customer_exists": True,
            "customer": customer
        }
    except:
        context = {
            "customer_exists": False,
            "customer": Customer(name='null', user=user, pickup_day="null", address='address', zipcode='zip')
        }
    return context