# # from django.db import models
# from import_export.admin import ImportExportModelAdmin # type: ignore
# from django.contrib import admin # type: ignore
# from django.shortcuts import redirect # type: ignore
# from django.db import connection # type: ignore

# from django.http import HttpResponse # type: ignore
# # import csv
# from django.utils import timezone # type: ignore
# import datetime
# from datetime import datetime
# from .models import *
# from setups.models import *
# from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter
# from django.contrib.contenttypes.models import ContentType # type: ignore
# from django.http import HttpResponseRedirect # type: ignore
# from decimal import Decimal

# class CreditFilter(admin.SimpleListFilter):
#     title = 'Remains'  # Displayed title in the admin sidebar
#     parameter_name = 'remains'  # Parameter used in URL query
    
#     def lookups(self, request, model_admin):
#         return (
#             ('credit', 'My Credits'),
#         )
    
#     def queryset(self, request, queryset):
#         if self.value() == 'credit':
#             return queryset.filter(remains__gt=0)

# class PurchasedInlineAdmin(admin.TabularInline):
# 	model = PurchasedInline
# 	extra = 0
# 	list_filter = ['item_lists', 'item_type']
# 	readonly_fields = ['purchased_total_price']

# @admin.register(PurchasedItem)
# class PurchasedItemAdmin(ImportExportModelAdmin):
#     '''Admin View for PurchasedItem'''
#     inlines = [PurchasedInlineAdmin]
#     fields = [('vendor', 'date_purchased'), ('grand_total', 'paid_amount'), ('remains', 'current_payment'), 'receipt_number']
#     list_display = ('id', 'vendor', 'date_purchased', 'grand_total', 'paid_amount', 'remains', 'current_payment', 'created_by', 'created_at', 'modified_by', 'modified_at')
#     list_display_links = ('id', 'vendor', 'date_purchased', 'grand_total', 'paid_amount', 'remains', 'current_payment', 'created_by', 'created_at', 'modified_by', 'modified_at')
#     list_filter=(CreditFilter, ('date_purchased', DateRangeFilter), 'vendor__name')
#     # raw_id_fields =, 'vendor')
#     readonly_fields = ('id','created_by', 'created_at', 'modified_by', 'modified_at',)
#     search_fields = ('id', 'vendor','date_purchased')
#     # date_hierarchy = 'd'
#     # ordering = ('id',)

#     def year(self, obj):
#         return obj.purchase_years.name  # Adjust as needed
#     year.short_description = 'year'  # Adjust as needed


#     def response_add(self, request, new_object):
#         obj = self.after_saving_model_and_related_inlines(new_object)
#         return super(PurchasedItemAdmin, self).response_add(request, obj)

#     def response_change(self, request, obj):
#         obj = self.after_saving_model_and_related_inlines(obj)
#         return super(PurchasedItemAdmin, self).response_change(request, obj)

#     def after_saving_model_and_related_inlines(self, obj):
#         if obj.pk:
#             invoice_lines = PurchasedInline.objects.filter(purchased_item=obj.id)
#             obj.grand_total = 0
#             for line in invoice_lines:
#                 obj.grand_total += line.purchased_total_price
#             obj.remains = (obj.grand_total - obj.paid_amount) 

#             obj.save()  # Save the updated object
#         return obj

# class MonthlyPurchasedAdmin(admin.ModelAdmin):
#     fieldsets = [
#         ('General informations', {
#             'fields': [('id','vendor_name'),('item_category', 'item_type', 'measurement')],
#         }), 
#         ('Detail information', {
#             'fields': [('purchased_items', 'purchased_total_price'), ('purchase_month_name', 'purchase_year')],
#         }),
#     ]
#     list_display = ['id', 'vendor_name', 'item_category', 'item_type', 'measurement', 'purchased_items', 'purchased_total_price', 'purchase_month_name', 'purchase_year']
#     search_fields = ['id','item_category', 'item_type']
#     list_filter = ['item_category', 'item_type']
#     list_display_links = ['id', 'vendor_name', 'item_category', 'item_type', 'measurement', 'purchased_items', 'purchased_total_price', 'purchase_month_name', 'purchase_year']
#     readonly_fields = ('id', 'vendor_name', 'item_category', 'item_type', 'measurement', 'purchased_items', 'purchased_total_price', 'purchase_month_name', 'purchase_year')
#     list_per_page = 10
#     list_select_related = True

#     actions = ['download_pdf']

#     def download_pdf(self, request, queryset):
#         model_name = self.model._meta.verbose_name_plural.title()

#         response = HttpResponse(content_type='application/pdf')
#         response['Content-Disposition'] = f'attachment; filename="{model_name}.pdf"'

#         pdf = SimpleDocTemplate(response, pagesize=letter)
#         styles = getSampleStyleSheet()

#         elements = []

#         title_style = ParagraphStyle(name='Title', parent=styles['Title'], textColor=colors.black, underline=True)
#         title = Paragraph(model_name, title_style)
#         elements.append(title)
#         elements.append(Spacer(1, 12))

#         headers = [field.verbose_name.title() for field in self.model._meta.fields]
#         headers.insert(0, '#')
#         data = [headers]

#         total_purchased_items = 0
#         total_purchased_total_price = 0

#         for idx, obj in enumerate(queryset, start=0):
#             row_data = [str(idx)] + [str(getattr(obj, field.name)) for field in self.model._meta.fields[:]]
#             purchased_items = obj.purchased_items
#             purchased_total_price = obj.purchased_total_price
#             total_purchased_items += purchased_items
#             total_purchased_total_price += purchased_total_price
#             # row_data.append(str(purchased_items))
#             # row_data.append(str(purchased_total_price))
#             data.append(row_data)

#         totals_row = ['Total'] + [''] * (len(headers) - 5) + [str(total_purchased_items), str(total_purchased_total_price)]
#         data.append(totals_row)

#         table = Table(data)
#         table.setStyle(TableStyle([
#             ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
#             ('GRID', (0, 0), (-1, -1), 1, colors.black),
#             ('SPAN', (0, -1), (2, -1)),
#         ]))

#         elements.append(table)

#         pdf.build(elements, onFirstPage=self.add_page_info, onLaterPages=self.add_page_info)

#         return response

#     download_pdf.short_description = 'Download selected items'

#     def add_page_info(self, canvas, doc):
#         page_num_text = f"Page {canvas.getPageNumber()}"
#         printed_date_text = f"Printed Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

#         canvas.saveState()
#         canvas.setFont('Times-Roman', 10)

#         canvas.drawString(10, 20, page_num_text)

#         printed_date_width = canvas.stringWidth(printed_date_text)
#         canvas.drawString(canvas._pagesize[0] - printed_date_width - 10, 20, printed_date_text)

#         canvas.restoreState()

#     class Meta:
#         model = MonthlyPurchased  

#     def save_model(self, request, obj, form, change):
#         if change:
#             obj.Update_by = request.user
#             obj.Registered_date = datetime.now()
#         obj.save()

# admin.site.register(MonthlyPurchased, MonthlyPurchasedAdmin)


# class FirstQuarterPurchasedAdmin(ImportExportModelAdmin):
#     pass
#     fieldsets = [
#         ('General informations', {
#             'fields': [('id','vendor_name'),('item_category', 'item_type', 'measurement')],
#         }), 
#         ('Detail information', {
#             'fields': [('purchased_items', 'purchased_total_price'), ('purchase_month_name', 'purchase_year')],
#         }),
#     ]
#     list_display = ['id', 'vendor_name', 'item_category', 'item_type', 'measurement', 'purchased_items', 'purchased_total_price', 'purchase_month_name', 'purchase_year']
#     search_fields = ['id','item_category', 'item_type']
#     list_filter = ['item_category', 'item_type']
#     list_display_links = ['id', 'vendor_name', 'item_category', 'item_type', 'measurement', 'purchased_items', 'purchased_total_price', 'purchase_month_name', 'purchase_year']
#     readonly_fields = ('id', 'vendor_name', 'item_category', 'item_type', 'measurement', 'purchased_items', 'purchased_total_price', 'purchase_month_name', 'purchase_year')
#     list_per_page = 10
#     list_select_related = True

#     actions = ['download_pdf']

#     def download_pdf(self, request, queryset):
#         model_name = self.model._meta.verbose_name_plural.title()

#         response = HttpResponse(content_type='application/pdf')
#         response['Content-Disposition'] = f'attachment; filename="{model_name}.pdf"'

#         pdf = SimpleDocTemplate(response, pagesize=letter)
#         styles = getSampleStyleSheet()

#         elements = []

#         title_style = ParagraphStyle(name='Title', parent=styles['Title'], textColor=colors.black, underline=True)
#         title = Paragraph(model_name, title_style)
#         elements.append(title)
#         elements.append(Spacer(1, 12))

#         headers = [field.verbose_name.title() for field in self.model._meta.fields]
#         headers.insert(0, '#')
#         data = [headers]

#         total_purchased_items = 0
#         total_purchased_total_price = 0

#         for idx, obj in enumerate(queryset, start=0):
#             row_data = [str(idx)] + [str(getattr(obj, field.name)) for field in self.model._meta.fields[:]]
#             purchased_items = obj.purchased_items
#             purchased_total_price = obj.purchased_total_price
#             total_purchased_items += purchased_items
#             total_purchased_total_price += purchased_total_price
#             # row_data.append(str(purchased_items))
#             # row_data.append(str(purchased_total_price))
#             data.append(row_data)

#         totals_row = ['Total'] + [''] * (len(headers) - 5) + [str(total_purchased_items), str(total_purchased_total_price)]
#         data.append(totals_row)

#         table = Table(data)
#         table.setStyle(TableStyle([
#             ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
#             ('GRID', (0, 0), (-1, -1), 1, colors.black),
#             ('SPAN', (0, -1), (2, -1)),
#         ]))

#         elements.append(table)

#         pdf.build(elements, onFirstPage=self.add_page_info, onLaterPages=self.add_page_info)

#         return response

#     download_pdf.short_description = 'Download selected items'

#     def add_page_info(self, canvas, doc):
#         page_num_text = f"Page {canvas.getPageNumber()}"
#         printed_date_text = f"Printed Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

#         canvas.saveState()
#         canvas.setFont('Times-Roman', 10)

#         canvas.drawString(10, 20, page_num_text)

#         printed_date_width = canvas.stringWidth(printed_date_text)
#         canvas.drawString(canvas._pagesize[0] - printed_date_width - 10, 20, printed_date_text)

#         canvas.restoreState()

#     class Meta:
#         model = FirstQuarterPurchased  

#     def save_model(self, request, obj, form, change):
#         if change:
#             obj.Update_by = request.user
#             obj.Registered_date = datetime.now()
#         obj.save()

# admin.site.register(FirstQuarterPurchased, FirstQuarterPurchasedAdmin)


# class SecondQuarterPurchasedAdmin(ImportExportModelAdmin):
#     pass
#     fieldsets = [
#         ('General informations', {
#             'fields': [('id','vendor_name'),('item_category', 'item_type', 'measurement')],
#         }), 
#         ('Detail information', {
#             'fields': [('purchased_items', 'purchased_total_price'), ('purchase_month_name', 'purchase_year')],
#         }),
#     ]
#     list_display = ['id', 'vendor_name', 'item_category', 'item_type', 'measurement', 'purchased_items', 'purchased_total_price', 'purchase_month_name', 'purchase_year']
#     search_fields = ['id','item_category', 'item_type']
#     list_filter = ['item_category', 'item_type']
#     list_display_links = ['id', 'vendor_name', 'item_category', 'item_type', 'measurement', 'purchased_items', 'purchased_total_price', 'purchase_month_name', 'purchase_year']
#     readonly_fields = ('id', 'vendor_name', 'item_category', 'item_type', 'measurement', 'purchased_items', 'purchased_total_price', 'purchase_month_name', 'purchase_year')
#     list_per_page = 10
#     list_select_related = True

#     actions = ['download_pdf']

#     def download_pdf(self, request, queryset):
#         model_name = self.model._meta.verbose_name_plural.title()

#         response = HttpResponse(content_type='application/pdf')
#         response['Content-Disposition'] = f'attachment; filename="{model_name}.pdf"'

#         pdf = SimpleDocTemplate(response, pagesize=letter)
#         styles = getSampleStyleSheet()

#         elements = []

#         title_style = ParagraphStyle(name='Title', parent=styles['Title'], textColor=colors.black, underline=True)
#         title = Paragraph(model_name, title_style)
#         elements.append(title)
#         elements.append(Spacer(1, 12))

#         headers = [field.verbose_name.title() for field in self.model._meta.fields]
#         headers.insert(0, '#')
#         data = [headers]

#         total_purchased_items = 0
#         total_purchased_total_price = 0

#         for idx, obj in enumerate(queryset, start=0):
#             row_data = [str(idx)] + [str(getattr(obj, field.name)) for field in self.model._meta.fields[:]]
#             purchased_items = obj.purchased_items
#             purchased_total_price = obj.purchased_total_price
#             total_purchased_items += purchased_items
#             total_purchased_total_price += purchased_total_price
#             # row_data.append(str(purchased_items))
#             # row_data.append(str(purchased_total_price))
#             data.append(row_data)

#         totals_row = ['Total'] + [''] * (len(headers) - 5) + [str(total_purchased_items), str(total_purchased_total_price)]
#         data.append(totals_row)

#         table = Table(data)
#         table.setStyle(TableStyle([
#             ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
#             ('GRID', (0, 0), (-1, -1), 1, colors.black),
#             ('SPAN', (0, -1), (2, -1)),
#         ]))

#         elements.append(table)

#         pdf.build(elements, onFirstPage=self.add_page_info, onLaterPages=self.add_page_info)

#         return response

#     download_pdf.short_description = 'Download selected items'

#     def add_page_info(self, canvas, doc):
#         page_num_text = f"Page {canvas.getPageNumber()}"
#         printed_date_text = f"Printed Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

#         canvas.saveState()
#         canvas.setFont('Times-Roman', 10)

#         canvas.drawString(10, 20, page_num_text)

#         printed_date_width = canvas.stringWidth(printed_date_text)
#         canvas.drawString(canvas._pagesize[0] - printed_date_width - 10, 20, printed_date_text)

#         canvas.restoreState()

#     class Meta:
#         model = SecondQuarterPurchased  

#     def save_model(self, request, obj, form, change):
#         if change:
#             obj.Update_by = request.user
#             obj.Registered_date = datetime.now()
#         obj.save()

# admin.site.register(SecondQuarterPurchased, SecondQuarterPurchasedAdmin)


# class ThirdQuarterPurchasedAdmin(ImportExportModelAdmin):
#     pass
#     fieldsets = [
#         ('General informations', {
#             'fields': [('id','vendor_name'),('item_category', 'item_type', 'measurement')],
#         }), 
#         ('Detail information', {
#             'fields': [('purchased_items', 'purchased_total_price'), ('purchase_month_name', 'purchase_year')],
#         }),
#     ]
#     list_display = ['id', 'vendor_name', 'item_category', 'item_type', 'measurement', 'purchased_items', 'purchased_total_price', 'purchase_month_name', 'purchase_year']
#     search_fields = ['id','item_category', 'item_type']
#     list_filter = ['item_category', 'item_type']
#     list_display_links = ['id', 'vendor_name', 'item_category', 'item_type', 'measurement', 'purchased_items', 'purchased_total_price', 'purchase_month_name', 'purchase_year']
#     readonly_fields = ('id', 'vendor_name', 'item_category', 'item_type', 'measurement', 'purchased_items', 'purchased_total_price', 'purchase_month_name', 'purchase_year')
#     list_per_page = 10
#     list_select_related = True

#     actions = ['download_pdf']

#     def download_pdf(self, request, queryset):
#         model_name = self.model._meta.verbose_name_plural.title()

#         response = HttpResponse(content_type='application/pdf')
#         response['Content-Disposition'] = f'attachment; filename="{model_name}.pdf"'

#         pdf = SimpleDocTemplate(response, pagesize=letter)
#         styles = getSampleStyleSheet()

#         elements = []

#         title_style = ParagraphStyle(name='Title', parent=styles['Title'], textColor=colors.black, underline=True)
#         title = Paragraph(model_name, title_style)
#         elements.append(title)
#         elements.append(Spacer(1, 12))

#         headers = [field.verbose_name.title() for field in self.model._meta.fields]
#         headers.insert(0, '#')
#         data = [headers]

#         total_purchased_items = 0
#         total_purchased_total_price = 0

#         for idx, obj in enumerate(queryset, start=0):
#             row_data = [str(idx)] + [str(getattr(obj, field.name)) for field in self.model._meta.fields[:]]
#             purchased_items = obj.purchased_items
#             purchased_total_price = obj.purchased_total_price
#             total_purchased_items += purchased_items
#             total_purchased_total_price += purchased_total_price
#             # row_data.append(str(purchased_items))
#             # row_data.append(str(purchased_total_price))
#             data.append(row_data)

#         totals_row = ['Total'] + [''] * (len(headers) - 5) + [str(total_purchased_items), str(total_purchased_total_price)]
#         data.append(totals_row)

#         table = Table(data)
#         table.setStyle(TableStyle([
#             ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
#             ('GRID', (0, 0), (-1, -1), 1, colors.black),
#             ('SPAN', (0, -1), (2, -1)),
#         ]))

#         elements.append(table)

#         pdf.build(elements, onFirstPage=self.add_page_info, onLaterPages=self.add_page_info)

#         return response

#     download_pdf.short_description = 'Download selected items'

#     def add_page_info(self, canvas, doc):
#         page_num_text = f"Page {canvas.getPageNumber()}"
#         printed_date_text = f"Printed Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

#         canvas.saveState()
#         canvas.setFont('Times-Roman', 10)

#         canvas.drawString(10, 20, page_num_text)

#         printed_date_width = canvas.stringWidth(printed_date_text)
#         canvas.drawString(canvas._pagesize[0] - printed_date_width - 10, 20, printed_date_text)

#         canvas.restoreState()

#     class Meta:
#         model = ThirdQuarterPurchased  

#     def save_model(self, request, obj, form, change):
#         if change:
#             obj.Update_by = request.user
#             obj.Registered_date = datetime.now()
#         obj.save()

# admin.site.register(ThirdQuarterPurchased, ThirdQuarterPurchasedAdmin)


# class AnnualPurchasedAdmin(ImportExportModelAdmin):
#     pass
#     fieldsets = [
#         ('General informations', {
#             'fields': [('id','vendor_name'),('item_category', 'item_type', 'measurement')],
#         }), 
#         ('Detail information', {
#             'fields': [('purchased_items', 'purchased_total_price'), ('purchase_year')],
#         }),
#     ]
#     list_display = ['id', 'vendor_name', 'item_category', 'item_type', 'measurement', 'purchased_items', 'purchased_total_price', 'purchase_year']
#     search_fields = ['id','item_category', 'item_type']
#     list_filter = ['item_category', 'item_type']
#     list_display_links = ['id', 'vendor_name', 'item_category', 'item_type', 'measurement', 'purchased_items', 'purchased_total_price', 'purchase_year']
#     readonly_fields = ('id', 'vendor_name', 'item_category', 'item_type', 'measurement', 'purchased_items', 'purchased_total_price', 'purchase_year')
#     list_per_page = 10
#     list_select_related = True

#     actions = ['download_pdf']

#     def download_pdf(self, request, queryset):
#         model_name = self.model._meta.verbose_name_plural.title()

#         response = HttpResponse(content_type='application/pdf')
#         response['Content-Disposition'] = f'attachment; filename="{model_name}.pdf"'

#         pdf = SimpleDocTemplate(response, pagesize=letter)
#         styles = getSampleStyleSheet()

#         elements = []

#         title_style = ParagraphStyle(name='Title', parent=styles['Title'], textColor=colors.black, underline=True)
#         title = Paragraph(model_name, title_style)
#         elements.append(title)
#         elements.append(Spacer(1, 12))

#         headers = [field.verbose_name.title() for field in self.model._meta.fields]
#         headers.insert(0, '#')
#         data = [headers]

#         total_purchased_items = 0
#         total_purchased_total_price = 0

#         for idx, obj in enumerate(queryset, start=0):
#             row_data = [str(idx)] + [str(getattr(obj, field.name)) for field in self.model._meta.fields[:]]
#             purchased_items = obj.purchased_items
#             purchased_total_price = obj.purchased_total_price
#             total_purchased_items += purchased_items
#             total_purchased_total_price += purchased_total_price
#             # row_data.append(str(purchased_items))
#             # row_data.append(str(purchased_total_price))
#             data.append(row_data)

#         totals_row = ['Total'] + [''] * (len(headers) - 4) + [str(total_purchased_items), str(total_purchased_total_price)]
#         data.append(totals_row)

#         table = Table(data)
#         table.setStyle(TableStyle([
#             ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
#             ('GRID', (0, 0), (-1, -1), 1, colors.black),
#             ('SPAN', (0, -1), (2, -1)),
#         ]))

#         elements.append(table)

#         pdf.build(elements, onFirstPage=self.add_page_info, onLaterPages=self.add_page_info)

#         return response

#     download_pdf.short_description = 'Download selected items'

#     def add_page_info(self, canvas, doc):
#         page_num_text = f"Page {canvas.getPageNumber()}"
#         printed_date_text = f"Printed Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

#         canvas.saveState()
#         canvas.setFont('Times-Roman', 10)

#         canvas.drawString(10, 20, page_num_text)

#         printed_date_width = canvas.stringWidth(printed_date_text)
#         canvas.drawString(canvas._pagesize[0] - printed_date_width - 10, 20, printed_date_text)

#         canvas.restoreState()

#     class Meta:
#         model = AnnualPurchased  

#     def save_model(self, request, obj, form, change):
#         if change:
#             obj.Update_by = request.user
#             obj.Registered_date = datetime.now()
#         obj.save()

# admin.site.register(AnnualPurchased, AnnualPurchasedAdmin)
