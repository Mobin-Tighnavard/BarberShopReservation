from datetime import datetime , timedelta
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,ListAPIView,DestroyAPIView,UpdateAPIView,RetrieveAPIView
from ....models import Barber , Service , BarberService , TimeSlot
from ..permissions import IsBarberShopManager
from ..services import get_or_create_weekly_plan
from ..serializers.admin import (AdminCreateBarberSerializers,AdminBarberListSerializer,AdminUpdateBarberSerializer
                                 ,AdminCreateServiceSerializer,AdminServiceListSerializer,
                                 ServicePriceUpdateSerializers,AdminTimeSlotStatusSerializer,
                                 WorkingHourWeeklySerializer,CreateManagerSerializer,
                                 AdminBarberServiceCreateSerializer,WeeklyPlanSerializer,
                                 AdminBarberServiceListSerializer,AdminServicePriceUpdateSerializers)

# crud for Barbers
class AdminCreateBarberApiView(CreateAPIView):
    # permission_classes = [IsBarberShopManager]
    queryset = Barber.objects.all()
    serializer_class = AdminCreateBarberSerializers

class AdminBarberListApiView(ListAPIView):
    # permission_classes = [IsBarberShopManager]
    queryset = Barber.objects.filter(is_active=True)
    serializer_class = AdminBarberListSerializer
    # def get_queryset(self):
    #     queryset = Barber.objects.all().filter(is_active=True)
    #     return queryset
    #

class AdminRetrieveBarberApiView(RetrieveAPIView):
    # permission_classes = [IsBarberShopManager]
    queryset = Barber.objects.all()
    serializer_class = AdminBarberListSerializer

class AdminUpdateBarberApiview(UpdateAPIView):
    # permission_classes = [IsBarberShopManager]
    queryset = Barber.objects.all()
    serializer_class = AdminUpdateBarberSerializer

class AdminDeleteBarberApiView(DestroyAPIView):
    # permission_classes = [IsBarberShopManager]
    queryset = Barber.objects.all()

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

# Crud For Service

class AdminCreateServiceApiView(CreateAPIView):
    # permission_classes = [IsBarberShopManager]
    queryset = Service.objects.all()
    serializer_class = AdminCreateServiceSerializer

class AdminServiceListApiView(ListAPIView):
    # permission_classes = [IsBarberShopManager]
    queryset = Service.objects.all().filter(delete_flag = False)
    serializer_class = AdminServiceListSerializer

class AdminRetrieveServiceApiView(RetrieveAPIView):
    # permission_classes = [IsBarberShopManager]
    queryset = Service.objects.all()
    serializer_class = AdminServiceListSerializer

class AdminUpdateServiceApiView(UpdateAPIView):
    # permission_classes = [IsBarberShopManager]
    queryset = Service.objects.all()
    serializer_class = AdminServiceListSerializer

class AdminDeleteServiceApiView(DestroyAPIView):
    # permission_classes = [IsBarberShopManager]
    queryset = Service.objects.all()

    def perform_destroy(self, instance):
        instance.delete_flag = True
        instance.save()


# crud BarberService

class AdminBarberServiceList(ListAPIView):
    serializer_class = AdminBarberServiceListSerializer
    def get_queryset(self):
        return BarberService.objects.filter(
            barber__is_active = True,
            service__delete_flag = False
        )

class AdminServiceListForBarber(ListAPIView):
    serializer_class = AdminServiceListSerializer
    def get_queryset(self):
        barber_id = self.request.query_params.get('barber_id')

        if not barber_id:
            return Service.objects.none()

        existing_service = BarberService.objects.filter(
            barber_id = barber_id
        ).values_list("service_id",flat=True)

        return Service.objects.filter(delete_flag = False).exclude(id__in=existing_service)

class AdminCreateBarberServiceApiView(CreateAPIView):
    queryset = BarberService.objects.all()
    serializer_class = AdminBarberServiceCreateSerializer

class AdminUpdateServicePriceApiView(UpdateAPIView):
    # permission_classes = [IsBarberShopManager]
    queryset = BarberService.objects.all()
    serializer_class = ServicePriceUpdateSerializers

class AdminRetrieveBarberServiceApiView(RetrieveAPIView):
    queryset = BarberService.objects.all()
    serializer_class = AdminServicePriceUpdateSerializers

class AdminDeleteBarberServiceApiView(DestroyAPIView):
    queryset = BarberService.objects.all()


# TimeSlot

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


# Admin Menu Count

class AdminMenuCount(APIView):
    def get(self,request):
        return Response({
            "barbers_count":Barber.objects.filter(is_active=True).count(),
            "service_count":Service.objects.filter(delete_flag=False).count(),
            "barber_service_count":BarberService.objects.filter(barber__is_active=True,
                                                                service__delete_flag=False).count(),
        }
        )