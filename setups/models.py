from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
# Create your models here.
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime
from humanresource.models import *
from django.conf import settings
from humanresource.models import StaffProfile

class Year(models.Model):
	status = (
		('Active', 'Active'),
		('In Active', 'In Active'),
	)
	id = models.AutoField(primary_key=True, unique=True)
	year = models.CharField(max_length=100, unique=True)  
	description = models.CharField(max_length=250, blank=True, null=True)
	status = models.CharField(max_length=50, choices=status)

	class Meta:
		verbose_name_plural = "Academic year"
		abstract = False

	def __str__(self):
		return "%s" % self.year

class ReportHeader(models.Model):
    school_name = models.CharField(
        max_length=255,
        verbose_name="የት/ት ቤት ስም",
        help_text="የትምህርት ቤቱ ሙሉ ስም"
    )

    education_bureau = models.CharField(
        max_length=255,
        default="በአማራ ክልል ት/ት ቢሮ",
        verbose_name="የት/ት ቢሮ",
        help_text="ላይኛው የአስተዳደር አካል"
    )

    city_admin = models.CharField(
        max_length=255,
        default="ጎንደር ከተማ አስተዳደር",
        verbose_name="ከተማ አስተዳደር",
        help_text="የከተማ አስተዳደር ስም"
    )

    archive_officer = models.ForeignKey(
        AdminStaffProfile,
        on_delete=models.DO_NOTHING,
        related_name="archive_report_headers",
        verbose_name="የመዘክር ክፍል ኃላፊ",
        help_text="የመዘክር ክፍል ኃላፊ ስም"
    )

    school_director = models.ForeignKey(
        StaffProfile,
        on_delete=models.DO_NOTHING,
        related_name="director_report_headers",
        verbose_name="የት/ት ቤቱ ር/መ/ር",
        help_text="የት/ት ቤቱ ርዕሰ መምህር"
    )

    academic_year = models.ForeignKey(
        Year,
        on_delete=models.DO_NOTHING,
        verbose_name="የትምህርት ዓመት",
        help_text="ምሳሌ፡ 2016 / 2017"
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateField(
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Report header"
        verbose_name_plural = "Report headers"
        ordering = ["-academic_year"]

    def __str__(self):
        return f"{self.school_name} | {self.academic_year}"

class Month(models.Model):
	status = (
		('Active', 'Active'),
		('In Active', 'In Active'),
	)
	id = models.AutoField(primary_key=True, unique=True)
	month_amharic = models.CharField(max_length=100, unique=True)
	month_english = models.CharField(max_length=100, unique=True)
	description = models.CharField(max_length=250)
	status = models.CharField(max_length=50, choices=status)

	class Meta:
		verbose_name_plural = "Months"
		abstract = False

	def __str__(self):
		return "%s" % self.month_english
 
class Term(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=50, unique=True)  # e.g., "Term 1", "Semester 2"
    academic_year = models.ForeignKey(Year, on_delete=models.CASCADE)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['academic_year', 'name']

    def __str__(self):
        return f"{self.name}"

class Grade(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    code = models.CharField(max_length=10, unique=True) # e.g. KG1, KG2, 1, 2, ...
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)

    class Meta:
        verbose_name_plural = "Grades"

    def __str__(self):
        return f"{self.name}"

class Section(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    description = models.CharField(max_length=250)

    class Meta:
        verbose_name_plural = "Sections"
        db_table = "SETUPS_SECTION"   # match your actual table name

    def __str__(self):
        return self.name

class Stream(models.Model):
    STREAM_CHOICES = [
        ('regular', 'Regular'),
        ('natural', 'Natural'),
        ('social', 'Social'),
    ]
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=20, choices=STREAM_CHOICES, unique=True)
    status = models.BooleanField(default=True)
    def __str__(self):
        return self.get_name_display()

class Subject(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=100, unique=True)
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE, related_name='subjects', null=True, blank=True)
    code = models.CharField(
        max_length=20,
        unique=True,
        help_text="Short code (e.g., ENG, MATH, PHYS)"
    )
    description = models.TextField(blank=True)
    # ManyToManyField: One subject can have many grades, one grade can have many subjects
    grade_levels = models.ManyToManyField(
        "Grade",
        related_name="subjects",
        help_text="Check/Select grade levels where this subject is taught",
        blank=True  # Allows no grades to be selected initially
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Active"
    )

    class Meta:
        ordering = ["name"]
        db_table = "SETUPS_SUBJECT"
    
    def __str__(self):
        return f"{self.name} ({self.code}) ({self.stream})"
    
class TeacherAssignment(models.Model):
    teacher = models.ForeignKey(
        StaffProfile,
        on_delete=models.CASCADE,
        db_column='TEACHER_ID',
        related_name='assignments',
        verbose_name='Teacher'
    )

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column='ASSIGNED_TO_ID',
        verbose_name='User Name',
        null=True,
        blank=True
    )

    academic_year = models.ForeignKey(
        Year,
        on_delete=models.CASCADE,
        db_column='ACADEMIC_YEAR_ID',
        verbose_name='Academic Year',
        null=True,
        blank=True
    )

    grade = models.ForeignKey(
        Grade,
        on_delete=models.CASCADE,
        db_column='GRADE_ID',
        to_field='code',
        verbose_name='Grade',
        null=True,
        blank=True
    )

    section = models.ForeignKey(
        Section,
        to_field='name',
        on_delete=models.CASCADE,
        db_column='Section_name',
        null=True,
        blank=True
    )

    is_section_head = models.BooleanField(
        default=False,
        db_column='IS_SECTION_HEAD',
        verbose_name='Is Section Head'
    )

    number_of_sessions = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        db_column='NUMBER_OF_SESSIONS'
    )

    assigned_date = models.DateField(
        auto_now_add=True,
        db_column='ASSIGNED_DATE'
    )

    class Meta:
        db_table = 'SETUPS_TEACHERASSIGNMENT'
        verbose_name = 'Teacher Assignment'
        verbose_name_plural = 'Teacher Assignments'
        # constraints = [
        #     models.UniqueConstraint(
        #         fields=['academic_year', 'grade', 'section'],
        #         condition=models.Q(is_section_head=True),
        #         name='unique_section_head_per_grade_section_year'
        #     )
        # ]

    def __str__(self):
        return f"{self.teacher} - {self.grade}{self.section}"

class TeacherAssignmentDetail(models.Model):
    assignment = models.ForeignKey(
        TeacherAssignment,
        on_delete=models.CASCADE,
        related_name='details'
    )

    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, to_field='code')
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    status = models.CharField(
        max_length=20,
        choices=[
            ('ACTIVE', 'Active'),
            ('INACTIVE', 'Inactive')
        ],
        default='ACTIVE'
    )

    class Meta:
        unique_together = (
            'assignment',
            'grade',
            'section',
            'subject',
        )

    def __str__(self):
        return f"{self.assignment.teacher} - {self.subject} ({self.grade}-{self.section})"
            
class AssessmentName(models.Model):
    CATEGORY_CHOICES = [
        ("exam", "Exam"),
        ("quiz", "Quiz"),
        ("assignment", "Assignment"),
        ("project", "Project"),
        ("presentation", "Presentation"),
        ("practical", "Practical/Lab"),
        ("participation", "Class Participation"),
        ("continuous", "Continuous Assessment"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=100, unique=True)  
    description = models.TextField(blank=True)  
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="exam",
        help_text="Broad type of assessment"
    )
    is_active = models.BooleanField(default=True)  

    class Meta:
        ordering = ["name"]
        verbose_name = "Assessment Name"
        verbose_name_plural = "Assessment Names"

    def __str__(self):
        return f"{self.name} ({self.category})"
    
class AssessmentFormula(models.Model):
    """
    Main assessment formula model
    Defines the formula/weights for assessment calculation
    """
    # Basic Information
    name = models.CharField(
        max_length=100,
        help_text="Name of assessment formula (e.g., 'Comprehensive Assessment', 'Term-Based System')"
    )

    description = models.TextField(
        blank=True,
        help_text="Description of this assessment formula"
    )

    # ForeignKeys
    grade_level = models.ForeignKey(
        'Grade',
        to_field='code',
        on_delete=models.CASCADE,
        help_text="Grade level this assessment formula applies to"
    )

    academic_year = models.ForeignKey(
        'Year',
        on_delete=models.CASCADE,
        help_text="Academic year this assessment formula applies to"
    )

    subject = models.ForeignKey(
        'Subject',
        on_delete=models.CASCADE,
        help_text="Subject this assessment formula applies to"
    )

    # Scoring
    max_score = models.IntegerField(
        default=100,
        help_text="Maximum total score"
    )

    passing_score = models.IntegerField(
        default=50,
        help_text="Minimum passing score"
    )

    # Status
    is_active = models.BooleanField(default=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        managed = True
        db_table = 'SETUPS_ASSESSMENTFORMULA'

    def __str__(self):
        return f"{self.name} ({self.academic_year} - {self.grade_level} - {self.subject})"

    def total_weight(self):
        """Calculate total weight from weight components."""
        return sum(w.weight for w in self.weights.all())

    def clean(self):
        """Validate the assessment formula."""
        super().clean()

        # Validate scoring range
        if self.max_score is not None and self.max_score <= 0:
            raise ValidationError({"max_score": "Maximum score must be greater than 0."})

        if (
            self.passing_score is not None
            and self.max_score is not None
            and self.passing_score > self.max_score
        ):
            raise ValidationError(
                {"passing_score": "Passing score cannot exceed maximum score."}
            )

        # Validate total weights only when weights already exist.
        # (On the admin *add* page the inline weights are not saved yet —
        #  that check belongs in an inline formset, see admin notes below.)
        if self.pk and self.weights.exists():
            total = self.total_weight()
            if total != 100:
                raise ValidationError(
                    f"Total weight must equal 100%. Current total: {total}%."
                )
            
class Weight(models.Model):
    """
    Weight component for assessment formula
    This is an inline model for AssessmentFormula
    """
    assessment_formula = models.ForeignKey(
        AssessmentFormula,
        on_delete=models.CASCADE,
        related_name='weights'
    )

    # Name of the weight component
    name = models.ForeignKey(
        'AssessmentName',
        on_delete=models.CASCADE,
        help_text="Name of weight component (e.g., 'Continuous Assessment', 'Quiz', 'Assignments')"
    )

    # Weight value (percentage)
    weight = models.IntegerField(
        default=0,
        help_text="Weight percentage (e.g., 30 for 30%)"
    )

    # Display order
    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order"
    )

    # Is this weight component required?
    is_required = models.BooleanField(
        default=True,
        help_text="Is this weight component required for calculation?"
    )

    # Description (optional)
    description = models.TextField(
        blank=True,
        help_text="Optional description of this weight component"
    )

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Weight"
        verbose_name_plural = "Weights"
        # unique_together = ['assessment_formula', 'name']

    def __str__(self):
        return f"{self.name} ({self.weight}%)"

    def clean(self):
        """Validate weight component."""
        super().clean()

        if self.weight is None or not (0 <= self.weight <= 100):
            raise ValidationError({"weight": "Weight must be between 0 and 100."})

class SponsorshipType(models.Model):
    # id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=100, primary_key=True, unique=True)
    description = models.CharField(max_length=250)

    class Meta:
        verbose_name_plural = "Sponsorship types"

    def __str__(self):
        return "%s" % self.name
    
class TransportCategory(models.Model):
    # id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=100, primary_key=True, unique=True)
    description = models.CharField(max_length=250)

    class Meta:
        verbose_name_plural = "Transport categories"

    def __str__(self):
        return "%s" % self.name
    
class Fermata(models.Model):
    # id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=100, primary_key=True, unique=True)
    description = models.CharField(max_length=250)

    class Meta:
        verbose_name_plural = "Fermata"

    def __str__(self):
        return "%s" % self.name
    
class Registration(models.Model):
    type = (
		('Senior', 'Senior'),
  		('Fresh', 'Fresh'),
	)
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    type = models.CharField(max_length=50, choices=type)
    amount = models.DecimalField(decimal_places=2, max_digits=15)

    class Meta:
        verbose_name_plural = "Registration"

    def __str__(self):
        return "%s" % self.name
    
class Nutrition(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    grade = models.ForeignKey(Grade, on_delete=models.DO_NOTHING)
    amount = models.DecimalField(decimal_places=2, max_digits=15)

    class Meta:
        verbose_name_plural = "Nutrition"

    def __str__(self):
        return "%s" % self.name
    
class PenaltySchool(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=250)
    amount = models.DecimalField(decimal_places=2, max_digits=15)

    class Meta:
        verbose_name_plural = "School penalties"

    def __str__(self):
        return "%s" % self.name
    
class Other(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=250)
    amount = models.DecimalField(decimal_places=2, max_digits=15)

    class Meta:
        verbose_name_plural = "Others"

    def __str__(self):
        return "%s" % self.name
    
class TuitionFormula(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250, null=True, blank=True)
    grade = models.ForeignKey(Grade, on_delete=models.DO_NOTHING)
    amount = models.DecimalField(decimal_places=2, max_digits=15)
    
    class Meta:
        verbose_name_plural = "Tuition formula"

    def __str__(self):
        return "%s" % self.name
    
class TransportFormula(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250, null=True, blank=True)
    fermata = models.ForeignKey(Fermata, on_delete=models.DO_NOTHING)
    amount = models.DecimalField(decimal_places=2, max_digits=15)
    
    class Meta:
        verbose_name_plural = "Transport formula"

    def __str__(self):
        return "%s" % self.name
 
class AcademicFormula(models.Model):
    def get_current_year():
        try:
            current_year = Year.objects.get(status__iexact='Active')
            year = current_year.year
            return year
        except Year.DoesNotExist:
            return None
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250, null=True, blank=True)
    academic_year = models.CharField('የትምህርት ዘመን', max_length=50, default=get_current_year, null=True, blank=True) 
    grade = models.ForeignKey(Grade, on_delete=models.DO_NOTHING)
    pass_mark = models.DecimalField(decimal_places=2, max_digits=15)
    
    class Meta:
        verbose_name_plural = "Academic formula"

    def __str__(self):
        return "%s" % self.name
    
class Organization(models.Model):
	status = (
		('Active', 'Active'),
		('In Active', 'In Active'),
	)
	id = models.AutoField(primary_key=True, unique=True)
	name = models.CharField(max_length=100, unique=True)  
	description = models.CharField(max_length=250, blank=True, null=True)
	status = models.CharField(max_length=50, choices=status, default='Active')

	class Meta:
		verbose_name_plural = "Organizations"

	def __str__(self):
		return "%s" % self.name

class Department(models.Model):
	status = (
		('Active', 'Active'),
		('In Active', 'In Active'),
	)
	id = models.AutoField(primary_key=True, unique=True)
	organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
	name = models.CharField(max_length=100, unique=True)  
	description = models.CharField(max_length=250, blank=True, null=True)
	status = models.CharField(max_length=50, choices=status, default='Active')

	class Meta:
		verbose_name_plural = "Departments"

	def __str__(self):
		return "%s" % self.name

class Task(models.Model):
	status = (
		('Active', 'Active'),
		('In Active', 'In Active'),
	)
	id = models.AutoField(primary_key=True, unique=True)
	department = models.ForeignKey(Department, on_delete=models.CASCADE)
	name = models.CharField(max_length=100, unique=True)  
	description = models.CharField(max_length=250, blank=True, null=True)
	status = models.CharField(max_length=50, choices=status, default='Active')

	class Meta:
		verbose_name_plural = "Tasks"

	def __str__(self):
		return "%s" % self.name

class Measurement(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=250)
    value = models.PositiveIntegerField()
    
    class Meta:
        verbose_name_plural = "Measurements"

    def __str__(self):
        return "%s" % self.name
    
class ItemLists(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=100, unique=True)    
    description = models.CharField(max_length=250, blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Item lists"

    def __str__(self):
        return "%s" % self.name
   		
class Kebele(models.Model):
	status = (
        ('Active', 'Active'),
        ('In Active', 'In Active'),
    )
	id = models.AutoField(primary_key=True, unique=True)
	kebele = models.CharField(max_length=100, unique=True)  
	description = models.CharField(max_length=250, blank=True, null=True)
	status = models.CharField(max_length=50, choices=status)

	class Meta:
	    verbose_name_plural = "Kebeles"

	def __str__(self):
	    return "%s" % self.kebele

class ItemCategory(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=100, unique=True)    
    description = models.CharField(max_length=250, blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Item categories"

    def __str__(self):
        return "%s" % self.name

class ItemType(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    item_categories = models.ForeignKey(ItemCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=250)
    # status = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Item types"

    def __str__(self):
        return "%s" % self.name
    
class Vendor(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=100, unique=True)
    phone = models.CharField(max_length=250)
    email = models.EmailField()
    address = models.CharField(max_length=100)
    zone = models.CharField(max_length=100)
    kebele = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = "Vendors"

    def __str__(self):
        return "%s" % self.name
    
class Customer(models.Model):
    def get_current_month():
        try:
            current_month = Month.objects.get(is_current__iexact=True)
            return current_month
        except Month.DoesNotExist:
            return None
    
    def get_current_year():
        try:
            current_year = Year.objects.get(is_current__iexact=True)
            return current_year
        except Year.DoesNotExist:
            return None
        
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=100, unique=True)
    phone = models.CharField(max_length=250)
    email = models.EmailField()
    address = models.CharField(max_length=100)
    zone = models.CharField(max_length=100)
    kebele = models.CharField(max_length=100)
    # month = models.ForeignKey(Month, on_delete=models.CASCADE, related_name='c_months', default=get_current_month)
    # year = models.ForeignKey(Year, on_delete=models.CASCADE, related_name='c_years', default=get_current_year)
    
    class Meta:
        verbose_name_plural = "Customers"

    def __str__(self):
        return "%s" % self.name
