import os
from rest_framework import serializers
from PIL import Image
from ....models import Payment

class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['reservation','receipt_image']

    def validate_receipt_image(self,value):
        # manage size
        max_size = 20 * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError(
                {"message" : "حجم عکس بیشتر از 20 مگابایت است" }
            )
        # manage format
        try:
            image = Image.open(value)
        except Exception:
            raise serializers.ValidationError(
                {"message" : "فایل ارسال شده یک تصویر معتبر نیست"}
            )
        # manage real image
        try:
            image.verify()
        except Exception:
            raise serializers.ValidationError(
                {"message" : "فایل تصویر معتبر نیست یا خراب است"}
            )
        # have to open image after user verify
        value.seek(0)
        image = Image.open(value)
        allowed_formats = ["JPEG","PNG","WEBP"]
        if image.format not in allowed_formats:
            raise serializers.ValidationError(
                {"message":"فرمت تصویر باید JPEG,PNG,WEBP باشد"}
            )
        extension = os.path.splitext(value.name)[1].lower()
        allowed_extension = [".jpg",".jpeg",".png",".webp"]
        if extension not in allowed_extension:
            raise serializers.ValidationError(
                {"message":"پسوند فایل باید jpeg. ,.jpg,.png,.webp"}
            )
        return value

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"