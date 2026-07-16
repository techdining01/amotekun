from django.core.management.base import BaseCommand
from accounts.models import User
from accounts.choices import UserRole


class Command(BaseCommand):
    help = "Creates mock users for all roles except admin and super admin"

    def handle(self, *args, **options):
        roles = [
            UserRole.CITIZEN,
            UserRole.PATROL_OFFICER,
            UserRole.CCTV_OPERATOR,
            UserRole.DISPATCHER,
            UserRole.EMERGENCY_OPERATOR,
            UserRole.PATROL_SUPERVISOR,
            UserRole.STATE_COMMANDER,
            UserRole.LGA_COMMANDER,
            UserRole.STATION_COMMANDER,
            UserRole.RESPONDER,
            UserRole.ANALYST,
            UserRole.AGENCY_STAFF,
            UserRole.AUDITOR,
        ]

        for role in roles:
            username = role.lower().replace(" ", "_")
            email = f"{username}@example.com"

            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": email,
                    "first_name": role.title(),
                    "last_name": "User",
                    "role": role,
                    "is_active": True,
                    "email_verified": True,
                }
            )

            if created:
                user.set_password("password123")
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Created user: {username}"))
            else:
                self.stdout.write(f"User {username} already exists")

        self.stdout.write(self.style.SUCCESS("Successfully created mock users"))