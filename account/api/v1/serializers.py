from rest_framework import serializers
from ...models import Customer

class CreateCustomerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['first_name','last_name','phone_number']
        extra_kwargs={
            "phone_number":{
                "validators":[]
            }
        }
    def validate(self, attrs):
        phone_number = attrs["phone_number"]
        first_name = attrs["first_name"]
        last_name = attrs["last_name"]

        customer = Customer.objects.filter(phone_number = phone_number).first()

        if customer:
            if customer.first_name != first_name or customer.last_name != last_name:
                raise serializers.ValidationError({"message":"this phone number already exist with another first and last name"})
        return attrs

    def create(self, validated_data):
        customer,created=Customer.objects.get_or_create(
            phone_number = validated_data['phone_number'],
            defaults={
                "first_name":validated_data['first_name'],
                "last_name":validated_data['last_name']
            }
        )
        return customer
