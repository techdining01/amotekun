from django.shortcuts import render


def search_global(request):
    query = request.GET.get("q", "")

    return render(
        request,
        "dashboard/widgets/search_results.html",
        {
            "query": query,
        },
    )