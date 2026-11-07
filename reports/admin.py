# from django.contrib import admin
# from .models import *
# import requests
# # from django.db import models
# from import_export.admin import ImportExportModelAdmin
# from django.shortcuts import redirect
# from django.db import connection
# # from django.conf.urls import url
# # from django.conf.urls import url
# # from django.urls import url
# from django.http import HttpResponse
# # import csv
# from django.utils import timezone
# import datetime
# from datetime import datetime
# from django.contrib.contenttypes.models import ContentType
# from django.http import HttpResponseRedirect

# from django.db.models import Sum
# from reportlab.lib import colors
# from reportlab.lib.pagesizes import letter
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, PageTemplate, Frame, Spacer, PageBreak
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib.units import inch
# from reportlab.lib.enums import TA_RIGHT
# from django.http import HttpResponse
# from django import forms

# class RevenuePerformanceFromAprilToJuneAdmin(ImportExportModelAdmin):
#     pass
#     fieldsets = [
#         ('General informations', {
#             'fields': [('id'),('Code'), ('Year'), ('Revenue_title_amharic', 'Measurement')],
#         }), 
#         ('Detail information', {
#             'fields': [('Revenue_annual_plan', 'Plan', 'Performed', 'Performance')],
#         }),
#     ]
#     list_display = ['id', 'Code', 'Year', 'Revenue_title_amharic', 'Measurement', 'Revenue_annual_plan', 'Plan', 'Performed', 'Performance']
#     search_fields = ['id','Code','Revenue_title_amharic']
#     list_filter = ['Year']
#     list_display_links = ['id', 'Code', 'Year', 'Revenue_title_amharic', 'Measurement', 'Revenue_annual_plan', 'Plan', 'Performed', 'Performance']
#     readonly_fields = ('id', 'Code', 'Year', 'Revenue_title_amharic', 'Measurement', 'Revenue_annual_plan', 'Plan', 'Performed', 'Performance')
#     list_per_page = 10
#     list_select_related = True

#     # actions = ['download_pdf']

#     # def download_pdf(self, request, queryset):
#     #     # Getting the model name
#     #     model_name = self.model._meta.verbose_name_plural.title()

#     #     # Creating an HttpResponse object
#     #     response = HttpResponse(content_type='application/pdf')
#     #     response['Content-Disposition'] = f'attachment; filename="{model_name}.pdf"'

#     #     # Creating a PDF document
#     #     pdf = SimpleDocTemplate(response, pagesize=letter)
#     #     styles = getSampleStyleSheet()

#     #     # Create report elements
#     #     elements = []

#     #     # Add title
#     #     title = Paragraph(model_name, styles['Title'])
#     #     elements.append(title)

#     #     # Extracting headers and data from the queryset
#     #     headers = [field.verbose_name.title() for field in self.model._meta.fields]
        
#     #     # Add row numbers
#     #     headers.insert(0, 'Row Number')
#     #     data = [headers]

#     #     # Initialize the total variable for the 'purchased_items' column
#     #     total_purchased_items = sum(obj.purchased_items for obj in queryset)

#     #     # Iterate through queryset to create data rows
#     #     for idx, obj in enumerate(queryset, start=1):
#     #         data_row = [str(idx)] + [str(getattr(obj, field.name)) for field in self.model._meta.fields[:-1]]  # Exclude last column
#     #         data_row.append(str(obj.purchased_items))  # Include purchased items value
#     #         data.append(data_row)

#     #     # Create the total row
#     #     total_row = ['Total'] + [''] * (len(headers) - 2)  # Filling with empty strings for all columns except the first and last
#     #     total_row.extend([str(total_purchased_items)])  # Adding the total at the last cell

#     #     # Creating a table and styling it
#     #     table = Table(data + [total_row])
#     #     table.setStyle(TableStyle([
#     #         ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
#     #         ('GRID', (0, 0), (-1, -1), 1, colors.black),
#     #         ('SPAN', (0, -1), (-2, -1)),  # Merging cells for the total row, spanning from the first to the second to last cell
#     #     ]))

#     #     # Add table to elements
#     #     elements.append(table)

#     #      # Build PDF document with elements
#     #     pdf.build(elements, onFirstPage=self.add_page_info, onLaterPages=self.add_page_info)

#     #     return response

#     # download_pdf.short_description = 'Download selected items'

#     # def add_page_info(self, canvas, doc):
#     #     """
#     #     Add page number and printed date to PDF.
#     #     """
#     #     page_num_text = f"Page {canvas.getPageNumber()}"
#     #     printed_date_text = f"Printed Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

#     #     canvas.saveState()
#     #     canvas.setFont('Times-Roman', 10)

#     #     # Add page number at the bottom left corner
#     #     canvas.drawString(10, 20, page_num_text)

#     #     # Add printed date at the bottom right corner
#     #     printed_date_width = canvas.stringWidth(printed_date_text)
#     #     canvas.drawString(canvas._pagesize[0] - printed_date_width - 10, 20, printed_date_text)

#     #     canvas.restoreState()

#     class Meta:
#         model = RevenuePerformanceFromAprilToJune 

#     def save_model(self, request, obj, form, change):
#         if change:
#             obj.Update_by = request.user
#             obj.Registered_date = datetime.now()
#         obj.save()

# admin.site.register(RevenuePerformanceFromAprilToJune, RevenuePerformanceFromAprilToJuneAdmin)

# class RevenuePerformanceFromJanuaryToMarchAdmin(ImportExportModelAdmin):
#     pass
#     fieldsets = [
#         ('General informations', {
#             'fields': [('id'),('Code'), ('Year'), ('Revenue_title_amharic', 'Measurement')],
#         }), 
#         ('Detail information', {
#             'fields': [('Revenue_annual_plan', 'Plan', 'Performed', 'Performance')],
#         }),
#     ]
#     list_display = ['id', 'Code', 'Year', 'Revenue_title_amharic', 'Measurement', 'Revenue_annual_plan', 'Plan', 'Performed', 'Performance']
#     search_fields = ['id','Code','Revenue_title_amharic']
#     list_filter = ['Year']
#     list_display_links = ['id', 'Code', 'Year', 'Revenue_title_amharic', 'Measurement', 'Revenue_annual_plan', 'Plan', 'Performed', 'Performance']
#     readonly_fields = ('id', 'Code', 'Year', 'Revenue_title_amharic', 'Measurement', 'Revenue_annual_plan', 'Plan', 'Performed', 'Performance')
#     list_per_page = 10
#     list_select_related = True

#     # actions = ['download_pdf']

#     # def download_pdf(self, request, queryset):
#     #     # Getting the model name
#     #     model_name = self.model._meta.verbose_name_plural.title()

#     #     # Creating an HttpResponse object
#     #     response = HttpResponse(content_type='application/pdf')
#     #     response['Content-Disposition'] = f'attachment; filename="{model_name}.pdf"'

#     #     # Creating a PDF document
#     #     pdf = SimpleDocTemplate(response, pagesize=letter)
#     #     styles = getSampleStyleSheet()

#     #     # Create report elements
#     #     elements = []

#     #     # Add title
#     #     title = Paragraph(model_name, styles['Title'])
#     #     elements.append(title)

#     #     # Extracting headers and data from the queryset
#     #     headers = [field.verbose_name.title() for field in self.model._meta.fields]
        
#     #     # Add row numbers
#     #     headers.insert(0, 'Row Number')
#     #     data = [headers]

#     #     # Initialize the total variable for the 'purchased_items' column
#     #     total_purchased_items = sum(obj.purchased_items for obj in queryset)

#     #     # Iterate through queryset to create data rows
#     #     for idx, obj in enumerate(queryset, start=1):
#     #         data_row = [str(idx)] + [str(getattr(obj, field.name)) for field in self.model._meta.fields[:-1]]  # Exclude last column
#     #         data_row.append(str(obj.purchased_items))  # Include purchased items value
#     #         data.append(data_row)

#     #     # Create the total row
#     #     total_row = ['Total'] + [''] * (len(headers) - 2)  # Filling with empty strings for all columns except the first and last
#     #     total_row.extend([str(total_purchased_items)])  # Adding the total at the last cell

#     #     # Creating a table and styling it
#     #     table = Table(data + [total_row])
#     #     table.setStyle(TableStyle([
#     #         ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
#     #         ('GRID', (0, 0), (-1, -1), 1, colors.black),
#     #         ('SPAN', (0, -1), (-2, -1)),  # Merging cells for the total row, spanning from the first to the second to last cell
#     #     ]))

#     #     # Add table to elements
#     #     elements.append(table)

#     #      # Build PDF document with elements
#     #     pdf.build(elements, onFirstPage=self.add_page_info, onLaterPages=self.add_page_info)

#     #     return response

#     # download_pdf.short_description = 'Download selected items'

#     # def add_page_info(self, canvas, doc):
#     #     """
#     #     Add page number and printed date to PDF.
#     #     """
#     #     page_num_text = f"Page {canvas.getPageNumber()}"
#     #     printed_date_text = f"Printed Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

#     #     canvas.saveState()
#     #     canvas.setFont('Times-Roman', 10)

#     #     # Add page number at the bottom left corner
#     #     canvas.drawString(10, 20, page_num_text)

#     #     # Add printed date at the bottom right corner
#     #     printed_date_width = canvas.stringWidth(printed_date_text)
#     #     canvas.drawString(canvas._pagesize[0] - printed_date_width - 10, 20, printed_date_text)

#     #     canvas.restoreState()

#     class Meta:
#         model = RevenuePerformanceFromJanuaryToMarch 

#     def save_model(self, request, obj, form, change):
#         if change:
#             obj.Update_by = request.user
#             obj.Registered_date = datetime.now()
#         obj.save()

# admin.site.register(RevenuePerformanceFromJanuaryToMarch, RevenuePerformanceFromJanuaryToMarchAdmin)

# class RevenuePerformanceFromJulyToSeptemberAdmin(ImportExportModelAdmin):
#     pass
#     fieldsets = [
#         ('General informations', {
#             'fields': [('id'),('Code'), ('Year'), ('Revenue_title_amharic', 'Measurement')],
#         }), 
#         ('Detail information', {
#             'fields': [('Revenue_annual_plan', 'Plan', 'Performed', 'Performance')],
#         }),
#     ]
#     list_display = ['id', 'Code', 'Year', 'Revenue_title_amharic', 'Measurement', 'Revenue_annual_plan', 'Plan', 'Performed', 'Performance']
#     search_fields = ['id','Code','Revenue_title_amharic']
#     list_filter = ['Year']
#     list_display_links = ['id', 'Code', 'Year', 'Revenue_title_amharic', 'Measurement', 'Revenue_annual_plan', 'Plan', 'Performed', 'Performance']
#     readonly_fields = ('id', 'Code', 'Year', 'Revenue_title_amharic', 'Measurement', 'Revenue_annual_plan', 'Plan', 'Performed', 'Performance')
#     list_per_page = 10
#     list_select_related = True

#     # actions = ['download_pdf']

#     # def download_pdf(self, request, queryset):
#     #     # Getting the model name
#     #     model_name = self.model._meta.verbose_name_plural.title()

#     #     # Creating an HttpResponse object
#     #     response = HttpResponse(content_type='application/pdf')
#     #     response['Content-Disposition'] = f'attachment; filename="{model_name}.pdf"'

#     #     # Creating a PDF document
#     #     pdf = SimpleDocTemplate(response, pagesize=letter)
#     #     styles = getSampleStyleSheet()

#     #     # Create report elements
#     #     elements = []

#     #     # Add title
#     #     title = Paragraph(model_name, styles['Title'])
#     #     elements.append(title)

#     #     # Extracting headers and data from the queryset
#     #     headers = [field.verbose_name.title() for field in self.model._meta.fields]
        
#     #     # Add row numbers
#     #     headers.insert(0, 'Row Number')
#     #     data = [headers]

#     #     # Initialize the total variable for the 'purchased_items' column
#     #     total_purchased_items = sum(obj.purchased_items for obj in queryset)

#     #     # Iterate through queryset to create data rows
#     #     for idx, obj in enumerate(queryset, start=1):
#     #         data_row = [str(idx)] + [str(getattr(obj, field.name)) for field in self.model._meta.fields[:-1]]  # Exclude last column
#     #         data_row.append(str(obj.purchased_items))  # Include purchased items value
#     #         data.append(data_row)

#     #     # Create the total row
#     #     total_row = ['Total'] + [''] * (len(headers) - 2)  # Filling with empty strings for all columns except the first and last
#     #     total_row.extend([str(total_purchased_items)])  # Adding the total at the last cell

#     #     # Creating a table and styling it
#     #     table = Table(data + [total_row])
#     #     table.setStyle(TableStyle([
#     #         ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
#     #         ('GRID', (0, 0), (-1, -1), 1, colors.black),
#     #         ('SPAN', (0, -1), (-2, -1)),  # Merging cells for the total row, spanning from the first to the second to last cell
#     #     ]))

#     #     # Add table to elements
#     #     elements.append(table)

#     #      # Build PDF document with elements
#     #     pdf.build(elements, onFirstPage=self.add_page_info, onLaterPages=self.add_page_info)

#     #     return response

#     # download_pdf.short_description = 'Download selected items'

#     # def add_page_info(self, canvas, doc):
#     #     """
#     #     Add page number and printed date to PDF.
#     #     """
#     #     page_num_text = f"Page {canvas.getPageNumber()}"
#     #     printed_date_text = f"Printed Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

#     #     canvas.saveState()
#     #     canvas.setFont('Times-Roman', 10)

#     #     # Add page number at the bottom left corner
#     #     canvas.drawString(10, 20, page_num_text)

#     #     # Add printed date at the bottom right corner
#     #     printed_date_width = canvas.stringWidth(printed_date_text)
#     #     canvas.drawString(canvas._pagesize[0] - printed_date_width - 10, 20, printed_date_text)

#     #     canvas.restoreState()

#     class Meta:
#         model = RevenuePerformanceFromJulyToSeptember 

#     def save_model(self, request, obj, form, change):
#         if change:
#             obj.Update_by = request.user
#             obj.Registered_date = datetime.now()
#         obj.save()

# admin.site.register(RevenuePerformanceFromJulyToSeptember, RevenuePerformanceFromJulyToSeptemberAdmin)

# class RevenuePerformanceFromOctoberToDecemberAdmin(ImportExportModelAdmin):
#     pass
#     fieldsets = [
#         ('General informations', {
#             'fields': [('id'),('Code'), ('Year'), ('Revenue_title_amharic', 'Measurement')],
#         }), 
#         ('Detail information', {
#             'fields': [('Revenue_annual_plan', 'Plan', 'Performed', 'Performance')],
#         }),
#     ]
#     list_display = ['id', 'Code', 'Year', 'Revenue_title_amharic', 'Measurement', 'Revenue_annual_plan', 'Plan', 'Performed', 'Performance']
#     search_fields = ['id','Code','Revenue_title_amharic']
#     list_filter = ['Year']
#     list_display_links = ['id', 'Code', 'Year', 'Revenue_title_amharic', 'Measurement', 'Revenue_annual_plan', 'Plan', 'Performed', 'Performance']
#     readonly_fields = ('id', 'Code', 'Year', 'Revenue_title_amharic', 'Measurement', 'Revenue_annual_plan', 'Plan', 'Performed', 'Performance')
#     list_per_page = 10
#     list_select_related = True

#     # actions = ['download_pdf']

#     # def download_pdf(self, request, queryset):
#     #     # Getting the model name
#     #     model_name = self.model._meta.verbose_name_plural.title()

#     #     # Creating an HttpResponse object
#     #     response = HttpResponse(content_type='application/pdf')
#     #     response['Content-Disposition'] = f'attachment; filename="{model_name}.pdf"'

#     #     # Creating a PDF document
#     #     pdf = SimpleDocTemplate(response, pagesize=letter)
#     #     styles = getSampleStyleSheet()

#     #     # Create report elements
#     #     elements = []

#     #     # Add title
#     #     title = Paragraph(model_name, styles['Title'])
#     #     elements.append(title)

#     #     # Extracting headers and data from the queryset
#     #     headers = [field.verbose_name.title() for field in self.model._meta.fields]
        
#     #     # Add row numbers
#     #     headers.insert(0, 'Row Number')
#     #     data = [headers]

#     #     # Initialize the total variable for the 'purchased_items' column
#     #     total_purchased_items = sum(obj.purchased_items for obj in queryset)

#     #     # Iterate through queryset to create data rows
#     #     for idx, obj in enumerate(queryset, start=1):
#     #         data_row = [str(idx)] + [str(getattr(obj, field.name)) for field in self.model._meta.fields[:-1]]  # Exclude last column
#     #         data_row.append(str(obj.purchased_items))  # Include purchased items value
#     #         data.append(data_row)

#     #     # Create the total row
#     #     total_row = ['Total'] + [''] * (len(headers) - 2)  # Filling with empty strings for all columns except the first and last
#     #     total_row.extend([str(total_purchased_items)])  # Adding the total at the last cell

#     #     # Creating a table and styling it
#     #     table = Table(data + [total_row])
#     #     table.setStyle(TableStyle([
#     #         ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
#     #         ('GRID', (0, 0), (-1, -1), 1, colors.black),
#     #         ('SPAN', (0, -1), (-2, -1)),  # Merging cells for the total row, spanning from the first to the second to last cell
#     #     ]))

#     #     # Add table to elements
#     #     elements.append(table)

#     #      # Build PDF document with elements
#     #     pdf.build(elements, onFirstPage=self.add_page_info, onLaterPages=self.add_page_info)

#     #     return response

#     # download_pdf.short_description = 'Download selected items'

#     # def add_page_info(self, canvas, doc):
#     #     """
#     #     Add page number and printed date to PDF.
#     #     """
#     #     page_num_text = f"Page {canvas.getPageNumber()}"
#     #     printed_date_text = f"Printed Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

#     #     canvas.saveState()
#     #     canvas.setFont('Times-Roman', 10)

#     #     # Add page number at the bottom left corner
#     #     canvas.drawString(10, 20, page_num_text)

#     #     # Add printed date at the bottom right corner
#     #     printed_date_width = canvas.stringWidth(printed_date_text)
#     #     canvas.drawString(canvas._pagesize[0] - printed_date_width - 10, 20, printed_date_text)

#     #     canvas.restoreState()

#     class Meta:
#         model = RevenuePerformanceFromOctoberToDecember 

#     def save_model(self, request, obj, form, change):
#         if change:
#             obj.Update_by = request.user
#             obj.Registered_date = datetime.now()
#         obj.save()

# admin.site.register(RevenuePerformanceFromOctoberToDecember, RevenuePerformanceFromOctoberToDecemberAdmin)

# class RevenueMonthlyPerformanceAdmin(ImportExportModelAdmin):
#     pass
#     fieldsets = [
#         ('General informations', {
#             'fields': [('id'),('Code'), ('Month', 'Year'), ('Revenue_title_amharic', 'Measurement')],
#         }), 
#         ('Detail information', {
#             'fields': [('Revenue_annual_plan', 'Plan', 'Performed', 'Performance')],
#         }),
#     ]
#     list_display = ['id', 'Code', 'Month', 'Year', 'Revenue_title_amharic', 'Measurement', 'Revenue_annual_plan', 'Plan', 'Performed', 'Performance']
#     search_fields = ['id','Code','Revenue_title_amharic']
#     list_filter = ['Month', 'Year']
#     list_display_links = ['id', 'Code', 'Month', 'Year', 'Revenue_title_amharic', 'Measurement', 'Revenue_annual_plan', 'Plan', 'Performed', 'Performance']
#     readonly_fields = ('id', 'Code', 'Month', 'Year', 'Revenue_title_amharic', 'Measurement', 'Revenue_annual_plan', 'Plan', 'Performed', 'Performance')
#     list_per_page = 10
#     list_select_related = True

#     # actions = ['download_pdf']

#     # def download_pdf(self, request, queryset):
#     #     # Getting the model name
#     #     model_name = self.model._meta.verbose_name_plural.title()

#     #     # Creating an HttpResponse object
#     #     response = HttpResponse(content_type='application/pdf')
#     #     response['Content-Disposition'] = f'attachment; filename="{model_name}.pdf"'

#     #     # Creating a PDF document
#     #     pdf = SimpleDocTemplate(response, pagesize=letter)
#     #     styles = getSampleStyleSheet()

#     #     # Create report elements
#     #     elements = []

#     #     # Add title
#     #     title = Paragraph(model_name, styles['Title'])
#     #     elements.append(title)

#     #     # Extracting headers and data from the queryset
#     #     headers = [field.verbose_name.title() for field in self.model._meta.fields]
        
#     #     # Add row numbers
#     #     headers.insert(0, 'Row Number')
#     #     data = [headers]

#     #     # Initialize the total variable for the 'purchased_items' column
#     #     total_purchased_items = sum(obj.purchased_items for obj in queryset)

#     #     # Iterate through queryset to create data rows
#     #     for idx, obj in enumerate(queryset, start=1):
#     #         data_row = [str(idx)] + [str(getattr(obj, field.name)) for field in self.model._meta.fields[:-1]]  # Exclude last column
#     #         data_row.append(str(obj.purchased_items))  # Include purchased items value
#     #         data.append(data_row)

#     #     # Create the total row
#     #     total_row = ['Total'] + [''] * (len(headers) - 2)  # Filling with empty strings for all columns except the first and last
#     #     total_row.extend([str(total_purchased_items)])  # Adding the total at the last cell

#     #     # Creating a table and styling it
#     #     table = Table(data + [total_row])
#     #     table.setStyle(TableStyle([
#     #         ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
#     #         ('GRID', (0, 0), (-1, -1), 1, colors.black),
#     #         ('SPAN', (0, -1), (-2, -1)),  # Merging cells for the total row, spanning from the first to the second to last cell
#     #     ]))

#     #     # Add table to elements
#     #     elements.append(table)

#     #      # Build PDF document with elements
#     #     pdf.build(elements, onFirstPage=self.add_page_info, onLaterPages=self.add_page_info)

#     #     return response

#     # download_pdf.short_description = 'Download selected items'

#     # def add_page_info(self, canvas, doc):
#     #     """
#     #     Add page number and printed date to PDF.
#     #     """
#     #     page_num_text = f"Page {canvas.getPageNumber()}"
#     #     printed_date_text = f"Printed Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

#     #     canvas.saveState()
#     #     canvas.setFont('Times-Roman', 10)

#     #     # Add page number at the bottom left corner
#     #     canvas.drawString(10, 20, page_num_text)

#     #     # Add printed date at the bottom right corner
#     #     printed_date_width = canvas.stringWidth(printed_date_text)
#     #     canvas.drawString(canvas._pagesize[0] - printed_date_width - 10, 20, printed_date_text)

#     #     canvas.restoreState()

#     class Meta:
#         model = RevenueMonthlyPerformance 

#     def save_model(self, request, obj, form, change):
#         if change:
#             obj.Update_by = request.user
#             obj.Registered_date = datetime.now()
#         obj.save()

# admin.site.register(RevenueMonthlyPerformance, RevenueMonthlyPerformanceAdmin)


# class RevenueAnnualPerformanceAdmin(ImportExportModelAdmin):
#     pass
#     fieldsets = [
#         ('General informations', {
#             'fields': [('id'),('Code'), ('Year'), ('Revenue_title_amharic', 'Measurement')],
#         }), 
#         ('Detail information', {
#             'fields': [('Revenue_annual_plan', 'Plan', 'Performed', 'Performance')],
#         }),
#     ]
#     list_display = ['id', 'Code', 'Year', 'Revenue_title_amharic', 'Measurement', 'Revenue_annual_plan', 'Plan', 'Performed', 'Performance']
#     search_fields = ['id','Code','Revenue_title_amharic']
#     list_filter = ['Year']
#     list_display_links = ['id', 'Code', 'Year', 'Revenue_title_amharic', 'Measurement', 'Revenue_annual_plan', 'Plan', 'Performed', 'Performance']
#     readonly_fields = ('id', 'Code', 'Year', 'Revenue_title_amharic', 'Measurement', 'Revenue_annual_plan', 'Plan', 'Performed', 'Performance')
#     list_per_page = 10
#     list_select_related = True

#     # actions = ['download_pdf']

#     # def download_pdf(self, request, queryset):
#     #     # Getting the model name
#     #     model_name = self.model._meta.verbose_name_plural.title()

#     #     # Creating an HttpResponse object
#     #     response = HttpResponse(content_type='application/pdf')
#     #     response['Content-Disposition'] = f'attachment; filename="{model_name}.pdf"'

#     #     # Creating a PDF document
#     #     pdf = SimpleDocTemplate(response, pagesize=letter)
#     #     styles = getSampleStyleSheet()

#     #     # Create report elements
#     #     elements = []

#     #     # Add title
#     #     title = Paragraph(model_name, styles['Title'])
#     #     elements.append(title)

#     #     # Extracting headers and data from the queryset
#     #     headers = [field.verbose_name.title() for field in self.model._meta.fields]
        
#     #     # Add row numbers
#     #     headers.insert(0, 'Row Number')
#     #     data = [headers]

#     #     # Initialize the total variable for the 'purchased_items' column
#     #     total_purchased_items = sum(obj.purchased_items for obj in queryset)

#     #     # Iterate through queryset to create data rows
#     #     for idx, obj in enumerate(queryset, start=1):
#     #         data_row = [str(idx)] + [str(getattr(obj, field.name)) for field in self.model._meta.fields[:-1]]  # Exclude last column
#     #         data_row.append(str(obj.purchased_items))  # Include purchased items value
#     #         data.append(data_row)

#     #     # Create the total row
#     #     total_row = ['Total'] + [''] * (len(headers) - 2)  # Filling with empty strings for all columns except the first and last
#     #     total_row.extend([str(total_purchased_items)])  # Adding the total at the last cell

#     #     # Creating a table and styling it
#     #     table = Table(data + [total_row])
#     #     table.setStyle(TableStyle([
#     #         ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
#     #         ('GRID', (0, 0), (-1, -1), 1, colors.black),
#     #         ('SPAN', (0, -1), (-2, -1)),  # Merging cells for the total row, spanning from the first to the second to last cell
#     #     ]))

#     #     # Add table to elements
#     #     elements.append(table)

#     #      # Build PDF document with elements
#     #     pdf.build(elements, onFirstPage=self.add_page_info, onLaterPages=self.add_page_info)

#     #     return response

#     # download_pdf.short_description = 'Download selected items'

#     # def add_page_info(self, canvas, doc):
#     #     """
#     #     Add page number and printed date to PDF.
#     #     """
#     #     page_num_text = f"Page {canvas.getPageNumber()}"
#     #     printed_date_text = f"Printed Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

#     #     canvas.saveState()
#     #     canvas.setFont('Times-Roman', 10)

#     #     # Add page number at the bottom left corner
#     #     canvas.drawString(10, 20, page_num_text)

#     #     # Add printed date at the bottom right corner
#     #     printed_date_width = canvas.stringWidth(printed_date_text)
#     #     canvas.drawString(canvas._pagesize[0] - printed_date_width - 10, 20, printed_date_text)

#     #     canvas.restoreState()

#     class Meta:
#         model = RevenueAnnualPerformance 

#     def save_model(self, request, obj, form, change):
#         if change:
#             obj.Update_by = request.user
#             obj.Registered_date = datetime.now()
#         obj.save()

# admin.site.register(RevenueAnnualPerformance, RevenueAnnualPerformanceAdmin)

# class ExpensePerformanceFromAprilToJuneAdmin(ImportExportModelAdmin):
#     pass
#     fieldsets = [
#         ('General informations', {
#             'fields': [('id'),('Code'), ('Year'), ('Expense_title_amharic', 'Measurement')],
#         }), 
#         ('Detail information', {
#             'fields': [('Expense_annual_plan', 'Plan', 'Performed', 'Performance')],
#         }),
#     ]
#     list_display = ['id', 'Code', 'Year', 'Expense_title_amharic', 'Measurement', 'Expense_annual_plan', 'Plan', 'Performed', 'Performance']
#     search_fields = ['id','Code','Expensetitle_amharic']
#     list_filter = ['Year']
#     list_display_links = ['id', 'Code', 'Year', 'Expense_title_amharic', 'Measurement', 'Expense_annual_plan', 'Plan', 'Performed', 'Performance']
#     readonly_fields = ('id', 'Code', 'Year', 'Expense_title_amharic', 'Measurement', 'Expense_annual_plan', 'Plan', 'Performed', 'Performance')
#     list_per_page = 10
#     list_select_related = True

#     # actions = ['download_pdf']

#     # def download_pdf(self, request, queryset):
#     #     # Getting the model name
#     #     model_name = self.model._meta.verbose_name_plural.title()

#     #     # Creating an HttpResponse object
#     #     response = HttpResponse(content_type='application/pdf')
#     #     response['Content-Disposition'] = f'attachment; filename="{model_name}.pdf"'

#     #     # Creating a PDF document
#     #     pdf = SimpleDocTemplate(response, pagesize=letter)
#     #     styles = getSampleStyleSheet()

#     #     # Create report elements
#     #     elements = []

#     #     # Add title
#     #     title = Paragraph(model_name, styles['Title'])
#     #     elements.append(title)

#     #     # Extracting headers and data from the queryset
#     #     headers = [field.verbose_name.title() for field in self.model._meta.fields]
        
#     #     # Add row numbers
#     #     headers.insert(0, 'Row Number')
#     #     data = [headers]

#     #     # Initialize the total variable for the 'purchased_items' column
#     #     total_purchased_items = sum(obj.purchased_items for obj in queryset)

#     #     # Iterate through queryset to create data rows
#     #     for idx, obj in enumerate(queryset, start=1):
#     #         data_row = [str(idx)] + [str(getattr(obj, field.name)) for field in self.model._meta.fields[:-1]]  # Exclude last column
#     #         data_row.append(str(obj.purchased_items))  # Include purchased items value
#     #         data.append(data_row)

#     #     # Create the total row
#     #     total_row = ['Total'] + [''] * (len(headers) - 2)  # Filling with empty strings for all columns except the first and last
#     #     total_row.extend([str(total_purchased_items)])  # Adding the total at the last cell

#     #     # Creating a table and styling it
#     #     table = Table(data + [total_row])
#     #     table.setStyle(TableStyle([
#     #         ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
#     #         ('GRID', (0, 0), (-1, -1), 1, colors.black),
#     #         ('SPAN', (0, -1), (-2, -1)),  # Merging cells for the total row, spanning from the first to the second to last cell
#     #     ]))

#     #     # Add table to elements
#     #     elements.append(table)

#     #      # Build PDF document with elements
#     #     pdf.build(elements, onFirstPage=self.add_page_info, onLaterPages=self.add_page_info)

#     #     return response

#     # download_pdf.short_description = 'Download selected items'

#     # def add_page_info(self, canvas, doc):
#     #     """
#     #     Add page number and printed date to PDF.
#     #     """
#     #     page_num_text = f"Page {canvas.getPageNumber()}"
#     #     printed_date_text = f"Printed Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

#     #     canvas.saveState()
#     #     canvas.setFont('Times-Roman', 10)

#     #     # Add page number at the bottom left corner
#     #     canvas.drawString(10, 20, page_num_text)

#     #     # Add printed date at the bottom right corner
#     #     printed_date_width = canvas.stringWidth(printed_date_text)
#     #     canvas.drawString(canvas._pagesize[0] - printed_date_width - 10, 20, printed_date_text)

#     #     canvas.restoreState()

#     class Meta:
#         model = ExpensePerformanceFromAprilToJune 

#     def save_model(self, request, obj, form, change):
#         if change:
#             obj.Update_by = request.user
#             obj.Registered_date = datetime.now()
#         obj.save()

# admin.site.register(ExpensePerformanceFromAprilToJune, ExpensePerformanceFromAprilToJuneAdmin)

# class ExpensePerformanceFromJulyToSeptemberAdmin(ImportExportModelAdmin):
#     pass
#     fieldsets = [
#         ('General informations', {
#             'fields': [('id'),('Code'), ('Year'), ('Expense_title_amharic', 'Measurement')],
#         }), 
#         ('Detail information', {
#             'fields': [('Expense_annual_plan', 'Plan', 'Performed', 'Performance')],
#         }),
#     ]
#     list_display = ['id', 'Code', 'Year', 'Expense_title_amharic', 'Measurement', 'Expense_annual_plan', 'Plan', 'Performed', 'Performance']
#     search_fields = ['id','Code','Expense_title_amharic']
#     list_filter = ['Year']
#     list_display_links = ['id', 'Code', 'Year', 'Expense_title_amharic', 'Measurement', 'Expense_annual_plan', 'Plan', 'Performed', 'Performance']
#     readonly_fields = ('id', 'Code', 'Year', 'Expense_title_amharic', 'Measurement', 'Expense_annual_plan', 'Plan', 'Performed', 'Performance')
#     list_per_page = 10
#     list_select_related = True

#     # actions = ['download_pdf']

#     # def download_pdf(self, request, queryset):
#     #     # Getting the model name
#     #     model_name = self.model._meta.verbose_name_plural.title()

#     #     # Creating an HttpResponse object
#     #     response = HttpResponse(content_type='application/pdf')
#     #     response['Content-Disposition'] = f'attachment; filename="{model_name}.pdf"'

#     #     # Creating a PDF document
#     #     pdf = SimpleDocTemplate(response, pagesize=letter)
#     #     styles = getSampleStyleSheet()

#     #     # Create report elements
#     #     elements = []

#     #     # Add title
#     #     title = Paragraph(model_name, styles['Title'])
#     #     elements.append(title)

#     #     # Extracting headers and data from the queryset
#     #     headers = [field.verbose_name.title() for field in self.model._meta.fields]
        
#     #     # Add row numbers
#     #     headers.insert(0, 'Row Number')
#     #     data = [headers]

#     #     # Initialize the total variable for the 'purchased_items' column
#     #     total_purchased_items = sum(obj.purchased_items for obj in queryset)

#     #     # Iterate through queryset to create data rows
#     #     for idx, obj in enumerate(queryset, start=1):
#     #         data_row = [str(idx)] + [str(getattr(obj, field.name)) for field in self.model._meta.fields[:-1]]  # Exclude last column
#     #         data_row.append(str(obj.purchased_items))  # Include purchased items value
#     #         data.append(data_row)

#     #     # Create the total row
#     #     total_row = ['Total'] + [''] * (len(headers) - 2)  # Filling with empty strings for all columns except the first and last
#     #     total_row.extend([str(total_purchased_items)])  # Adding the total at the last cell

#     #     # Creating a table and styling it
#     #     table = Table(data + [total_row])
#     #     table.setStyle(TableStyle([
#     #         ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
#     #         ('GRID', (0, 0), (-1, -1), 1, colors.black),
#     #         ('SPAN', (0, -1), (-2, -1)),  # Merging cells for the total row, spanning from the first to the second to last cell
#     #     ]))

#     #     # Add table to elements
#     #     elements.append(table)

#     #      # Build PDF document with elements
#     #     pdf.build(elements, onFirstPage=self.add_page_info, onLaterPages=self.add_page_info)

#     #     return response

#     # download_pdf.short_description = 'Download selected items'

#     # def add_page_info(self, canvas, doc):
#     #     """
#     #     Add page number and printed date to PDF.
#     #     """
#     #     page_num_text = f"Page {canvas.getPageNumber()}"
#     #     printed_date_text = f"Printed Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

#     #     canvas.saveState()
#     #     canvas.setFont('Times-Roman', 10)

#     #     # Add page number at the bottom left corner
#     #     canvas.drawString(10, 20, page_num_text)

#     #     # Add printed date at the bottom right corner
#     #     printed_date_width = canvas.stringWidth(printed_date_text)
#     #     canvas.drawString(canvas._pagesize[0] - printed_date_width - 10, 20, printed_date_text)

#     #     canvas.restoreState()

#     class Meta:
#         model = ExpensePerformanceFromJulyToSeptember 

#     def save_model(self, request, obj, form, change):
#         if change:
#             obj.Update_by = request.user
#             obj.Registered_date = datetime.now()
#         obj.save()

# admin.site.register(ExpensePerformanceFromJulyToSeptember, ExpensePerformanceFromJulyToSeptemberAdmin)

# class ExpensePerformanceFromOctoberToDecemberAdmin(ImportExportModelAdmin):
#     pass
#     fieldsets = [
#         ('General informations', {
#             'fields': [('id'),('Code'), ('Year'), ('Expense_title_amharic', 'Measurement')],
#         }), 
#         ('Detail information', {
#             'fields': [('Expense_annual_plan', 'Plan', 'Performed', 'Performance')],
#         }),
#     ]
#     list_display = ['id', 'Code', 'Year', 'Expense_title_amharic', 'Measurement', 'Expense_annual_plan', 'Plan', 'Performed', 'Performance']
#     search_fields = ['id','Code','Expense_title_amharic']
#     list_filter = ['Year']
#     list_display_links = ['id', 'Code', 'Year', 'Expense_title_amharic', 'Measurement', 'Expense_annual_plan', 'Plan', 'Performed', 'Performance']
#     readonly_fields = ('id', 'Code', 'Year', 'Expense_title_amharic', 'Measurement', 'Expense_annual_plan', 'Plan', 'Performed', 'Performance')
#     list_per_page = 10
#     list_select_related = True

#     # actions = ['download_pdf']

#     # def download_pdf(self, request, queryset):
#     #     # Getting the model name
#     #     model_name = self.model._meta.verbose_name_plural.title()

#     #     # Creating an HttpResponse object
#     #     response = HttpResponse(content_type='application/pdf')
#     #     response['Content-Disposition'] = f'attachment; filename="{model_name}.pdf"'

#     #     # Creating a PDF document
#     #     pdf = SimpleDocTemplate(response, pagesize=letter)
#     #     styles = getSampleStyleSheet()

#     #     # Create report elements
#     #     elements = []

#     #     # Add title
#     #     title = Paragraph(model_name, styles['Title'])
#     #     elements.append(title)

#     #     # Extracting headers and data from the queryset
#     #     headers = [field.verbose_name.title() for field in self.model._meta.fields]
        
#     #     # Add row numbers
#     #     headers.insert(0, 'Row Number')
#     #     data = [headers]

#     #     # Initialize the total variable for the 'purchased_items' column
#     #     total_purchased_items = sum(obj.purchased_items for obj in queryset)

#     #     # Iterate through queryset to create data rows
#     #     for idx, obj in enumerate(queryset, start=1):
#     #         data_row = [str(idx)] + [str(getattr(obj, field.name)) for field in self.model._meta.fields[:-1]]  # Exclude last column
#     #         data_row.append(str(obj.purchased_items))  # Include purchased items value
#     #         data.append(data_row)

#     #     # Create the total row
#     #     total_row = ['Total'] + [''] * (len(headers) - 2)  # Filling with empty strings for all columns except the first and last
#     #     total_row.extend([str(total_purchased_items)])  # Adding the total at the last cell

#     #     # Creating a table and styling it
#     #     table = Table(data + [total_row])
#     #     table.setStyle(TableStyle([
#     #         ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
#     #         ('GRID', (0, 0), (-1, -1), 1, colors.black),
#     #         ('SPAN', (0, -1), (-2, -1)),  # Merging cells for the total row, spanning from the first to the second to last cell
#     #     ]))

#     #     # Add table to elements
#     #     elements.append(table)

#     #      # Build PDF document with elements
#     #     pdf.build(elements, onFirstPage=self.add_page_info, onLaterPages=self.add_page_info)

#     #     return response

#     # download_pdf.short_description = 'Download selected items'

#     # def add_page_info(self, canvas, doc):
#     #     """
#     #     Add page number and printed date to PDF.
#     #     """
#     #     page_num_text = f"Page {canvas.getPageNumber()}"
#     #     printed_date_text = f"Printed Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

#     #     canvas.saveState()
#     #     canvas.setFont('Times-Roman', 10)

#     #     # Add page number at the bottom left corner
#     #     canvas.drawString(10, 20, page_num_text)

#     #     # Add printed date at the bottom right corner
#     #     printed_date_width = canvas.stringWidth(printed_date_text)
#     #     canvas.drawString(canvas._pagesize[0] - printed_date_width - 10, 20, printed_date_text)

#     #     canvas.restoreState()

#     class Meta:
#         model = ExpensePerformanceFromOctoberToDecember 

#     def save_model(self, request, obj, form, change):
#         if change:
#             obj.Update_by = request.user
#             obj.Registered_date = datetime.now()
#         obj.save()

# admin.site.register(ExpensePerformanceFromOctoberToDecember, ExpensePerformanceFromOctoberToDecemberAdmin)

# class ExpensePerformanceFromJanuaryToMarchAdmin(ImportExportModelAdmin):
#     pass
#     fieldsets = [
#         ('General informations', {
#             'fields': [('id'),('Code'), ('Year'), ('Expense_title_amharic', 'Measurement')],
#         }), 
#         ('Detail information', {
#             'fields': [('Expense_annual_plan', 'Plan', 'Performed', 'Performance')],
#         }),
#     ]
#     list_display = ['id', 'Code', 'Year', 'Expense_title_amharic', 'Measurement', 'Expense_annual_plan', 'Plan', 'Performed', 'Performance']
#     search_fields = ['id','Code','Expense_title_amharic']
#     list_filter = ['Year']
#     list_display_links = ['id', 'Code', 'Year', 'Expense_title_amharic', 'Measurement', 'Expense_annual_plan', 'Plan', 'Performed', 'Performance']
#     readonly_fields = ('id', 'Code', 'Year', 'Expense_title_amharic', 'Measurement', 'Expense_annual_plan', 'Plan', 'Performed', 'Performance')
#     list_per_page = 10
#     list_select_related = True

#     # actions = ['download_pdf']

#     # def download_pdf(self, request, queryset):
#     #     # Getting the model name
#     #     model_name = self.model._meta.verbose_name_plural.title()

#     #     # Creating an HttpResponse object
#     #     response = HttpResponse(content_type='application/pdf')
#     #     response['Content-Disposition'] = f'attachment; filename="{model_name}.pdf"'

#     #     # Creating a PDF document
#     #     pdf = SimpleDocTemplate(response, pagesize=letter)
#     #     styles = getSampleStyleSheet()

#     #     # Create report elements
#     #     elements = []

#     #     # Add title
#     #     title = Paragraph(model_name, styles['Title'])
#     #     elements.append(title)

#     #     # Extracting headers and data from the queryset
#     #     headers = [field.verbose_name.title() for field in self.model._meta.fields]
        
#     #     # Add row numbers
#     #     headers.insert(0, 'Row Number')
#     #     data = [headers]

#     #     # Initialize the total variable for the 'purchased_items' column
#     #     total_purchased_items = sum(obj.purchased_items for obj in queryset)

#     #     # Iterate through queryset to create data rows
#     #     for idx, obj in enumerate(queryset, start=1):
#     #         data_row = [str(idx)] + [str(getattr(obj, field.name)) for field in self.model._meta.fields[:-1]]  # Exclude last column
#     #         data_row.append(str(obj.purchased_items))  # Include purchased items value
#     #         data.append(data_row)

#     #     # Create the total row
#     #     total_row = ['Total'] + [''] * (len(headers) - 2)  # Filling with empty strings for all columns except the first and last
#     #     total_row.extend([str(total_purchased_items)])  # Adding the total at the last cell

#     #     # Creating a table and styling it
#     #     table = Table(data + [total_row])
#     #     table.setStyle(TableStyle([
#     #         ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
#     #         ('GRID', (0, 0), (-1, -1), 1, colors.black),
#     #         ('SPAN', (0, -1), (-2, -1)),  # Merging cells for the total row, spanning from the first to the second to last cell
#     #     ]))

#     #     # Add table to elements
#     #     elements.append(table)

#     #      # Build PDF document with elements
#     #     pdf.build(elements, onFirstPage=self.add_page_info, onLaterPages=self.add_page_info)

#     #     return response

#     # download_pdf.short_description = 'Download selected items'

#     # def add_page_info(self, canvas, doc):
#     #     """
#     #     Add page number and printed date to PDF.
#     #     """
#     #     page_num_text = f"Page {canvas.getPageNumber()}"
#     #     printed_date_text = f"Printed Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

#     #     canvas.saveState()
#     #     canvas.setFont('Times-Roman', 10)

#     #     # Add page number at the bottom left corner
#     #     canvas.drawString(10, 20, page_num_text)

#     #     # Add printed date at the bottom right corner
#     #     printed_date_width = canvas.stringWidth(printed_date_text)
#     #     canvas.drawString(canvas._pagesize[0] - printed_date_width - 10, 20, printed_date_text)

#     #     canvas.restoreState()

#     class Meta:
#         model = ExpensePerformanceFromJanuaryToMarch 

#     def save_model(self, request, obj, form, change):
#         if change:
#             obj.Update_by = request.user
#             obj.Registered_date = datetime.now()
#         obj.save()

# admin.site.register(ExpensePerformanceFromJanuaryToMarch, ExpensePerformanceFromJanuaryToMarchAdmin)

# class ExpenseMonthlyPerformanceAdmin(ImportExportModelAdmin):
#     pass
#     fieldsets = [
#         ('General informations', {
#             'fields': [('id'),('Code'), ('Month', 'Year'), ('Expense_title_amharic', 'Measurement')],
#         }), 
#         ('Detail information', {
#             'fields': [('Expense_annual_plan', 'Plan', 'Performed', 'Performance')],
#         }),
#     ]
#     list_display = ['id', 'Code', 'Month', 'Year', 'Expense_title_amharic', 'Measurement', 'Expense_annual_plan', 'Plan', 'Performed', 'Performance']
#     search_fields = ['id','Code','Revenue_title_amharic']
#     list_filter = ['Month', 'Year']
#     list_display_links = ['id', 'Code', 'Month', 'Year', 'Expense_title_amharic', 'Measurement', 'Expense_annual_plan', 'Plan', 'Performed', 'Performance']
#     readonly_fields = ('id', 'Code', 'Month', 'Year', 'Expense_title_amharic', 'Measurement', 'Expense_annual_plan', 'Plan', 'Performed', 'Performance')
#     list_per_page = 10
#     list_select_related = True

#     # actions = ['download_pdf']

#     # def download_pdf(self, request, queryset):
#     #     # Getting the model name
#     #     model_name = self.model._meta.verbose_name_plural.title()

#     #     # Creating an HttpResponse object
#     #     response = HttpResponse(content_type='application/pdf')
#     #     response['Content-Disposition'] = f'attachment; filename="{model_name}.pdf"'

#     #     # Creating a PDF document
#     #     pdf = SimpleDocTemplate(response, pagesize=letter)
#     #     styles = getSampleStyleSheet()

#     #     # Create report elements
#     #     elements = []

#     #     # Add title
#     #     title = Paragraph(model_name, styles['Title'])
#     #     elements.append(title)

#     #     # Extracting headers and data from the queryset
#     #     headers = [field.verbose_name.title() for field in self.model._meta.fields]
        
#     #     # Add row numbers
#     #     headers.insert(0, 'Row Number')
#     #     data = [headers]

#     #     # Initialize the total variable for the 'purchased_items' column
#     #     total_purchased_items = sum(obj.purchased_items for obj in queryset)

#     #     # Iterate through queryset to create data rows
#     #     for idx, obj in enumerate(queryset, start=1):
#     #         data_row = [str(idx)] + [str(getattr(obj, field.name)) for field in self.model._meta.fields[:-1]]  # Exclude last column
#     #         data_row.append(str(obj.purchased_items))  # Include purchased items value
#     #         data.append(data_row)

#     #     # Create the total row
#     #     total_row = ['Total'] + [''] * (len(headers) - 2)  # Filling with empty strings for all columns except the first and last
#     #     total_row.extend([str(total_purchased_items)])  # Adding the total at the last cell

#     #     # Creating a table and styling it
#     #     table = Table(data + [total_row])
#     #     table.setStyle(TableStyle([
#     #         ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
#     #         ('GRID', (0, 0), (-1, -1), 1, colors.black),
#     #         ('SPAN', (0, -1), (-2, -1)),  # Merging cells for the total row, spanning from the first to the second to last cell
#     #     ]))

#     #     # Add table to elements
#     #     elements.append(table)

#     #      # Build PDF document with elements
#     #     pdf.build(elements, onFirstPage=self.add_page_info, onLaterPages=self.add_page_info)

#     #     return response

#     # download_pdf.short_description = 'Download selected items'

#     # def add_page_info(self, canvas, doc):
#     #     """
#     #     Add page number and printed date to PDF.
#     #     """
#     #     page_num_text = f"Page {canvas.getPageNumber()}"
#     #     printed_date_text = f"Printed Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

#     #     canvas.saveState()
#     #     canvas.setFont('Times-Roman', 10)

#     #     # Add page number at the bottom left corner
#     #     canvas.drawString(10, 20, page_num_text)

#     #     # Add printed date at the bottom right corner
#     #     printed_date_width = canvas.stringWidth(printed_date_text)
#     #     canvas.drawString(canvas._pagesize[0] - printed_date_width - 10, 20, printed_date_text)

#     #     canvas.restoreState()

#     class Meta:
#         model = ExpenseMonthlyPerformance 

#     def save_model(self, request, obj, form, change):
#         if change:
#             obj.Update_by = request.user
#             obj.Registered_date = datetime.now()
#         obj.save()

# admin.site.register(ExpenseMonthlyPerformance, ExpenseMonthlyPerformanceAdmin)


# class ExpenseAnnualPerformanceAdmin(ImportExportModelAdmin):
#     pass
#     fieldsets = [
#         ('General informations', {
#             'fields': [('id'),('Code'), ('Year'), ('Expense_title_amharic', 'Measurement')],
#         }), 
#         ('Detail information', {
#             'fields': [('Expense_annual_plan', 'Plan', 'Performed', 'Performance')],
#         }),
#     ]
#     list_display = ['id', 'Code', 'Year', 'Expense_title_amharic', 'Measurement', 'Expense_annual_plan', 'Plan', 'Performed', 'Performance']
#     search_fields = ['id','Code','Expense_title_amharic']
#     list_filter = ['Year']
#     list_display_links = ['id', 'Code', 'Year', 'Expense_title_amharic', 'Measurement', 'Expense_annual_plan', 'Plan', 'Performed', 'Performance']
#     readonly_fields = ('id', 'Code', 'Year', 'Expense_title_amharic', 'Measurement', 'Expense_annual_plan', 'Plan', 'Performed', 'Performance')
#     list_per_page = 10
#     list_select_related = True

#     # actions = ['download_pdf']

#     # def download_pdf(self, request, queryset):
#     #     # Getting the model name
#     #     model_name = self.model._meta.verbose_name_plural.title()

#     #     # Creating an HttpResponse object
#     #     response = HttpResponse(content_type='application/pdf')
#     #     response['Content-Disposition'] = f'attachment; filename="{model_name}.pdf"'

#     #     # Creating a PDF document
#     #     pdf = SimpleDocTemplate(response, pagesize=letter)
#     #     styles = getSampleStyleSheet()

#     #     # Create report elements
#     #     elements = []

#     #     # Add title
#     #     title = Paragraph(model_name, styles['Title'])
#     #     elements.append(title)

#     #     # Extracting headers and data from the queryset
#     #     headers = [field.verbose_name.title() for field in self.model._meta.fields]
        
#     #     # Add row numbers
#     #     headers.insert(0, 'Row Number')
#     #     data = [headers]

#     #     # Initialize the total variable for the 'purchased_items' column
#     #     total_purchased_items = sum(obj.purchased_items for obj in queryset)

#     #     # Iterate through queryset to create data rows
#     #     for idx, obj in enumerate(queryset, start=1):
#     #         data_row = [str(idx)] + [str(getattr(obj, field.name)) for field in self.model._meta.fields[:-1]]  # Exclude last column
#     #         data_row.append(str(obj.purchased_items))  # Include purchased items value
#     #         data.append(data_row)

#     #     # Create the total row
#     #     total_row = ['Total'] + [''] * (len(headers) - 2)  # Filling with empty strings for all columns except the first and last
#     #     total_row.extend([str(total_purchased_items)])  # Adding the total at the last cell

#     #     # Creating a table and styling it
#     #     table = Table(data + [total_row])
#     #     table.setStyle(TableStyle([
#     #         ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
#     #         ('GRID', (0, 0), (-1, -1), 1, colors.black),
#     #         ('SPAN', (0, -1), (-2, -1)),  # Merging cells for the total row, spanning from the first to the second to last cell
#     #     ]))

#     #     # Add table to elements
#     #     elements.append(table)

#     #      # Build PDF document with elements
#     #     pdf.build(elements, onFirstPage=self.add_page_info, onLaterPages=self.add_page_info)

#     #     return response

#     # download_pdf.short_description = 'Download selected items'

#     # def add_page_info(self, canvas, doc):
#     #     """
#     #     Add page number and printed date to PDF.
#     #     """
#     #     page_num_text = f"Page {canvas.getPageNumber()}"
#     #     printed_date_text = f"Printed Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

#     #     canvas.saveState()
#     #     canvas.setFont('Times-Roman', 10)

#     #     # Add page number at the bottom left corner
#     #     canvas.drawString(10, 20, page_num_text)

#     #     # Add printed date at the bottom right corner
#     #     printed_date_width = canvas.stringWidth(printed_date_text)
#     #     canvas.drawString(canvas._pagesize[0] - printed_date_width - 10, 20, printed_date_text)

#     #     canvas.restoreState()

#     class Meta:
#         model = ExpenseAnnualPerformance 

#     def save_model(self, request, obj, form, change):
#         if change:
#             obj.Update_by = request.user
#             obj.Registered_date = datetime.now()
#         obj.save()

# admin.site.register(ExpenseAnnualPerformance, ExpenseAnnualPerformanceAdmin)
