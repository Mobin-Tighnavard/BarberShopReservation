from django.db import models
from django.core.validators import RegexValidator


def phone_validator():
    validator = RegexValidator(regex=r'^09\d{9}$',
                                    message="Enter a valid 11-digit phone number starting with 09",
                                    code="invalid_phone")
    return validator
def national_code_validator():
    validator = RegexValidator(regex=r'^\d{10}$',
                               message="national code must be 10 digit",
                               code="invalid_national_code")
    return validator

class Barber(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=11,validators=[phone_validator()],unique=True)
    national_code = models.CharField(max_length=10,validators=[national_code_validator()],unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.first_name +" " + self.last_name


# Create your models here.
class Service(models.Model):
    name = models.CharField(max_length=50,unique=True)
    def __str__(self):
        return self.name