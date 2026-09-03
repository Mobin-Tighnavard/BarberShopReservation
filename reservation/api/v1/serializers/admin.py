from rest_framework import serializers
from ....models import Reservation , Payment, BarberService
from account.models import Customer
from salon.models import TimeSlot

class AdminReservationCreateSerializer(serializers.Serializer):
    customer = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all()
    )
    barber_service = serializers.PrimaryKeyRelatedField(
        queryset=BarberService.objects.all()
    )
    slot = serializers.PrimaryKeyRelatedField(
        queryset=TimeSlot.objects.all()
    )
    reservation_date = serializers.DateField()

class ReservationResponseSerializer(serializers.ModelSerializer):
    barber_fullname = serializers.SerializerMethodField()
    service_name = serializers.CharField(source="barber_service.service.name")
    price = serializers.CharField(source="barber_service.price")

    class Meta:
        model = Reservation
        fields = ['id','barber_fullname','service_name','price']

    def get_barber_fullname(self,obj):
        return f'{obj.barber_service.barber.first_name} {obj.barber_service.barber.last_name}'

class AdminReservationListSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()
    customer_phone = serializers.CharField(source="customer.phone_number")
    barber_name = serializers.SerializerMethodField()
    service_name = serializers.CharField(source="barber_service.service.name")
    service_price = serializers.CharField(source="barber_service.price" , read_only=True)
    payment_id = serializers.IntegerField(source="payment.id",read_only=True)
    payment_status = serializers.CharField(source="payment.status" , read_only=True)
    receipt_image = serializers.SerializerMethodField()

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

    def get_receipt_image(self,obj):
        if hasattr(obj,"payment") and obj.payment.receipt_image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.payment.receipt_image.url)
        return None

class AdminPaymentStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['status']