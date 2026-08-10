from rest_framework.generics import CreateAPIView,ListAPIView,DestroyAPIView,UpdateAPIView
from ....models import Barber
from ..serializers.admin import CreateBarberSerializers,AdminBarberListSerializer,AdminUpdateBarberSerializer
# crud for Barbers
class AdminCreateBarberApiView(CreateAPIView):
    queryset = Barber.objects.all()
    serializer_class = CreateBarberSerializers

class AdminBarberListApiView(ListAPIView):
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