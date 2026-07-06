from django.shortcuts import render


def recent_incidents_widget(request):
    return render(
        request,
        "dashboard/widgets/recent_incidents.html",
    )