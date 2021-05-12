from django.urls import path
from .views import CreateCheckoutSessionView
from . import views

app_name = "customers"
urlpatterns = [
    path('', views.index, name="index"),
    path('pickup_day/', views.pickup_day, name="pickup_day"),
    path('suspend/', views.suspend, name="suspend"),
    path('account_info/', views.account_info, name="account_info"),
    path('make_payment/', views.make_payment, name='checkout'),
    path('create_checkout_session/<int:customer_id>', CreateCheckoutSessionView.as_view(), name='create_checkout_session'),
    path('success/', views.pay_success, name="success"),
    path('cancel/',views.pay_fail, name="cancel"),
    path('onboard/', views.onboard, name="onboard"),
    path('resume/', views.resume, name="resume")
]
