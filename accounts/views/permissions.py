from rest_framework.permissions import BasePermission

class HasRole(BasePermission):

    allowed_roles = []

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        return request.user.role in self.allowed_roles


class IsSuperAdmin(HasRole):

    allowed_roles = [
        "SUPER_ADMIN",
    ]

class IsPlatformAdmin(HasRole):

    allowed_roles = [
        "SUPER_ADMIN",
        "PLATFORM_ADMIN",
    ]

class IsCommander(HasRole):

    allowed_roles = [

        "STATE_COMMANDER",

        "LGA_COMMANDER",

        "STATION_COMMANDER",

    ]

class IsDispatcher(HasRole):

    allowed_roles = [

        "DISPATCHER",

        "STATE_COMMANDER",

        "STATION_COMMANDER",

    ]

class IsPatrolOfficer(HasRole):

    allowed_roles = [

        "PATROL_OFFICER",

        "PATROL_SUPERVISOR",

    ]



class IsResponder(BasePermission):
    def has_permission(self, request, view):
        return has_role(request.user, "RESPONDER")
        

class IsCCTVOperator(HasRole):

    allowed_roles = [

        "CCTV_OPERATOR",

        "PLATFORM_ADMIN",

    ]

class IsAnalyst(HasRole):

    allowed_roles = [

        "ANALYST",

        "PLATFORM_ADMIN",

    ]

class IsCitizen(HasRole):

    allowed_roles = [

        "STATE_COMMANDER",

        "LGA_COMMANDER",

        "STATION_COMMANDER",

        "RESPONDER",

    ]

class IsAgencyStaff(HasRole):

    allowed_roles = [

        "RESPONDER",

        "PATROL_OFFICER",

        "PATROL_SUPERVISOR",

        "DISPATCHER",

        "STATION_COMMANDER",

        "LGA_COMMANDER",

        "STATE_COMMANDER",

        "ANALYST",

        "CCTV_OPERATOR",

    ]

class IsStaffMember(BasePermission):

    def has_permission(self, request, view):

        return (

            request.user.is_authenticated

            and request.user.is_staff

        )


class IsVerified(BasePermission):

    def has_permission(self, request, view):

        return (

            request.user.is_authenticated

            and request.user.verification_status == "VERIFIED"

        )


class IsActiveUser(BasePermission):

    def has_permission(self, request, view):

        return (

            request.user.is_authenticated

            and request.user.status == "ACTIVE"

        )

class IsAvailableResponder(BasePermission):

    def has_permission(self, request, view):

        if not request.user.is_authenticated:

            return False

        try:

            return (

                request.user.responder_status.availability

                == "AVAILABLE"

            )

        except Exception:

            return False


class CanManageIncident(BasePermission):

    def has_permission(self, request, view):

        return request.user.role in [

            "SUPER_ADMIN",

            "PLATFORM_ADMIN",

            "STATE_COMMANDER",

            "LGA_COMMANDER",

            "STATION_COMMANDER",

            "DISPATCHER",

        ]


class CanCloseIncident(BasePermission):

    def has_permission(self, request, view):

        return request.user.role in [

            "SUPER_ADMIN",

            "PLATFORM_ADMIN",

            "STATE_COMMANDER",

            "LGA_COMMANDER",

        ]

class CanViewAnalytics(BasePermission):

    def has_permission(self, request, view):

        return request.user.role in [

            "SUPER_ADMIN",

            "PLATFORM_ADMIN",

            "STATE_COMMANDER",

            "ANALYST",

        ]

class CanUseAI(BasePermission):

    def has_permission(self, request, view):

        return (

            request.user.is_authenticated

            and request.user.ai_enabled

        )

class CanViewCCTV(BasePermission):

    def has_permission(self, request, view):

        return request.user.role in [

            "SUPER_ADMIN",

            "PLATFORM_ADMIN",

            "CCTV_OPERATOR",

            "STATE_COMMANDER",

            "LGA_COMMANDER",

        ]

class CanDispatchPatrol(BasePermission):

    def has_permission(self, request, view):

        return request.user.role in [

            "DISPATCHER",

            "STATION_COMMANDER",

            "STATE_COMMANDER",

        ]

class CanApproveReport(BasePermission):

    def has_permission(self, request, view):

        return request.user.role in [

            "PLATFORM_ADMIN",

            "STATE_COMMANDER",

            "LGA_COMMANDER",

        ]

    
def has_role(user, role_code):
        return (
            user.is_authenticated and
            user.roles.filter(code=role_code).exists()
        )
