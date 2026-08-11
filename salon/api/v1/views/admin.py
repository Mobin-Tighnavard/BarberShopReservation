from rest_framework.generics import CreateAPIView,ListAPIView,DestroyAPIView,UpdateAPIView,RetrieveAPIView
from ....models import Barber , Service , BarberService
from ..serializers.admin import (AdminCreateBarberSerializers,AdminBarberListSerializer,AdminUpdateBarberSerializer
                                 ,AdminCreateServiceSerializer,AdminServiceListSerializer,
                                 ServicePriceUpdateSerializers)

# crud for Barbers
class AdminCreateBarberApiView(CreateAPIView):
    queryset = Barber.objects.all()
    serializer_class = AdminCreateBarberSerializers

class AdminBarberListApiView(ListAPIView):
    queryset = Barber.objects.all()
    serializer_class = AdminBarberListSerializer

class AdminRetrieveBarberApiView(RetrieveAPIView):
    queryset = Barber.objects.all()
    serializer_class = AdminBarberListSerializer

class AdminUpdateBarberApiview(UpdateAPIView):
    queryset = Barber.objects.all()
    serializer_class = AdminUpdateBarberSerializer

class AdminDeleteBarberApiView(DestroyAPIView):
    queryset = Barber.objects.all()

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

# Crud For Service

class AdminCreateServiceApiView(CreateAPIView):
    queryset = Service.objects.all()
    serializer_class = AdminCreateServiceSerializer

class AdminServiceListApiView(ListAPIView):
    queryset = Service.objects.all()
    serializer_class = AdminServiceListSerializer

class AdminRetrieveServiceApiView(RetrieveAPIView):
    queryset = Service.objects.all()
    serializer_class = AdminServiceListSerializer

class AdminUpdateServiceApiView(UpdateAPIView):
    queryset = Service.objects.all()
    serializer_class = AdminServiceListSerializer

class AdminDeleteServiceApiView(DestroyAPIView):
    queryset = Service.objects.all()

    def perform_destroy(self, instance):
        instance.delete_flag = True
        instance.save()


# update price of service

class AdminUpdateServicePriceApiView(UpdateAPIView):
    queryset = BarberService.objects.all()
    serializer_class = ServicePriceUpdateSerializers
