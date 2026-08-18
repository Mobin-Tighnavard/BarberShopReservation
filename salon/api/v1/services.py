from rest_framework.response import Response
from rest_framework import status

from datetime import datetime ,timedelta
from ...models import TimeSlot , WorkingHourBase , WeeklyPlan

# def generate_slots(barber_id,date):
#     date = datetime.strptime(date, "%Y-%m-%d").date()
#     try:
#         weekly_plan = WeeklyPlan.objects.get(
#             barber_id=barber_id,
#             date=date,
#             status=WeeklyPlan.WeeklyStatus.ACTIVE
#         )
#     except WeeklyPlan.DoesNotExist:
#         raise WeeklyPlan.DoesNotExist
#
#     current =datetime.combine(date,weekly_plan.start_time)
#     end = datetime.combine(date,weekly_plan.end_time)
#     duration = timedelta(hours=1)
#     slots = []
#     while current < end:
#         end_slot = current + duration
#         slots.append({"start_time":current.time(),
#                       "end_time":end_slot.time(),
#                       "status":weekly_plan.status,
#                       "id":weekly_plan.id})
#         current = end_slot
#     return slots

def generate_slots(weekly_plan):
    if weekly_plan.status != WeeklyPlan.WeeklyStatus.ACTIVE:
        return []
    current =datetime.combine(weekly_plan.date,weekly_plan.start_time)
    end = datetime.combine(weekly_plan.date,weekly_plan.end_time)
    duration = timedelta(hours=1)
    slots = []
    while current < end:
        end_slot = current + duration
        slot = TimeSlot.objects.get_or_create(
            weekly_plan=weekly_plan,
            start_time = current.time(),
            end_time = end_slot.time()
        )
        slots.append(slot[0])
        current = end_slot
    return slots

def get_or_create_weekly_plan(barber,date):
    weekday = date.weekday()

    working_hour = WorkingHourBase.objects.filter(
        barber_id = barber,
        weekday = weekday
    ).first()
    if not working_hour :
        return None
    weekly_plan , created = WeeklyPlan.objects.get_or_create(
        barber = barber,
        date = date,
        defaults = {
            "start_time" : working_hour.start_time,
            "end_time" : working_hour.end_time,
            "status" : (WeeklyPlan.WeeklyStatus.OFF if working_hour.is_off
                        else WeeklyPlan.WeeklyStatus.ACTIVE)
        }
    )
    if created and WeeklyPlan.status == WeeklyPlan.WeeklyStatus.ACTIVE:
        generate_slots(weekly_plan)
    return weekly_plan




