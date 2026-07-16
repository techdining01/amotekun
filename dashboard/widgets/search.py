from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from accounts.models import User
from reports.models import Incident


@login_required
def search_global(request):
    query = request.GET.get("q", "").strip()
    results = {"users": [], "incidents": []}

    if len(query) >= 2:
        results["users"] = User.objects.filter(
            Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(email__icontains=query)
            | Q(username__icontains=query)
        ).only("id", "first_name", "last_name", "email", "role", "status")[:10]

        results["incidents"] = Incident.objects.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(state__icontains=query)
            | Q(lga__icontains=query)
        ).only("id", "title", "report_type", "status", "priority", "created_at")[:10]

    return render(
        request,
        "dashboard/widgets/search_results.html",
        {"query": query, "results": results},
    )