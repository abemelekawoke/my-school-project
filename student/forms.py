# student/forms.py
from django import forms
from .models import Subject, Year, Term
from .models import StudentAssessmentScore
from student.models import StudentProfile 
class GenerateAssessmentForm(forms.Form):
    """Form used inside the admin modal to trigger assessment generation."""

    subject = forms.ModelChoiceField(
        queryset=Subject.objects.none(),
        required=True,
        widget=forms.Select(attrs={"class": "select select-bordered w-full"}),
    )

    academic_year = forms.ModelChoiceField(
        queryset=Year.objects.none(),
        required=True,
        widget=forms.Select(attrs={"class": "select select-bordered w-full"}),
    )

    term = forms.ModelChoiceField(
        queryset=Term.objects.none(),
        required=True,
        widget=forms.Select(attrs={"class": "select select-bordered w-full"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["subject"].queryset = Subject.objects.filter(is_active=True)
        self.fields["academic_year"].queryset = Year.objects.filter(status="Active")
        self.fields["term"].queryset = Term.objects.filter(is_active=True)


class StudentAssessmentScoreForm(forms.ModelForm):
    class Meta:
        model = StudentAssessmentScore
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        raw_score = cleaned_data.get('raw_score')

        if raw_score is not None and raw_score < 0:
            # Validation error will appear on the same page, above the field
            self.add_error('raw_score', "Raw score must be greater than or equal to 0.")

        return cleaned_data

from django import forms
from datetime import date
from .models import StudentProfile


class ClearanceForm(forms.Form):
    reason = forms.CharField(
        label="ት/ቤቱን የለቀቀበት ምክንያት",
        initial="በግል ምክንያት",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "በግል ምክንያት",
        }),
    )
    leave_date = forms.DateField(
        label="ት/ቤቱን የለቀቀበት ቀን",
        initial=date.today,
        widget=forms.DateInput(attrs={
            "class": "form-control",
            "type": "date",
            "placeholder": "current date",
        }),
    )
    property_status = forms.CharField(
        label="የት/ቤቱ ንብረት",
        initial="ተመልሷል",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "ተመልሷል",
        }),
    )
    result_status = forms.CharField(
        label="የተሰጠው ት/ት ውጤት",
        initial="ወደ ሚቀጥለው ክፍል ተዛዉሯል",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "ወደ ሚቀጥለው ክፍል ተዛዉሯል",
        }),
    )