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
    print(reservation.status)
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
def create_reservation(customer, barber_service, reservation_date, reservation_time):

    slot = TimeSlot.objects.select_for_update().get(
        weekly_plan__barber = barber_service.barber,
        weekly_plan__date = reservation_date,
        start_time = reservation_time
    )

    if slot.stats != TimeSlot.TimeSlotStatus.ACTIVE:
        raise ValueError("این زمان قابل رزرو نیست")

    existing_reservation = Reservation.objects.filter(
        barber_service = barber_service,
        reservation_date = reservation_date,
        reservation_time = reservation_time,
    ).exclude(
        status__in=[Reservation.ReservationStatus.EXPIRED,Reservation.ReservationStatus.CANCELED]
    ).first()

    if existing_reservation:
        raise ValueError("این زمان قبلا رزرو شده است")

    expires_at = timezone.now() +timedelta(minutes=10)

    reservation = Reservation.objects.create(
        customer = customer,
        barber_service = barber_service,
        reservation_date = reservation_date,
        reservation_time = reservation_time,
        status = Reservation.ReservationStatus.PENDING_PAYMENT,
        expires_at = expires_at
    )

    return reservation



