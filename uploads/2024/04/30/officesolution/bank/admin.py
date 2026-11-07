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

class BankBookAdmin(ImportExportModelAdmin):
	pass
	fields = [('id', 'Date'),('Deposite', 'Withdrawal'),('Balance'),('Registered_at','Updated_by','Registered_by')]
	list_display = ['id', 'Date', 'Deposite', 'Withdrawal', 'Balance', 'Registered_at', 'Updated_by', 'Registered_by']
	search_fields = ['id', 'Date', 'Deposite', 'Withdrawal', 'Balance', 'Registered_at', 'Updated_by', 'Registered_by']
	list_filter = ['Date']
	list_display_links = ['id', 'Date', 'Deposite', 'Withdrawal', 'Balance', 'Registered_at', 'Updated_by', 'Registered_by']
	readonly_fields = ('id','Balance','Registered_at','Updated_by','Registered_by')
	list_per_page = 10
	list_select_related = True
	class Meta:
		model = BankBook	

	def save_model(self, request, obj, form, change):
		if change:
			obj.Updated_by = request.user
			obj.Registered_at = datetime.now()
		obj.save()

admin.site.register(BankBook, BankBookAdmin) 