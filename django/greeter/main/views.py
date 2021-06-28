from django.shortcuts import render
from .models import User


def index(response):
    data = {}
    try:
        last_user = list(User.objects.all())[-1]
        data["entries"] = list(User.objects.all())[::-1]
        data["first_name"] = last_user.first_name
        data["last_name"] = last_user.last_name
    except IndexError:
        data["first_name"] = "unknown"
        data["last_name"] = "unknown"
        last_user = "unknown"

    if response.method == "POST":
        first_name = response.POST["first_name"]
        last_name = response.POST["last_name"]

        new_user = User(first_name=first_name, last_name=last_name)
        if last_user not in list(User.objects.all()):
            new_user.save()
            data["first_name"] = first_name
            data["last_name"] = last_name
            data["entries"] = list(User.objects.all())[::-1] or ["empty"]
        print(list(User.objects.all()))

    return render(response, "index.html", data)
