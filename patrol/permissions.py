from rest_framework.permissions import BasePermission, SAFE_METHODS

class PatrolPermission(BasePermission):

    def is_super_admin(self, user):

        return getattr(user, "is_super_admin", False)

    def is_platform_admin(self, user):

        return getattr(user, "is_platform_admin", False)

    def is_dispatcher(self, user):

        return getattr(user, "is_dispatcher", False)

    def is_commander(self, user):

        return getattr(user, "is_patrol_commander", False)

    def is_responder(self, user):

        return getattr(user, "is_responder", False)

    def is_analyst(self, user):

        return getattr(user, "is_analyst", False)


class PatrolReadOnly(PatrolPermission):

    def has_permission(self, request, view):

        return request.method in SAFE_METHODS

class IsPatrolCommander(PatrolPermission):

    def has_permission(self, request, view):

        if not request.user.is_authenticated:

            return False

        return (

            self.is_super_admin(request.user)

            or

            self.is_platform_admin(request.user)

            or

            self.is_commander(request.user)
        )
            
            
class IsDispatcher(PatrolPermission):

    def has_permission(self, request, view):

        if not request.user.is_authenticated:

            return False

        return (

            self.is_dispatcher(request.user)

            or

            self.is_platform_admin(request.user)

            or

            self.is_super_admin(request.user)

        )


class IsResponder(PatrolPermission):

    def has_permission(self, request, view):

        if not request.user.is_authenticated:

            return False

        return (

            self.is_responder(request.user)

            or

            self.is_commander(request.user)

            or

            self.is_platform_admin(request.user)

            or

            self.is_super_admin(request.user)

        )


class IsAnalyst(PatrolPermission):

    def has_permission(self, request, view):

        if not request.user.is_authenticated:

            return False

        return (

            self.is_analyst(request.user)

            or

            self.is_platform_admin(request.user)

            or

            self.is_super_admin(request.user)

        )


class CanManageVehicles(PatrolPermission):

    def has_permission(self, request, view):

        if not request.user.is_authenticated:

            return False

        return (

            self.is_commander(request.user)

            or

            self.is_platform_admin(request.user)

            or

            self.is_super_admin(request.user)

        )


class CanManageEquipment(PatrolPermission):

    def has_permission(self, request, view):

        if not request.user.is_authenticated:

            return False

        return (

            self.is_commander(request.user)

            or

            self.is_platform_admin(request.user)

            or

            self.is_super_admin(request.user)

        )


class MissionPermission(PatrolPermission):

    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:

            return True

        return (

            self.is_dispatcher(request.user)

            or

            self.is_commander(request.user)

            or

            self.is_platform_admin(request.user)

            or

            self.is_super_admin(request.user)

        )


class GPSPermission(PatrolPermission):

    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:

            return True

        return (

            self.is_responder(request.user)

            or

            self.is_commander(request.user)

            or

            self.is_super_admin(request.user)

        )


class IsAssignedMission(PatrolPermission):

    def has_object_permission(

        self,

        request,

        view,

        obj,

    ):

        if self.is_super_admin(request.user):

            return True

        if self.is_commander(request.user):

            return True

        return obj.patrol_team.memberships.filter(

            personnel__user=request.user

        ).exists()
   

