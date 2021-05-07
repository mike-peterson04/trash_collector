from django.urls import path, include
from . import views


app_name = "employees"
urlpatterns = [
    path('', views.index, name="index"),
    path('todays_route/', views.todays_route, name="todays_route"),
    path('future_route/', views.future_route, name="future_route"),
    path('customers_in_area/', views.customers_in_area, name="customers_in_area"),
    path('onboarding/', views.onboard, name="onboard")
]