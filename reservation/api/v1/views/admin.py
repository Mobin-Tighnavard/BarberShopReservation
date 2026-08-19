from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView , UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from salon.api.v1.permissions import IsBarberShopManager
from ..serializers.admin import AdminReservationListSerializer,AdminPaymentStatusUpdateSerializer
from ..serializers.public import PaymentSerializer
from ....models import Reservation , Payment
from ..services import update_payment_status

class AdminReservationListApiView(ListAPIView):
    # permission_classes = [IsAuthenticated,IsBarberShopManager]
    serializer_class = AdminReservationListSerializer

    def get_queryset(self):
        return Reservation.objects.select_related('customer',
                                                  'barber_service',
                                                  'barber_service__barber',
                                                  'barber_service__service',
                                                  'payment').all().order_by('-created_date')

class AdminPendingPaymentListApiView(ListAPIView):
    # permission_classes = [IsAuthenticated,IsBarberShopManager]
    serializer_class = AdminReservationListSerializer

    def get_queryset(self):
        return Reservation.objects.select_related('customer',
                                                  'barber_service',
                                                  'barber_service__barber',
                                                  'barber_service__service',
                    'payment').filter(payment__status = Payment.PaymentStatus.PENDING).order_by('created_date')

class AdminPaymentStatusUpdateApiView(APIView):

    def patch(self,request,pk):

        payment = get_object_or_404(Payment.objects.select_related("reservation"),pk=pk)
        serializer = AdminPaymentStatusUpdateSerializer(payment,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        new_status = serializer.validated_data['status']
        try:
            payment = update_payment_status(payment,new_status)

        except ValueError as e :
            return Response(
                {"message":str(e)},status=status.HTTP_400_BAD_REQUEST
            )

        return Response(PaymentSerializer(payment).data,status=status.HTTP_200_OK)

