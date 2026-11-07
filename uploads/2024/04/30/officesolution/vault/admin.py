from django.db import models
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from django.shortcuts import redirect
from django.db import connection
from django.contrib import admin
from django.http import HttpResponse
from django.utils import timezone
import datetime
from datetime import datetime
from .models import *
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
# Register your models here.

class VaultControlAdmin(ImportExportModelAdmin):
	pass
	fieldsets = [
        ('General informations', {
            'fields': [('Turned_total','Date'),('Income','Total_income')],
        }),
        ('Detail information', {
            'fields': [('Cost','Balance')],
        }),
    ]
	list_display = ['id','Date', 'Turned_total', 'Income', 'Total_income', 'Cost', 'Balance', 'Remark','Registered_at','Updated_by','Registered_by']
	search_fields = ['id','Date', 'Turned_total', 'Income', 'Total_income', 'Cost', 'Balance', 'Remark','Registered_at','Updated_by','Registered_by']
	list_filter = ['Date']
	list_display_links = ['id','Date', 'Turned_total', 'Income', 'Total_income', 'Cost', 'Balance', 'Remark','Registered_at','Updated_by','Registered_by']
	readonly_fields = ('id','Registered_at','Updated_by','Registered_by')
	list_per_page = 10
	list_select_related = True
	class Meta:
		model = VaultControl	

	def save_model(self, request, obj, form, change):
		if change:
			obj.Updated_by = request.user
			obj.Registered_at = datetime.now()
		obj.save()

admin.site.register(VaultControl, VaultControlAdmin)