from django import forms
from django.utils.html import format_html
from .models import Subject, Grade

class SubjectForm(forms.ModelForm):
    # This field will replace grade_levels in the form
    grades = forms.ModelMultipleChoiceField(
        queryset=Grade.objects.all().order_by('name'),
        required=False,
        widget=forms.SelectMultiple(attrs={'size': '10'}),
        label="Select Grade Levels"
    )
    
    class Meta:
        model = Subject
        fields = ['name', 'code', 'description', 'is_active']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set initial grades from the ManyToMany field
        if self.instance.pk:
            self.fields['grades'].initial = self.instance.grade_levels.all()
    
    def save(self, commit=True):
        # Save the Subject instance
        subject = super().save(commit=commit)
        
        # Save the grades to the ManyToMany field
        if commit:
            subject.grade_levels.set(self.cleaned_data['grades'])
        else:
            # If not committing, store grades for later
            self._grades = self.cleaned_data['grades']
            self.save_m2m = self._save_m2m
        
        return subject
    
    def _save_m2m(self):
        """Save ManyToMany relationships."""
        self.instance.grade_levels.set(self._grades)