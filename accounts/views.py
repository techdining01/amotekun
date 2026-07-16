from django.views.generic import TemplateView


class DashboardBaseView(TemplateView):

    role_display = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["role_display"] = self.role_display
        return context


class AdminDashboardView(DashboardBaseView):
    template_name = "dashboard/admin_dashboard.html"
    role_display = "Administrator"


class SuperAdminDashboardView(DashboardBaseView):
    template_name = "dashboard/super_admin_dashboard.html"
    role_display = "Super Administrator"


class PoliceDashboardView(DashboardBaseView):
    template_name = "dashboard/police_dashboard.html"
    role_display = "Police Command"


class AmotekunDashboardView(DashboardBaseView):
    template_name = "dashboard/amotekun_dashboard.html"
    role_display = "Amotekun Command"


class DispatcherDashboardView(DashboardBaseView):
    template_name = "dashboard/dispatcher_dashboard.html"
    role_display = "Dispatcher"


class AnalystDashboardView(DashboardBaseView):
    template_name = "dashboard/analyst_dashboard.html"
    role_display = "Intelligence Analyst"


class FacilityDashboardView(DashboardBaseView):
    template_name = "dashboard/facility_dashboard.html"
    role_display = "Emergency Facility"


class CitizenDashboardView(DashboardBaseView):
    template_name = "dashboard/citizen_dashboard.html"
    role_display = "Citizen"


class ResponderDashboardView(DashboardBaseView):
    template_name = "dashboard/responder_dashboard.html"
    role_display = "Emergency Responder"


class AIDashboardView(DashboardBaseView):
    template_name = "dashboard/ai_dashboard.html"
    role_display = "AI Operations"


class AuditorDashboardView(DashboardBaseView):
    template_name = "dashboard/auditor_dashboard.html"
    role_display = "System Auditor"
