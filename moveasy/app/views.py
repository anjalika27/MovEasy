from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from app.models import *
from django.core.mail import send_mail,EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from moveasy.settings import EMAIL_HOST_USER

# Create your views here.


def home(request):
    bus = Bus.objects.all()
    return render(request, "home.html", context={"bus": bus})


def registerform(request):
    if request.method == "POST":
        data = request.POST
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        user = User.objects.filter(username=username)

        if user.exists():
            return HttpResponse("<h1>User exists!</h1>")

        user = User.objects.create(username=username, email=email)
        user.set_password(password)
        user.save()

        return redirect("/login/")

    return render(request, "register.html")


def logoutform(request):
    logout(request)
    return redirect("/login/")


def loginform(request):
    if request.method == "POST":
        data = request.POST
        username = data.get("username")
        password = data.get("password")

        if not User.objects.filter(username=username).exists():
            return HttpResponse("<h1>Enter valid username</h1>")

        user = authenticate(username=username, password=password)

        if user is None:
            return HttpResponse("<h1>Enter valid password</h1>")

        else:
            login(request, user)  # session of user
            return redirect("/")

    return render(request, "login.html")


def bookingform(request):
    bus = Bus.objects.all()
    source = []
    destination = []

    for b in bus:
        source.append(b.source)
        destination.append(b.destination)

    source = list(set(source))
    destination = list(set(destination))

    if request.user.is_authenticated:
        return render(
            request,
            "bookingform.html",
            context={"source": source, "destination": destination},
        )
    else:
        return HttpResponse("<h1>User not authenticated</h1>")


temp = {}
def routes(request):
    global temp
    if request.user.is_authenticated:
        b = Bus.objects.filter(
            source=request.POST.get("source"),
            destination=request.POST.get("destination"),
        )

        if len(b) > 0:
            temp["name"] = request.POST["name"]
            temp["age"] = request.POST["age"]
            temp["gender"] = request.POST["gender"]

            return render(request, "routes.html", context={"bus": b})

        else:
            return HttpResponse("<h1>No routes available</h1>")

    else:
        return HttpResponse("<h1>User not authenticated</h1>")


def booking(request, bus_id):
    b = Bus.objects.get(pk=bus_id)
    if b.seats_available > 0:
        b.seats_available -= 1
        person = Person.objects.create(
            username=temp["name"],
            age=temp["age"],
            gender=temp["gender"],
            email=request.user.email,
            bus_id=b,
        )
        person.save()
        b.save()
        # print("booking done")
        # print(details.price,' ',details.source)
        id=bus_id
        name=temp['name']
        return redirect(f'/seats/{id}/{name}')


        # sending_email()

        # return HttpResponse(f"<h1>Sent mail {request.user.email} for booking</h1>")
    else:
        return HttpResponse("<h1>No seats available</h1>")




def seat_selection(request,id,name):
    bus=Bus.objects.get(pk=id)
    price=bus.price
    person=Person.objects.get(bus_id=id,username=name)
    # seat=Seats.objects.get(bus_number=id)
    # for i in 
    print(person.username)

    available_seats=Seats.objects.filter(bus_number=id)

    list_of_available_seats=[s.seat_number for s in available_seats]
    
    

    if request.method=='POST':

        selected_seat_ids=request.POST.getlist('selected_seats')
        print(selected_seat_ids)
        if not len(selected_seat_ids)>0:
            return HttpResponse('<h1>No seats chosen</h1>')
        

        number_of_tickets=len(selected_seat_ids)
        if number_of_tickets>5:
            return HttpResponse("<h1>Can't book more than 5 seats")
        
        total_price=price*number_of_tickets
        print(len(selected_seat_ids))
        
        for i in selected_seat_ids:
            s=Seats.objects.create(bus_number=person,seat_number=i,passenger_name=person.username,total_price=total_price)
            s.save()

        # print(s.bus_number,' ',s.passenger_name,s.total_price)

        

        return render(request,'summary_booking.html',{'person':person,'seat':number_of_tickets,'bus':bus,'total_price':total_price})

        # print('here ',total_price)


    lis=[1,2,3,4,5,6,7,8,9,10]
    return render(request,'seats.html',{'lis':lis,'price':price,'avail_seats':list_of_available_seats})



def summary(request):

    return render(request,'summary_booking.html')






def mybookings(request):
    if request.user.is_authenticated:
        p=Person.objects.filter(email=request.user.email)
        return render(request,'mybookings.html',context={'person':p})

    else:
        return HttpResponse('<h1>User not authenticated</h1>')








def sending_email(request,bus_id,name,price):

    person=Person.objects.get(username=name,bus_id=bus_id)
    bus=Bus.objects.get(pk=bus_id)
    # price=bus.price
    print(person.username,' ',person.bus_id,' ',)
    source=bus.source
    destination=bus.destination
    departure=bus.time
    arrival=bus.time
    date=person.date_and_time_of_booking.date()
    name=person.username

    print(person.username,' ',price)
    subject = "Bus Ticket Booking"

    html_message=render_to_string('email.html',{'source':source,'destination':destination,'departure':departure,'arrival':arrival,'price':price,'date':date,'name':name})
    plain_message=strip_tags(html_message)

    message = EmailMultiAlternatives(
        subject=subject,
        body=plain_message,
        from_email=EMAIL_HOST_USER,
        to = ["bt21ece095@iiitn.ac.in"]   
    )

    message.attach_alternative(html_message,'text/html')
    message.send()

    return HttpResponse(f"<h1>Sent mail {request.user.email} for booking</h1>")
    
    # send_mail(subject, message, from_email, to_email)




def cancel_ticket(request,id):
    person=Person.objects.get(pk=id)
    bus=person.bus_id
    bus.seats_available+=1
    bus.save()
    person.delete()
    return HttpResponse('<h1>Ticket is cancelled successfully</h1>')