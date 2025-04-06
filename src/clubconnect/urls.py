# Add these to your existing urls.py

from django.urls import path
from .views import admin_views

# Admin dashboard URLs
urlpatterns += [
    path('admin-dashboard/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/clubs/', admin_views.admin_manage_clubs, name='admin_manage_clubs'),
    path('admin-dashboard/clubs/<int:club_id>/edit/', admin_views.admin_edit_club, name='admin_edit_club'),
    path('admin-dashboard/clubs/<int:club_id>/delete/', admin_views.admin_delete_club, name='admin_delete_club'),
    path('admin-dashboard/users/', admin_views.admin_manage_users, name='admin_manage_users'),
    path('admin-dashboard/users/<int:user_id>/toggle-admin/', admin_views.admin_toggle_user_admin, name='admin_toggle_user_admin'),
]
