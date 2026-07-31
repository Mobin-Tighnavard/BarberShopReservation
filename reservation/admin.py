from django.contrib import admin
from .models import Reservation , Payment

class ReservationAdmin(admin.ModelAdmin):
    list_display = ["customer","barber_service","reservation_date","reservation_time","status"]

class PaymentAdmin(admin.ModelAdmin):
    list_display = ["reservation","receipt_image","status","created_date"]

admin.site.register(Reservation,ReservationAdmin)
admin.site.register(Payment,PaymentAdmin)

# Register your models here.
