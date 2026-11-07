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

# Create your models here.
class StaffProfile(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    First_name = models.CharField(max_length = 150)
    Father_name = models.CharField(max_length = 150)
    Last_name = models.CharField(max_length = 150)
    Educational_level  = models.CharField(max_length = 150)
    Position  = models.CharField(max_length = 150)
    Employee_status = models.CharField(max_length = 150)
    Contact_number = models.CharField(max_length = 150)
    # image = models.ImageField(blank=True, null=True, upload_to="Staff_photo/%Y%M%D/")
    Registered_at = models.DateTimeField(auto_now=True, verbose_name="Registered at")
    Updated_by = CurrentUserField(related_name="up_by4")
    Registered_by = CurrentUserField(related_name="pl_by4")

    def __str__(self):
        return "%s" % (self.First_name)