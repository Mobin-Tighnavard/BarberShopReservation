from django.urls import path,include
from .views import CreateCustomerApiView
urlpatterns =[
    path("v1/create-customer/",CreateCustomerApiView.as_view() , name = "create_customer")
]