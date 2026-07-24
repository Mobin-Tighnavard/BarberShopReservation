from rest_framework.response import Response
from rest_framework import status
from datetime import datetime ,timedelta
from ...models import WeeklyPlan

def generate_slots(barber_id,date):
    date = datetime.strptime(date, "%Y-%m-%d").date()
    try:
        weekly_plan = WeeklyPlan.objects.get(
            barber_id=barber_id,
            date=date,
            status=WeeklyPlan.WeeklyStatus.ACTIVE
        )
    except WeeklyPlan.DoesNotExist:
        raise WeeklyPlan.DoesNotExist

    current =datetime.combine(date,weekly_plan.start_time)
    end = datetime.combine(date,weekly_plan.end_time)
    duration = timedelta(hours=1)
    slots = []
    while current < end:
        end_slot = current + duration
        slots.append({"start_time":current.time(),
                      "end_time":end_slot.time()})
        current = end_slot
    return slots




