from django.urls import path, include
from . import views


app_name = "employees"
urlpatterns = [
    path('', views.index, name="index"),
    path('schedule/', views.todays_route, name="today"),
    path('planner/', views.future_route, name="scheduler"),
    path('customers_in_area/', views.customers_in_area, name="area"),
    path('customer_detail/<int:customer_id>', views.customer, name="customer"),
    path('onboarding/', views.onboard, name="onboard")
]