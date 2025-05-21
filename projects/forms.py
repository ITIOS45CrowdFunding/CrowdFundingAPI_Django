from django import forms
from .models import Project
# from .validators import *
from datetime import date
import json

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'details', 'target', 'startDate', 'endDate', 'category']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['images'] = forms.FileField(
                widget=forms.ClearableFileInput(attrs={'multiple': True}),
                required=True,
                label="Project Images"
            )

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 3 or " " not in title:
            raise forms.ValidationError("Title should have at least 2 words.")
        return title

    def clean_details(self):
        details = self.cleaned_data['details']
        if len(details) < 30:
            raise forms.ValidationError("details should be at least 30 characters.")
        return details

    def clean_target(self):
        target = self.cleaned_data['target']
        if target < 1000:
            raise forms.ValidationError("Target should be at least 1000 EGP.")
        return target

    def clean_startDate(self):
        startDate = self.cleaned_data['startDate']
        if startDate < date.today():
            raise forms.ValidationError("Start date should be today or in the future.")
        return startDate

    def clean_endDate(self):
        endDate = self.cleaned_data['endDate']
        if endDate < date.today():
            raise forms.ValidationError("End date should be today or in the future.")
        return endDate

    def clean_category(self):
        category = self.cleaned_data['category']
        if not category:
            raise forms.ValidationError("Category should not be empty.")
        return category