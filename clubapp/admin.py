from django.contrib import admin
from .models import Club, Member, Event, Announcement

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'founded_date')
    search_fields = ('name', 'description')

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'club', 'role', 'join_date')
    list_filter = ('club', 'role')
    search_fields = ('name', 'club__name')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'club', 'date')
    list_filter = ('club', 'date')
    search_fields = ('title', 'description', 'club__name')

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'club', 'posted_on')
    list_filter = ('club', 'posted_on')
    search_fields = ('title', 'message', 'club__name')
