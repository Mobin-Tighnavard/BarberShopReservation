from django.contrib import admin
from .models import Barber , Service , BarberService , TimeSlot ,WorkingHourBase
class BarberAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','phone_number','national_code','is_active']

class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name','delete_flag']

class BarberServiceAdmin(admin.ModelAdmin):
    list_display = ["barber","service","price","delete_flag"]
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ["barber","date","start_time","end_time","status"]

class WorkingHourBaseAdmin(admin.ModelAdmin):
    list_display = ["barber", "weekday" ,"start_time", "end_time", "is_off"]

admin.site.register(Barber,BarberAdmin)
admin.site.register(Service,ServiceAdmin)
admin.site.register(BarberService,BarberServiceAdmin)
admin.site.register(TimeSlot,TimeSlotAdmin)
admin.site.register(WorkingHourBase,WorkingHourBaseAdmin)
# Register your models here.
