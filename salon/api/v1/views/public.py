from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework .views import APIView
from rest_framework import status
from datetime import datetime
from ..services import generate_slots

from ....models import Barber , BarberService , WeeklyPlan , TimeSlot
from ..serializers.public import BarberSerializers , BarberServiceSerializers , TimeSlotSerializer

class BarberListApiView(ListAPIView):
    queryset = Barber.objects.filter(is_active = True)
    serializer_class = BarberSerializers

class BarberServiceListApiView(ListAPIView):
    serializer_class = BarberServiceSerializers
    def get_queryset(self):
        barber_id = self.kwargs["barber_id"]
        return BarberService.objects.filter(barber_id=barber_id)

# class TimeSlotList(APIView):
#     def get(self,request,barber_id):
#          date = request.query_params.get("date")
#          try :
#              barber = Barber.objects.get(id = barber_id)
#          except Barber.DoesNotExist:
#              return Response({"message":"barber with this id does not exist"},status=status.HTTP_404_NOT_FOUND)
#          if date:
#              try:
#                 result=generate_slots(barber_id,date)
#              except WeeklyPlan.DoesNotExist:
#                  return Response(
#                      {"message": "No Weekly plan found"}, status=status.HTTP_404_NOT_FOUND
#                  )
#              return Response(result)
#          else:
#              return Response(
#                  {"message": "فرستادن تاریخ در ریکوِئست الزامی است"}, status=status.HTTP_400_BAD_REQUEST
#              )

class TimeSlotList(APIView):
    def get(self,request , barber_id):
        date = request.query_params.get('date')
        try :
            barber = Barber.objects.get(id = barber_id)
        except Barber.DoesNotExist:
            return Response({"message":"barber with this id does not exist"},
                             status=status.HTTP_404_NOT_FOUND)
        if date :
            try:
                date = datetime.strptime(date, "%Y-%m-%d").date()
            except ValueError:
                return Response(
                    {"message": "فرمت تاریخ اشتباه است"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            slots = TimeSlot.objects.filter(weekly_plan__barber_id=barber_id,
                                            weekly_plan__date=date).order_by("start_time")
            serializer = TimeSlotSerializer(slots,many=True)
            return Response(serializer.data)
        else:
                 return Response(
                     {"message": "فرستادن تاریخ در ریکوِئست الزامی است"}, status=status.HTTP_400_BAD_REQUEST
                 )
