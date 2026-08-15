import re
from rest_framework import serializers
from ....models import Barber , Service , BarberService , TimeSlot
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