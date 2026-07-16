from django.shortcuts import render
from dashboard.services.ai_service import AIService



def ai_summary_widget(request):

    context = {

        "summary":

            AIService().dashboard_summary()

    }

    return render(

        request, "dashboard/widgets/ai_summary.html", context,

    )

def ai_cluster_widget(request):
    return render(
        request,
        "dashboard/widgets/ai_cluster.html",
    )


def ai_recommendation_widget(request):
    return render(
        request,
        "dashboard/widgets/ai_recommendations.html",
    )