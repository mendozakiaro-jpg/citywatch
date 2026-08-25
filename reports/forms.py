from django import forms
from .models import Report, ReportFeedback

class ReportForm(forms.ModelForm):
    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo and photo.size > 5 * 1024 * 1024:
            raise forms.ValidationError('Photo must be 5 MB or smaller.')
        return photo

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