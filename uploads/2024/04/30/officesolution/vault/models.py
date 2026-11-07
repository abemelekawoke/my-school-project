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

class VaultControl(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    Date = models.DateField('ቀን')
    Turned_total = models.CharField('የዞረ', max_length=150)
    Income = models.CharField('ገቢ', max_length=150)
    Total_income = models.CharField('ጠ/ገቢ', max_length=150)
    Cost = models.CharField('ወጪ', max_length=150)
    Balance = models.CharField('ከወጪ ቀሪ', max_length=150)
    
    Remark = models.CharField('ምርመራ', max_length = 150, blank=True)
    Registered_at = models.DateTimeField(auto_now=True, verbose_name="Registered at")
    Updated_by = CurrentUserField(related_name="ur1")
    Registered_by = CurrentUserField(related_name="rr1")
 
    def __str__(self):
        return "%s" % (self.id)

    class Meta:
        verbose_name="Vault Control"
        verbose_name_plural="Vault Controls"

    def save(self, *args, **kwargs):
        self.Total_price = self.Quantity * self.Individual_price
        super(Material, self).save(*args, **kwargs)