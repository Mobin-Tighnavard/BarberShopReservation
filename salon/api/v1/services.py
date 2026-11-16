from rest_framework.response import Response
from rest_framework import status

from datetime import datetime ,timedelta, date
from ...models import TimeSlot , WorkingHourBase

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

def generate_future_slots(barber, days=7):
    today = date.today()


    for i in range(7):
        target_date = today + timedelta(days=i)

        weekday = (target_date.weekday() + 2) % 7

        try:
            working_hour = WorkingHourBase.objects.get(
                barber=barber,
                weekday=weekday
            )
        except WorkingHourBase.DoesNotExist:
            continue
        generate_slots(working_hour,date=target_date)

def generate_slots(working_hour, date):
    if working_hour.is_off:
        return []
    current = datetime.combine(date,working_hour.start_time)
    end = datetime.combine(date,working_hour.end_time)

    slots = []

    while current < end:
        end_slot = current + timedelta(hours=1)

        if end_slot > end:
            break

        slot ,created = TimeSlot.objects.get_or_create(
            barber = working_hour.barber,
            date = date,
            start_time = current.time(),
            end_time = end_slot.time(),
            defaults={
                "status":TimeSlot.TimeSlotStatus.ACTIVE
            }
        )
        slots.append(slot)
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
    return weekly_plan




