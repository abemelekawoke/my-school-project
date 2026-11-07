from import_export import resources
from django.db.models import Subquery, OuterRef
from django.db import connection
from django.db import models
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
from staff.models import StaffProfile
from django.db.models import Sum

# Create your models here.
class Loan(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    Name = models.ForeignKey(StaffProfile, on_delete=models.CASCADE)
    Date = models.DateField()
    Loan = models.DecimalField('Loan/ብድር', max_digits = 9, decimal_places = 2, blank=True, null=True)
    Balance = models.DecimalField(max_digits = 9, decimal_places = 2, blank=True, null=True)
    Registered_at = models.DateTimeField(auto_now=True, verbose_name="Registered at")
    Updated_by = CurrentUserField(related_name="up_by19")
    Registered_by = CurrentUserField(related_name="pl_by19")

    def __str__(self):
        return "%s" % (self.Name) 

    def save(self, *args, **kwargs): 
        if self.pk is None:  # Check if this is a new instance
            total_deposits = 0  # Set total deposits to zero for new instances
        else:
            # Get all related loan lines
            loan_lines = LoanInline.objects.filter(Loan=self)
            
            # Sum up all deposits associated with this loan
            total_deposits = loan_lines.aggregate(total_deposits=Sum('Deposite'))['total_deposits'] or 0

        # Calculate the balance
        self.Balance = self.Loan - total_deposits

        # Call the parent class's save method
        super(Loan, self).save(*args, **kwargs)

class LoanInline(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    Loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    Date = models.DateField()
    Deposite = models.DecimalField(max_digits = 9, decimal_places = 2, blank=True, null=True)
    Registered_at = models.DateTimeField(auto_now=True, verbose_name="Registered at")
    Updated_by = CurrentUserField(related_name="upd_by")
    Registered_by = CurrentUserField(related_name="re_by")

    def __str__(self):
        return "%s" % (self.id)