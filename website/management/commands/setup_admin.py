from __future__ import annotations

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create or update a Django superuser (idempotent)."

    def add_arguments(self, parser):
        parser.add_argument('--username', required=True)
        parser.add_argument('--password', required=True)
        parser.add_argument('--name', required=True)
        parser.add_argument('--email', default='')

    def handle(self, *args, **options):
        username: str = options['username']
        password: str = options['password']
        name: str = options['name']
        email: str = options.get('email') or ''

        User = get_user_model()

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
            },
        )

        # Always ensure admin flags are set.
        user.is_staff = True
        user.is_superuser = True
        if hasattr(user, 'is_active'):
            user.is_active = True

        # Update profile-ish fields if the User model supports them.
        if email and hasattr(user, 'email'):
            user.email = email
        if hasattr(user, 'first_name'):
            user.first_name = name
        if hasattr(user, 'last_name'):
            user.last_name = ''

        user.set_password(password)
        user.save()

        action = 'Created' if created else 'Updated'
        self.stdout.write(self.style.SUCCESS(f"{action} superuser '{username}'."))
