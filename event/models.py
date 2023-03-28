from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # id=models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phoneNumber = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    username = models.CharField(max_length=20,unique=True)
    password=models.CharField(max_length=150)
    eventBooked=models.ManyToManyField('Event',null=True,blank=True)
    isAdmin=models.BooleanField(default=False)

class Event(models.Model):
    SHOWS_CHOICES = (
        ("1", "1st"),   ("2", "2nd"),   ("3", "3rd"),   ("4", "4th"),
    )
    name=models.CharField(max_length=20)
    capacity = models.IntegerField()
    shows=models.CharField(max_length = 20,choices = SHOWS_CHOICES,default = '1st')
    price=models.DecimalField(max_digits=6, decimal_places=2)
    startTime=models.TimeField(null=True,blank=True,auto_now=False, auto_now_add=False)
    endTime=models.TimeField(null=True,blank=True,auto_now=False, auto_now_add=False)
    def __str__(self):
        return self.name + self.shows
    # issuedTo=models.ForeignKey('Student', on_delete=models.CASCADE,null=True,blank=True)
