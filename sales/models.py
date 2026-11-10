# import decimal
# from django.db import models # type: ignore
# from decimal import Decimal
# from django_currentuser.middleware import get_current_user, get_current_authenticated_user # type: ignore
# from django_currentuser.db.models import CurrentUserField # type: ignore
# from setups.models import *
# from purchases.models import *
# from smart_selects.db_fields import ChainedForeignKey

# class SoldItem(models.Model):
#     Customer_choices = (
# 	    ('Permanent', 'Permanent'),
# 	    ('Regular', 'Regular'),
# 	)
#     Stock_choices = (
# 	    ('Yes', 'Yes'),
# 	    ('No', 'No'),
# 	)
#     def get_current_date():
#         try:
#             current_date = Date.objects.get(is_current__iexact=True)
#             return current_date
#         except Date.DoesNotExist:
#             return None  # or handle accordingly if no Calendar exists
        
#     def get_current_month():
#         try:
#             current_month = Month.objects.get(is_current__iexact=True)
#             return current_month
#         except Month.DoesNotExist:
#             return None  # or handle accordingly if no Calendar exists
    
#     def get_current_year():
#         try:
#             current_year = Year.objects.get(is_current__iexact=True)
#             return current_year
#         except Year.DoesNotExist:
#             return None  # or handle accordingly if no Calendar exists
        
#     id = models.AutoField(primary_key=True, unique=True)
#     date_sold = models.DateTimeField(verbose_name="Date Sold", default=timezone.now)
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    
#     grand_total = models.DecimalField(max_digits=25, decimal_places=2, default=0)
#     paid_amount = models.DecimalField(max_digits=25, decimal_places=2, default=0)
#     remains = models.DecimalField(max_digits=25, decimal_places=2, default=0)
#     current_payment = models.DecimalField(max_digits=25, decimal_places=2, default=0)
#     receipt_number = models.PositiveBigIntegerField(
#         unique=True, 
#         verbose_name='Receipt Number',
#         help_text='Unique receipt number for the purchase transaction'
#     )
#     created_by = CurrentUserField(related_name="rb23c")
#     created_at = models.DateField(auto_now=True)
#     modified_by = CurrentUserField(related_name="ub23c")
#     modified_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"Sold items for {self.customer.name}"

#     class Meta:
#         # db_table = 'PROPERTIES_OUTS_SOLDITEM'
#         verbose_name = 'የእቃ ወይም የንብረት ወጪ'
#         verbose_name_plural = 'የእቃ ወይም የንብረት ወጪዎች'
   
# class SoldInline(models.Model):             
#     id = models.AutoField(primary_key=True, unique=True)
#     sold_item = models.ForeignKey(SoldItem, on_delete=models.DO_NOTHING)
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
#     # measurement = models.ForeignKey(Measurement, on_delete=models.CASCADE, verbose_name='Measure')
#     purchased_unit_price  = models.DecimalField(max_digits=25, decimal_places=2, verbose_name='purchased price', default=0)
#     discount = models.DecimalField(max_digits=25, decimal_places=2, default=0)
#     quantity = models.DecimalField(max_digits=25, decimal_places=2, default=1)

#     def __str__(self):
#         return self.item_type.name

#     class Meta:
#         verbose_name = "Sold Material"
#         verbose_name_plural = "Sold Materials"

# class MonthlySold(models.Model):
#     id = models.AutoField(primary_key = True, unique = True)
#     sold_month_name = models.CharField(max_length=150, verbose_name='month')
#     sold_year = models.CharField(max_length = 150, verbose_name='year')
#     customer_name = models.CharField(max_length = 150, verbose_name='name')
#     item_category = models.CharField(max_length = 150, verbose_name='category')
#     item_type = models.CharField(max_length = 150, verbose_name='type')
#     total_sold_items = models.IntegerField(verbose_name='items')
#     sold_total_price = models.DecimalField(max_digits=25, decimal_places=2, blank=True, null=True, verbose_name=' price')
#     profit_by_unit = models.DecimalField(max_digits=25, decimal_places=2, blank=True, null=True, verbose_name='unit profit')
#     total_profit = models.DecimalField(max_digits=25, decimal_places=2, blank=True, null=True)
#     total_asrat = models.DecimalField(max_digits=25, decimal_places=2, blank=True, null=True, verbose_name='asrat')

#     def __str__(self):
#         return "%s" % (self.id)

#     class Meta:
#         managed = False
#         db_table = "sold_monthly_item"
#         verbose_name="Sold items profit"
#         verbose_name_plural="Sold monthly items" 

# class FirstQuarterSold(models.Model):
#     id = models.AutoField(primary_key = True, unique = True)
#     sold_month_name = models.CharField(max_length=150, verbose_name='month')
#     sold_year = models.CharField(max_length = 150, verbose_name='year')
#     customer_name = models.CharField(max_length = 150, verbose_name='name')
#     item_category = models.CharField(max_length = 150, verbose_name='category')
#     item_type = models.CharField(max_length = 150, verbose_name='type')
#     total_sold_items = models.IntegerField(verbose_name='items')
#     sold_total_price = models.DecimalField(max_digits=25, decimal_places=2, blank=True, null=True, verbose_name=' price')
#     profit_by_unit = models.DecimalField(max_digits=25, decimal_places=2, blank=True, null=True, verbose_name='unit profit')
#     total_profit = models.DecimalField(max_digits=25, decimal_places=2, blank=True, null=True)
#     total_asrat = models.DecimalField(max_digits=25, decimal_places=2, blank=True, null=True, verbose_name='asrat')

#     def __str__(self):
#         return "%s" % (self.id)

#     class Meta:
#         managed = False
#         db_table = "sold_first_quarter_item"
#         verbose_name="Sold first quarter item"
#         verbose_name_plural="Sold first quarter items" 

# class SecondQuarterSold(models.Model):
#     id = models.AutoField(primary_key = True, unique = True)
#     sold_month_name = models.CharField(max_length=150, verbose_name='month')
#     sold_year = models.CharField(max_length = 150, verbose_name='year')
#     customer_name = models.CharField(max_length = 150, verbose_name='name')
#     item_category = models.CharField(max_length = 150, verbose_name='category')
#     item_type = models.CharField(max_length = 150, verbose_name='type')
#     total_sold_items = models.IntegerField(verbose_name='items')
#     sold_total_price = models.DecimalField(max_digits=25, decimal_places=2, blank=True, null=True, verbose_name=' price')
#     profit_by_unit = models.DecimalField(max_digits=25, decimal_places=2, blank=True, null=True, verbose_name='unit profit')
#     total_profit = models.DecimalField(max_digits=25, decimal_places=2, blank=True, null=True)
#     total_asrat = models.DecimalField(max_digits=25, decimal_places=2, blank=True, null=True, verbose_name='asrat')

#     def __str__(self):
#         return "%s" % (self.id)

#     class Meta:
#         managed = False
#         db_table = "sold_second_quarter_item"
#         verbose_name="Sold second quarter item"
#         verbose_name_plural="Sold second quarter items"
      
# class ThirdQuarterSold(models.Model):
#     id = models.AutoField(primary_key = True, unique = True)
#     sold_month_name = models.CharField(max_length=150, verbose_name='month')
#     sold_year = models.CharField(max_length = 150, verbose_name='year')
#     customer_name = models.CharField(max_length = 150, verbose_name='name')
#     item_category = models.CharField(max_length = 150, verbose_name='category')
#     item_type = models.CharField(max_length = 150, verbose_name='type')
#     total_sold_items = models.IntegerField(verbose_name='items')
#     sold_total_price = models.DecimalField(max_digits=25, decimal_places=2, blank=True, null=True, verbose_name=' price')
#     profit_by_unit = models.DecimalField(max_digits=25, decimal_places=2, blank=True, null=True, verbose_name='unit profit')
#     total_profit = models.DecimalField(max_digits=25, decimal_places=2, blank=True, null=True)
#     total_asrat = models.DecimalField(max_digits=25, decimal_places=2, blank=True, null=True, verbose_name='asrat')

#     def __str__(self):
#         return "%s" % (self.id)

#     class Meta:
#         managed = False
#         db_table = "sold_third_quarter_item"
#         verbose_name="Sold third quarter item"
#         verbose_name_plural="Sold third quarter items"

# class AnnualSold(models.Model):
#     id = models.AutoField(primary_key = True, unique = True)
#     sold_year = models.CharField(max_length = 150, verbose_name='year')
#     customer_name = models.CharField(max_length = 150, verbose_name='name')
#     item_category = models.CharField(max_length = 150, verbose_name='category')
#     item_type = models.CharField(max_length = 150, verbose_name='type')
#     total_sold_items = models.IntegerField(verbose_name='items')
#     sold_total_price = models.DecimalField(max_digits=25, decimal_places=2, blank=True, null=True, verbose_name=' price')
#     profit_by_unit = models.DecimalField(max_digits=25, decimal_places=2, blank=True, null=True, verbose_name='unit profit')
#     total_profit = models.DecimalField(max_digits=25, decimal_places=2, blank=True, null=True)
#     total_asrat = models.DecimalField(max_digits=25, decimal_places=2, blank=True, null=True, verbose_name='asrat')

#     def __str__(self):
#         return "%s" % (self.id)

#     class Meta:
#         managed = False
#         db_table = "sold_annual_item"
#         verbose_name="Sold annual item"
#         verbose_name_plural="Sold annual items"