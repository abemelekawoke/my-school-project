# from import_export.admin import ImportExportModelAdmin
# from django.contrib import admin
# from django.shortcuts import redirect
# from django.db import connection, transaction

# from django.http import HttpResponse
# # import csv
# from django.utils import timezone
# import datetime
# from datetime import datetime
# from .models import *
# from django.contrib.contenttypes.models import ContentType
# from django.http import HttpResponseRedirect
# from decimal import Decimal
# from django.contrib import messages
# from django import forms
# # Register your models here.
# from django.contrib import admin
# from import_export.admin import ImportExportModelAdmin
# from datetime import datetime

# from django.utils.html import format_html

# # class RevenueAdmin(ImportExportModelAdmin):
# #     # Organize the fieldsets for better grouping of related fields
# #     fieldsets = [
# #         ('General Information', {
# #             'fields': [
# #                 'id', 'Student', 'Full_name', 
# #                 ('month', 'year'), 
# #                 'School_pay_date', 'Bank_pay_date', 
# #                 'Receipt_number', 'Total_fee'
# #             ],
# #             'description': 'Details about the student and payment dates.'
# #         }),
# #         ('Payment Information', {
# #             'fields': [
# #                 ('Registration', 'Tuition', 'Transport'), 
# #                 ('Nutrition', 'Penality', 'other', 
# #                 'status')
# #             ],
# #             'description': 'Breakdown of payment components.'
# #         }),
# #         ('Audit Trail', {
# #             'fields': ['Updated_by', 'Updated_at'],
# #             'description': 'Automatic fields for tracking changes.',
# #         }),
# #     ]
    
# #     # Display fields for listing page
# #     list_display = [
# #         'Student__id', 'Total_fee', 'status', 'Receipt_number', 'School_pay_date', 
# #         'Bank_pay_date', 'Student', 'month', 'year', 
# #     ]
    
# #     # Fields to search
# #     search_fields = ('Full_name', 'Student__id',)
    
# #     # Fields to filter by
# #     list_filter = ['status', 'month', 'year', 'School_pay_date', 'Bank_pay_date', 'Updated_at']
    
# #     # Clickable links
# #     list_display_links = ['Student__id', 'month', 'year', 'Total_fee']
    
# #     # Editable fields in the list view
# #     list_editable = [
# #         'status', 'School_pay_date', 'Receipt_number', 'Bank_pay_date'
# #     ]
    
# #     # Read-only fields
# #     readonly_fields = ['id', 'Total_fee', 'Updated_by', 'Updated_at']
    
# #     # Pagination and performance optimization
# #     list_per_page = 25  # Adjusted for better usability
# #     list_select_related = True  # Optimizes queries for related fields

# #     # Add custom CSS for styling
# #     class Media:
# #         css = {
# #             'all': ('css/admin_custom.css',)
# #         }

# #     # Custom save logic to track modifications
# #     def save_model(self, request, obj, form, change):
# #         if change:  # Only update these fields on change
# #             obj.Updated_by = request.user
# #             obj.Updated_at = datetime.now()
# #         obj.save()

# #     class Meta:
# #         model = Revenue

# # # Register the customized admin
# # admin.site.register(Revenue, RevenueAdmin)
# class RevenueAdmin(ImportExportModelAdmin):
#     fieldsets = [
#         ('General Information', {
#             'fields': [
#                 'id', 'Student', 'Full_name', 
#                 ('month', 'year'), 
#                 'School_pay_date', 'Bank_pay_date', 
#                 'Receipt_number', 'Total_fee'
#             ],
#             'description': 'Details about the student and payment dates.'
#         }),
#         ('Payment Information', {
#             'fields': [
#                 ('Registration', 'Tuition', 'Transport'), 
#                 ('Nutrition', 'Penality', 'other', 
#                 'status')
#             ],
#             'description': 'Breakdown of payment components.'
#         }),
#         ('Audit Trail', {
#             'fields': ['Updated_by', 'Updated_at'],
#             'description': 'Automatic fields for tracking changes.',
#         }),
#     ]
    
#     list_display = [
#         'Student__id', 'Total_fee', 'status', 'Receipt_number', 'School_pay_date', 
#         'Bank_pay_date', 'Student', 'month', 'year', 
#     ]
    
#     search_fields = ('Full_name', 'Student__id',)
    
#     list_filter = ['status', 'month', 'year', 'School_pay_date', 'Bank_pay_date', 'Updated_at']
    
#     list_display_links = ['Student__id', 'month', 'year', 'Total_fee']
    
#     list_editable = [
#         'status', 'School_pay_date', 'Receipt_number', 'Bank_pay_date'
#     ]
    
#     readonly_fields = ['id', 'Total_fee', 'Updated_by', 'Updated_at']
    
#     list_per_page = 12  
#     list_select_related = True

#     class Media:
#         css = {
#             'all': ('css/admin_custom.css',)
#         }

#     def save_model(self, request, obj, form, change):
#         if change:
#             obj.Updated_by = request.user
#             obj.Updated_at = datetime.now()
#         obj.save()

#     # =======================
#     # ADD UNPAID PAYMENT ALERT HERE
#     # =======================
#     def get_unpaid_count(self):
#         return Revenue.objects.filter(status__in=['Not Paid', 'Pending']).count()

#     def changelist_view(self, request, extra_context=None):
#         unpaid_count = self.get_unpaid_count()
#         extra_context = extra_context or {}
#         extra_context['title'] = format_html(
#             '<b>Revenue Management</b> | <span style="color:red;">Unpaid Payments: {}</span>',
#             unpaid_count
#         )
#         return super().changelist_view(request, extra_context=extra_context)

#     class Meta:
#         model = Revenue

# admin.site.register(Revenue, RevenueAdmin)

# # class InputDataCurrentSeasonForm(forms.ModelForm):
# #     class Meta:
# #         model = InputDataCurrentSeason
# #         fields = ['month', 'year']
# #         # fields = ['uploaded_file']
# #         widgets = {
# #             'mid_id': forms.HiddenInput(),
# #             'yid_id': forms.HiddenInput(),
# #         }
        
# # class InputDataCurrentSeasonAdmin(admin.ModelAdmin):
# #     actions = ['run_stored_procedure']

# #     @transaction.atomic
# #     def run_stored_procedure(self, request, queryset):
# #         try:
# #             for input_data in queryset:
# #                 # month = input_data.month_id
# #                 year = input_data.year_id  # Adjust based on actual field name

# #                 # Log the values for debugging
# #                 self.message_user(request, f"Calling stored procedure with year={year}", messages.INFO)

# #                 # Check for None values
# #                 if None in [year]:
# #                     self.message_user(request, f"Skipping {input_data} due to missing data.", messages.WARNING)
# #                     continue

# #                 with connection.cursor() as cursor:
# #                     cursor.callproc('insert_revenue_records_az', [year])

# #             self.message_user(request, "Payments prepared successfully.", messages.SUCCESS)
# #         except Exception as e:
# #             self.message_user(request, f"Error: {str(e)}", messages.ERROR)

# #     run_stored_procedure.short_description = "Prepare payments"

# # admin.site.register(InputDataCurrentSeason, InputDataCurrentSeasonAdmin)

# class InputDataPaymentForm(forms.ModelForm):
#     class Meta:
#         model = InputDataPayment
#         fields = ['year', 'grade', 'section']
#         # fields = ['uploaded_file']
#         # widgets = {
#         #     'mid_id': forms.HiddenInput(),
#         #     'yid_id': forms.HiddenInput(),
#         # }
        
# class InputDataPaymentAdmin(admin.ModelAdmin):
#     actions = ['run_stored_procedure']

#     @transaction.atomic
#     def run_stored_procedure(self, request, queryset):
#         try:
#             for input_data in queryset:
#                 # month = input_data.month_id
#                 year = input_data.year  # Adjust based on actual field name 
#                 grade = input_data.grade_id  # Adjust based on actual field name
#                 # section = input_data.section_id  # Adjust based on actual field name
#                 # Log the values for debugging
#                 self.message_user(request, f"Calling stored procedure with year={year}, grade={grade}", messages.INFO)

#                 # Check for None values
#                 if None in [year]:
#                     self.message_user(request, f"Skipping {input_data} due to missing data.", messages.WARNING)
#                     continue

#                 with connection.cursor() as cursor:
#                     cursor.callproc('insert_revenue_records_shimela', [year, grade])

#             self.message_user(request, "Payments calculated successfully.", messages.SUCCESS)
#         except Exception as e:
#             self.message_user(request, f"Error: {str(e)}", messages.ERROR)

#     run_stored_procedure.short_description = "Calculate payments"

# admin.site.register(InputDataPayment, InputDataPaymentAdmin)

# @admin.register(PaymentMonthlyReport)
# class PaymentMonthlyReportAdmin(ImportExportModelAdmin):
#     list_display = (
#         'year', 
#         'month', 
#         'status', 
#         'total_transactions', 
#         'total_collected_fees'
#     )
#     list_filter = ('year', 'month', 'status')
#     search_fields = ('year', 'month', 'status')
#     readonly_fields = (
#         'total_transactions',
#         'total_registration_fees',
#         'total_tuition_fees',
#         'total_transport_fees',
#         'total_nutrition_fees',
#         'total_penalties',
#         'total_other_fees',
#         'total_collected_fees'
#     )

#     def has_add_permission(self, request):
#         return False  # Disallow adding new reports manually

#     def has_delete_permission(self, request, obj=None):
#         return False  # Disallow deleting reports