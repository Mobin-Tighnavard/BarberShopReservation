from django.urls import path , include
from .views import BarberListApiView , ServiceListApiView , TimeSlotList

urlpatterns = [
    path("v1/barbers/",BarberListApiView.as_view(),name="barber-list"),
    path("v1/service/",ServiceListApiView.as_view(),name="service-list"),
    path("v1/barbers/<int:barber_id>/all-slots/", TimeSlotList.as_view(), name="barber-slot-list"),

]