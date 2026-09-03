from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from ...models import Customer
import re

class CreateCustomerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id','first_name','last_name','phone_number']
        # extra_kwargs={
        #     "phone_number":{
        #         "validators":[]
        #     }
        # }

    def validate_first_name(self, value):
        if not re.match(r"^[آ-ی\s]+$", value):
            raise serializers.ValidationError(
                "نام باید فقط شامل حروف فارسی باشد"
            )
        return value

    def validate_last_name(self, value):
        if not re.match(r"^[آ-ی\s]+$", value):
            raise serializers.ValidationError(
                "نام خانوادگی باید فقط شامل حروف فارسی باشد"
            )
        return value

    def validate_phone_number(self, value):
        if not re.match(r"^09\d{9}$", value):
            raise serializers.ValidationError(
                "شماره تلفن باید 11 رقم و با 09 شروع شود"
            )
        return value

    # def validate(self, attrs):
    #     phone_number = attrs["phone_number"]
    #     first_name = attrs["first_name"]
    #     last_name = attrs["last_name"]
    #
    #     customer = Customer.objects.filter(phone_number = phone_number).first()
    #
    #     if customer:
    #         if customer.first_name != first_name or customer.last_name != last_name:
    #             raise serializers.ValidationError({"message":"این شماره با نام و فامیلی دیگر قبلا مراجعه کرده"})
    #     return attrs

    def create(self, validated_data):
        customer,created=Customer.objects.get_or_create(
            phone_number = validated_data['phone_number'],
            defaults={
                "first_name":validated_data['first_name'],
                "last_name":validated_data['last_name']
            }
        )
        return customer

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        try:
            token = RefreshToken(attrs['refresh'])
            token.blacklist()
        except Exception:
            raise serializers.ValidationError(
                "invalid or expired refresh token."
            )
        return attrs

