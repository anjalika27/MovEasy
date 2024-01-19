from django.db import models

# Create your models here.

class Bus(models.Model):
    source=models.CharField(max_length=20)
    destination=models.CharField(max_length=20)
    time=models.TimeField(auto_now=False,auto_now_add=False)
    price=models.IntegerField()
    seats_available=models.IntegerField()



class Person(models.Model):
    username=models.CharField(max_length=30)
    age=models.IntegerField()
    gender=models.CharField(max_length=10)
    email=models.EmailField()
    date_and_time_of_booking=models.DateTimeField(auto_now_add=True)
    bus_id=models.ForeignKey('Bus',on_delete=models.CASCADE)

