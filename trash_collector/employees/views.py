from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Employee
from django.apps import apps
from django.db.models import Q
import datetime

# Create your views here.


def index(request):
    # Get the Customer model from the other app, it can now be used to query the db
    Customer = apps.get_model('customers.Customer')
    user = request.user
    context = context_gen(user)
    return render(request, 'employees/index.html', context)


def todays_route(request):
    user = request.user
    context = context_gen(user)
    day = datetime.datetime.now()
    day = day.strftime("%A")
    date = datetime.date.today()
    Customer = apps.get_model('customers.Customer')
    result = Customer.objects.filter(Q(pickup_day=day)|Q(one_time_pickup=date))
    context['customers'] = result
    context['day'] = day
    return render(request, 'employees/today.html', context)


def future_route(request):
    return


def customers_in_area(request):
    return


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

def build_users():
    pass
