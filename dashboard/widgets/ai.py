from django.shortcuts import render


def ai_summary_widget(request):
    return render(
        request,
        "dashboard/widgets/ai_summary.html",
    )


def ai_cluster_widget(request):
    return render(
        request,
        "dashboard/widgets/ai_cluster.html",
    )


def ai_recommendation_widget(request):
    return render(
        request,
        "dashboard/widgets/ai_recommendation.html",
    )