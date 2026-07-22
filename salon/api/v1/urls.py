from django.urls import path , include
from .views import BarberListApiView , ServiceListApiView

urlpatterns = [
    path("v1/barbers/",BarberListApiView.as_view(),name="barber-list"),
    path("v1/service/",ServiceListApiView.as_view(),name="service-list"),
]