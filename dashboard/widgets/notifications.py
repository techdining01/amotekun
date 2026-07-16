from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from notifications.models import Notification


@login_required
def notification_list(request):
    qs = Notification.objects.filter(recipient=request.user).order_by("-created_at")
    unread_count = qs.filter(is_read=False).count()
    notifications = qs[:50]
    return render(request, "dashboard/widgets/notification_list.html", {
        "notifications": notifications,
        "unread_count": unread_count,
    })


@login_required
def mark_all_read(request):
    if request.method == "POST":
        Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
    qs = Notification.objects.filter(recipient=request.user).order_by("-created_at")[:50]
    return render(request, "dashboard/widgets/notification_items.html", {
        "notifications": qs,
        "unread_count": 0,
    })


@login_required
def clear_all_notifications(request):
    if request.method == "POST":
        Notification.objects.filter(recipient=request.user).delete()
    # Return only the empty-state inner content so hx-swap="innerHTML" on #notification-list works
    empty_html = '''
        <div class="text-center py-10 text-slate-400">
            <div class="text-3xl mb-2">&#x1F514;</div>
            <p class="text-sm">No notifications</p>
        </div>
    '''
    from django.http import HttpResponse
    return HttpResponse(empty_html)
