from datetime import datetime , timedelta
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,ListAPIView,DestroyAPIView,UpdateAPIView,RetrieveAPIView
from ....models import Barber , Service , BarberService , TimeSlot
from ..permissions import IsBarberShopManager
from ..services import get_or_create_weekly_plan
from ..serializers.admin import WeeklyPlanSerializer
from ..serializers.admin import (AdminCreateBarberSerializers,AdminBarberListSerializer,AdminUpdateBarberSerializer
                                 ,AdminCreateServiceSerializer,AdminServiceListSerializer,
                                 ServicePriceUpdateSerializers,AdminTimeSlotStatusSerializer,
                                 WorkingHourWeeklySerializer,CreateManagerSerializer)

# crud for Barbers
class AdminCreateBarberApiView(CreateAPIView):
    permission_classes = [IsBarberShopManager]
    queryset = Barber.objects.all()
    serializer_class = AdminCreateBarberSerializers

class AdminBarberListApiView(ListAPIView):
    permission_classes = [IsBarberShopManager]
    queryset = Barber.objects.all()
    serializer_class = AdminBarberListSerializer

class AdminRetrieveBarberApiView(RetrieveAPIView):
    permission_classes = [IsBarberShopManager]
    queryset = Barber.objects.all()
    serializer_class = AdminBarberListSerializer

class AdminUpdateBarberApiview(UpdateAPIView):
    permission_classes = [IsBarberShopManager]
    queryset = Barber.objects.all()
    serializer_class = AdminUpdateBarberSerializer

class AdminDeleteBarberApiView(DestroyAPIView):
    permission_classes = [IsBarberShopManager]
    queryset = Barber.objects.all()

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

# Crud For Service

class AdminCreateServiceApiView(CreateAPIView):
    permission_classes = [IsBarberShopManager]
    queryset = Service.objects.all()
    serializer_class = AdminCreateServiceSerializer

class AdminServiceListApiView(ListAPIView):
    permission_classes = [IsBarberShopManager]
    queryset = Service.objects.all()
    serializer_class = AdminServiceListSerializer

class AdminRetrieveServiceApiView(RetrieveAPIView):
    permission_classes = [IsBarberShopManager]
    queryset = Service.objects.all()
    serializer_class = AdminServiceListSerializer

class AdminUpdateServiceApiView(UpdateAPIView):
    permission_classes = [IsBarberShopManager]
    queryset = Service.objects.all()
    serializer_class = AdminServiceListSerializer

class AdminDeleteServiceApiView(DestroyAPIView):
    permission_classes = [IsBarberShopManager]
    queryset = Service.objects.all()

    def perform_destroy(self, instance):
        instance.delete_flag = True
        instance.save()

# update price of service

class AdminUpdateServicePriceApiView(UpdateAPIView):
    permission_classes = [IsBarberShopManager]
    queryset = BarberService.objects.all()
    serializer_class = ServicePriceUpdateSerializers

class UpdateTimeSlotStatusApiView(UpdateAPIView):
    permission_classes = [IsBarberShopManager]
    queryset = TimeSlot.objects.all()
    serializer_class = AdminTimeSlotStatusSerializer

# Set Work Time

class AdminWorkingHoursWeeklyCreateApiview(CreateAPIView):
    permission_classes = [IsBarberShopManager]
    serializer_class = WorkingHourWeeklySerializer

class WeeklyPlanListApiView(APIView):
    permission_classes = [IsBarberShopManager]

    def get(self,request,barber_id):
        try:
            barber = Barber.objects.get(id=barber_id)
        except Barber.DoesNotExist:
            return Response(
                {"message":"barber with this id does not exist"},
                status = status.HTTP_404_NOT_FOUND
            )
        start_date = request.query_params.get("start_date")

        if not start_date:
            return Response(
                {"message":"send start_date in query params is required"},
                status = status.HTTP_400_BAD_REQUEST
            )
        try:
            start_date = datetime.strptime(start_date,"%Y-%m-%d").date()
        except ValueError:
            return Response(
                {"message":"format of date is wrong"},
                status = status.HTTP_400_BAD_REQUEST
            )
        weekly_plans = []
        for i in range(7):
            date = start_date + timedelta(days=i)
            weekly_plan = get_or_create_weekly_plan(barber,date)

            if weekly_plan:
                weekly_plans.append(weekly_plan)

        serializer = WeeklyPlanSerializer(weekly_plans,many=True)

        return Response(serializer.data)

# create manager for barbershop

class CreateManagerApiView(CreateAPIView):
    serializer_class = CreateManagerSerializer
    permission_classes = [IsAdminUser]