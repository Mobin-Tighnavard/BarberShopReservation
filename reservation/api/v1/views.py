from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser , FormParser
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .serializers import PaymentCreateSerializer,PaymentSerializer
from .services import create_payment

class PaymentCreateApiView(APIView):
    parser_classes = [MultiPartParser,FormParser]

    @swagger_auto_schema(request_body=PaymentCreateSerializer)
    def post(self,request):
        serializer = PaymentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reservation = serializer.validated_data['reservation']
        receipt_image = serializer.validated_data['receipt_image']
        payment = create_payment(reservation=reservation,receipt_image=receipt_image)
        return Response(PaymentSerializer(payment).data,status=status.HTTP_201_CREATED)
