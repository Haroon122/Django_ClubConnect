from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('clubs/', views.clubs, name='clubs'),
    path('clubs/<int:club_id>/', views.club_detail, name='club_detail'),
    path('events/', views.events, name='events'),
    path('announcements/', views.announcements, name='announcements'),
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/clubs/', views.manage_clubs, name='manage_clubs'),
    path('dashboard/clubs/edit/<int:pk>/', views.edit_club, name='edit_club'),
    path('dashboard/clubs/delete/<int:pk>/', views.delete_club, name='delete_club'),
    path('dashboard/members/', views.manage_members, name='manage_members'),
    path('dashboard/members/edit/<int:pk>/', views.edit_member, name='edit_member'),
    path('dashboard/members/delete/<int:pk>/', views.delete_member, name='delete_member'),
    path('dashboard/events/', views.manage_events, name='manage_events'),
    path('dashboard/events/edit/<int:pk>/', views.edit_event, name='edit_event'),
    path('dashboard/events/delete/<int:pk>/', views.delete_event, name='delete_event'),
    path('dashboard/announcements/', views.manage_announcements, name='manage_announcements'),
    path('dashboard/announcements/edit/<int:pk>/', views.edit_announcement, name='edit_announcement'),
    path('dashboard/announcements/delete/<int:pk>/', views.delete_announcement, name='delete_announcement'),
]
