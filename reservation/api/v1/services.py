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
    reservation.status=Reservation.ReservationStatus.PENDING_CONFIRMATION
    reservation.save()
    return payment