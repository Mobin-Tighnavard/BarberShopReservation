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
    delete_flag = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class BarberService(models.Model):
    barber = models.ForeignKey(Barber,on_delete=models.CASCADE,related_name="barber_service")
    service = models.ForeignKey(Service,on_delete=models.CASCADE,related_name="barber_service")
    price = models.PositiveIntegerField()
    delete_flag = models.BooleanField(default=False)

    def __str__(self):
        return self.barber.first_name + " " + self.barber.last_name +"/"+ self.service.name + "/"+ str(self.price)



class TimeSlot(models.Model):
    class TimeSlotStatus(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        OFF = "OFF", 'Off'
        FULL = "FULL", "Full"
    barber = models.ForeignKey(
        Barber,
        on_delete=models.PROTECT,
        related_name="time_slots"
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=10,choices=TimeSlotStatus.choices,default=TimeSlotStatus.ACTIVE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["barber", "date" ,"start_time" ],
                name="unique_barber_date_start_time"
            )
        ]

class WorkingHourBase(models.Model):
    barber = models.ForeignKey(Barber,on_delete=models.PROTECT,related_name="barber_working_hour")
    weekday = models.IntegerField()
    start_time = models.TimeField(null=True , blank=True)
    end_time = models.TimeField(null=True , blank=True)
    is_off = models.BooleanField(default=False)

    class Meta :
        constraints = [
            models.UniqueConstraint(
                fields=["barber","weekday"],
                name = "unique_barber_weekday"
            )
        ]

class AboutUs(models.Model):
    address = models.TextField()
    Phone_number = models.CharField(max_length=11,validators=[phone_validator()],unique=True)