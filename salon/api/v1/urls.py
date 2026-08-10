from django.urls import path
from .views.public import BarberListApiView , BarberServiceListApiView , TimeSlotList
from .views.admin import AdminCreateBarberApiView , AdminDeleteBarberApiView

urlpatterns = [
    path("v1/barbers/",BarberListApiView.as_view(),name="barber-list"),
    path("v1/barbers/create/", AdminCreateBarberApiView.as_view(), name="barber-create"),
    # path("v1/barbers/delete/<int:pk>/", AdminDeleteBarberApiView.as_view(), name="barber-delete"),#have think about type of delete


    path("v1/barbers/<int:barber_id>/service/",BarberServiceListApiView.as_view(),name="service-list"),
    path("v1/barbers/<int:barber_id>/all-slots/", TimeSlotList.as_view(), name="barber-slot-list"),

]