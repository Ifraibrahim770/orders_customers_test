from django.urls import path

from store import views
from store.views import AddCustomer, AddOrder

urlpatterns = [

    path('', views.sign_in, name="sign_in"),
    path('make_order/', AddOrder.as_view(), name='MakeOrder'),
    path('add_customer/', AddCustomer.as_view(),name='AddCustomer'),

]
