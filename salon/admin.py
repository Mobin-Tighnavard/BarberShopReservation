from django.contrib import admin
from .models import Barber , Service , WeeklyPlan , BarberService
class BarberAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','phone_number','national_code','is_active']

class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name','delete_flag']

class WeeklyPlanAdmin(admin.ModelAdmin):
    list_display = ['barber_id','date','start_time','end_time','status']

class BarberServiceAdmin(admin.ModelAdmin):
    list_display = ["barber","service","price","delete_flag"]

admin.site.register(Barber,BarberAdmin)
admin.site.register(Service,ServiceAdmin)
admin.site.register(WeeklyPlan,WeeklyPlanAdmin)
admin.site.register(BarberService,BarberServiceAdmin)
# Register your models here.
