from rest_framework import serializers
from ....models import Barber , BarberService,TimeSlot
class BarberSerializers(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    class Meta:
        model = Barber
        fields = ["id","full_name"]
    def get_full_name(self,obj):
        return f"{obj.first_name} {obj.last_name}"

class BarberServiceSerializers(serializers.ModelSerializer):
    service_name = serializers.CharField(source="service.name")
    class Meta:
        model = BarberService
        fields = ['id','service_name','price','delete_flag']

class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ['id','start_time','end_time','status']