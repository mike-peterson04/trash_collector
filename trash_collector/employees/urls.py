from django.urls import path

from . import views

# TODO: Determine what distinct pages are required for the customer user stories, add a path for each in urlpatterns

app_name = "employees"
urlpatterns = [
    path('', views.index, name="index"),
    path('todays_route', views.todays_route, name="todays_route"),
    path('future_route', views.future_route, name="future_route"),
    path('customers_in_area', views.customers_in_area, name="customers_in_area"),
]