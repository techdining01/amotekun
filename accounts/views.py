from django.contrib.auth import logout
from django.shortcuts import redirect, render


def custom_logout(request):
    if request.method == "POST":
        logout(request)
        return redirect("account_logged_out")
    return render(request, "account/logout.html")


def logged_out(request):
    return render(request, "account/logged_out.html")
