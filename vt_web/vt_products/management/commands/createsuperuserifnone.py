import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create a superuser if no users exist'

    def handle(self, *args, **kwargs):
        user = get_user_model()
        if not user.objects.exists():
            username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
            email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
            password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'adminpassword')
            user.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully'))
        else:
            self.stdout.write(self.style.SUCCESS('Users already exist, no superuser created'))