from django.urls import path,include
from .views import CreateCustomerApiView,AdminLogoutApiView
urlpatterns =[
    path("v1/create-customer/",CreateCustomerApiView.as_view() , name = "create_customer"),
    path("admin/logout/",AdminLogoutApiView.as_view() , name = "admin-logout"),
]