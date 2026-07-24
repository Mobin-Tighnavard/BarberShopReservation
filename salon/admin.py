from django.contrib import admin
from .models import Barber , Service , WeeklyPlan
class BarberAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','phone_number','national_code']

class WeeklyPlanAdmin(admin.ModelAdmin):
    list_display = ['barber_id','date','start_time','end_time','status']

admin.site.register(Barber,BarberAdmin)
admin.site.register(Service)
admin.site.register(WeeklyPlan,WeeklyPlanAdmin)# Register your models here.
