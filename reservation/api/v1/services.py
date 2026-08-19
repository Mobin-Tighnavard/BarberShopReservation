from rest_framework.exceptions import ValidationError
from django.db import transaction
from ...models import Reservation , Payment

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



