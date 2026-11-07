from import_export import resources
from django.db.models import Subquery, OuterRef
from django.db import connection
from django.utils import timezone
import datetime
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)
from django_currentuser.db.models import CurrentUserField
from django.urls import reverse
from django.http import HttpResponse
from django.utils.timezone import now
from datetime import date

# Create your models here.
from django.db import models, transaction
import django_currentuser.db.models.fields
from django.conf import settings
import django.db.models.deletion
# from setups.models import *
class StaffProfile(models.Model):
    MARITAL_STATUS_CHOICES = [
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
    ]

    EMPLOYEE_STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('terminated', 'Terminated'),
        ('retired', 'Retired'),
    ]

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    SCHOOL_CHOICES = (
        ('#1', 'ቁጥር 1'),
        ('#2', 'ቁጥር 2'),
    )
    CYCLE_CHOICES = (
        ('KG', 'KG'),
        ('1-8', '1-8'),
        ('9-12', '9-12'),
    )
    
    educational_level_choices = [
        ('PhD', 'PhD'),
        ('Masters', 'Masters'),
        ('Bachelors', 'Bachelors'),
        ('Diploma', 'Diploma'),
        ('Certificate', 'Certificate'),
    ]

    id = models.AutoField(primary_key=True)
    full_name_am = models.CharField('ሙሉ ስም', max_length=150)
    full_name_en = models.CharField('Full name', max_length=150)
    gender = models.CharField('ጾታ', max_length=150, choices=GENDER_CHOICES)
    date_of_birth = models.CharField('የትውልድ ቀን', max_length=100, null=True, blank=True)
    marital_status = models.CharField('የጋብቻ ሁኔታ', max_length=10, choices=MARITAL_STATUS_CHOICES, default='single')
    nationality = models.CharField('ዜግነት', max_length=100, default='Ethiopian')
    hired_date = models.CharField('የቅጥር ቀን', max_length=100, null=True, blank=True)  # Changed to DateField for proper date storage
    teaching_certificate = models.CharField('የመምህርነት ማዕረግ', max_length=150)
    work_cycles = models.CharField('የሚሰሩበት ሳይክል', max_length=100, choices=CYCLE_CHOICES,)
    school = models.CharField(max_length=50, choices=SCHOOL_CHOICES, default='#1', verbose_name='የሚሰራበት ት/ት ቤት', null=True, blank=True) 
    career_growth = models.CharField('ያደጉበት ሁኔታ', max_length=100)
    previous_growth_hired = models.CharField('ቀድም ሲል ያደጉበት/የተቀጠሩበት ጊዜ', max_length=100)  
    contact_number = models.CharField('ስልክ', max_length=15)
    email = models.EmailField('ኢሜል', max_length=254, unique=True)
    specialization = models.CharField('የትምህርት አይነት', max_length=200)
    educational_level = models.CharField('የትምህርት ደረጃ', max_length=150, choices=educational_level_choices)
    job_grade = models.CharField('የስራ ደረጃ', max_length=150)
    position = models.CharField('ኃላፊነት', max_length=150)
    salary = models.DecimalField('ደሞዝ', max_digits=10, decimal_places=2, default=0.00)
    employee_status = models.CharField('የስራ ሁኔታ', max_length=10, choices=EMPLOYEE_STATUS_CHOICES, default='active')
    profile_picture = models.ImageField('ፎቶ ግራፍ', upload_to='profile_pictures/', blank=True, null=True)
    registered_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    registered_by = models.ForeignKey(User, related_name='staff_registered', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name='staff_updated', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.full_name_am} {self.full_name_en}"

    class Meta:
        verbose_name = "Academic Staff Profile"
        verbose_name_plural = "Academic Staff Profiles"
        # db_table = 'staff_profile'  # Uncomment if you need a custom table name
 
class AdminStaffProfile(models.Model):
    MARITAL_STATUS_CHOICES = [
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
    ]

    EMPLOYEE_STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('terminated', 'Terminated'),
        ('retired', 'Retired'),
    ]

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    SCHOOL_CHOICES = (
        ('#1', 'ቁጥር 1'),
        ('#2', 'ቁጥር 2'),
    )
      
    educational_level_choices = [
        ('PhD', 'PhD'),
        ('Masters', 'Masters'),
        ('Bachelors', 'Bachelors'),
        ('Diploma', 'Diploma'),
        ('Certificate', 'Certificate'),
    ]

    id = models.AutoField(primary_key=True)
    full_name_am = models.CharField('ሙሉ ስም', max_length=150, null=True, blank=True)
    full_name_en = models.CharField('Full name', max_length=150)
    gender = models.CharField('ጾታ', max_length=150, choices=GENDER_CHOICES)
    date_of_birth = models.CharField('የትውልድ ቀን', max_length=100, null=True, blank=True)
    marital_status = models.CharField('የጋብቻ ሁኔታ', max_length=10, choices=MARITAL_STATUS_CHOICES, default='single', null=True, blank=True)
    nationality = models.CharField('ዜግነት', max_length=100)
    hired_date = models.CharField('የቅጥር ቀን', max_length=100, null=True, blank=True)  # Changed to CharField for proper date storage
    school = models.CharField(max_length=50, choices=SCHOOL_CHOICES, default='#1', verbose_name='የሚሰራበት ት/ት ቤት', null=True, blank=True)         
    contact_number = models.CharField('ስልክ', max_length=15, null=True, blank=True)
    email = models.EmailField('ኢሜል', max_length=254, unique=True, null=True, blank=True)
    job_title = models.CharField('የስራ መደብ መጠሪያ', max_length=150)
    new_job_code = models.CharField(max_length=100, verbose_name="አዲሱ የሥራ መደብ መታ.ቁጥር")
    job_grade = models.CharField(max_length=50, verbose_name="አዲሱ ደረጃ")
    rank = models.CharField(max_length=50, verbose_name="እርከን")
    educational_level = models.CharField('የትምህርት ደረጃ', max_length=150, choices=educational_level_choices, null=True, blank=True)
    position = models.CharField('ኃላፊነት', max_length=150, null=True, blank=True)
    salary = models.DecimalField('ደሞዝ', max_digits=10, decimal_places=2, default=0.00)
    employee_status = models.CharField('የስራ ሁኔታ', max_length=10, choices=EMPLOYEE_STATUS_CHOICES, default='active')
    profile_picture = models.ImageField('ፎቶ ግራፍ', upload_to='profile_pictures/', blank=True, null=True)
    registered_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    registered_by = models.ForeignKey(User, related_name='admin_staff_registered', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name='admin_staff_updated', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.full_name_am} {self.full_name_en}"

    class Meta:
        verbose_name = "Admin Staff Profile"
        verbose_name_plural = "Admin Staff Profiles"
        # db_table = 'staff_profile'  # Uncomment if you need a custom table name
  
class Experience(models.Model):
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, related_name="experiences")
    admin = models.ForeignKey(AdminStaffProfile, on_delete=models.CASCADE, related_name="admin_experiences")
    institution = models.CharField(max_length=200)
    from_date = models.DateField()
    to_date = models.DateField()
    position = models.CharField(max_length=150)
    net_duration = models.CharField(max_length=50, blank=True, null=True)  # Will be auto-calculated

    def save(self, *args, **kwargs):
        """Automatically calculate the net duration in years, months, and days"""
        if self.from_date and self.to_date:
            delta = self.to_date - self.from_date
            years = delta.days // 365
            months = (delta.days % 365) // 30
            days = (delta.days % 365) % 30
            self.net_duration = f"{years} years, {months} months, {days} days"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee.full_name_en} - {self.position} at {self.institution}"

    class Meta:
        ordering = ["-to_date"]
        verbose_name = "Experience"
        verbose_name_plural = "Experiences"

class LeaveRequest(models.Model):
    LEAVE_TYPE_CHOICES = [
        ('Sick Leave', 'Sick Leave'),
        ('Casual Leave', 'Casual Leave'),
        ('Vacation Leave', 'Vacation Leave'),
    ]
    
    Leave = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    id = models.AutoField(primary_key=True, unique=True)
    employee = models.ForeignKey(StaffProfile, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=50, choices=LEAVE_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=Leave, default='Pending')  # e.g., Pending, Approved, Rejected
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.employee} - {self.leave_type} ({self.status})"
    
class OpenPosition(models.Model):
    educational_level_choices = [
        ('PhD', 'PhD'),
        ('Masters', 'Masters'),
        ('Bachelors', 'Bachelors'),
        ('Diploma', 'Diploma'),
        ('Certificate', 'Certificate'),
    ]
    
    STATUS_CHOICES = [
        ('open', 'ክፍት'),
        ('closed', 'ዝግ'),
    ]

    id = models.AutoField(primary_key=True, verbose_name="መታወቂያ")
    job_title = models.CharField(max_length=255, verbose_name="የሥራ መደብ መጠሪያ")
    new_job_code = models.CharField(max_length=100, verbose_name="አዲሱ የሥራ መደብ መታ.ቁጥር")
    current_rank = models.CharField('የት/ደረጃ ደረጃ', max_length=150, choices=educational_level_choices)
    new_rank = models.CharField('አዲሱ ደረጃ', max_length=100)
    rank = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="እርከን")
    salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="ደመወዝ")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open', verbose_name="ሁኔታ")
    notes = models.TextField(blank=True, null=True, verbose_name="ማብራሪያ")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="የተፈጠረበት ቀን")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="የተቀየረበት ቀን")

    def __str__(self):
        return f"{self.job_title} ({self.new_job_code})"

    class Meta:
        # verbose_name = "ክፍት የሥራ መደብ"
        # verbose_name_plural = "ክፍት የሥራ መደቦች"
        ordering = ['-created_at']
