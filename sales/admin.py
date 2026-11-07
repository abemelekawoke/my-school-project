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
# from django.contrib.contenttypes.models import ContentType # type: ignore
# from django.http import HttpResponseRedirect # type: ignore
# from decimal import Decimal
# from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter
# from setups.admin import *

# from django.urls import reverse
# from django.utils.html import format_html
# from django.forms import ModelForm
# # from django.conf.urls import url
# from django.http import JsonResponse
# from purchases.models import PurchasedInline
# from .resources import OrderResource

# class CreditFilter(admin.SimpleListFilter):
#     title = 'Remains'  # Displayed title in the admin sidebar
#     parameter_name = 'remains'  # Parameter used in URL query
    
#     def lookups(self, request, model_admin):
#         return (
#             ('credit', 'Credited Customers'),
#         )
    
#     def queryset(self, request, queryset):
#         if self.value() == 'credit':
#             return queryset.filter(remains__gt=0)

# class SoldInlineAdmin(admin.TabularInline):
#      model = SoldInline
#      extra = 0
#      list_filter = ['item_lists', 'item_type']
#      readonly_fields = ['purchased_unit_price']
#     #  raw_id_fields = ['sold_unit_price']
#     #  autocomplete_fields = ['sold_unit_price']
#     #  filter_horizontal = ['item_lists']

# class SoldItemAdmin(ImportExportModelAdmin):
#     '''Admin View for PurchasedItem'''
#     inlines = [SoldInlineAdmin]
#     resource_class = OrderResource
#     fields = [('customer', 'date_sold'), ('grand_total', 'paid_amount', 'remains', 'current_payment'), 'receipt_number']
#     list_display = ('id', 'customer_name', 'date_sold', 'grand_total', 'paid_amount', 'remains', 'current_payment', 'created_by', 'created_at', 'modified_by', 'modified_at')
#     list_display_links = ('id', 'customer_name', 'date_sold', 'grand_total', 'paid_amount', 'remains', 'current_payment', 'created_by', 'created_at', 'modified_by', 'modified_at')
#     # list_filter = ('customer__name', 'date__date', 'month__month', 'year__year')
#     list_filter = (CreditFilter, ('date_sold', DateRangeFilter), 'customer__name')
#     readonly_fields = ('id','created_by', 'created_at', 'modified_by', 'modified_at',)
#     search_fields = ('id', 'customer', 'date_sold')
#     # date_hierarchy = 'Sold_at'
#     # ordering = ('id',)

#     def customer_name(self, obj):
#          return obj.customer.name
    
#     customer_name.short_description='Customer'

#     def response_add(self, request, new_object):
#         obj = self.after_saving_model_and_related_inlines(new_object)
#         return super(SoldItemAdmin, self).response_add(request, obj)

#     def response_change(self, request, obj):
#         obj = self.after_saving_model_and_related_inlines(obj)
#         return super(SoldItemAdmin, self).response_change(request, obj)

#     def after_saving_model_and_related_inlines(self, obj):
#         if obj.pk:
#             invoice_lines = SoldInline.objects.filter(sold_item=obj.id)
#             # obj.paid_amount += obj.current_payment
#             obj.grand_total = 0
#             for line in invoice_lines:
#                 obj.grand_total
#             obj.remains = (obj.grand_total - obj.paid_amount) 
#             obj.save()  # Save the updated object
#         return obj
    
#     class Media:
#         js = ('admin/js/sale.js',)

# admin.site.register(SoldItem, SoldItemAdmin) 


# class SoldFilter(admin.SimpleListFilter):
#     title = 'Sold Status'
#     parameter_name = 'sold_status'

#     def lookups(self, request, model_admin):
#         return (
#             ('sold', 'Sold items'),
#             ('unsold', 'Unsold items'),
#         )

#     def queryset(self, request, queryset):
#         if self.value() == 'sold':
#             return queryset.filter(total_sold_items__gt=Decimal('0.00'))
#         if self.value() == 'unsold':
#             return queryset.filter(total_sold_items__lte=Decimal('0.00'))
#         return queryset
    
            
# class MonthlySoldAdmin(ImportExportModelAdmin):
#     fieldsets = [
#         ('General informations', {
#             'fields': [('id'), ('customer_name'), ('item_category', 'item_type')],
#         }),
#         ('Detail information', {
#             'fields': [('sold_month_name', 'sold_year'), ('total_sold_items', 'sold_total_price'), ('profit_by_unit', 'total_profit'), ('total_asrat')],
#         }),
#     ]
#     list_display = ['id', 'sold_month_name', 'sold_year', 'customer_name', 'item_category', 'item_type', 'total_sold_items', 'sold_total_price', 'profit_by_unit', 'total_profit', 'total_asrat']
#     search_fields = ['id', 'item_category', 'item_type']
#     list_filter = (SoldFilter, 'item_category', 'item_type')
#     list_display_links = ['id', 'sold_month_name', 'sold_year', 'customer_name', 'item_category', 'item_type', 'total_sold_items', 'sold_total_price', 'profit_by_unit', 'total_profit', 'total_asrat']
#     readonly_fields = ['id', 'sold_month_name', 'sold_year', 'customer_name', 'item_category', 'item_type', 'total_sold_items', 'sold_total_price', 'profit_by_unit', 'total_profit', 'total_asrat']
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

#         total_sold_items_t = 0
#         sold_total_price_t = 0
#         profit_by_unit_t = 0
#         total_profit_t = 0
#         total_asrat_t = 0

#         for idx, obj in enumerate(queryset, start=0):
#             row_data = [str(idx)] + [str(getattr(obj, field.name)) for field in self.model._meta.fields[:]]

#             total_sold_items = Decimal(obj.total_sold_items)
#             sold_total_price = Decimal(obj.sold_total_price)
#             profit_by_unit = Decimal(obj.profit_by_unit)
#             total_profit = Decimal(obj.total_profit)
#             total_asrat = Decimal(obj.total_asrat)
#             total_sold_items_t += total_sold_items
#             sold_total_price_t += sold_total_price
#             profit_by_unit_t += profit_by_unit
#             total_profit_t += total_profit
#             total_asrat_t += total_asrat
#             data.append(row_data)

#         totals_row = ['Total'] + [''] * (len(headers) - 6) + [str(total_sold_items_t), str(sold_total_price_t), str(profit_by_unit_t), str(total_profit_t), str(total_asrat_t)]
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
#         model = MonthlySold  

#     def save_model(self, request, obj, form, change):
#         if change:
#             obj.Update_by = request.user
#             obj.Registered_date = datetime.now()
#         obj.save()

# admin.site.register(MonthlySold, MonthlySoldAdmin)


# class FirstQuarterSoldAdmin(ImportExportModelAdmin):
#     fieldsets = [
#         ('General informations', {
#             'fields': [('id'), ('customer_name'), ('item_category', 'item_type')],
#         }),
#         ('Detail information', {
#             'fields': [('sold_month_name', 'sold_year'), ('total_sold_items', 'sold_total_price'), ('profit_by_unit', 'total_profit'), ('total_asrat')],
#         }),
#     ]
#     list_display = ['id', 'sold_month_name', 'sold_year', 'customer_name', 'item_category', 'item_type', 'total_sold_items', 'sold_total_price', 'profit_by_unit', 'total_profit', 'total_asrat']
#     search_fields = ['id', 'item_category', 'item_type']
#     list_filter = (SoldFilter, 'item_category', 'item_type')
#     list_display_links = ['id', 'sold_month_name', 'sold_year', 'customer_name', 'item_category', 'item_type', 'total_sold_items', 'sold_total_price', 'profit_by_unit', 'total_profit', 'total_asrat']
#     readonly_fields = ['id', 'sold_month_name', 'sold_year', 'customer_name', 'item_category', 'item_type', 'total_sold_items', 'sold_total_price', 'profit_by_unit', 'total_profit', 'total_asrat']
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

#         total_sold_items_t = 0
#         sold_total_price_t = 0
#         profit_by_unit_t = 0
#         total_profit_t = 0
#         total_asrat_t = 0

#         for idx, obj in enumerate(queryset, start=0):
#             row_data = [str(idx)] + [str(getattr(obj, field.name)) for field in self.model._meta.fields[:]]

#             total_sold_items = Decimal(obj.total_sold_items)
#             sold_total_price = Decimal(obj.sold_total_price)
#             profit_by_unit = Decimal(obj.profit_by_unit)
#             total_profit = Decimal(obj.total_profit)
#             total_asrat = Decimal(obj.total_asrat)
#             total_sold_items_t += total_sold_items
#             sold_total_price_t += sold_total_price
#             profit_by_unit_t += profit_by_unit
#             total_profit_t += total_profit
#             total_asrat_t += total_asrat
#             data.append(row_data)

#         totals_row = ['Total'] + [''] * (len(headers) - 6) + [str(total_sold_items_t), str(sold_total_price_t), str(profit_by_unit_t), str(total_profit_t), str(total_asrat_t)]
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
#         model = FirstQuarterSold  

#     def save_model(self, request, obj, form, change):
#         if change:
#             obj.Update_by = request.user
#             obj.Registered_date = datetime.now()
#         obj.save()

# admin.site.register(FirstQuarterSold, FirstQuarterSoldAdmin)


# class SecondQuarterSoldAdmin(ImportExportModelAdmin):
#     fieldsets = [
#         ('General informations', {
#             'fields': [('id'), ('customer_name'), ('item_category', 'item_type')],
#         }),
#         ('Detail information', {
#             'fields': [('sold_month_name', 'sold_year'), ('total_sold_items', 'sold_total_price'), ('profit_by_unit', 'total_profit'), ('total_asrat')],
#         }),
#     ]
#     list_display = ['id', 'sold_month_name', 'sold_year', 'customer_name', 'item_category', 'item_type', 'total_sold_items', 'sold_total_price', 'profit_by_unit', 'total_profit', 'total_asrat']
#     search_fields = ['id', 'item_category', 'item_type']
#     list_filter = (SoldFilter, 'item_category', 'item_type')
#     list_display_links = ['id', 'sold_month_name', 'sold_year', 'customer_name', 'item_category', 'item_type', 'total_sold_items', 'sold_total_price', 'profit_by_unit', 'total_profit', 'total_asrat']
#     readonly_fields = ['id', 'sold_month_name', 'sold_year', 'customer_name', 'item_category', 'item_type', 'total_sold_items', 'sold_total_price', 'profit_by_unit', 'total_profit', 'total_asrat']
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

#         total_sold_items_t = 0
#         sold_total_price_t = 0
#         profit_by_unit_t = 0
#         total_profit_t = 0
#         total_asrat_t = 0

#         for idx, obj in enumerate(queryset, start=0):
#             row_data = [str(idx)] + [str(getattr(obj, field.name)) for field in self.model._meta.fields[:]]

#             total_sold_items = Decimal(obj.total_sold_items)
#             sold_total_price = Decimal(obj.sold_total_price)
#             profit_by_unit = Decimal(obj.profit_by_unit)
#             total_profit = Decimal(obj.total_profit)
#             total_asrat = Decimal(obj.total_asrat)
#             total_sold_items_t += total_sold_items
#             sold_total_price_t += sold_total_price
#             profit_by_unit_t += profit_by_unit
#             total_profit_t += total_profit
#             total_asrat_t += total_asrat
#             data.append(row_data)

#         totals_row = ['Total'] + [''] * (len(headers) - 6) + [str(total_sold_items_t), str(sold_total_price_t), str(profit_by_unit_t), str(total_profit_t), str(total_asrat_t)]
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
#         model = SecondQuarterSold  

#     def save_model(self, request, obj, form, change):
#         if change:
#             obj.Update_by = request.user
#             obj.Registered_date = datetime.now()
#         obj.save()

# admin.site.register(SecondQuarterSold, SecondQuarterSoldAdmin)


# class ThirdQuarterSoldAdmin(ImportExportModelAdmin):
#     fieldsets = [
#         ('General informations', {
#             'fields': [('id'), ('customer_name'), ('item_category', 'item_type')],
#         }),
#         ('Detail information', {
#             'fields': [('sold_month_name', 'sold_year'), ('total_sold_items', 'sold_total_price'), ('profit_by_unit', 'total_profit'), ('total_asrat')],
#         }),
#     ]
#     list_display = ['id', 'sold_month_name', 'sold_year', 'customer_name', 'item_category', 'item_type', 'total_sold_items', 'sold_total_price', 'profit_by_unit', 'total_profit', 'total_asrat']
#     search_fields = ['id', 'item_category', 'item_type']
#     list_filter = (SoldFilter, 'item_category', 'item_type')
#     list_display_links = ['id', 'sold_month_name', 'sold_year', 'customer_name', 'item_category', 'item_type', 'total_sold_items', 'sold_total_price', 'profit_by_unit', 'total_profit', 'total_asrat']
#     readonly_fields = ['id', 'sold_month_name', 'sold_year', 'customer_name', 'item_category', 'item_type', 'total_sold_items', 'sold_total_price', 'profit_by_unit', 'total_profit', 'total_asrat']
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

#         total_sold_items_t = 0
#         sold_total_price_t = 0
#         profit_by_unit_t = 0
#         total_profit_t = 0
#         total_asrat_t = 0

#         for idx, obj in enumerate(queryset, start=0):
#             row_data = [str(idx)] + [str(getattr(obj, field.name)) for field in self.model._meta.fields[:]]

#             total_sold_items = Decimal(obj.total_sold_items)
#             sold_total_price = Decimal(obj.sold_total_price)
#             profit_by_unit = Decimal(obj.profit_by_unit)
#             total_profit = Decimal(obj.total_profit)
#             total_asrat = Decimal(obj.total_asrat)
#             total_sold_items_t += total_sold_items
#             sold_total_price_t += sold_total_price
#             profit_by_unit_t += profit_by_unit
#             total_profit_t += total_profit
#             total_asrat_t += total_asrat
#             data.append(row_data)

#         totals_row = ['Total'] + [''] * (len(headers) - 6) + [str(total_sold_items_t), str(sold_total_price_t), str(profit_by_unit_t), str(total_profit_t), str(total_asrat_t)]
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
#         model = ThirdQuarterSold  

#     def save_model(self, request, obj, form, change):
#         if change:
#             obj.Update_by = request.user
#             obj.Registered_date = datetime.now()
#         obj.save()

# admin.site.register(ThirdQuarterSold, ThirdQuarterSoldAdmin)


# class AnnualSoldAdmin(ImportExportModelAdmin):
#     fieldsets = [
#         ('General informations', {
#             'fields': [('id'), ('customer_name'), ('item_category', 'item_type')],
#         }),
#         ('Detail information', {
#             'fields': [('sold_year'), ('total_sold_items', 'sold_total_price'), ('profit_by_unit', 'total_profit'), ('total_asrat')],
#         }),
#     ]
#     list_display = ['id', 'sold_year', 'customer_name', 'item_category', 'item_type', 'total_sold_items', 'sold_total_price', 'profit_by_unit', 'total_profit', 'total_asrat']
#     search_fields = ['id', 'item_category', 'item_type']
#     list_filter = (SoldFilter, 'item_category', 'item_type')
#     list_display_links = ['id', 'sold_year', 'customer_name', 'item_category', 'item_type', 'total_sold_items', 'sold_total_price', 'profit_by_unit', 'total_profit', 'total_asrat']
#     readonly_fields = ['id', 'sold_year', 'customer_name', 'item_category', 'item_type', 'total_sold_items', 'sold_total_price', 'profit_by_unit', 'total_profit', 'total_asrat']
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

#         total_sold_items_t = 0
#         sold_total_price_t = 0
#         profit_by_unit_t = 0
#         total_profit_t = 0
#         total_asrat_t = 0

#         for idx, obj in enumerate(queryset, start=0):
#             row_data = [str(idx)] + [str(getattr(obj, field.name)) for field in self.model._meta.fields[:]]

#             total_sold_items = Decimal(obj.total_sold_items)
#             sold_total_price = Decimal(obj.sold_total_price)
#             profit_by_unit = Decimal(obj.profit_by_unit)
#             total_profit = Decimal(obj.total_profit)
#             total_asrat = Decimal(obj.total_asrat)
#             total_sold_items_t += total_sold_items
#             sold_total_price_t += sold_total_price
#             profit_by_unit_t += profit_by_unit
#             total_profit_t += total_profit
#             total_asrat_t += total_asrat
#             data.append(row_data)

#         totals_row = ['Total'] + [''] * (len(headers) - 6) + [str(total_sold_items_t), str(sold_total_price_t), str(profit_by_unit_t), str(total_profit_t), str(total_asrat_t)]
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
#         model = AnnualSold  

#     def save_model(self, request, obj, form, change):
#         if change:
#             obj.Update_by = request.user
#             obj.Registered_date = datetime.now()
#         obj.save()

# admin.site.register(AnnualSold, AnnualSoldAdmin)