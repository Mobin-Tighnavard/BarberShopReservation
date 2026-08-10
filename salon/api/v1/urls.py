from django.urls import path
from .views.public import BarberListApiView , BarberServiceListApiView , TimeSlotList
from .views.admin import (AdminCreateBarberApiView,AdminDeleteBarberApiView,
                          AdminBarberListApiView,AdminUpdateBarberApiview,)

urlpatterns = [
    path("v1/barbers/",BarberListApiView.as_view(),name="barber-list"),

    path("v1/admin/barbers/create/", AdminCreateBarberApiView.as_view(), name="barber-create"),
    path("v1/admin/barbers/list/", AdminBarberListApiView.as_view(), name="barber-list"),
    path("v1/admin/barbers/update/<int:pk>", AdminUpdateBarberApiview.as_view(), name="barber-update"),
    path("v1/admin/barbers/delete/<int:pk>/", AdminDeleteBarberApiView.as_view(), name="barber-delete"),


    path("v1/barbers/<int:barber_id>/service/",BarberServiceListApiView.as_view(),name="service-list"),
    path("v1/barbers/<int:barber_id>/all-slots/", TimeSlotList.as_view(), name="barber-slot-list"),

]