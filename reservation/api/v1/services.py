from datetime import timedelta
from rest_framework.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from ...models import Reservation , Payment
from salon.models import TimeSlot

@transaction.atomic
def create_payment(reservation,receipt_image):

    if hasattr(reservation , 'payment'):
        raise ValidationError("Payment already exist")
    payment = Payment.objects.create(
        reservation = reservation,
        receipt_image = receipt_image
    )
    print('---------')
    reservation.status=Reservation.ReservationStatus.PENDING_CONFIRMATION
    reservation.save(update_fields = ["status"])
    return payment

@transaction.atomic
def update_payment_status(payment,new_status):
    reservation = payment.reservation

    if payment.status != Payment.PaymentStatus.PENDING:
        raise ValueError("this payment has already been processed.")

    if new_status == Payment.PaymentStatus.ACCEPTED:
        payment.status = Payment.PaymentStatus.ACCEPTED
        payment.save(update_fields = ["status","updated_date"])

        reservation.status = Reservation.ReservationStatus.CONFIRMED
        reservation.save(update_fields = ["status","updated_date"])

    elif new_status == Payment.PaymentStatus.REJECTED:
        payment.status = Payment.PaymentStatus.REJECTED
        payment.save(update_fields = ["status","updated_date"])

        reservation.status = Reservation.ReservationStatus.PENDING_PAYMENT
        reservation.save(update_fields = ["status","updated_date"])

    else:
        raise ValueError("invalid payment status")

    return payment

@transaction.atomic
def create_reservation(customer, barber_service, slot ):# به ایرعلی بگم resevation_date رو برداشتم و برام نفرسته

    slot = TimeSlot.objects.select_for_update().get(pk=slot.pk)

    if slot.status != TimeSlot.TimeSlotStatus.ACTIVE:
        raise ValueError("این زمان قابل رزرو نیست")

    if slot.barber_id != barber_service.barber_id:
        raise ValueError("این زمان متعلق به آرایشگر این سرویس نیست")


    existing_reservation = Reservation.objects.filter(
        barber_service = barber_service,
        reservation_time = slot.start_time,
        reservation_date = slot.date,
    ).exclude(
        status__in=[Reservation.ReservationStatus.EXPIRED,Reservation.ReservationStatus.CANCELED]
    ).first()

    if existing_reservation:
        raise ValueError("این زمان قبلا رزرو شده است")

    expires_at = timezone.now() +timedelta(minutes=10)

    reservation = Reservation.objects.create(
        customer = customer,
        barber_service = barber_service,
        reservation_time = slot.start_time,
        reservation_date = reservation_date,
        status = Reservation.ReservationStatus.PENDING_PAYMENT,
        expires_at = expires_at
    )
    slot.status = TimeSlot.TimeSlotStatus.OFF
    slot.save(update_fields=["status"])
    return reservation



