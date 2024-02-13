from django.db import models

# Create your models here.

class Bus(models.Model):
    source=models.CharField(max_length=20)
    destination=models.CharField(max_length=20)
    time=models.TimeField(auto_now=False,auto_now_add=False)
    # date=models.DateField(auto_now=False,auto_now_add=False)
    price=models.IntegerField()
    seats_available=models.IntegerField()



class Person(models.Model):
    username=models.CharField(max_length=30)
    age=models.IntegerField()
    gender=models.CharField(max_length=10)
    email=models.EmailField()
    date_and_time_of_booking=models.DateTimeField(auto_now_add=True)
    bus_id=models.ForeignKey('Bus',on_delete=models.CASCADE)


class Seats(models.Model):
    bus_number=models.ForeignKey('Person',on_delete=models.CASCADE)
    seat_number=models.CharField(max_length=5)
    passenger_name=models.CharField(max_length=30)
    total_price=models.IntegerField()


#     date=models.DateField(auto_now=False,auto_now_add=False)

