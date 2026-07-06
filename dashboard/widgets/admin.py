from django.shortcuts import render


def admin_stats_widget(request):
    return render(
        request,
        "dashboard/widgets/admin_stats.html",
    )


def live_activity_widget(request):
    return render(
        request,
        "dashboard/widgets/live_activity.html",
    )