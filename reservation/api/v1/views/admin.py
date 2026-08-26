from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView , UpdateAPIView , RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from account.models import Customer
from salon.api.v1.permissions import IsBarberShopManager
from ..serializers.admin import (AdminReservationListSerializer,AdminPaymentStatusUpdateSerializer,
                                 AdminReservationCreateSerializer)
from ..serializers.public import PaymentSerializer
from ....models import Reservation , Payment
from ..services import update_payment_status , create_reservation

class AdminReservationCreateApiView(APIView):

    def post(self,request):
        serializer = AdminReservationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        first_name = serializer.validated_data['first_name']
        last_name = serializer.validated_data['last_name']
        phone_number = serializer.validated_data['phone_number']

        customer , created = Customer.objects.get_or_create(
            phone_number = phone_number,
            defaults = {
                "first_name" : first_name,
                "last_name" : last_name
            }
        )

        try:
            reservation = create_reservation(customer=customer,
                                             barber_service = serializer.validated_data['barber_service'],
                                             reservation_date = serializer.validated_data['reservation_date'],
                                             reservation_time = serializer.validated_data['reservation_time'])

        except ValueError as e:
            return Response(
                {"message":str(e)},
                status = status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {
                "message":"رزرو با موفقیت ثبت شد",
                "reservation_id": reservation.id,
                "status": reservation.status,
                "expires_at": reservation.expires_at
            } ,
            status = status.HTTP_201_CREATED
        )

class AdminReservationListApiView(ListAPIView):
    # permission_classes = [IsAuthenticated,IsBarberShopManager]
    serializer_class = AdminReservationListSerializer

    def get_queryset(self):
        queryset= Reservation.objects.select_related('customer',
                                                  'barber_service',
                                                  'barber_service__barber',
                                                  'barber_service__service',
                                                  'payment').all().order_by('-created_date')
        from_date = self.request.query_params.get('from_date')
        to_date = self.request.query_params.get('to_date')

        if from_date:
            queryset = queryset.filter(reservation_date__gte = from_date)

        if to_date:
            queryset = queryset.filter(reservation_date__lte = to_date)

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