from django.urls import path,include
from .views import CreateCustomerApiView
urlpatterns =[
    path("create-customer/",CreateCustomerApiView.as_view() , name = "create_customer")
]