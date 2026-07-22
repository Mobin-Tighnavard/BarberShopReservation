from django.db import models
from salon.models import phone_validator

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=11 , validators=[phone_validator()],unique=True)
    def __str__(self):
        return self.first_name + " " + self.last_name

# Create your models here.
