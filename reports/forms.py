from django import forms
from .models import Report, ReportFeedback

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['title', 'description', 'category', 'urgency', 'photo', 'barangay', 'latitude', 'longitude']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class ReportFeedbackForm(forms.ModelForm):
    class Meta:
        model = ReportFeedback
        fields = ['rating', 'comment']