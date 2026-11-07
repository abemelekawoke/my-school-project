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
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.
class BankBook(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    Date = models.DateField()
    Deposite = models.DecimalField(max_digits = 9, decimal_places = 2, blank=True, null=True, default=0)
    Withdrawal = models.DecimalField(max_digits = 9, decimal_places = 2, blank=True, null=True, default=0)
    Balance = models.DecimalField(max_digits = 9, decimal_places = 2, blank=True, null=True, default=0)
    Registered_at = models.DateTimeField(auto_now=True, verbose_name="Registered at")
    Updated_by = CurrentUserField(related_name="up_by44")
    Registered_by = CurrentUserField(related_name="pl_by44")

    def __str__(self):
        return "%s" % (self.id)


    def save(self, *args, **kwargs):
        try:
            previous_balance = BankBook.objects.latest('id').Balance
        except ObjectDoesNotExist:
            # If no BankBook records exist, set previous_balance to 0
            previous_balance = 0

        # Ensure previous_balance is not None
        if previous_balance is None:    
            previous_balance = 0

        # Update balance based on previous balance, deposite, and withdrawal
        self.Balance = previous_balance + self.Deposite - self.Withdrawal

        super(BankBook, self).save(*args, **kwargs)