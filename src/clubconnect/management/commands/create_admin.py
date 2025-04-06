from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from clubconnect.models import AdminProfile

class Command(BaseCommand):
    help = 'Creates a site admin user'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Admin username')
        parser.add_argument('email', type=str, help='Admin email')
        parser.add_argument('password', type=str, help='Admin password')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']
        
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            self.stdout.write(f'User {username} already exists.')
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(f'User {username} created successfully.')
        
        admin_profile, created = AdminProfile.objects.get_or_create(user=user)
        admin_profile.is_site_admin = True
        admin_profile.save()
        
        if created:
            self.stdout.write(f'User {username} is now a site admin.')
        else:
            self.stdout.write(f'User {username} was already a site admin.')
