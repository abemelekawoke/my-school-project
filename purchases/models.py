# import decimal
# from django.db import models
# import os
# from django.db.models import Subquery, OuterRef
# from django.db import connection
# from django.utils import timezone
# import datetime
# from datetime import datetime
# from django.conf import settings
# from django.contrib.auth.models import User
# from django_currentuser.middleware import (
#     get_current_user, get_current_authenticated_user)
# from django_currentuser.db.models import CurrentUserField

# from django.urls import reverse
# from django.http import HttpResponse
# from setups.models import *
# # from .forms import *
# import logging
# from smart_selects.db_fields import ChainedForeignKey

# class PurchasedItem(models.Model):
#     def get_current_date():
#         try:
#             current_date = Date.objects.get(is_current__iexact=True)
#             return current_date
#         except Date.DoesNotExist:
#             return None
        
#     def get_current_month():
#         try:
#             current_month = Month.objects.get(is_current__iexact=True)
#             return current_month
#         except Month.DoesNotExist:
#             return None
    
#     def get_current_year():
#         try:
#             current_year = Year.objects.get(is_current__iexact=True)
#             return current_year
#         except Year.DoesNotExist:
#             return None
    
#     id = models.AutoField(primary_key=True)
#     date_purchased = models.DateTimeField(verbose_name="Date Purchased", default=timezone.now)
#     # date = models.ForeignKey(Date, on_delete=models.CASCADE, related_name='purchase_dates', default=get_current_date)
#     # month = models.ForeignKey(Month, on_delete=models.CASCADE, related_name='purchase_months', default=get_current_month)
#     # year = models.ForeignKey(Year, on_delete=models.CASCADE, related_name='purchase_years', default=get_current_year)
#     vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    
#     grand_total = models.DecimalField(max_digits=25, decimal_places=2, default=0)
#     paid_amount = models.DecimalField(max_digits=25, decimal_places=2, default=0)
#     remains = models.DecimalField(max_digits=25, decimal_places=2, default=0)
#     current_payment = models.DecimalField(max_digits=25, decimal_places=2, default=0)
#     receipt_number = models.PositiveBigIntegerField(
#         unique=True, 
#         verbose_name='Receipt Number',
#         help_text='Unique receipt number for the purchase transaction'
#     )
#     created_by = CurrentUserField(related_name="rb1")
#     created_at = models.DateField(auto_now=True)
#     modified_by = CurrentUserField(related_name="ub1")
#     modified_at = models.DateTimeField(auto_now=True)

    
#     def __str__(self):
#         return f"የ {self.vendor.name} አቅራቢ ገቢ ግዥ እቃዎች ወይም ንብረቶች"

#     class Meta:
#         db_table = 'PROPERTIES_IN_PURCHASEDITEM'
#         verbose_name = 'የእቃ ወይም የንብረት ገቢ'
#         verbose_name_plural = 'የእቃ ወይም የንብረት ገቢዎች'

#     def save(self, *args, **kwargs):
#         if self.pk:
#             self.paid_amount += self.current_payment # Add current payment to paid amount once
#             invoice_lines = PurchasedInline.objects.filter(purchased_item=self.id)
#             self.grand_total = sum(line.purchased_total_price for line in invoice_lines)
#             self.remains = self.grand_total - self.paid_amount  
#             self.current_payment = 0  # Reset current payment after it's added to paid amount         
                    
#         super(PurchasedItem, self).save(*args, **kwargs)
    
# class PurchasedInline(models.Model):
#     id = models.AutoField(primary_key=True, unique=True)
#     purchased_item = models.ForeignKey(PurchasedItem, on_delete=models.CASCADE)
#     item_categories = models.ForeignKey(ItemCategory, on_delete=models.CASCADE)
#     item_type = ChainedForeignKey(
#         ItemType,
#         chained_field="item_categories",
#         chained_model_field="item_categories",
#         show_all=False,
#         auto_choose=True,
#         sort=True,
#         on_delete=models.CASCADE
#     )
#     # item_type = models.ForeignKey(ItemType, on_delete=models.CASCADE, verbose_name='Type')
#     measurement = models.ForeignKey(Measurement, on_delete=models.CASCADE, verbose_name='Measure')
#     quantity = models.DecimalField(max_digits=25, decimal_places=2)
#     purchased_unit_price = models.DecimalField(max_digits=25, decimal_places=2, verbose_name='unit cost')
#     purchased_total_price = models.DecimalField(max_digits=25, decimal_places=2, null=True, blank=True, default=0, verbose_name='total cost')

#     def save(self, *args, **kwargs):
#         self.purchased_total_price = self.purchased_unit_price * self.quantity
#         super(PurchasedInline, self).save(*args, **kwargs)

#     class Meta:
#         verbose_name = "Purchased Material"
#         verbose_name_plural = "Purchased Materials"

#     def __str__(self):
#         return f'{self.item_type.name}'
    
# class MonthlyPurchased(models.Model):
#     id = models.AutoField(primary_key = True, unique = True)
#     vendor_name = models.CharField(max_length=150)
#     item_category = models.CharField(max_length = 150)
#     item_type = models.CharField(max_length=150)
#     measurement = models.CharField(max_length=150)
#     purchased_items = models.CharField(max_length = 150)
#     purchased_total_price = models.CharField(max_length=150, verbose_name='Total price')
#     purchase_month_name = models.CharField(max_length = 150, verbose_name='Month')
#     purchase_year = models.CharField(max_length = 150, verbose_name='Year')
    
#     def __str__(self):
#         return "%s" % (self.id)

#     class Meta:
#         verbose_name="Purchased monthly item"
#         verbose_name_plural="Purchased monthly items" 
#     class Meta:
#         managed = False
#         db_table = "Purchased_monthly_item"


# class FirstQuarterPurchased(models.Model):
#     id = models.AutoField(primary_key = True, unique = True)
#     vendor_name = models.CharField(max_length=150)
#     item_category = models.CharField(max_length = 150)
#     item_type = models.CharField(max_length=150)
#     measurement = models.CharField(max_length=150)
#     purchased_items = models.CharField(max_length = 150)
#     purchased_total_price = models.CharField(max_length=150, verbose_name='Total price')
#     purchase_month_name = models.CharField(max_length = 150, verbose_name='Month')
#     purchase_year = models.CharField(max_length = 150, verbose_name='Year')

#     def __str__(self):
#         return "%s" % (self.id)

#     class Meta:
#         verbose_name="Purchased first quarter item"
#         verbose_name_plural="Purchased first quarter item" 
#     class Meta:
#         managed = False
#         db_table = "purchased_first_quarter_item"


# class SecondQuarterPurchased(models.Model):
#     id = models.AutoField(primary_key = True, unique = True)
#     vendor_name = models.CharField(max_length=150)
#     item_category = models.CharField(max_length = 150)
#     item_type = models.CharField(max_length=150)
#     measurement = models.CharField(max_length=150)
#     purchased_items = models.CharField(max_length = 150)
#     purchased_total_price = models.CharField(max_length=150, verbose_name='Total price')
#     purchase_month_name = models.CharField(max_length = 150, verbose_name='Month')
#     purchase_year = models.CharField(max_length = 150, verbose_name='Year')

#     def __str__(self):
#         return "%s" % (self.id)

#     class Meta:
#         verbose_name="Purchased second quarter item"
#         verbose_name_plural="Purchased second quarter items" 
#     class Meta:
#         managed = False
#         db_table = "Purchased_second_quarter_item"


# class ThirdQuarterPurchased(models.Model):
#     id = models.AutoField(primary_key = True, unique = True)
#     vendor_name = models.CharField(max_length=150)
#     item_category = models.CharField(max_length = 150)
#     item_type = models.CharField(max_length=150)
#     measurement = models.CharField(max_length=150)
#     purchased_items = models.CharField(max_length = 150)
#     purchased_total_price = models.CharField(max_length=150, verbose_name='Total price')
#     purchase_month_name = models.CharField(max_length = 150, verbose_name='Month')
#     purchase_year = models.CharField(max_length = 150, verbose_name='Year')

#     def __str__(self):
#         return "%s" % (self.id)

#     class Meta:
#         verbose_name="Purchased third quarter item"
#         verbose_name_plural="Purchased third quarter items" 
#     class Meta:
#         managed = False
#         db_table = "Purchased_third_quarter_item"


# class AnnualPurchased(models.Model):
#     id = models.AutoField(primary_key = True, unique = True)
#     vendor_name = models.CharField(max_length=150)
#     item_category = models.CharField(max_length = 150)
#     item_type = models.CharField(max_length=150)
#     measurement = models.CharField(max_length=150)
#     purchased_items = models.CharField(max_length = 150)
#     purchased_total_price = models.CharField(max_length=150, verbose_name='Total price')
#     purchase_year = models.CharField(max_length = 150, verbose_name='Year')

#     def __str__(self):
#         return "%s" % (self.id)

#     class Meta:
#         verbose_name="Purchased annual item"
#         verbose_name_plural="Purchased annual item" 
#     class Meta:
#         managed = False
#         db_table = "Purchased_annual_item"


