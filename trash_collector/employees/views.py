from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Employee
from django.apps import apps
from django.db.models import Q
import googlemaps
import api
import datetime

# Create your views here.


def index(request):
    # Get the Customer model from the other app, it can now be used to query the db
    Customer = apps.get_model('customers.Customer')
    user = request.user
    context = context_gen(user)
    return render(request, 'employees/index.html', context)


def todays_route(request):
    suspension_check()
    user = request.user
    day = datetime.datetime.now()
    context = context_gen(user)
    day = day.strftime("%A")
    date = datetime.date.today()
    Customer = apps.get_model('customers.Customer')
    result = Customer.objects.filter(Q(zipcode=context["employee"].area),Q(suspension=False),
                                     Q(pickup_day=day)|Q(one_time_pickup=date))
    if request.method=='POST':
        for customer in result:
            test = request.POST.getlist(str(customer.id))
            if request.POST.get(f"{customer.id}") == 'on':
                pickup_complete(customer)
        context = context_gen(user)
        return HttpResponseRedirect(reverse('employees:today'))

    context['customers'] = result
    context['day'] = day
    context['key'] = api.google_maps_api_key
    return render(request, 'employees/today.html', context)

def pickup_complete(customer):
    customer.account_balance += 10.95
    customer.one_time_pickup = None
    customer.suspension = True
    customer.suspension_start = datetime.date.today()
    customer.suspension_end = datetime.date.today() + datetime.timedelta(days=1)
    customer.save()


def future_route(request):
    suspension_check()
    user = request.user
    context = context_gen(user)
    if request.method == 'POST':
        date = request.POST.get('date')
        date_check = date.split('-')
        count = 0
        for x in date_check:
            date_check[count] = int(x)
            count += 1
        date = datetime.datetime(date_check[0], date_check[1], date_check[2])
        day = date.strftime("%A")
        Customer = apps.get_model('customers.Customer')
        result = Customer.objects.filter(Q(zipcode=context["employee"].area), Q(suspension=False),
                                         Q(pickup_day=day) | Q(one_time_pickup=date))
        context['customers'] = result
        context['day'] = day
        return render(request, 'employees/scheduler.html', context)
    else:
        context['customer'] = None
        return render(request, 'employees/scheduler.html', context)


def customers_in_area(request):

    user = request.user
    context = context_gen(user)
    Customer = apps.get_model('customers.Customer')
    result = Customer.objects.filter(zipcode=context["employee"].area)
    local = []
    count = 0
    for customer in result:
        geo = get_coord(customer.address)
        local.append(geo[count]['geometry']['location'])
        count += 1
    context['coord']=local

    return render(request, 'employees/area.html', context)


def onboard(request):
    user = request.user
    context = context_gen(user)
    if request.method == 'POST':
        name = request.POST.get('name')
        zip = request.POST.get('zip')
        new_employee = Employee(name=name, user=user, area=zip)
        new_employee.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        return render(request, 'employees/onboard.html', context)


def context_gen(user):
    try:
        employee = Employee.objects.get(user=user.id)
        context = {
            "employee_exists": True,
            "employee": employee
        }
    except:
        context = {
            "employee_exists": False,
            "employee": Employee(name='null', user=user, area='zip')
        }
    return context

def suspension_check():
    Customer = apps.get_model('customers.Customer')
    date = datetime.date.today()
    dataset = Customer.objects.all()
    for customer in dataset:
        if customer.suspension == True:
            if customer.suspension_end <= date:
                customer.suspension = False
                customer.suspension_start = None
                customer.suspension_end = None
                customer.save()
        else:
            if customer.suspension_start == None:
                pass
            else:
                if customer.suspension_start >= date >= customer.suspension_end:
                    customer.suspension = True
                    customer.save()

def get_coord(address):
    gmaps = googlemaps.Client(key=api.google_maps_api_key)
    return gmaps.geocode(address)

