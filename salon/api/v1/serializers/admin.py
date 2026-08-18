import re
from rest_framework import serializers
from django.db import transaction
from django.contrib.auth.models import User,Group
from ....models import Barber , Service , BarberService , TimeSlot , WorkingHourBase , WeeklyPlan
from .public import TimeSlotSerializer

class AdminCreateBarberSerializers(serializers.ModelSerializer):
    class Meta:
        model = Barber
        fields = ["first_name","last_name","phone_number","national_code"]

    def validate_first_name(self,value):
        if not re.match(r"^[آ-ی\s]+$",value):
            raise serializers.ValidationError(
                "نام باید فقط شامل حروف فارسی باشد"
            )
        return value
    def validate_last_name(self,value):
        if not re.match(r"^[آ-ی\S]+$",value):
            raise serializers.ValidationError(
                "نام خانوادگی باید فقط شامل حروف فارسی باشد"
            )
        return value
    def validate_phone_number(self,value):
        if not re.match(r"^09\d{9}$",value):
            raise serializers.ValidationError(
                "شمااره تلفن باید 11 رقم و با 09 شروع شود"
            )
        return value
    def validate_national_code(self,value):
        if not re.match(r"^\d{10}$",value):
            raise serializers.ValidationError(
                "کد ملی باید 10 رقم باشد!"
            )
        return value

class AdminBarberListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barber
        fields = ['id','first_name','last_name','phone_number','national_code','is_active']


class AdminUpdateBarberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barber
        fields = ['first_name','last_name','phone_number','national_code']

    def validate_first_name(self,value):
        if not re.match(r"^[آ-ی\s]+$",value):
            raise serializers.ValidationError(
                "نام باید فقط شامل حروف فارسی باشد!"
            )
        return value

    def validate_last_name(self,value):
        if not re.match(r"^[آ-ی\s]+$",value):
            raise serializers.ValidationError(
                "نام خانوادگی باید فقط شامل حروف فارسی باشد!"
            )
        return value

    def validate_phone_number(self,value):
        if not re.match(r"^09\d{9}$",value):
            raise serializers.ValidationError(
                "شماره تلفن باید 11 رقم و با 09 شروع شود!"
            )
        return value

    def validate_national_code(self,value):
        if not re.match(r"^\d{10}$",value):
            raise serializers.ValidationError(
                "کد ملی باید 10 رقم باشد!"
            )
        return value

class AdminCreateServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['name']

class AdminServiceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['name']

class ServicePriceUpdateSerializers(serializers.ModelSerializer):
    class Meta:
        model = BarberService
        fields = ['price']

class AdminTimeSlotStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ['status']

class WorkingHourBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkingHourBase
        fields = ['weekday','start_time','end_time','is_off']

    def validate(self,attrs):
        is_off = attrs.get("is_off",False)
        start_time = attrs.get("start_time")
        end_time = attrs.get("end_time")

        if is_off :
            if start_time is not None or end_time is not None:
                raise serializers.ValidationError(
                    "برای روز تعطیل نباید ساعت شروع و پایان وارد شود."
                )
        else:
            if start_time is None or end_time is None:
                raise serializers.ValidationError(
                    "برای روز کاری باید ساعت شروع و پایان مشخص شود."
                )
            if start_time >= end_time:
                raise serializers.ValidationError(
                    "ساعت پایان باید بعد از ساعت شروع باشد."
                )
        return attrs

    def validate_weekday(self,value):
        if value < 0 or value > 6:
            raise serializers.ValidationError(
            "weekday باید بین 0 تا 6 باشد."
            )
        return value

class WorkingHourWeeklySerializer(serializers.Serializer):
    barber = serializers.PrimaryKeyRelatedField(queryset=Barber.objects.all())
    working_hours = WorkingHourBaseSerializer(many=True)

    def validate_working_hours(self,value):
        weekdays  = [item['weekday'] for item in value]
        if len(weekdays) != len(set(weekdays)):
            raise serializers.ValidationError(
                "برای یک روز نمی‌توان بیشتر از یک برنامه ثبت کرد."
            )
        return value
    @transaction.atomic
    def create(self, validated_data):
        barber = validated_data['barber']
        working_hours = validated_data['working_hours']

        for working_hour in working_hours:
            WorkingHourBase.objects.update_or_create(
                barber = barber,
                weekday = working_hour['weekday'],
                defaults={
                    "start_time":working_hour['start_time'],
                    "end_time":working_hour['end_time'],
                    "is_off":working_hour['is_off']
                }
            )
        return validated_data

class WeeklyPlanSerializer(serializers.ModelSerializer):
    slots = TimeSlotSerializer(many=True , read_only=True)
    class Meta:
        model = WeeklyPlan
        fields = ['id','date','start_time','end_time','status','slots']

# serializer for create manager

class CreateManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','password']
        extra_kwargs = {
            "password": {"write_only":True}
        }

    def create(self, validated_data):
        user=User.objects.create_user(
            username = validated_data['username'],
            password = validated_data['password']
        )

        group = Group.objects.get(name = "Barbershop manager")
        user.groups.add(group)

        return user
