from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings


class CustomAccountAdapter(DefaultAccountAdapter):
    """
    Custom account adapter for django-allauth
    Handles user creation and role assignment
    """
    
    def save_user(self, request, user, form, commit=True):
        """
        Save the user with default role
        """
        user = super().save_user(request, user, form, commit=False)
        
        # Set default role to CITIZEN if not set
        if not user.role:
            user.role = 'CITIZEN'
        
        if commit:
            user.save()
        
        return user
    
    def is_open_for_signup(self, request):
        """
        Whether signup is allowed
        """
        return getattr(settings, 'ACCOUNT_ALLOW_REGISTRATION', True)


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Custom social account adapter for future OAuth integration
    """
    
    def pre_social_login(self, request, sociallogin):
        """
        Handle pre-social login logic
        """
        # Future: Link social accounts to existing users
        pass
