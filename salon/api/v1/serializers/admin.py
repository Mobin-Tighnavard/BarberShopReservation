import re
from rest_framework import serializers
from ....models import Barber
class CreateBarberSerializers(serializers.ModelSerializer):
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
    # validate_national_code
        return value