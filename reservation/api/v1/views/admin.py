from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView , UpdateAPIView , RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from account.models import Customer
from salon.api.v1.permissions import IsBarberShopManager
from drf_yasg.utils import swagger_auto_schema
from ..serializers.admin import (AdminReservationListSerializer,AdminPaymentStatusUpdateSerializer,
                                 AdminReservationCreateSerializer,ReservationResponseSerializer)
from ..serializers.public import PaymentSerializer
from ....models import Reservation , Payment
from ..services import update_payment_status , create_reservation

class AdminReservationCreateApiView(APIView):
    @swagger_auto_schema(
        request_body=AdminReservationCreateSerializer
    )
    def post(self,request):
        serializer = AdminReservationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            reservation = create_reservation(customer= serializer.validated_data['customer'],
                                             barber_service = serializer.validated_data['barber_service'],
                                             slot = serializer.validated_data['slot'],
                                             reservation_date = serializer.validated_data['reservation_date'],
                                             )

        except ValueError as e:
            return Response(
                {"message":str(e)},
                status = status.HTTP_400_BAD_REQUEST
            )
        response_serializer = ReservationResponseSerializer(reservation)
        print('---------')
        print(response_serializer.data)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )

class AdminReservationListApiView(ListAPIView):
    # permission_classes = [IsAuthenticated,IsBarberShopManager]
    serializer_class = AdminReservationListSerializer

    def get_queryset(self):
        queryset= Reservation.objects.select_related('customer',
                                                  'barber_service',
                                                  'barber_service__barber',
                                                  'barber_service__service',
                                                  'payment').all().order_by('-created_date').exclude(
            status__in=['PENDING_PAYMENT','EXPIRED'])
        from_date = self.request.query_params.get('from_date')
        to_date = self.request.query_params.get('to_date')
        status = self.request.query_params.get('status')

        if from_date:
            queryset = queryset.filter(reservation_date__gte = from_date)

        if to_date:
            queryset = queryset.filter(reservation_date__lte = to_date)

        if status:
            queryset = queryset.filter(status = status)

        return queryset

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

class AdminPaymentStatusUpdateAcceptedApiView(APIView):

    def patch(self, request,pk):
        payment = get_object_or_404(Payment,pk=pk)
        payment.status = Payment.PaymentStatus.ACCEPTED
        payment.save(update_fields=['status'])
        reservation = payment.reservation
        reservation.status = reservation.ReservationStatus.CONFIRMED
        reservation.save(update_fields=['status'])
        return Response(
            {
                'message': 'Payment accepted successfully',
                'status': payment.status
            },
            status=status.HTTP_200_OK
        )

class AdminPaymentStatusUpdateRejectedApiView(APIView):

    def patch(self, request, pk):
        payment = get_object_or_404(Payment, pk=pk)
        payment.status = Payment.PaymentStatus.REJECTED
        payment.save(update_fields=['status'])
        reservation = payment.reservation
        reservation.status = reservation.ReservationStatus.CANCELED
        reservation.save(update_fields=['status'])
        return Response(
            {
                'message': 'Payment rejected successfully',
                'status': payment.status
            },
            status=status.HTTP_200_OK
        )

class AdminReservationRetrieveApiview(RetrieveAPIView):
    serializer_class = AdminReservationListSerializer

    def get_queryset(self):
        queryset = Reservation.objects.select_related('customer',
                                                    'barber_service',
                                                    'barber_service__barber',
                                                    'barber_service__service',
                                                    'payment').order_by('created_date')
        return queryset

class AdminReservationPendingRetrieveApiView(RetrieveAPIView):
    serializer_class = AdminReservationListSerializer

    def get_queryset(self):
        queryset = Reservation.objects.select_related('customer',
                                                      'barber_service',
                                                      'barber_service__barber',
                                                      'barber_service__service',
                    'payment').filter(payment__status = Payment.PaymentStatus.PENDING).order_by('created_date')
        return queryset