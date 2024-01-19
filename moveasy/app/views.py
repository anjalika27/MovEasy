from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from app.models import *

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
            b.seats_available-=1
            person=Person.objects.create(username=temp['name'],age=temp['age'],gender=temp['gender'],email=request.user.email,bus_id=b)
            person.save()
            b.save()
            print('booking done')
            return HttpResponse(f"<h1>Sent mail {request.user.email} for booking</h1>")
        else:
            return HttpResponse("<h1>No seats available</h1>")
    

def mybookings(request):
    if request.user.is_authenticated:
        p=Person.objects.filter(email=request.user.email)
        return render(request,'mybookings.html',context={'person':p})

    else:
        return HttpResponse('<h1>User not authenticated</h1>')