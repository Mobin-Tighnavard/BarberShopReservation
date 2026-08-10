from rest_framework.generics import CreateAPIView,DestroyAPIView
from ....models import Barber
from ..serializers.admin import CreateBarberSerializers
# crud for Barbers
class AdminCreateBarberApiView(CreateAPIView):
    queryset = Barber.objects.all()
    serializer_class = CreateBarberSerializers

class AdminDeleteBarberApiView(DestroyAPIView):
    queryset = Barber.objects.all()