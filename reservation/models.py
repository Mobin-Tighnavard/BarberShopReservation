from django.db import models
from account.models import Customer
from salon.models import BarberService

class Reservation(models.Model):
    class ReservationStatus(models.TextChoices):
        PENDING_PAYMENT = "PENDING_PAYMENT" , "pending_payment"
        PENDING_CONFIRMATION = "PENDING_CONFIRMATION" , "pending_confirmation"
        CONFIRMED = "CONFIRMED" , "confirmed"
        CANCELED = "CANCELED" , "canceled"
        EXPIRED = "EXPIRED" , "expired"
    customer = models.ForeignKey(Customer,on_delete=models.PROTECT)
    barber_service = models.ForeignKey(BarberService,on_delete=models.PROTECT)
    reservation_time = models.TimeField()
    reservation_date = models.DateField()
    status = models.CharField(max_length=70,choices=ReservationStatus.choices,default=ReservationStatus.PENDING_PAYMENT)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

def payment_receipt_path(instance, filename):
    return f"payment_receipts/reservation_{instance.reservation.id}/{filename}"

class Payment(models.Model):
    class PaymentStatus(models.TextChoices):
        PENDING = "PENDING" , "pending"
        ACCEPTED = "ACCEPTED" , "accepted"
        REJECTED = "REJECTED" , "rejected"

    reservation = models.OneToOneField(Reservation,on_delete=models.PROTECT)
    receipt_image = models.ImageField(upload_to=payment_receipt_path)
    status = models.CharField(max_length=20,choices=PaymentStatus.choices,default=PaymentStatus.PENDING)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


# Create your models here.
