from django.contrib import admin
from .models import Reservation

class ReservationAdmin(admin.ModelAdmin):
    list_display = ["customer","barber_service","reservation_date","reservation_time","status"]

admin.site.register(Reservation,ReservationAdmin)

# Register your models here.
