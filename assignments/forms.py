from django import forms
from .models import Assignment

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['department', 'assigned_to', 'notes']