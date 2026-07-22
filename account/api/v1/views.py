from rest_framework.generics import CreateAPIView
from ...models import Customer
from .serializers import CreateCustomerSerializers

class CreateCustomerApiView(CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CreateCustomerSerializers