from django.contrib.auth import login, logout
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Agency,
)

from .serializers import (
    AgencySerializer,
    AssignRoleSerializer,
    ChangePasswordSerializer,
    LoginSerializer,
    NotificationPreferenceSerializer,
    OnlineUserSerializer,
    RegistrationSerializer,
    ResetPasswordSerializer,
    UpdateProfileSerializer,
    UserDetailSerializer,
    UserListSerializer,
)

from .permissions import (
    IsPlatformAdmin,
)

from .managers import (
    AccountManager,
    DashboardManager,
    NotificationManager,
    ProfileManager,
    UserManager,
)


class AgencyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Agency.objects.all()

    serializer_class = AgencySerializer

    permission_classes = [
        IsAuthenticated,
    ]


class UserViewSet(viewsets.ViewSet):
    permission_classes = [
        IsAuthenticated,
    ]

    def list(self, request):

        users = UserManager.responders()

        serializer = UserListSerializer(
            users,
            many=True,
        )

        return Response(
            serializer.data,
        )

    def retrieve(self, request, pk=None):

        user = UserManager.by_id(pk)

        serializer = UserDetailSerializer(user)

        return Response(
            serializer.data,
        )

    @action(
        detail=False,
        methods=["get"],
    )
    def me(self, request):

        serializer = UserDetailSerializer(
            request.user,
        )

        return Response(
            serializer.data,
        )

    @action(
        detail=False,
        methods=["get"],
    )
    def online(self, request):

        users = UserManager.responders()

        serializer = OnlineUserSerializer(
            users,
            many=True,
        )

        return Response(
            serializer.data,
        )

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsPlatformAdmin],
    )
    def assign_role(self, request, pk=None):

        serializer = AssignRoleSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        user = UserManager.by_id(pk)

        AccountManager.assign_role(
            user,
            serializer.validated_data["role"],
            serializer.validated_data,
        )

        return Response({"detail": "Role assigned."})


class RegisterAPIView(APIView):
    permission_classes = [
        AllowAny,
    ]

    def post(self, request):

        serializer = RegistrationSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        user = AccountManager.register_user(
            serializer.validated_data,
        )

        return Response(
            UserDetailSerializer(user).data,
            status=status.HTTP_201_CREATED,
        )


class LoginAPIView(APIView):
    permission_classes = [
        AllowAny,
    ]

    def post(self, request):

        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(
            raise_exception=True,
        )

        from .services import AuthenticationService

        user = AuthenticationService.login(
            request,
            serializer.validated_data["email"],
            serializer.validated_data["password"],
        )

        if user is None:
            return Response(
                {"detail": "Invalid credentials."},
                status=400,
            )

        login(request, user)

        return Response({"redirect": DashboardManager.dashboard_url(user)})


class LogoutAPIView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request):

        logout(request)

        return Response({"detail": "Logged out."})


class ProfileAPIView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):

        serializer = UserDetailSerializer(
            request.user,
        )

        return Response(
            serializer.data,
        )

    def put(self, request):

        serializer = UpdateProfileSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        profile = ProfileManager.update(
            request.user,
            serializer.validated_data,
        )

        return Response(
            UpdateProfileSerializer(
                profile,
            ).data
        )


class NotificationPreferenceAPIView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(
        self,
        request,
    ):

        serializer = NotificationPreferenceSerializer(
            request.user.notification_preferences,
        )

        return Response(
            serializer.data,
        )

    def put(
        self,
        request,
    ):

        preferences = NotificationManager.update_preferences(
            request.user,
            **request.data,
        )

        return Response(
            NotificationPreferenceSerializer(
                preferences,
            ).data
        )


class ChangePasswordAPIView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def post(
        self,
        request,
    ):

        serializer = ChangePasswordSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        user = request.user

        if not user.check_password(
            serializer.validated_data["old_password"],
        ):
            return Response(
                {"detail": "Old password is incorrect."},
                status=400,
            )

        user.set_password(
            serializer.validated_data["new_password"],
        )

        user.save()

        return Response({"detail": "Password updated successfully."})


class ResetPasswordAPIView(APIView):
    permission_classes = [
        AllowAny,
    ]

    def post(
        self,
        request,
    ):

        serializer = ResetPasswordSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        return Response({"detail": "Password reset email queued."})
