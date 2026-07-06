from django.shortcuts import render


def dashboard_map(request):
    return render(
        request,
        "dashboard/widgets/dashboard_map.html",
    )