from django.shortcuts import render


def notification_list(request):
    return render(
        request,
        "dashboard/widgets/notification_list.html",
    )