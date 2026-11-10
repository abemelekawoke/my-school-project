# from import_export import resources
# from django.db.models import Subquery, OuterRef
# from django.db import connection
# from django.db import models
# from django.utils import timezone
# from decimal import Decimal
# import datetime
# from datetime import datetime
# from django.conf import settings
# from django.contrib.auth.models import User
# from django_currentuser.middleware import (
#     get_current_user, get_current_authenticated_user)
# from django_currentuser.db.models import CurrentUserField
# from django.urls import reverse
# from django.http import HttpResponse
# from django.core.exceptions import ObjectDoesNotExist
# from setups.models import *
# # from stocks.models import *
# # from employees.models import *

# class GeneralLeisure(models.Model):
#     id = models.AutoField(primary_key = True, unique = True)
#     Dates = models.DateField('Date')
#     Tasks = models.CharField(max_length = 150)
#     Year = models.ForeignKey(Year, on_delete=models.CASCADE)
#     Month = models.ForeignKey(Month, on_delete=models.CASCADE)
#     General = models.PositiveIntegerField(default=0)
#     Check_no = models.PositiveIntegerField(default=0)
#     Check_payable = models.PositiveIntegerField(default=0)
#     Receipt_no = models.CharField(max_length = 250,default=0)
#     Deposit = models.DecimalField(decimal_places=2, max_digits=25, default=0)
#     Withdraw = models.DecimalField(decimal_places=2, max_digits=25, default=0)
#     Balance = models.DecimalField(decimal_places=2, max_digits=25, default=0)
#     Registered_date = models.CharField(max_length=150, verbose_name="Registered at")
#     Updated_by = CurrentUserField(related_name="up_by1111")
#     Registered_by = CurrentUserField(related_name="pl_by1111")
#     def __str__(self):
#         return "%s" % (self.Tasks)
#     class Meta:
#         verbose_name="General leisure"
#         verbose_name_plural="General leisure"

#     def save(self, *args, **kwargs):
#         try:
#             previous_balance = GeneralLeisure.objects.latest('id').Balance
#         except ObjectDoesNotExist:
#             # If no BankBook records exist, set previous_balance to 0
#             previous_balance = 0

#         # Ensure previous_balance is not None
#         if previous_balance is None:    
#             previous_balance = 0

#         # Update balance based on previous balance, deposite, and withdrawal
#         self.Balance = previous_balance + self.Deposit - self.Withdraw

#         super(GeneralLeisure, self).save(*args, **kwargs)
        
# class RevenueType(models.Model):
#     id = models.AutoField(primary_key = True, unique = True)
#     Dates = models.DateField('Date')
#     department = models.ForeignKey(Department, on_delete=models.CASCADE)
#     Code = models.CharField(max_length = 150)
#     Revenue_title_amharic = models.ForeignKey(Task, on_delete=models.CASCADE)
#     Revenue_title_english = models.CharField(max_length = 150, default='None')

#     Revenue_annual_plan = models.DecimalField(max_digits=30, decimal_places=2, blank=True, null=True)
#     Measurement = models.ForeignKey(Measurement, on_delete=models.CASCADE)
#     Year = models.ForeignKey(Year, on_delete=models.CASCADE)

#     Registered_date = models.CharField(max_length=150,verbose_name="Registered at")
#     Updated_by = CurrentUserField(related_name="up_by11111")
#     Registered_by = CurrentUserField(related_name="pl_by11111")
  
#     def __str__(self):
#         return "%s" % (self.Code)

#     class Meta:
#         verbose_name="Revenue plan"
#         verbose_name_plural="Revenue plan"

# class AllRevenue(models.Model):
#     id = models.AutoField(primary_key = True, unique = True)
#     Dates = models.DateField('Date')
#     Code = models.ForeignKey(RevenueType, on_delete=models.CASCADE)
#     Amount = models.DecimalField(decimal_places=2, max_digits=25, default=0)
#     Year = models.ForeignKey(Year, on_delete=models.CASCADE)
#     Month = models.ForeignKey(Month, on_delete=models.CASCADE)

#     Registered_date = models.CharField(max_length=150,verbose_name="Registered at")
#     Updated_by = CurrentUserField(related_name="up_by111111")
#     Registered_by = CurrentUserField(related_name="pl_by111111")

#     def __str__(self):
#         return "%s" % (self.Code)

#     class Meta:
#         verbose_name="Revenue performed"
#         verbose_name_plural="Revenue performed"

#     # def save(self, *args, **kwargs):
#     #     br = RevenueReport.objects.get(id=self.Code_id)
#     #     getbal = br.Balances
#     #     if getbal == None:
#     #         getbal=0
#     #     self.Balance = getbal + self.Amount
#     #     super(AllRevenue, self).save(*args, **kwargs)

# class ExpenseType(models.Model):
#     id = models.AutoField(primary_key = True, unique = True)
#     Dates = models.DateField('Date')
#     department = models.ForeignKey(Department, on_delete=models.CASCADE)
#     Code = models.CharField(max_length = 150)
#     Expense_title_amharic = models.ForeignKey(Task, on_delete=models.CASCADE)
#     Expense_title_english = models.CharField(max_length = 150, default='None')

#     Expense_annual_plan = models.DecimalField(max_digits=30, decimal_places=2, blank=True, null=True)
#     Measurement = models.ForeignKey(Measurement, on_delete=models.CASCADE)
#     Year = models.ForeignKey(Year, on_delete=models.CASCADE)

#     Registered_date = models.CharField(max_length=150,verbose_name="Registered at")
#     Updated_by = CurrentUserField(related_name="up_by1111111")
#     Registered_by = CurrentUserField(related_name="pl_by1111111")

#     def __str__(self):
#         return "%s" % (self.Code)

#     class Meta:
#         verbose_name="Expense plan"
#         verbose_name_plural="Expense plan"

# class AllExpense(models.Model):
#     id = models.AutoField(primary_key = True, unique = True)
#     Dates = models.DateField('Date')
#     Code = models.ForeignKey(ExpenseType, on_delete=models.CASCADE)
#     Amount = models.DecimalField(decimal_places=2, max_digits=25, default=0)
#     Year = models.ForeignKey(Year, on_delete=models.CASCADE)
#     Month = models.ForeignKey(Month, on_delete=models.CASCADE)

#     Registered_date = models.CharField(max_length=150, verbose_name="Registered at")
#     Updated_by = CurrentUserField(related_name="up_by11111111")
#     Registered_by = CurrentUserField(related_name="pl_by11111111")

#     def __str__(self):
#         return "%s" % (self.Code)

#     class Meta:
#         verbose_name="Expense performed"
#         verbose_name_plural="Expense performed" 

# class DepartmentPerformanceRank(models.Model):
#     id = models.AutoField(primary_key = True, unique = True)
#     department = models.CharField(max_length = 150)
#     month = models.CharField(max_length = 150)
#     year = models.CharField(max_length = 150)
#     total_plan = models.CharField(max_length = 150) 
#     total_performed = models.CharField(max_length = 150) 
#     performance_percentage = models.CharField(max_length = 150)
#     rank = models.CharField(max_length=100)
 
#     def __str__(self):
#         return "%s" % (self.id)

#     class Meta:
#         managed = False
#         # verbose_name = "የስራ ሂደት የአፈጻጸም ደረጃ"
#         # verbose_name_plural = "የስራ ሂደት የአፈጻጸም ደረጃ"
#         db_table = "DEPARTMENTPERFORMANCERANK"