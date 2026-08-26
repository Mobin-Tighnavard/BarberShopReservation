from django.urls import path
from .views.public import BarberListApiView , BarberServiceListApiView , TimeSlotList
from .views.admin import (AdminCreateBarberApiView,AdminDeleteBarberApiView,
                          AdminBarberListApiView,AdminUpdateBarberApiview,AdminCreateServiceApiView,
                          AdminServiceListApiView,AdminUpdateServiceApiView,AdminDeleteServiceApiView,
                          AdminRetrieveServiceApiView,AdminRetrieveBarberApiView,AdminUpdateServicePriceApiView,
                          UpdateTimeSlotStatusApiView,AdminWorkingHoursWeeklyCreateApiview,WeeklyPlanListApiView,
                          CreateManagerApiView,AdminCreateBarberServiceApiView,AdminServiceListForBarber,
                          AdminBarberServiceList,AdminRetrieveBarberServiceApiView,AdminDeleteBarberServiceApiView,
                          AdminMenuCount)

urlpatterns = [
    path("v1/barbers/",BarberListApiView.as_view(),name="barber-list"),

    path("v1/admin/barbers/create/", AdminCreateBarberApiView.as_view(), name="barber-create"),
    path("v1/admin/barbers/list/", AdminBarberListApiView.as_view(), name="barber-list"),
    path("v1/admin/barber/<int:pk>/", AdminRetrieveBarberApiView.as_view(), name="barber-retrieve"),
    path("v1/admin/barbers/update/<int:pk>/", AdminUpdateBarberApiview.as_view(), name="barber-update"),
    path("v1/admin/barbers/delete/<int:pk>/", AdminDeleteBarberApiView.as_view(), name="barber-delete"),
    path("v1/admin/barbers/<int:barber_id>/weekly-plan/", WeeklyPlanListApiView.as_view(), name="weekly-plan-list"),

    path("v1/admin/service/create/", AdminCreateServiceApiView.as_view(), name="service-create"),
    path("v1/admin/service/list/", AdminServiceListApiView.as_view(), name="service-list"),
    path("v1/admin/service/<int:pk>/", AdminRetrieveServiceApiView.as_view(), name="service-retrieve"),
    path("v1/admin/service/update/<int:pk>/", AdminUpdateServiceApiView.as_view(), name="service-update"),
    path("v1/admin/service/delete/<int:pk>/", AdminDeleteServiceApiView.as_view(), name="service-delete"),

    path("v1/admin/barbers-service/<int:pk>/change-price/", AdminUpdateServicePriceApiView.as_view(),
         name="change_price"),
    path("v1/admin/barbers-service/create/", AdminCreateBarberServiceApiView.as_view(),
         name="create-barber-service"),
    path("v1/admin/barbers-service/list/", AdminBarberServiceList.as_view(),
         name="-barber-service-list"),
    path("v1/admin/new-service/barber/list/", AdminServiceListForBarber.as_view(),
         name="new-service-barber"),
    path("v1/admin/barber-service/<int:pk>/", AdminRetrieveBarberServiceApiView.as_view(),
         name="barber-service-price"),
    path("v1/admin/barber-service/delete/<int:pk>/", AdminDeleteBarberServiceApiView.as_view(),
         name="barber-service-price"),



    path("v1/admin/TimeSlot/<int:pk>/change-status/", UpdateTimeSlotStatusApiView.as_view(),
         name="update-time_slot_status"),
    path("v1/admin/working-hours/weekly/",AdminWorkingHoursWeeklyCreateApiview.as_view(),
         name ="working-hours-weekly"),

    path("v1/admin/create-manager/",CreateManagerApiView.as_view(),name = "create_manager"),

    path("v1/barbers/<int:barber_id>/service/",BarberServiceListApiView.as_view(),name="service-list"),
    path("v1/barbers/<int:barber_id>/all-slots/", TimeSlotList.as_view(), name="barber-slot-list"),

    path("v1/admin/menu-count/",AdminMenuCount.as_view(),name="menu-count")

]