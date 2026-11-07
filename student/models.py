from import_export import resources
from django.db.models import Subquery, OuterRef
from django.db import connection
from django.db import models
from django.utils import timezone
from decimal import Decimal
import datetime
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)
from django_currentuser.db.models import CurrentUserField
from django.urls import reverse
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from setups.models import *
import inspect
import os
class StudentProfile(models.Model):
    # Gender choices
    Gender = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    
    parent_job=(
        ('Staff', 'Staff'),
        ('None Staff', 'None Staff'),
    )

    Transport_type = (
        ('School', 'በትምህርት ቤቱ'),
        ('Private', 'በግል'),
    )
    
    Tuition_fee = (
        (Decimal('0.00'), '0%'),
        (Decimal('0.50'), '50%'),
        (Decimal('0.75'), '75%'),
        (Decimal('1.00'), '100%'),
        (Decimal('2.00'), '200%'),
    )
    
    Transport_payment = (
        (Decimal('0.00'), '0%'),
        (Decimal('0.50'), '50%'),
        (Decimal('0.75'), '75%'),
        (Decimal('1.00'), '100%'),
    )
    
    # Academic status choices
    ACADEMIC_STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Failing', 'Failing'),
        ('Dropped-Out', 'Dropped-Out'),
        ('Suspended', 'Suspended'),
        ('Graduated', 'Graduated'),
        ('Transferred', 'Transferred'),
        ('Inactive', 'Inactive'),
        ('Special-Interest', 'Special-Interest'),
        ('Other', 'Other'),
    )
    
    SCHOOL_CHOICES = (
        ('#1', 'ቁጥር 1'),
        ('#2', 'ቁጥር 2'),
    )
    CYCLE_CHOICES = (
        ('KG', 'KG'),
        ('1-8', '1-8'),
        ('9-12', '9-12'),
    )
    Sponsorship = (
        ('Regular-fee', 'መደበኛ ከፋይ'),
        ('Double-fee', 'እጥፍ ከፋይ'),
        ('Solid-DeAfric', 'ሶሊድ ዲአፍሪክ'),
        ('Decision-free', 'በውሳኔ ነፃ'),
        ('Teacher-free', 'የመምህር ልጅ ነፃ'),
        ('Teacher-half', 'የመምህር ልጅ ግማሽ'),
        ('Admin-free', 'የአስተዳደር ልጅ ነፃ'), 
        ('None', 'የለውም'),       
    )
    
    Transport_category= (
        ('Regular-fee', 'መደበኛ ከፋይ'),
        ('Solid-DeAfric', 'ሶሊድ ዲአፍሪክ'),
        ('Decision-free', 'በውሳኔ ነፃ'),
        ('Teacher-free', 'የመምህር ልጅ ነፃ'),
        ('Teacher-half', 'የመምህር ልጅ ግማሽ'),
        ('Admin-free', 'የአስተዳደር ልጅ ነፃ'), 
        ('Driver-free', 'የሹፌር ልጅ ነፃ'),  
        ('None', 'የለውም'),
    )
    
    def get_current_year():
        try:
            current_year = Year.objects.get(status__iexact='Active')
            year = current_year.year
            return year
        except Year.DoesNotExist:
            return None
    id = models.AutoField(primary_key=True, unique=True)
    Full_name = models.CharField('ሙሉ ስም', max_length=100)
    Full_name_en = models.CharField('Full name', max_length=100)
    Gender = models.CharField('ጾታ ', max_length=25, choices=Gender)
    Date_of_birth = models.DateField('የትውልድ ቀን', null=True, blank=True)
    admit_year = models.CharField('የገባበት አመት', max_length=50, null=True, blank=True) 
    academic_year = models.CharField('የትምህርት ዘመን', max_length=50, default=get_current_year, null=True, blank=True) 
    cycle = models.CharField(max_length=50, choices=CYCLE_CHOICES, verbose_name='የት/ሳይክል', null=True, blank=True) 

    parent_contact = models.CharField('የወላጅ ስ/ቁጥር', max_length=25, null=True, blank=True)
    # parent_job = models.CharField('የወላጅ ስራ', max_length=50, choices=parent_job, null=True, blank=True)

    # Transport_type = models.CharField('የትራንስፖርት ሁኔታ', max_length=50, choices=Transport_type)
    # Fermata = models.ForeignKey(Fermata, on_delete=models.DO_NOTHING, verbose_name='አድራሻ/ፌርማታ', null=True, blank=True)
    # Transport_payment = models.DecimalField('የትራንስፖርት ክፍያ ሁኔታ', max_digits=12, decimal_places=2, choices=Transport_payment, default=Decimal('0.00'))

    New_grade = models.ForeignKey(Grade, on_delete=models.DO_NOTHING, related_name='new_grade', verbose_name='የአሁኑ ደረጃ', null=True, blank=True, to_field='code')
    New_section = models.ForeignKey(Section, on_delete=models.DO_NOTHING, related_name='new_section', verbose_name='የአሁኑ ክፍል', null=True, blank=True)
    Grade = models.ForeignKey(Grade, on_delete=models.DO_NOTHING, verbose_name='የገባበት ደረጃ', null=True, blank=True, to_field='code')
    Section = models.ForeignKey(Section, on_delete=models.DO_NOTHING, verbose_name='የገባበት ክፍል', null=True, blank=True) 
    # Sponsorship_type = models.ForeignKey(SponsorshipType, on_delete=models.DO_NOTHING, verbose_name='የተማሪው አይነት')
    # Sponsorship_type = models.CharField(max_length=90)
    # Transport_category = models.ForeignKey(TransportCategory, on_delete=models.DO_NOTHING, verbose_name='የትራንስፖርት አይነት')
    # Fee_amount = models.DecimalField('የክፍያ ሁኔታ', max_digits=12, decimal_places=2, choices=Tuition_fee, default=Decimal('0.00'))
    status = models.CharField(max_length=50, choices=ACADEMIC_STATUS_CHOICES, default='Active', verbose_name='የተማሪ የት/ሁኔታ') 
    school = models.CharField(max_length=50, choices=SCHOOL_CHOICES, default='#1', verbose_name='የሚማርበት ት/ቤት', null=True, blank=True) 
    student_image = models.ImageField('የተማሪ ምስል KG', upload_to='student_images/', null=True, blank=True)
    student_image1 = models.ImageField('የተማሪ ምስል 6', upload_to='student_images/', null=True, blank=True)
    student_image2 = models.ImageField('የተማሪ ምስል 8', upload_to='student_images/', null=True, blank=True)
    student_image3 = models.ImageField('የተማሪ ምስል 12', upload_to='student_images/', null=True, blank=True)
    discipline = models.CharField('ትምህርታዊ ሥነ ምግባር', max_length=150, null=True, blank=True, default='A')
    Remark = models.CharField('ምርመራ', max_length = 150, null=True, blank=True)
    
    created_by = CurrentUserField(related_name="rb2")
    created_at = models.DateField(auto_now=True)
    modified_by = CurrentUserField(related_name="ub2")
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Full_name

    class Meta:
        verbose_name="Student profile"
        verbose_name_plural="Student profile"
        
class AcademicHistory(models.Model):
    student = models.ForeignKey(
        'student.StudentProfile',  # adjust app name if needed
        on_delete=models.CASCADE,
        related_name='academic_histories'
    )

    academic_year = models.CharField(
        max_length=9,  # e.g. 2023/2024
        help_text="Format: YYYY/YYYY"
    )

    grade = models.CharField(
        max_length=20,
        help_text="Grade or Year Level (e.g. Grade 10, Year 2)"
    )

    section = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ('Promoted', 'Promoted'),
            ('Repeated', 'Repeated'),
            ('Transferred', 'Transferred'),
            ('Dropped', 'Dropped'),
        ],
        default='Promoted'
    )

    remark = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['student', 'academic_year']
        unique_together = ('student', 'academic_year')
        verbose_name = "Academic History"
        verbose_name_plural = "Academic Histories"

    def __str__(self):
        return f"{self.student} - {self.academic_year}"

        
class StudentAssessment(models.Model):
    def get_current_year():
        try:
            current_year = Year.objects.get(status__iexact='Active')
            year = current_year.year
            return year
        except Year.DoesNotExist:
            return None
    student = models.ForeignKey(StudentProfile, on_delete=models.SET_NULL, null=True, related_name="assessments")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    assessment_formula = models.ForeignKey(AssessmentFormula, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(Year, default=get_current_year, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    total_score = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    result_status = models.CharField(max_length=20, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.subject} ({self.term})"

class AssignmentCompletenessView(models.Model):
    """
    Database view to check assignment completeness.
    """
    ISSUE_TYPE_CHOICES = [
        ('SECTION_WITHOUT_HEAD', 'Section Without Head'),
        ('SUBJECT_WITHOUT_TEACHER', 'Subject Without Teacher'),
        ('STUDENT_WITHOUT_SUBJECTS', 'Student Without Subjects'),
    ]
    id = models.AutoField(primary_key=True, unique=True)
    issue_type = models.CharField(max_length=50, choices=ISSUE_TYPE_CHOICES)
    academic_year = models.CharField(max_length=50)
    grade = models.CharField(max_length=10)
    section = models.CharField(max_length=100)
    subject_name = models.CharField(max_length=100, null=True, blank=True)
    teacher_name = models.CharField(max_length=255, null=True, blank=True)
    affected_count = models.IntegerField(default=0)  # Add this field
    
    class Meta:
        managed = False
        db_table = 'ASSIGNMENT_COMPLETENESS_VIEW'
        verbose_name = 'Assignment Completeness Check'
        verbose_name_plural = 'Assignment Completeness Checks'
    
    def __str__(self):
        if self.issue_type == 'SECTION_WITHOUT_HEAD':
            return f"Section {self.grade}{self.section} needs head"
        elif self.issue_type == 'SUBJECT_WITHOUT_TEACHER':
            return f"{self.subject_name} needs teacher in {self.grade}{self.section}"
        elif self.issue_type == 'STUDENT_WITHOUT_SUBJECTS':
            return f"{self.affected_count} students in {self.grade}{self.section} have no subjects"
        return f"{self.get_issue_type_display()}"

import os
import inspect
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class StudentAssessmentScore(models.Model):
    def get_current_year():
        try:
            return Year.objects.get(status__iexact="Active").year
        except Year.DoesNotExist:
            return None

    student = models.ForeignKey(
        StudentProfile, on_delete=models.SET_NULL, null=True,
        related_name="assess",
    )
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="sub",
    )
    student_assessment = models.ForeignKey(
        StudentAssessment, on_delete=models.CASCADE, related_name="scores",
    )
    weight = models.ForeignKey(Weight, on_delete=models.CASCADE)

    grade   = models.ForeignKey(Grade,   on_delete=models.CASCADE, to_field="code")
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    term    = models.ForeignKey(Term,    on_delete=models.CASCADE)
    academic_year = models.ForeignKey(
        Year, default=get_current_year, on_delete=models.CASCADE,
    )

    raw_score = models.DecimalField(
        max_digits=5, decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    weighted_score = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
    )

    def clean(self):
        """Kept for form/serializer validation. NOT called from save()."""
        super().clean()
        if self.weight_id and self.raw_score is not None:
            # avoid a second DB hit if weight is already loaded
            max_weight = self.weight.weight
            if self.raw_score > max_weight:
                raise ValidationError({
                    "raw_score": (
                        f"Raw score ({self.raw_score}) cannot be greater than "
                        f"weight ({max_weight})."
                    )
                })

    def save(self, *args, **kwargs):
        # Single targeted check instead of full_clean() (which ran ~11 queries).
        if self.weight_id and self.raw_score is not None:
            max_weight = self.weight.weight
            if self.raw_score > max_weight:
                raise ValidationError({
                    "raw_score": (
                        f"Raw score ({self.raw_score}) cannot be greater than "
                        f"weight ({max_weight})."
                    )
                })
        # Compute weighted_score here if you keep the column.
        if self.weight_id and self.raw_score is not None:
            self.weighted_score = (self.raw_score * self.weight.weight) / 100
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ("student_assessment", "weight")
        indexes = [
            models.Index(
                fields=["student", "academic_year", "term", "subject"],
                name="idx_sas_student_yr_term_subj",
            ),
            models.Index(fields=["student_assessment"], name="idx_sas_assessment"),
            models.Index(fields=["section"],            name="idx_sas_section"),
            models.Index(fields=["grade"],              name="idx_sas_grade"),
        ]
        verbose_name_plural = "Student Assessment Scores"

    def __str__(self):
        return f"{self.student_id} / {self.subject_id} / {self.weight_id}: {self.raw_score}"
    
from django.db import models


class StudentResultJSONView(models.Model):
    # ---- Primary key: BIGINT from CONV(MD5(...), 16, 10) ----
    id = models.DecimalField(primary_key=True, max_digits=20, decimal_places=0)

    student_id = models.IntegerField()
    student_name = models.CharField(max_length=150)
    gender = models.CharField(max_length=10)
    age = models.IntegerField(null=True, blank=True)
    school = models.CharField(max_length=50, null=True, blank=True)   # <- present in the view output
    grade = models.CharField(max_length=50)
    section = models.CharField(max_length=50)
    section_head = models.CharField(max_length=150, null=True, blank=True)
    academic_year = models.CharField(max_length=50)
    semester = models.CharField(max_length=50)                        # view returns "Term one", not an int
    subjects = models.JSONField()
    discipline = models.CharField(max_length=255, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    average = models.DecimalField(max_digits=10, decimal_places=6)    # 99.500000
    rank = models.IntegerField(db_column="RANK")                      # view column "RANK"
    yearly_rank = models.IntegerField(db_column="YEARLY_RANK", null=True, blank=True)
    result_status = models.CharField(max_length=50, null=True, blank=True)
    report_date = models.DateField()
    report_title = models.CharField(max_length=255, null=True, blank=True)
    archive_officer_name = models.CharField(max_length=150, null=True, blank=True)
    school_director_name = models.CharField(max_length=150, null=True, blank=True)

    class Meta:
        managed = False
        db_table = "STUDENT_RESULT_JSON_VIEW"
        verbose_name = "Student Result"
        verbose_name_plural = "Student Results"
        ordering = ("student_id", "academic_year", "semester")

    def __str__(self):
        return f"{self.student_name} - {self.semester} ({self.academic_year})"
    
# # student/models.py
# from django.db import models

# class StudentResultSectionSummary(models.Model):
#     id = models.IntegerField(primary_key=True)  # Synthetic ID from ROW_NUMBER

#     grade = models.CharField(max_length=20)
#     section = models.CharField(max_length=20)
#     academic_year = models.CharField(max_length=20)

#     section_head = models.CharField(max_length=150, null=True, blank=True)
#     report_date = models.DateField(null=True, blank=True)

#     archive_officer_name = models.CharField(max_length=150, null=True, blank=True)
#     school_director_name = models.CharField(max_length=150, null=True, blank=True)

#     subjects = models.TextField(null=True, blank=True)

#     registered_male = models.IntegerField()
#     registered_female = models.IntegerField()
#     registered_total = models.IntegerField()

#     seated_male = models.IntegerField()
#     seated_female = models.IntegerField()
#     seated_total = models.IntegerField()

#     not_seated_male = models.IntegerField()
#     not_seated_female = models.IntegerField()
#     not_seated_total = models.IntegerField()

#     mark_lt_50 = models.IntegerField()
#     mark_ge_50 = models.IntegerField()
#     mark_ge_75 = models.IntegerField()
#     mark_ge_85 = models.IntegerField()

#     pct_lt_50 = models.FloatField()
#     pct_ge_50 = models.FloatField()
#     pct_ge_75 = models.FloatField()
#     pct_ge_85 = models.FloatField()

#     section_total_mark = models.FloatField()
#     section_average_mark = models.FloatField()

#     class Meta:
#         managed = False  # Django won't try to create or alter this table
#         db_table = 'STUDENT_RESULT_SECTION_SUMMARY'
#         verbose_name = 'Student Result Section Summary'
#         verbose_name_plural = 'Student Result Section Summaries'

#     def __str__(self):
#         return f"{self.grade} - {self.section} ({self.academic_year})"

# class StudentAverage(models.Model):
#     def get_current_year():
#         try:
#             current_year = Year.objects.get(status__iexact='Active')
#             year = current_year.year
#             return year
#         except Year.DoesNotExist:
#             return None
#     id = models.AutoField(primary_key=True, unique=True)
#     student = models.ForeignKey(StudentProfile, on_delete=models.SET_NULL, null=True)
#     grade = models.ForeignKey(Grade, on_delete=models.DO_NOTHING)
#     section = models.ForeignKey(Section, on_delete=models.DO_NOTHING, verbose_name='ክፍል', null=True, blank=True) 
    
#     academic_year = models.CharField('የትምህርት ዘመን', max_length=50, default=get_current_year, null=True, blank=True) 
#     average = models.DecimalField(decimal_places=2, max_digits=15)
    
#     class Meta:
#         verbose_name_plural = "Student average"

#     def __str__(self):
#         return "%s" % self.student
    
# class StudentRoster(models.Model):
#     semester = (
#         ('1st', 'First'),
#         ('2nd', 'Second'),
#         ('Average', 'Average'),
#     )
#     def get_current_year():
#         try:
#             current_year = Year.objects.get(status__iexact='Active')
#             year = current_year.year
#             return year
#         except Year.DoesNotExist:
#             return None
#     id = models.AutoField(primary_key=True, unique=True)
#     academic_year = models.CharField('የትምህርት ዘመን', max_length=50, default=get_current_year, null=True, blank=True) 
#     student = models.ForeignKey(StudentProfile, on_delete=models.SET_NULL, null=True)
#     semester = models.CharField(max_length=25, choices=semester)
#     amharic = models.DecimalField(decimal_places=2, max_digits=15)
#     english = models.DecimalField(decimal_places=2, max_digits=15)
#     mathematics = models.DecimalField(decimal_places=2, max_digits=15)
#     physics = models.DecimalField(decimal_places=2, max_digits=15)
#     chemistry = models.DecimalField(decimal_places=2, max_digits=15)
#     biology = models.DecimalField(decimal_places=2, max_digits=15)
#     civics = models.DecimalField(decimal_places=2, max_digits=15, null=True, blank=True)
#     td = models.DecimalField('TD', decimal_places=2, max_digits=15, null=True, blank=True)  # TD can be a subject like Technology or similar
#     hpe = models.DecimalField('HPE', decimal_places=2, max_digits=15, null=True, blank=True)
#     it = models.DecimalField('IT', decimal_places=2, max_digits=15, null=True, blank=True)
#     agriculture = models.DecimalField('Agriculture', decimal_places=2, max_digits=15, null=True, blank=True)
#     total = models.DecimalField(decimal_places=2, max_digits=15)
#     average = models.DecimalField(decimal_places=2, max_digits=15)
#     rank = models.IntegerField(default=0)   
#     remark = models.CharField(max_length=25, blank=True, null=True)
#     conduct = models.CharField(max_length=25, blank=True, null=True)
#     created_by = CurrentUserField(related_name="rb111")
#     created_at = models.DateField(auto_now=True)
#     class Meta:
#         verbose_name_plural = "Natural Students Rosters"

#     def __str__(self):
#         return "%s" % self.student
    
#     def save(self, *args, **kwargs):
#         self.total = self.amharic + self.english + self.mathematics + self.physics + self.chemistry + self.biology + self.civics + self.td + self.hpe + self.it + self.agriculture

#         self.average = ((self.amharic + self.english + self.mathematics + self.physics + self.chemistry + self.biology + self.civics + self.td  + self.hpe + self.it + self.agriculture)/11) if self.amharic or self.english or self.mathematics or self.physics or self.chemistry or self.biology or self.civics or self.td or self.hpe or self.it or self.agriculture else 0

#         super(StudentRoster, self).save(*args, **kwargs)  # Call the real save() method

# class SocialStudentRoster(models.Model):
#     semester = (
#         ('1st', 'First'),
#         ('2nd', 'Second'),
#         ('Average', 'Average'),
#     )
#     def get_current_year():
#         try:
#             current_year = Year.objects.get(status__iexact='Active')
#             year = current_year.year
#             return year
#         except Year.DoesNotExist:
#             return None
#     id = models.AutoField(primary_key=True, unique=True)
#     academic_year = models.CharField('የትምህርት ዘመን', max_length=50, default=get_current_year, null=True, blank=True) 
#     student = models.ForeignKey(StudentProfile, on_delete=models.SET_NULL, null=True)
#     semester = models.CharField(max_length=25, choices=semester)
#     amharic = models.DecimalField('Amharic', decimal_places=2, max_digits=15)
#     english = models.DecimalField('English', decimal_places=2, max_digits=15)
#     mathematics = models.DecimalField('Mathematics', decimal_places=2, max_digits=15)
#     geography = models.DecimalField('Geography', decimal_places=2, max_digits=15)
#     gbusiness = models.DecimalField('G/Business', decimal_places=2, max_digits=15)
#     history = models.DecimalField('History', decimal_places=2, max_digits=15)
#     economics = models.DecimalField('Economics', decimal_places=2, max_digits=15)
#     civics = models.DecimalField('Civics', decimal_places=2, max_digits=15, null=True, blank=True)
#     hpe = models.DecimalField('HPE', decimal_places=2, max_digits=15, null=True, blank=True)
#     it = models.DecimalField('IT', decimal_places=2, max_digits=15, null=True, blank=True)
#     agriculture = models.DecimalField('Agriculture', decimal_places=2, max_digits=15, null=True, blank=True)
#     total = models.DecimalField('Total', decimal_places=2, max_digits=15)
#     average = models.DecimalField('Average', decimal_places=2, max_digits=15)
#     rank = models.IntegerField(default=0)   
#     remark = models.CharField(max_length=25, blank=True, null=True)
#     conduct = models.CharField(max_length=25, blank=True, null=True)
#     created_by = CurrentUserField(related_name="rb1111")
#     created_at = models.DateField(auto_now=True)
#     class Meta:
#         verbose_name_plural = "Social Students Rosters"

#     def __str__(self):
#         return "%s" % self.student
    
#     def save(self, *args, **kwargs):
#         self.total = self.amharic + self.english + self.mathematics + self.geography + self.gbusiness + self.history + self.economics + self.civics + self.hpe + self.it + self.agriculture

#         self.average = ((self.amharic + self.english + self.mathematics + self.geography + self.gbusiness + self.history + self.economics + self.civics + self.hpe + self.it + self.agriculture)/11) if self.amharic or self.english or self.mathematics or self.geography or self.gbusiness or self.history or self.economics or self.civics or self.hpe or self.it or self.agriculture else 0

#         super(StudentRoster, self).save(*args, **kwargs)  # Call the real save() method

    
class StudentsBySection(models.Model):
    grade_id = models.IntegerField()
    section_id = models.IntegerField()
    total_students = models.IntegerField()

    class Meta:
        managed = False  # This is a database view, not a Django-managed table
        db_table = "students_by_section"  # Matches the name of the database view
        verbose_name = "Students by Section"
        verbose_name_plural = "Students by Section"

    def __str__(self):
        return f"Grade {self.grade_id} - Section {self.section_id}: {self.total_students} Students"
    
class StudentStatistics(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    academic_year = models.CharField(max_length=50)
    grade = models.IntegerField()
    section = models.IntegerField()
    gender = models.CharField(max_length=50)
    total_students = models.IntegerField()

    class Meta:
        managed = False  # This is a database view, not a Django-managed table
        db_table = "student_statistics"  # Matches the name of the database view
        verbose_name = "Student statistics"
        verbose_name_plural = "Student statistics"

    def __str__(self):
        return f"Grade {self.grade} - Section {self.section}: {self.total_students} Students"

class StudentResultAnalysisView(models.Model):
    """
    Read-only mirror of the MySQL view `student_result_analysis_view`.
    One row per (academic_year, grade, subject).
    """
    id = models.BigIntegerField(primary_key=True)          # ROW_NUMBER() from the view
    academic_year = models.IntegerField()
    grade = models.CharField(max_length=20)                # '1'..'8' (kept as string to match view)
    subject_name = models.CharField(max_length=100)

    registered_males = models.IntegerField()
    registered_females = models.IntegerField()
    registered_total = models.IntegerField()

    tested_males = models.IntegerField()
    tested_females = models.IntegerField()
    tested_total = models.IntegerField()

    under_50_males = models.IntegerField()
    under_50_females = models.IntegerField()
    under_50_total = models.IntegerField()

    above_50_males = models.IntegerField()
    above_50_females = models.IntegerField()
    above_50_total = models.IntegerField()

    above_75_males = models.IntegerField()
    above_75_females = models.IntegerField()
    above_75_total = models.IntegerField()

    above_85_males = models.IntegerField()
    above_85_females = models.IntegerField()
    above_85_total = models.IntegerField()

    class Meta:
        managed = False
        db_table = "student_result_analysis_view"
        ordering = ("academic_year", "grade", "subject_name")
        verbose_name = "Subject Score Analysis"
        verbose_name_plural = "Subject Score Analysis"

    def __str__(self):
        return f"{self.academic_year} • Grade {self.grade} • {self.subject_name}"


class StudentGradeLevelAnalysisView(models.Model):
    """
    Read-only mirror of the MySQL view `student_grade_level_analysis_view`.
    One row per (academic_year, grade) + the ከ1-6 / ከ7-8 / ከ1-8 roll-ups.
    """
    id = models.BigIntegerField(primary_key=True)
    academic_year = models.IntegerField()
    grade = models.CharField(max_length=30)                # '1'..'8' or 'ከ1-6 ክፍል' etc.

    registered_males = models.IntegerField()
    registered_females = models.IntegerField()
    registered_total = models.IntegerField()

    tested_males = models.IntegerField()
    tested_females = models.IntegerField()
    tested_total = models.IntegerField()

    promoted_males = models.IntegerField()
    promoted_females = models.IntegerField()
    promoted_total = models.IntegerField()

    repeated_males = models.IntegerField()
    repeated_females = models.IntegerField()
    repeated_total = models.IntegerField()

    under_50_males = models.IntegerField()
    under_50_females = models.IntegerField()
    under_50_total = models.IntegerField()

    above_50_males = models.IntegerField()
    above_50_females = models.IntegerField()
    above_50_total = models.IntegerField()

    above_75_males = models.IntegerField()
    above_75_females = models.IntegerField()
    above_75_total = models.IntegerField()

    above_85_males = models.IntegerField()
    above_85_females = models.IntegerField()
    above_85_total = models.IntegerField()

    class Meta:
        managed = False
        db_table = "student_grade_level_analysis_view"
        ordering = ("academic_year", "id")
        verbose_name = "Grade Level Analysis"
        verbose_name_plural = "Grade Level Analysis"

    def __str__(self):
        return f"{self.academic_year} • {self.grade}"