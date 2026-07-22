from rest_framework.generics import  ListAPIView
from ...models import Barber , Service
from .serializers import BarberSerializers , ServiceSerializers

class BarberListApiView(ListAPIView):
    queryset = Barber.objects.filter(is_active = True)
    serializer_class = BarberSerializers

class ServiceListApiView(ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializers