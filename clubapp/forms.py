from django import forms
from .models import Club, Member, Event, Announcement

class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ['name', 'description', 'founded_date']
        widgets = {
            'founded_date': forms.DateInput(attrs={'type': 'date'}),
        }

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['club', 'name', 'role', 'join_date']
        widgets = {
            'join_date': forms.DateInput(attrs={'type': 'date'}),
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['club', 'title', 'description', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['club', 'title', 'message'] 