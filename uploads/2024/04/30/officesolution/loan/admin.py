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

class LoanInline(admin.TabularInline):
    model = LoanInline
    extra = 0
    list_filter = ['Date']
    readonly_fields=('id','Registered_at','Updated_by','Registered_by')

class LoanAdmin(ImportExportModelAdmin):
	pass     
	inlines = [LoanInline]
	fields = [('id'), ('Date'), ('Name', 'Loan'), ('Balance'), ('Registered_at','Updated_by','Registered_by')]
	list_display = ['id', 'Date', 'Name', 'Loan', 'Balance', 'Registered_at', 'Updated_by', 'Registered_by']
	search_fields = ['id', 'Date', 'Name', 'Registered_at', 'Updated_by', 'Registered_by']
	list_filter = ['Date']
	list_display_links = ['id', 'Date', 'Name', 'Loan', 'Balance', 'Registered_at', 'Updated_by', 'Registered_by']
	readonly_fields = ('id','Balance','Registered_at','Updated_by','Registered_by')
	list_per_page = 10
	list_select_related = True

	def response_add(self, request, new_object):
		obj = self.after_saving_model_and_related_inlines(new_object)
		return super(LoanAdmin, self).response_add(request, obj)

	def response_change(self, request, obj):
		obj = self.after_saving_model_and_related_inlines(obj)
		return super(LoanAdmin, self).response_change(request, obj)

	def after_saving_model_and_related_inlines(self, obj):
	    if obj.pk:
	        loan_lines = obj.loaninline_set.all()  # Retrieve related LoanInline instances
	        total_deposits = loan_lines.aggregate(total_deposits=Sum('Deposite'))['total_deposits'] or 0
	        obj.Balance = obj.Loan - total_deposits
	        obj.save()  # Save the updated object
	    return obj

    	# invoice_lines = NewInternalOrder.objects.filter(Total_price=obj.pk)
    	# obj.Item_total_price = 0
    	# for line in invoice_lines:
    	# 	obj.Item_total_price += line.Total_price

    	# obj.save()
    	# return obj

	class Meta:
		model = Loan	

	def save_model(self, request, obj, form, change):
		if change:
			obj.Updated_by = request.user
			obj.Registered_at = datetime.now()
		obj.save()

admin.site.register(Loan, LoanAdmin) 