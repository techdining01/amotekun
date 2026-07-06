from django.shortcuts import render


def traffic_widget(request):
    return render(
        request,
        "dashboard/widgets/traffic.html",
    )