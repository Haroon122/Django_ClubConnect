# Add this to your existing models.py or create if it doesn't exist

from django.db import models
from django.contrib.auth.models import User

# If you don't already have a Club model, add one
class Club(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    founder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='founded_clubs')
    members = models.ManyToManyField(User, related_name='clubs', through='ClubMembership')
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name

class ClubMembership(models.Model):
    ROLE_CHOICES = [
        ('MEMBER', 'Member'),
        ('MODERATOR', 'Moderator'),
        ('ADMIN', 'Admin'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='MEMBER')
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'club')
    
    def __str__(self) -> str:
        return f"{self.user.username} - {self.club.name} ({self.role})"

# Add an AdminProfile model to track site administrators
class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_site_admin = models.BooleanField(default=False)
    admin_since = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f"{self.user.username} - Site Admin"

