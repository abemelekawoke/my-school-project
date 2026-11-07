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

class StockManagement(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    Name = models.CharField(max_length = 150)
    Inch = models.PositiveIntegerField()
    Model = models.CharField(max_length = 150)
    Quantity = models.PositiveIntegerField()
    Individual_price = models.PositiveIntegerField()
    Total_price = models.PositiveIntegerField()
    Material_status = models.CharField(max_length = 150)
    Remark = models.CharField(max_length = 150, blank=True)
    Registered_at = models.DateTimeField(auto_now=True, verbose_name="Registered at")
    Updated_by = CurrentUserField(related_name="up_by5")
    Registered_by = CurrentUserField(related_name="pl_by5")

    def __str__(self):
        return "%s" % (self.id)

    class Meta:
        verbose_name="Stock Management"
        verbose_name_plural="Stock Management"

    def save(self, *args, **kwargs):
        self.Total_price = self.Quantity * self.Individual_price
        super(Material, self).save(*args, **kwargs)