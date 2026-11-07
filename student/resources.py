import re
from import_export import resources, fields

from .models import *
from setups.models import *


class StudentAssessmentScoreResource(resources.ModelResource):

    student = fields.Field(column_name='Student Full Name')
    subject = fields.Field(column_name='Subject')
    weight = fields.Field(column_name='Weight')
    raw_score = fields.Field(column_name='Raw Score')
    weighted_score = fields.Field(column_name='Weighted Score')

    class Meta:
        model = StudentAssessmentScore
        fields = (
            'student',
            'subject',
            'weight',
            'raw_score',
            'weighted_score',
        )
        exclude = ('id', 'student_assessment')
        import_id_fields = ()
        skip_unchanged = True
        report_skipped = True

    # =========================
    # EXPORT
    # =========================
    def dehydrate_weight(self, obj):
        # Example export: Final (exam) (40)
        return f"{obj.weight.name} ({obj.weight.weight})"

    def dehydrate_student(self, obj):
        return obj.student_assessment.student.Full_name

    def dehydrate_subject(self, obj):
        return obj.student_assessment.subject.name

    # =========================
    # IMPORT
    # =========================
    def before_import_row(self, row, **kwargs):
        student_name = row.get('Student Full Name')
        subject_name = row.get('Subject')
        weight_text = row.get('Weight')  # e.g. "Final (exam) (40)"

        if not weight_text:
            raise Exception("Weight column is empty")

        # ✅ Extract last number in brackets as weight_number
        match = re.search(r'\(([\d\.]+)\)\s*$', weight_text)
        if not match:
            raise Exception(f"Invalid Weight format: '{weight_text}'")

        weight_number = match.group(1)

        # Remove last (number) to get weight name
        weight_name = re.sub(r'\s*\([\d\.]+\)\s*$', '', weight_text).strip()

        try:
            # Resolve Student
            student = StudentProfile.objects.get(Full_name=student_name)
            # Resolve Subject
            subject = Subject.objects.get(name=subject_name)
            # Active year/term
            year = Year.objects.get(status__iexact='Active')
            term = Term.objects.get(status__iexact='Active')

            # Resolve StudentAssessment
            student_assessment = StudentAssessment.objects.get(
                student=student,
                subject=subject,
                academic_year=year,
                term=term
            )

            # Resolve Weight
            weight = Weight.objects.get(name=weight_name, weight_number=weight_number)

            # Inject FK numeric IDs for import
            row['student_assessment'] = student_assessment.id
            row['weight'] = weight.id

        except Exception as e:
            raise Exception(
                f"Import error: student='{student_name}', subject='{subject_name}', weight='{weight_text}' → {str(e)}"
            )