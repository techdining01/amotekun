from django.shortcuts import render


def state_performance_widget(request):
    return render(
        request,
        "dashboard/widgets/state_performance.html",
    )


def lga_performance_widget(request):
    return render(
        request,
        "dashboard/widgets/lga_performance.html",
    )


def national_hotspot_widget(request):
    return render(
        request,
        "dashboard/widgets/national_hotspot.html",
    )


def live_platform_activity(request):
    return render(
        request,
        "dashboard/widgets/live_platform_activity.html",
    )