# # from django.db import models
# from import_export.admin import ImportExportModelAdmin
# from django.contrib import admin
# from django.shortcuts import redirect
# from django.db import connection

# from django.http import HttpResponse
# # import csv
# from django.utils import timezone
# import datetime
# from datetime import datetime
# from .models import *
# from django.contrib.contenttypes.models import ContentType
# from django.http import HttpResponseRedirect
# from decimal import Decimal
# # from django.contrib.auth.models import Group

# class GeneralLeisureAdmin(ImportExportModelAdmin):
#     pass
#     fieldsets = [
#         ('General informations', {
#             'fields': [('Tasks','Dates'),('Year', 'Month'), ('General','Check_no','Check_payable','Receipt_no')],
#         }), 
# 		('Detail information', {
# 			'fields': [('Deposit','Withdraw','Balance')],
# 		}),
#     ]
#     list_display = ['id','Dates','Tasks','Deposit','Withdraw','Balance','General','Check_no','Receipt_no']
#     search_fields = ['id','Dates','Tasks','Deposit','Withdraw','Balance','General','Check_no','Receipt_no']
#     list_filter = ['Dates', 'Year', 'Month']
#     list_display_links = ['id','Dates','Tasks','Deposit','Withdraw','Balance','General','Check_no','Receipt_no']
#     readonly_fields = ('id','Balance','Registered_date','Updated_by','Registered_by')
#     list_per_page = 10
#     list_select_related = True
#     class Meta:
# 	    model = GeneralLeisure	

#     def save_model(self, request, obj, form, change):
# 	    if change:
# 		    obj.Update_by = request.user
# 		    obj.Registered_date = datetime.now()
# 	    obj.save()

# admin.site.register(GeneralLeisure, GeneralLeisureAdmin)

# class RevenueTypeAdmin(ImportExportModelAdmin):
#     pass
#     fieldsets = [
#         ('General informations', {
#             'fields': [('Dates', 'department'), ('Code'), ('Measurement', 'Year')],
#         }), 
# 		('Detail information', {
# 			'fields': [('Revenue_title_amharic','Revenue_title_english'), 'Revenue_annual_plan'],
# 		}),
#     ]
#     list_display = ['id','Dates','department','Code','Measurement', 'Year', 'Revenue_title_amharic','Revenue_title_english','Revenue_annual_plan']
#     search_fields = ['id','Dates','department','Code','Revenue_title_amharic','Revenue_title_english', 'Year']
#     list_filter = ['department__name', 'Code', 'Year']
#     list_display_links = ['id','Dates','department','Code','Measurement', 'Year', 'Revenue_title_amharic','Revenue_title_english','Revenue_annual_plan']
#     readonly_fields = ('id','Registered_date','Updated_by','Registered_by')
#     list_per_page = 10
#     list_select_related = True
#     class Meta:
# 	    model = RevenueType	

#     def save_model(self, request, obj, form, change):
# 	    if change:
# 		    obj.Update_by = request.user
# 		    obj.Registered_date = datetime.now()
# 	    obj.save()

# admin.site.register(RevenueType, RevenueTypeAdmin)

# class RevenueAdmin(ImportExportModelAdmin):
#     pass
#     fieldsets = [
#         ('General informations', {
#             'fields': [('Dates','Code'), ('Year', 'Month')],
#         }), 
# 		('Detail information', {
# 			'fields': ['Amount'],
# 		}),
#     ]
#     list_display = ['id','Dates','Year', 'Month','Code','Amount']
#     search_fields = ['id','Dates','Code','Amount', 'Year']
#     list_filter = ['Dates']
#     list_display_links = ['id','Dates','Year', 'Month','Code','Amount']
#     readonly_fields = ('id','Registered_date','Updated_by','Registered_by')
#     list_per_page = 10
#     list_select_related = True
#     class Meta:
# 	    model = AllRevenue	

#     def save_model(self, request, obj, form, change):
# 	    if change:
# 		    obj.Update_by = request.user
# 		    obj.Registered_date = datetime.now()
# 	    obj.save()

# admin.site.register(AllRevenue, RevenueAdmin)

# class ExpenseTypeAdmin(ImportExportModelAdmin):
#     pass
#     fieldsets = [
#         ('General informations', {
#             'fields': [('Dates', 'department'), ('Code'), ('Measurement', 'Year')],
#         }), 
# 		('Detail information', {
# 			'fields': [('Expense_title_amharic','Expense_title_english'), 'Expense_annual_plan'],
# 		}),
#     ]
#     list_display = ['id','Dates','department','Code','Measurement', 'Year', 'Expense_title_amharic','Expense_title_english', 'Expense_annual_plan']
#     search_fields = ['id','Dates','department','Code','Year', 'Expense_title_amharic','Expense_title_english']
#     list_filter = ['department__name', 'Code', 'Year']
#     list_display_links = ['id','Dates','department','Measurement', 'Year','Code','Expense_title_amharic','Expense_title_english', 'Expense_annual_plan']
#     readonly_fields = ('id','Registered_date','Updated_by','Registered_by')
#     list_per_page = 10
#     list_select_related = True
#     class Meta:
# 	    model = ExpenseType	

#     def save_model(self, request, obj, form, change):
# 	    if change:
# 		    obj.Update_by = request.user
# 		    obj.Registered_date = datetime.now()
# 	    obj.save()

# admin.site.register(ExpenseType, ExpenseTypeAdmin)

# class ExpenseAdmin(ImportExportModelAdmin):
#     pass
#     fieldsets = [
#         ('General informations', {
#             'fields': [('Dates','Code'),('Year', 'Month')],
#         }), 
# 		('Detail information', {
# 			'fields': ['Amount'],
# 		}),
#     ]
#     list_display = ['id','Dates','Year', 'Month','Code','Amount']
#     search_fields = ['id','Dates','Code','Amount']
#     list_filter = ['Dates']
#     list_display_links = ['id','Dates','Year', 'Month','Code','Amount']
#     readonly_fields = ('id','Registered_date','Updated_by','Registered_by')
#     list_per_page = 10
#     list_select_related = True
#     class Meta:
# 	    model = AllExpense	

#     def save_model(self, request, obj, form, change):
# 	    if change:
# 		    obj.Update_by = request.user
# 		    obj.Registered_date = datetime.now()
# 	    obj.save()

# admin.site.register(AllExpense, ExpenseAdmin)

# class DepartmentPerformanceRankAdmin(ImportExportModelAdmin):
#     # pass
#     fields = [('id'), ('department'), ('month', 'year'), ('total_plan', 'total_performed'), ('performance_percentage', 'rank')]
#     list_display = ['id', 'department', 'rank', 'month', 'year', 'total_plan', 'total_performed', 'performance_percentage']
#     search_fields = ['department']
#     list_filter = ['department', 'month', 'year']
#     list_display_links = ['id', 'department', 'month', 'year', 'total_plan', 'total_performed', 'performance_percentage', 'rank']
#     readonly_fields = ('id',)
#     list_per_page = 10
#     list_select_related = True

#     class Meta:
#         model = DepartmentPerformanceRank

# admin.site.register(DepartmentPerformanceRank, DepartmentPerformanceRankAdmin)
