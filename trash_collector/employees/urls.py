from django.urls import path, include
from . import views

# TODO: Determine what distinct pages are required for the customer user stories, add a path for each in urlpatterns

app_name = "employees"
urlpatterns = [
    path('', views.index, name="index"),
    path('user/', include('customers.urls')),
    path('employee/', include('employees.url'))
]