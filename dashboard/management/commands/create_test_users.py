from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings


User = get_user_model()


class Command(BaseCommand):
    help = "Create test users with all roles (citizen, officer, dispatcher, admin)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--password",
            type=str,
            default="TestPass123!",
            help="Password for all test users (default: TestPass123!)",
        )

    def handle(self, *args, **options):
        password = options["password"]

        # Define test users
        test_users = [
            {
                "username": "citizen",
                "email": "citizen@example.com",
                "role": User.ROLE_CHOICES[0][0],
            },
            {
                "username": "officer",
                "email": "officer@example.com",
                "role": User.ROLE_CHOICES[1][0],
            },
            {
                "username": "dispatcher",
                "email": "dispatcher@example.com",
                "role": User.ROLE_CHOICES[2][0],
            },
            {
                "username": "admin",
                "email": "admin@example.com",
                "role": User.ROLE_CHOICES[3][0],
            },
        ]

        created_count = 0
        existing_count = 0

        for user_data in test_users:
            user, created = User.objects.get_or_create(
                username=user_data["username"],
                defaults={
                    "email": user_data["email"],
                    "role": user_data["role"],
                },
            )

            if created:
                user.set_password(password)
                if user_data["role"] == User.ROLE_CHOICES[3][0]:  # Admin
                    user.is_staff = True
                    user.is_superuser = True
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created user: {user.username} (role: {user.get_role_display()})"
                    )
                )
                created_count += 1
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"User already exists: {user.username} (role: {user.get_role_display()})"
                    )
                )
                existing_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"\nDone! Created: {created_count}, Existing: {existing_count}"
            )
        )
        self.stdout.write(
            self.style.SUCCESS(f"All users have password: {password}")
        )
