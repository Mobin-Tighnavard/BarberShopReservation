from django.contrib import admin
from .models import Barber , Service
class BarberAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','phone_number','national_code']

admin.site.register(Barber,BarberAdmin)
admin.site.register(Service)

# Register your models here.
