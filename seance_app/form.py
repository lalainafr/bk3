from django import forms
from .models import Cinema

class CreateCinemaForm(forms.ModelForm):
    class Meta:
        model = Cinema
        fields = "__all__"
        
class UpdateCinemaForm(forms.ModelForm):
    class Meta:
        model = Cinema
        fields = '__all__'
        
