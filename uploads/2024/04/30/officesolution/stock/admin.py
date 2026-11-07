from django.db import models
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from django.shortcuts import redirect
from django.db import connection
from django.contrib import admin
# from django.conf.urls import url
# from django.conf.urls import url
# from django.urls import url
from django.http import HttpResponse
# import csv
from django.utils import timezone
import datetime
from datetime import datetime
from .models import *
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
# Register your models here.
class MaterialAdmin(ImportExportModelAdmin):
	pass
	fieldsets = [
        ('General informations', {
            'fields': [('Name','Model'),('Material_status','Remark')],
        }),
        ('Detail information', {
            'fields': [('Inch','Quantity','Individual_price')],
        }),
    ]
	list_display = ['id','Name','Inch','Model','Quantity','Individual_price','Total_price','Material_status','Remark','Registered_at','Updated_by','Registered_by']
	search_fields = ['id','Name','Inch','Model','Quantity','Individual_price','Total_price','Material_status','Remark','Registered_at','Updated_by','Registered_by']
	list_filter = ['Name','Inch']
	list_display_links = ['id','Name','Inch','Model','Quantity','Individual_price','Total_price','Material_status','Remark','Registered_at','Updated_by','Registered_by']
	readonly_fields = ('id','Total_price','Registered_at','Updated_by','Registered_by')
	list_per_page = 10
	list_select_related = True
	class Meta:
		model = StockManagement	

	def save_model(self, request, obj, form, change):
		if change:
			obj.Updated_by = request.user
			obj.Registered_at = datetime.now()
		obj.save()

admin.site.register(StockManagement, MaterialAdmin)