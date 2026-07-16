from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, Agency, UserProfile, PersonnelAssignment,
    NotificationPreference, ResponderStatus, EmergencyContact,
    UserDevice, UserAuditLog,
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'username', 'first_name', 'last_name', 'role', 'status', 'is_staff', 'is_active']
    list_filter = ['role', 'status', 'verification_status', 'is_staff', 'is_active']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['first_name']
    readonly_fields = ['created_at', 'updated_at', 'last_seen']

    # Fully explicit fieldsets — BaseUserAdmin.fieldsets includes 'date_joined'
    # which does not exist on this custom model, so we override completely.
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'middle_name', 'gender', 'date_of_birth', 'phone_number', 'avatar')}),
        ('Role & Status', {'fields': ('role', 'status', 'verification_status', 'email_verified', 'phone_verified')}),
        ('Location', {'fields': ('state', 'lga', 'ward')}),
        ('Preferences', {'fields': ('language', 'timezone', 'dark_mode', 'ai_enabled', 'notification_enabled')}),
        ('Security', {'fields': ('last_login_ip', 'failed_login_attempts', 'last_seen')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'role', 'password1', 'password2'),
        }),
    )


@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    list_display = ['name', 'agency_type', 'is_active', 'created_at']
    list_filter = ['agency_type', 'is_active']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(PersonnelAssignment)
class PersonnelAssignmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'agency', 'role', 'badge_number', 'is_primary', 'started_at']
    list_filter = ['agency', 'role', 'is_primary']
    search_fields = ['user__email', 'badge_number', 'employee_id']


@admin.register(UserAuditLog)
class UserAuditLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'ip_address', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__email', 'action']
    readonly_fields = ['created_at']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'occupation', 'nationality']
    search_fields = ['user__email', 'user__username']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'email', 'sms', 'push', 'in_app']
    search_fields = ['user__email']


@admin.register(ResponderStatus)
class ResponderStatusAdmin(admin.ModelAdmin):
    list_display = ['responder', 'availability', 'updated_at']
    list_filter = ['availability']
    search_fields = ['responder__email']


@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'phone_number', 'relationship', 'is_primary']
    search_fields = ['user__email', 'full_name']


@admin.register(UserDevice)
class UserDeviceAdmin(admin.ModelAdmin):
    list_display = ['user', 'device_name', 'platform', 'last_seen']
    search_fields = ['user__email', 'device_name']
