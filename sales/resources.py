# resources.py
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import SoldItem
from setups.models import *

class OrderResource(resources.ModelResource):
    # customer = fields.Field(
    #     column_name='customer',
    #     attribute='customer',
    #     widget=ForeignKeyWidget(Customer, 'name'))
    # date = fields.Field(
    #     column_name='date',
    #     attribute='date',
    #     widget=ForeignKeyWidget(Date, 'date'))
    # month = fields.Field(
    #     column_name='month',
    #     attribute='month',
    #     widget=ForeignKeyWidget(Month, 'month'))
    # year = fields.Field(
    #     column_name='year',
    #     attribute='year',
    #     widget=ForeignKeyWidget(Year, 'year'))

    class Meta:
        model = SoldItem
        fields = ('id', 'customer', 'date', 'month', 'year', 'grand_total', 'paid_amount', 'remains', 'current_payment')
        export_order = ('id', 'customer', 'date', 'month', 'year', 'grand_total', 'paid_amount', 'remains', 'current_payment')
