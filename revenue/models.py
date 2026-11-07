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
from student.models import *

class Revenue(models.Model):
    status = (
        ('Paid', 'Paid'),
        ('Not Paid', 'Not Paid'),
        ('Pending', 'Pending'),
    )
    
    def get_current_month():
        try:
            current_month = Month.objects.get(status__iexact='Active')
            month = current_month.month_english
            return month
        except Month.DoesNotExist:
            return None

    def get_current_year():
        try:
            current_year = Year.objects.get(status__iexact='Active')
            year = current_year.year
            return year
        except Year.DoesNotExist:
            return None

    id = models.AutoField(primary_key = True, unique = True)
    Student = models.ForeignKey(StudentProfile, on_delete=models.SET_NULL, null=True)
    Full_name = models.CharField(max_length=150, null=True, blank=True)
    # Grade = models.ForeignKey(Grade, on_delete=models.CASCADE, verbose_name='ደረጃ')
    # Section = models.ForeignKey(Section, on_delete=models.CASCADE, verbose_name='ክፍል')

    # Emergency_contact = models.CharField('የወላጅ ስ/ቁጥር', max_length = 150)
    # Transport_type = models.CharField('የትራንስፖርት ሁኔታ', max_length = 150)
    # Fermata = models.CharField('አድራሻ/ፌርማታ', max_length = 150)

    # Fee_amount = models.CharField('የክፍያ ሁኔታ', max_length = 150, null=True, blank=True)
    School_pay_date = models.CharField('ደረሰኝ የተቆረጠበት ቀን', max_length=100)
    
    month = models.CharField(max_length=50, default=get_current_month)
    year = models.CharField(max_length=50, default=get_current_year) 

    Registration = models.DecimalField('የምዝገባ', decimal_places=2, max_digits=15, default=0)
    Tuition = models.DecimalField('የትም/ት', decimal_places=2, max_digits=15, default=0)
    Transport = models.DecimalField('የትራንስፖርት', decimal_places=2, max_digits=15, default=0)
    Nutrition = models.DecimalField('የምገባ', decimal_places=2, max_digits=15, default=0)
    Penality = models.DecimalField('የቅጣት', decimal_places=2, max_digits=15, default=0)
    other = models.DecimalField('ልዩ ልዩ', decimal_places=2, max_digits=15, default=0)
    Total_fee = models.DecimalField('ጠ/ድምር', decimal_places=2, max_digits=15, default=0)

    Receipt_number = models.CharField('ደረሰኝ ቁጥር', max_length = 150, unique=True)

    Bank_pay_date = models.DateField('ባንክ የተከፈለበት ቀን', null=True, blank=True)
    status = models.CharField(max_length=50, choices=status, default='Pending')

    Updated_by = CurrentUserField(related_name="up_by11119")
    Updated_at = models.DateTimeField(auto_now=True)
    Registered_by = CurrentUserField(related_name="pl_by116711")

    def __str__(self):
        return self.Full_name
    
    # def __str__(self):
    #      return self.School_pay_date.strftime("%d/%m/%Y")
    
    # def __str__(self):
    #      return self.Bank_pay_date.strftime("%d/%m/%Y")

    class Meta:
        verbose_name="Revenue management"
        verbose_name_plural="Revenue managements"

    def save(self, *args, **kwargs):
        self.Total_fee = self.Registration + self.Tuition + self.Transport + self.Nutrition + self.Penality + self.other 
        super(Revenue, self).save(*args, **kwargs)
		
class InputDataPayment(models.Model):

	def get_current_year():
		try:
			current_year = Year.objects.get(status__iexact='Active')
			return current_year
		except Year.DoesNotExist:
			return None
        
	year = models.CharField(max_length=100, default=get_current_year)
	grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='cgrade')
	section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='csection') 

	def __str__(self):
		return f"Students of year: {self.year}, grade: {self.grade}"
        
class InputDataCurrentSeason(models.Model):
    
	def get_current_month_id():
		try:
			current_month = Month.objects.get(status__iexact='Active')
			return current_month.id
		except Month.DoesNotExist:
			return None
		
	def get_current_month():
		try:
			current_month = Month.objects.get(status__iexact='Active')
			return current_month
		except Month.DoesNotExist:
			return None
		
	def get_current_year_id():
		try:
			current_year = Year.objects.get(status__iexact='Active')
			return current_year.id
		except Year.DoesNotExist:
			return None

	def get_current_year():
		try:
			current_year = Year.objects.get(status__iexact='Active')
			return current_year
		except Year.DoesNotExist:
			return None
        
	mid = models.ForeignKey(Month, on_delete=models.CASCADE, related_name='zsmonthid', default=get_current_month_id)
	month = models.ForeignKey(Month, on_delete=models.CASCADE, related_name='zsmonth', default=get_current_month)
	yid = models.ForeignKey(Year, on_delete=models.CASCADE, related_name='zsyearid', default=get_current_year_id)
	year = models.ForeignKey(Year, on_delete=models.CASCADE, related_name='zsyear', default=get_current_year)
	grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='grade', null=True, blank=True)
	# section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='section', null=True, blank=True) 

	def __str__(self):
		return f"Month: {self.month}, Year: {self.year}"

class PaymentMonthlyReport(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    year = models.PositiveIntegerField()
    month = models.CharField(max_length=20)  # e.g., "January", "February"
    status = models.CharField(max_length=20, choices=[('Paid', 'Paid'), ('Pending', 'Pending')])
    total_transactions = models.PositiveIntegerField()
    total_registration_fees = models.DecimalField(max_digits=10, decimal_places=2)
    total_tuition_fees = models.DecimalField(max_digits=10, decimal_places=2)
    total_transport_fees = models.DecimalField(max_digits=10, decimal_places=2)
    total_nutrition_fees = models.DecimalField(max_digits=10, decimal_places=2)
    total_penalties = models.DecimalField(max_digits=10, decimal_places=2)
    total_other_fees = models.DecimalField(max_digits=10, decimal_places=2)
    total_collected_fees = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False  # This is a database view, not a Django-managed table
        db_table= "payment_monthly_report"
        verbose_name = "Payment Monthly Report"
        verbose_name_plural = "Payment Monthly Reports"
        ordering = ['year', 'month']

    def __str__(self):
        return f"{self.year} - {self.month} ({self.status})"