from django.shortcuts import render


def patrol_status_widget(request):
    return render(
        request,
        "dashboard/widgets/patrol_status.html",
    )