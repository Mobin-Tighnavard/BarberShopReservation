from django.db.models.signals import post_save
from django.dispatch import receiver
from .services import generate_slots
from ...models import WeeklyPlan
@receiver(post_save,sender=WeeklyPlan)
def create_time_slots(sender,instance,created,**kwargs):
    if created:
        generate_slots(instance)
