from django.urls import path

from . import views

# TODO: Determine what distinct pages are required for the customer user stories, add a path for each in urlpatterns

app_name = "customers"
urlpatterns = [
    path('', views.index, name="index"),
    path('pickup_day/', views.pickup_day, name="pickup_day"),
    path('suspend/', views.suspend, name="suspend"),
    path('account_info/', views.account_info, name="account_info"),
    path('onboard/', views.onboard, name="onboard")
]
