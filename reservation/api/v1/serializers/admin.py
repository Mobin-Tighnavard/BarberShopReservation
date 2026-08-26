from rest_framework import serializers
from ....models import Reservation , Payment, BarberService

class AdminReservationCreateSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone_number = serializers.CharField()
    barber_service = serializers.PrimaryKeyRelatedField(queryset=BarberService.objects.all())
    reservation_date = serializers.DateField()
    reservation_time = serializers.TimeField()

class AdminReservationListSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()
    customer_phone = serializers.CharField(source="customer.phone_number")
    barber_name = serializers.SerializerMethodField()
    service_name = serializers.CharField(source="barber_service.service.name")
    service_price = serializers.CharField(source="barber_service.price" , read_only=True)
    payment_id = serializers.IntegerField(source="payment.id",read_only=True)
    payment_status = serializers.CharField(source="payment.status" , read_only=True)
    receipt_image = serializers.CharField(source="payment.receipt_image" , read_only=True)

    class Meta:
        model = Reservation
        fields = ['id',
                  'customer_name',
                  'customer_phone',
                  'barber_name',
                  'service_name',
                  'service_price',
                  'status',
                  'payment_id',
                  'payment_status',
                  'receipt_image',
                  'reservation_date',
                  'reservation_time']

    def get_customer_name(self,obj):
        return f"{obj.customer.first_name} {obj.customer.last_name}"

    def get_barber_name(self,obj):
        return f"{obj.barber_service.barber.first_name} {obj.barber_service.barber.last_name}"

class AdminPaymentStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['status']