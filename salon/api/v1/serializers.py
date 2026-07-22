from rest_framework import serializers
from ...models import Barber , Service
class BarberSerializers(serializers.ModelSerializer):
    class Meta:
        model = Barber
        fields = ['first_name','last_name']

class ServiceSerializers(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'