from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from drf_yasg.utils import swagger_auto_schema
from ...models import Customer
from .serializers import CreateCustomerSerializers,LogoutSerializer

class CreateCustomerApiView(CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CreateCustomerSerializers

class AdminLogoutApiView(APIView):
    @swagger_auto_schema(
        request_body=LogoutSerializer
    )
    def post(self,request):

        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(
            {"message":"Successfully logged out"},
            status = status.HTTP_200_OK
        )