# Add this to your existing forms.py or create if it doesn't exist

from django import forms
from .models import Club

class ClubForm(forms.ModelForm):
    """Form for creating and editing clubs."""
    
    class Meta:
        model = Club
        fields = ['name', 'description', 'founder', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
