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
    lat = 3.3
    long = 3.3
    for x in result:
        a = get_coord(x)
        lat = a['lat']
        long = a['lng']
    context['lat'] = lat
    context['long'] = long
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
        suspension_check(date.date(), False)
        day = date.strftime("%A")
        Customer = apps.get_model('customers.Customer')
        result = Customer.objects.filter(Q(zipcode=context["employee"].area), Q(suspension=False),
                                         Q(pickup_day=day) | Q(one_time_pickup=date))
        suspension_check()
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
    if request.method == 'POST':
        for customer in result:
            if request.POST.get(f"{customer.id}") == 'on':
                pickup_complete(customer)
        return HttpResponseRedirect(reverse('employees:area'))
    context['customers'] = result
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


def suspension_check(date=None, today=True):
    Customer = apps.get_model('customers.Customer')
    dataset = Customer.objects.all()
    if date is None:
        date = datetime.date.today()
    for customer in dataset:
        if customer.suspension:
            if today:
                if customer.suspension_end <= date:
                    customer.suspension = False
                    customer.suspension_start = None
                    customer.suspension_end = None
                    customer.save()
            else:
                customer.suspension = False
                customer.save()
        else:
            if customer.suspension_start is None:
                pass
            else:
                if customer.suspension_start <= date <= customer.suspension_end:
                    customer.suspension = True
                    customer.save()


def customer(request, customer_id):
    user = request.user
    suspension_check()
    context = context_gen(user)
    Customer = apps.get_model('customers.Customer')
    customer = Customer.objects.get(pk=customer_id)
    context['customer'] = customer
    get_coord(context['customer'])
    context['lat'] = customer.lat
    context['long'] = customer.lng
    context['key'] = api.google_maps_api_key
    return render(request, 'employees/customer.html', context)


def get_coord(customer):
    if customer.lat is None or customer.lng is None:
        gmaps = googlemaps.Client(key=api.google_maps_api_key)
        latlng = gmaps.geocode(customer.address)
        latlng = latlng[0]
        latlng = latlng['geometry']['location']
        customer.lat = latlng['lat']
        customer.lng = latlng['lng']
        customer.save()
        return latlng
    else:
        latlng = {
            'lat':customer.lat,
            'lng':customer.lng
        }
        return latlng


