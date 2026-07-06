from django.shortcuts import render


def security_center_widget(request):
    return render(
        request,
        "dashboard/widgets/security_center.html",
    )


def api_health_widget(request):
    return render(
        request,
        "dashboard/widgets/api_health.html",
    )


def system_alert_widget(request):
    return render(
        request,
        "dashboard/widgets/system_alert.html",
    )


def global_audit_widget(request):
    return render(
        request,
        "dashboard/widgets/global_audit.html",
    )


def feature_flag_widget(request):
    return render(
        request,
        "dashboard/widgets/feature_flags.html",
    )