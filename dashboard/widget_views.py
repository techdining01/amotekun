from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from dashboard.services.dashboard_service import DashboardService


@login_required
def statistics_widget(request):

    service = DashboardService(request.user)

    context = {

        "stats": service.statistics.admin()

    }

    return render(

        request,

        "dashboard/widgets/statistics.html",

        context,

    )


@login_required
def activity_widget(request):

    service = DashboardService(request.user)

    return render(

        request,

        "dashboard/widgets/activity.html",

        {

            "activities":

                service.activity.admin()

        },

    )

@login_required
def map_widget(request):

    service = DashboardService(

        request.user

    )

    return render(

        request,

        "dashboard/widgets/map.html",

        {

            "layers":

                service.map.map_payload()

        },

    )


@login_required
def responder_widget(request):

    service = DashboardService(

        request.user

    )

    return render(

        request,

        "dashboard/widgets/responder_summary.html",

        service.responder(),

    )

