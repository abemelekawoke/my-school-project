# from django.db import models
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from django.shortcuts import redirect
from django.db import connection
from django.contrib import admin
# from django.conf.urls import url
# from django.conf.urls import url
# from django.urls import url
from django.http import HttpResponse
# import csv
from django.utils import timezone
import datetime
from datetime import datetime
from .models import *
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
# from django.contrib.auth.models import Group

class WSPlanAdmin(ImportExportModelAdmin):
	pass
	fields = ['Dates',('Tasks','Measurement'),('First_Quarter_Plan','Second_Quarter_Plan'),('Third_Quarter_Plan','Forth_Quarter_Plan')]
	list_display = ['id','Dates','Tasks','Measurement','First_Quarter_Plan','Second_Quarter_Plan','Third_Quarter_Plan','Forth_Quarter_Plan','Total_budget','Planned_at','Updated_by','Planned_by']
	search_fields = ['id','Dates','Tasks','Measurement','Plan','Total_budget','Planned_at','Updated_by','Planned_by']
	list_filter = ['Dates','First_Quarter_Plan','Second_Quarter_Plan','Third_Quarter_Plan','Forth_Quarter_Plan']
	list_display_links = ['id','Dates','Tasks','Measurement','First_Quarter_Plan','Second_Quarter_Plan','Third_Quarter_Plan','Forth_Quarter_Plan','Total_budget','Planned_at','Updated_by','Planned_by']
	readonly_fields = ('id','Total_budget','Planned_at','Updated_by','Planned_by')
	list_per_page = 10
	list_select_related = True
	class Meta:
		model = WaterSupplyPlan	

	def save_model(self, request, obj, form, change):
		if change:
			obj.Updated_by = request.user
			obj.Planned_at = datetime.now()
		obj.save()

admin.site.register(WaterSupplyPlan, WSPlanAdmin) 

class FIPlanAdmin(ImportExportModelAdmin):
	pass
	fields = [('Tasks','Measurement'),('First_Quarter_Plan','Second_Quarter_Plan'),('Third_Quarter_Plan','Forth_Quarter_Plan'),('Dates')]
	list_display = ['id','Dates','Tasks','Measurement','First_Quarter_Plan','Second_Quarter_Plan','Third_Quarter_Plan','Forth_Quarter_Plan','Total_budget','Planned_at','Updated_by','Planned_by']
	search_fields = ['id','Dates','Tasks','Measurement','Plan','Total_budget','Planned_at','Updated_by','Planned_by']
	list_filter = ['Dates','First_Quarter_Plan','Second_Quarter_Plan','Third_Quarter_Plan','Forth_Quarter_Plan']
	list_display_links = ['id','Dates','Tasks','Measurement','First_Quarter_Plan','Second_Quarter_Plan','Third_Quarter_Plan','Forth_Quarter_Plan','Total_budget','Planned_at','Updated_by','Planned_by']
	readonly_fields = ('id','Total_budget','Planned_at','Updated_by','Planned_by')
	list_per_page = 10
	list_select_related = True
	class Meta:
		model = FinanceIncomePlan	

	def save_model(self, request, obj, form, change):
		if change:
			obj.Updated_by = request.user
			obj.Planned_at = datetime.now()
		obj.save()

admin.site.register(FinanceIncomePlan, FIPlanAdmin) 

class FEPlanAdmin(ImportExportModelAdmin):
	pass
	fields = [('Tasks','Measurement'),('First_Quarter_Plan','Second_Quarter_Plan'),('Third_Quarter_Plan','Forth_Quarter_Plan'),('Dates')]
	list_display = ['id','Dates','Tasks','Measurement','First_Quarter_Plan','Second_Quarter_Plan','Third_Quarter_Plan','Forth_Quarter_Plan','Total_budget','Planned_at','Updated_by','Planned_by']
	search_fields = ['id','Dates','Tasks','Measurement','Plan','Total_budget','Planned_at','Updated_by','Planned_by']
	list_filter = ['Dates','First_Quarter_Plan','Second_Quarter_Plan','Third_Quarter_Plan','Forth_Quarter_Plan']
	list_display_links = ['id','Dates','Tasks','Measurement','First_Quarter_Plan','Second_Quarter_Plan','Third_Quarter_Plan','Forth_Quarter_Plan','Total_budget','Planned_at','Updated_by','Planned_by']
	readonly_fields = ('id','Total_budget','Planned_at','Updated_by','Planned_by')
	list_per_page = 10
	list_select_related = True
	class Meta:
		model = FinanceCostPlan	

	def save_model(self, request, obj, form, change):
		if change:
			obj.Updated_by = request.user
			obj.Planned_at = datetime.now()
		obj.save()

admin.site.register(FinanceCostPlan, FEPlanAdmin) 

class HRPlanAdmin(ImportExportModelAdmin):
	pass
	fields = [('Tasks','Measurement'),('First_Quarter_Plan','Second_Quarter_Plan'),('Third_Quarter_Plan','Forth_Quarter_Plan'),('Dates')]
	list_display = ['id','Dates','Tasks','Measurement','First_Quarter_Plan','Second_Quarter_Plan','Third_Quarter_Plan','Forth_Quarter_Plan','Total_budget','Planned_at','Updated_by','Planned_by']
	search_fields = ['id','Dates','Tasks','Measurement','Plan','Total_budget','Planned_at','Updated_by','Planned_by']
	list_filter = ['Dates','First_Quarter_Plan','Second_Quarter_Plan','Third_Quarter_Plan','Forth_Quarter_Plan']
	list_display_links = ['id','Dates','Tasks','Measurement','First_Quarter_Plan','Second_Quarter_Plan','Third_Quarter_Plan','Forth_Quarter_Plan','Total_budget','Planned_at','Updated_by','Planned_by']
	readonly_fields = ('id','Total_budget','Planned_at','Updated_by','Planned_by')
	list_per_page = 10
	list_select_related = True
	class Meta:
		model = HumanResourcePlan	

	def save_model(self, request, obj, form, change):
		if change:
			obj.Updated_by = request.user
			obj.Planned_at = datetime.now()
		obj.save()

admin.site.register(HumanResourcePlan, HRPlanAdmin) 

class PACIPAdmin(ImportExportModelAdmin):
	pass
	fields = [('Tasks','Measurement'),('First_Quarter_Plan','Second_Quarter_Plan'),('Third_Quarter_Plan','Forth_Quarter_Plan'),('Dates')]
	list_display = ['id','Dates','Tasks','Measurement','First_Quarter_Plan','Second_Quarter_Plan','Third_Quarter_Plan','Forth_Quarter_Plan','Total_budget','Planned_at','Updated_by','Planned_by']
	search_fields = ['id','Dates','Tasks','Measurement','Plan','Total_budget','Planned_at','Updated_by','Planned_by']
	list_filter = ['Dates','First_Quarter_Plan','Second_Quarter_Plan','Third_Quarter_Plan','Forth_Quarter_Plan']
	list_display_links = ['id','Dates','Tasks','Measurement','First_Quarter_Plan','Second_Quarter_Plan','Third_Quarter_Plan','Forth_Quarter_Plan','Total_budget','Planned_at','Updated_by','Planned_by']
	readonly_fields = ('id','Total_budget','Planned_at','Updated_by','Planned_by')
	list_per_page = 10
	list_select_related = True
	class Meta:
		model = PlanningAndCustomerIssuePlan	

	def save_model(self, request, obj, form, change):
		if change:
			obj.Updated_by = request.user
			obj.Planned_at = datetime.now()
		obj.save()

admin.site.register(PlanningAndCustomerIssuePlan, PACIPAdmin) 


class MRAdmin1(ImportExportModelAdmin):
	pass
	fieldsets = [
        ('General informations', {
            'fields': [('Full_name','Address'),('Kebele','House_number'),('Phone_number','Place'),('Simple_maintenance','Water_meter_transfer','Water_meter_change'),('Examine_or_clean_up','Water_meter_openning','Get_valve_change'),('For_waste','Service_type','For_Digging')],
        }),
		('Materials information', {
			'fields': [('Pipe_Quantity','Pipe_Single_price','Pipe_inch'),('HDP_tube_Quantity','HDP_Single_price','HDP_tube_inch'),('Elbow_Quantity','Elbow_Single_price','Elbow_inch'),('Naples_Quantity','Naples_Single_price','Naples_inch'),('Reducer_Quantity','Reducer_Single_price','Reducer_inch'),('Adapter_Quantity','Adapter_Single_price','Adapter_inch'),('Union_metal_Quantity','Union_metal_Single_price','Union_metal_inch'),('Union_HDP_Quantity','Union_HDP_Single_price','Union_HDP_inch'),('Get_valve_Quantity','Get_valve_Single_price','Get_valve_inch'),('Foss_set_Quantity','Foss_set_Single_price','Foss_set_inch'),('T_metal_Quantity','T_metal_Single_price','T_metal_inch'),('T_HDP_Quantity','T_HDP_Single_price','T_HDP_inch'),('Tape_Quantity','Tape_Single_price','Tape_inch'),('Water_meter_Quantity','Water_meter_Single_price','Water_meter_inch'),('Socket_Quantity','Socket_Single_price','Socket_inch'),'Grand_total'],
		}),
        ('Approval Requests', {
            'fields': ['Water_supply','Income_office','Amount','Cashier'],
        }),
    ]
	list_display = ['id','Full_name','Grand_total','Address','Kebele','House_number','Phone_number','Place','Service_type','Simple_maintenance','For_waste','Water_supply','Income_office','Amount','Cashier','Requested_at','Updated_by','Registered_by']
	search_fields = ['id','Full_name','Address','Kebele','House_number','Phone_number','Place','Service_type','Simple_maintenance','For_waste','Water_supply','Income_office','Amount','Cashier','Requested_at','Updated_by','Registered_by']
	list_filter = ['Kebele','Place']
	list_display_links = ['id','Full_name','Grand_total','Address','Kebele','House_number','Phone_number','Place','Service_type','Simple_maintenance','For_waste','Water_supply','Income_office','Amount','Cashier','Requested_at','Updated_by','Registered_by']
	readonly_fields = ('id','Grand_total','Requested_at','Updated_by','Registered_by')
	list_per_page = 10
	list_select_related = True
	class Meta:
		model = MaintenanceRequest

	def save_model(self, request, obj, form, change):
		if change:
			obj.Updated_by = request.user
			obj.Registered_at = datetime.now()
		obj.save()

admin.site.register(MaintenanceRequest, MRAdmin1)  

class MRAdmin2(admin.ModelAdmin):
	fieldsets = [
        ('General informations', {
            'fields': [('Full_name','Address'),('Kebele','House_number'),('Phone_number','Place'),('Simple_maintenance','Water_meter_transfer'),('Water_meter_change','Examine_or_clean_up'),('Water_meter_openning','Get_valve_change'),('For_waste','Service_type')],
        }),
		('Materials information', {
			'fields': [('Pipe_Quantity','Pipe_Single_price','Pipe_inch'),('HDP_tube_Quantity','HDP_Single_price','HDP_tube_inch'),('Elbow_Quantity','Elbow_Single_price','Elbow_inch'),('Naples_Quantity','Naples_Single_price','Naples_inch'),('Reducer_Quantity','Reducer_Single_price','Reducer_inch'),('Adapter_Quantity','Adapter_Single_price','Adapter_inch'),('Union_metal_Quantity','Union_metal_Single_price','Union_metal_inch'),('Union_HDP_Quantity','Union_HDP_Single_price','Union_HDP_inch'),('Get_valve_Quantity','Get_valve_Single_price','Get_valve_inch'),('Foss_set_Quantity','Foss_set_Single_price','Foss_set_inch'),('T_metal_Quantity','T_metal_Single_price','T_metal_inch'),('T_HDP_Quantity','T_HDP_Single_price','T_HDP_inch'),('Tape_Quantity','Tape_Single_price','Tape_inch'),('Water_meter_Quantity','Water_meter_Single_price','Water_meter_inch'),('Socket_Quantity','Socket_Single_price','Socket_inch'),'Grand_total'],
		}),
        ('Approval Requests', {
            'fields': ['Water_supply','Income_office','Amount','Cashier'],
        }),
    ]
	list_display = ['id','Full_name','Grand_total','Address','Kebele','House_number','Phone_number','Place','Service_type','Simple_maintenance','For_waste','Water_supply','Income_office','Amount','Cashier','Requested_at','Updated_by','Registered_by']
	search_fields = ['id','Full_name','Grand_total','Address','Kebele','House_number','Phone_number','Place','Service_type','Simple_maintenance','For_waste','Water_supply','Income_office','Amount','Cashier','Requested_at','Updated_by','Registered_by']
	list_filter = ['Kebele','Place']
	list_display_links = ['id','Full_name','Grand_total','Address','Kebele','House_number','Phone_number','Place','Service_type','Simple_maintenance','For_waste','Water_supply','Income_office','Amount','Cashier','Requested_at','Updated_by','Registered_by']
	readonly_fields = ('id','Full_name','Grand_total','Address','Kebele','House_number','Phone_number','Place','Service_type','Simple_maintenance','For_waste','Income_office','Amount','Cashier','Requested_at','Updated_by','Registered_by')
	list_per_page = 10
	list_select_related = True
	class Meta:
		model = MaintenanceRequestPotableWater	
	def save_model(self, request, obj, form, change):
		if change:
			obj.Updated_by = request.user
			obj.Registered_at = datetime.now()
		obj.save()

admin.site.register(MaintenanceRequestPotableWater, MRAdmin2)

class MRAdmin3(admin.ModelAdmin):
	fieldsets = [
        ('General informations', {
            'fields': [('Full_name','Address'),('Kebele','House_number'),('Phone_number','Place'),('Simple_maintenance','Water_meter_transfer'),('Water_meter_change','Examine_or_clean_up'),('Water_meter_openning','Get_valve_change'),('For_waste','Service_type')],
        }),
		('Materials information', {
			'fields': [('Pipe_Quantity','Pipe_Single_price','Pipe_inch'),('HDP_tube_Quantity','HDP_Single_price','HDP_tube_inch'),('Elbow_Quantity','Elbow_Single_price','Elbow_inch'),('Naples_Quantity','Naples_Single_price','Naples_inch'),('Reducer_Quantity','Reducer_Single_price','Reducer_inch'),('Adapter_Quantity','Adapter_Single_price','Adapter_inch'),('Union_metal_Quantity','Union_metal_Single_price','Union_metal_inch'),('Union_HDP_Quantity','Union_HDP_Single_price','Union_HDP_inch'),('Get_valve_Quantity','Get_valve_Single_price','Get_valve_inch'),('Foss_set_Quantity','Foss_set_Single_price','Foss_set_inch'),('T_metal_Quantity','T_metal_Single_price','T_metal_inch'),('T_HDP_Quantity','T_HDP_Single_price','T_HDP_inch'),('Tape_Quantity','Tape_Single_price','Tape_inch'),('Water_meter_Quantity','Water_meter_Single_price','Water_meter_inch'),('Socket_Quantity','Socket_Single_price','Socket_inch'),'Grand_total'],
		}),
        ('Approval Requests', {
            'fields': ['Water_supply','Income_office','Amount','Cashier'],
        }),
    ]
	list_display = ['id','Full_name','Grand_total','Address','Kebele','House_number','Phone_number','Place','Service_type','Simple_maintenance','For_waste','Water_supply','Income_office','Amount','Cashier','Requested_at','Updated_by','Registered_by']
	search_fields = ['id','Full_name','Grand_total','Address','Kebele','House_number','Phone_number','Place','Service_type','Simple_maintenance','For_waste','Water_supply','Income_office','Amount','Cashier','Requested_at','Updated_by','Registered_by']
	list_filter = ['Kebele','Place']
	list_display_links = ['id','Full_name','Grand_total','Address','Kebele','House_number','Phone_number','Place','Service_type','Simple_maintenance','For_waste','Water_supply','Income_office','Amount','Cashier','Requested_at','Updated_by','Registered_by']
	readonly_fields = ('id','Full_name','Grand_total','Address','Kebele','House_number','Phone_number','Place','Service_type','Simple_maintenance','For_waste','Water_supply','Amount','Cashier','Requested_at','Updated_by','Registered_by')
	list_per_page = 10
	list_select_related = True
	class Meta:
		model = MaintenanceRequestIncomeOfficer	
	def save_model(self, request, obj, form, change):
		if change:
			obj.Updated_by = request.user
			obj.Registered_at = datetime.now()
		obj.save()

admin.site.register(MaintenanceRequestIncomeOfficer, MRAdmin3)

class MRAdmin4(admin.ModelAdmin):
	fieldsets = [
        ('General informations', {
            'fields': [('Full_name','Address'),('Kebele','House_number'),('Phone_number','Place'),('Simple_maintenance','Water_meter_transfer'),('Water_meter_change','Examine_or_clean_up'),('Water_meter_openning','Get_valve_change'),('For_waste','Service_type')],
        }),
		('Materials information', {
			'fields': [('Pipe_Quantity','Pipe_Single_price','Pipe_inch'),('HDP_tube_Quantity','HDP_Single_price','HDP_tube_inch'),('Elbow_Quantity','Elbow_Single_price','Elbow_inch'),('Naples_Quantity','Naples_Single_price','Naples_inch'),('Reducer_Quantity','Reducer_Single_price','Reducer_inch'),('Adapter_Quantity','Adapter_Single_price','Adapter_inch'),('Union_metal_Quantity','Union_metal_Single_price','Union_metal_inch'),('Union_HDP_Quantity','Union_HDP_Single_price','Union_HDP_inch'),('Get_valve_Quantity','Get_valve_Single_price','Get_valve_inch'),('Foss_set_Quantity','Foss_set_Single_price','Foss_set_inch'),('T_metal_Quantity','T_metal_Single_price','T_metal_inch'),('T_HDP_Quantity','T_HDP_Single_price','T_HDP_inch'),('Tape_Quantity','Tape_Single_price','Tape_inch'),('Water_meter_Quantity','Water_meter_Single_price','Water_meter_inch'),('Socket_Quantity','Socket_Single_price','Socket_inch'),'Grand_total'],
		}),
        ('Approval Requests', {
            'fields': ['Water_supply','Income_office','Amount','Cashier'],
        }),
    ]
	list_display = ['id','Full_name','Grand_total','Address','Kebele','House_number','Phone_number','Place','Service_type','Simple_maintenance','For_waste','Water_supply','Income_office','Amount','Cashier','Requested_at','Updated_by','Registered_by']
	search_fields = ['id','Full_name','Grand_total','Address','Kebele','House_number','Phone_number','Place','Service_type','Simple_maintenance','For_waste','Water_supply','Income_office','Amount','Cashier','Requested_at','Updated_by','Registered_by']
	list_filter = ['Kebele','Place']
	list_display_links = ['id','Full_name','Grand_total','Address','Kebele','House_number','Phone_number','Place','Service_type','Simple_maintenance','For_waste','Water_supply','Income_office','Amount','Cashier','Requested_at','Updated_by','Registered_by']
	readonly_fields = ('id','Full_name','Grand_total','Address','Kebele','House_number','Phone_number','Place','Service_type','Simple_maintenance','For_waste','Water_supply','Income_office','Requested_at','Updated_by','Registered_by')
	list_per_page = 10
	list_select_related = True
	class Meta:
		model = MaintenanceRequestCashier	
	def save_model(self, request, obj, form, change):
		if change:
			obj.Updated_by = request.user
			obj.Registered_at = datetime.now()
		obj.save()

admin.site.register(MaintenanceRequestCashier, MRAdmin4)

class NCRAdmin1(ImportExportModelAdmin):
	pass
	fieldsets = [
        ('General informations', {
            'fields': [('Full_name','Address'),('Kebele','House_number'),('Phone_number','Place'),('Service_type')],
        }),
        ('Approval Requests', {
            'fields': ['Income_office','Amount','Cashier','Bill_processor'],
        }),
    ]
	list_display = ['id','Full_name','Address','Kebele','House_number','Phone_number','Place','Service_type','Income_office','Amount','Cashier','Bill_processor','Requested_at','Updated_by','Registered_by']
	search_fields = ['id','Full_name','Address','Kebele','House_number','Phone_number','Place','Service_type','Income_office','Amount','Cashier','Bill_processor','Requested_at','Updated_by','Registered_by']
	list_filter = ['Kebele','Place']
	list_display_links = ['id','Full_name','Address','Kebele','House_number','Phone_number','Place','Service_type','Income_office','Amount','Cashier','Bill_processor','Requested_at','Updated_by','Registered_by']
	readonly_fields = ('id','Requested_at','Updated_by','Registered_by')
	list_per_page = 10
	list_select_related = True
	class Meta:
		model = NameChangeRequest

	def save_model(self, request, obj, form, change):
		if change:
			obj.Updated_by = request.user
			obj.Registered_at = datetime.now()
		obj.save()

admin.site.register(NameChangeRequest, NCRAdmin1)  

class NCRAdmin2(ImportExportModelAdmin):
	pass
	fieldsets = [
        ('General informations', {
            'fields': [('Full_name','Address'),('Kebele','House_number'),('Phone_number','Place'),('Service_type')],
        }),
        ('Approval Requests', {
            'fields': ['Income_office','Amount','Cashier','Bill_processor'],
        }),
    ]
	list_display = ['id','Full_name','Address','Kebele','House_number','Phone_number','Place','Service_type','Income_office','Amount','Cashier','Bill_processor','Requested_at','Updated_by','Registered_by']
	search_fields = ['id','Full_name','Address','Kebele','House_number','Phone_number','Place','Service_type','Income_office','Amount','Cashier','Bill_processor','Requested_at','Updated_by','Registered_by']
	list_filter = ['Kebele','Place']
	list_display_links = ['id','Full_name','Address','Kebele','House_number','Phone_number','Place','Service_type','Income_office','Amount','Cashier','Bill_processor','Requested_at','Updated_by','Registered_by']
	readonly_fields = ('id','Full_name','Address','Kebele','House_number','Phone_number','Place','Service_type','Amount','Cashier','Bill_processor','Requested_at','Updated_by','Registered_by')
	list_per_page = 10
	list_select_related = True
	class Meta:
		model = NameChangeRequestIncomeOfficer

	def save_model(self, request, obj, form, change):
		if change:
			obj.Updated_by = request.user
			obj.Registered_at = datetime.now()
		obj.save()

admin.site.register(NameChangeRequestIncomeOfficer, NCRAdmin2) 

class NCRAdmin3(ImportExportModelAdmin):
	pass
	fieldsets = [
        ('General informations', {
            'fields': [('Full_name','Address'),('Kebele','House_number'),('Phone_number','Place'),('Service_type')],
        }),
        ('Approval Requests', {
            'fields': ['Income_office','Amount','Cashier','Bill_processor'],
        }),
    ]
	list_display = ['id','Full_name','Address','Kebele','House_number','Phone_number','Place','Service_type','Income_office','Amount','Cashier','Bill_processor','Requested_at','Updated_by','Registered_by']
	search_fields = ['id','Full_name','Address','Kebele','House_number','Phone_number','Place','Service_type','Income_office','Amount','Cashier','Bill_processor','Requested_at','Updated_by','Registered_by']
	list_filter = ['Kebele','Place']
	list_display_links = ['id','Full_name','Address','Kebele','House_number','Phone_number','Place','Service_type','Income_office','Amount','Cashier','Bill_processor','Requested_at','Updated_by','Registered_by']
	readonly_fields = ('id','Full_name','Address','Kebele','House_number','Phone_number','Place','Service_type','Income_office','Bill_processor','Requested_at','Updated_by','Registered_by')
	list_per_page = 10
	list_select_related = True
	class Meta:
		model = NameChangeRequestCashier

	def save_model(self, request, obj, form, change):
		if change:
			obj.Updated_by = request.user
			obj.Registered_at = datetime.now()
		obj.save()

admin.site.register(NameChangeRequestCashier, NCRAdmin3)

class NCRAdmin4(ImportExportModelAdmin):
	pass
	fieldsets = [
        ('General informations', {
            'fields': [('Full_name','Address'),('Kebele','House_number'),('Phone_number','Place'),('Service_type')],
        }),
        ('Approval Requests', {
            'fields': ['Income_office','Amount','Cashier','Bill_processor'],
        }),
    ]
	list_display = ['id','Full_name','Address','Kebele','House_number','Phone_number','Place','Service_type','Income_office','Amount','Cashier','Bill_processor','Requested_at','Updated_by','Registered_by']
	search_fields = ['id','Full_name','Address','Kebele','House_number','Phone_number','Place','Service_type','Income_office','Amount','Cashier','Bill_processor','Requested_at','Updated_by','Registered_by']
	list_filter = ['Kebele','Place']
	list_display_links = ['id','Full_name','Address','Kebele','House_number','Phone_number','Place','Service_type','Income_office','Amount','Cashier','Bill_processor','Requested_at','Updated_by','Registered_by']
	readonly_fields = ('id','Address','Kebele','House_number','Phone_number','Place','Service_type','Income_office','Amount','Cashier','Requested_at','Updated_by','Registered_by')
	list_per_page = 10
	list_select_related = True
	class Meta:
		model = NameChangeRequestBillProcessor

	def save_model(self, request, obj, form, change):
		if change:
			obj.Updated_by = request.user
			obj.Registered_at = datetime.now()
		obj.save()

admin.site.register(NameChangeRequestBillProcessor, NCRAdmin4)

class PWRAdmin1(ImportExportModelAdmin):
	pass
	fieldsets = [
        ('General informations', {
            'fields': [('Full_name','Address'),('Kebele','House_number'),('Phone_number','Place'),('Service_type','Line_joined')],
        }),
        ('Approval Requests', {
            'fields': ['Water_supply','Income_office','Amount','Cashier'],
        }),
    ]
	list_display = ['id','Full_name','Address','Kebele','House_number','Phone_number','Place','Service_type','Line_joined','Water_supply','Income_office','Amount','Cashier','Requested_at','Updated_by','Registered_by']
	search_fields = ['id','Full_name','Address','Kebele','House_number','Phone_number','Place','Service_type','Line_joined','Water_supply','Income_office','Amount','Cashier','Requested_at','Updated_by','Registered_by']
	list_filter = ['Kebele','Place']
	list_display_links = ['id','Full_name','Address','Kebele','House_number','Phone_number','Place','Service_type','Line_joined','Water_supply','Income_office','Amount','Cashier','Requested_at','Updated_by','Registered_by']
	readonly_fields = ('id','Requested_at','Updated_by','Registered_by')
	list_per_page = 10
	list_select_related = True
	class Meta:
		model = PotableWaterRequest	

	def save_model(self, request, obj, form, change):
		if change:
			obj.Updated_by = request.user
			obj.Registered_at = datetime.now()
		obj.save()

admin.site.register(PotableWaterRequest, PWRAdmin1)  

class PWRAdmin2(admin.ModelAdmin):
	fieldsets = [
        ('General informations', {
            'fields': [('Full_name','Address'),('Kebele','House_number'),('Phone_number','Place'),('Service_type','Line_joined')],
        }),
        ('Approval Requests', {
            'fields': ['Water_supply','Income_office','Amount','Cashier'],
        }),
    ]
	list_display = ['id','Full_name','Address','Kebele','House_number','Phone_number','Place','Service_type','Line_joined','Water_supply','Income_office','Amount','Cashier','Requested_at','Updated_by','Registered_by']
	search_fields = ['id','Full_name','Address','Kebele','House_number','Phone_number','Place','Service_type','Line_joined','Water_supply','Income_office','Amount','Cashier','Requested_at','Updated_by','Registered_by']
	list_filter = ['Kebele','Place']
	list_display_links = ['id','Full_name','Address','Kebele','House_number','Phone_number','Place','Service_type','Line_joined','Water_supply','Income_office','Amount','Cashier','Requested_at','Updated_by','Registered_by']
	readonly_fields = ('id','Full_name','Address','Kebele','House_number','Phone_number','Place','Service_type','Line_joined','Income_office','Amount','Cashier','Requested_at','Updated_by','Registered_by')
	list_per_page = 10
	list_select_related = True
	class Meta:
		model = PotableWaterRequestPotableWater	

	def save_model(self, request, obj, form, change):
		if change:
			obj.Updated_by = request.user
			obj.Registered_at = datetime.now()
		obj.save()

admin.site.register(PotableWaterRequestPotableWater, PWRAdmin2) 

class PWRAdmin3(admin.ModelAdmin):
	fieldsets = [
        ('General informations', {
            'fields': [('Full_name','Address'),('Kebele','House_number'),('Phone_number','Place'),('Service_type','Line_joined')],
        }),
        ('Approval Requests', {
            'fields': ['Water_supply','Income_office','Amount','Cashier'],
        }),
    ]
	list_display = ['id','Full_name','Address','Kebele','House_number','Phone_number','Place','Service_type','Line_joined','Water_supply','Income_office','Amount','Cashier','Requested_at','Updated_by','Registered_by']
	search_fields = ['id','Full_name','Address','Kebele','House_number','Phone_number','Place','Service_type','Line_joined','Water_supply','Income_office','Amount','Cashier','Requested_at','Updated_by','Registered_by']
	list_filter = ['Kebele','Place']
	list_display_links = ['id','Full_name','Address','Kebele','House_number','Phone_number','Place','Service_type','Line_joined','Water_supply','Income_office','Amount','Cashier','Requested_at','Updated_by','Registered_by']
	readonly_fields = ('id','Full_name','Address','Kebele','House_number','Phone_number','Place','Service_type','Line_joined','Water_supply','Amount','Cashier','Requested_at','Updated_by','Registered_by')
	list_per_page = 10
	list_select_related = True
	class Meta:
		model = PotableWaterRequestIncomeOfficer	

	def save_model(self, request, obj, form, change):
		if change:
			obj.Updated_by = request.user
			obj.Registered_at = datetime.now()
		obj.save()

admin.site.register(PotableWaterRequestIncomeOfficer, PWRAdmin3) 

class PWRAdmin4(admin.ModelAdmin):
	fieldsets = [
        ('General informations', {
            'fields': [('Full_name','Address'),('Kebele','House_number'),('Phone_number','Place'),('Service_type','Line_joined')],
        }),
        ('Approval Requests', {
            'fields': ['Water_supply','Income_office','Amount','Cashier'],
        }),
    ]
	list_display = ['id','Full_name','Address','Kebele','House_number','Phone_number','Place','Service_type','Line_joined','Water_supply','Income_office','Amount','Cashier','Requested_at','Updated_by','Registered_by']
	search_fields = ['id','Full_name','Address','Kebele','House_number','Phone_number','Place','Service_type','Line_joined','Water_supply','Income_office','Amount','Cashier','Requested_at','Updated_by','Registered_by']
	list_filter = ['Kebele','Place']
	list_display_links = ['id','Full_name','Address','Kebele','House_number','Phone_number','Place','Service_type','Line_joined','Water_supply','Income_office','Amount','Cashier','Requested_at','Updated_by','Registered_by']
	readonly_fields = ('id','Full_name','Address','Kebele','House_number','Phone_number','Place','Service_type','Line_joined','Water_supply','Income_office','Amount','Requested_at','Updated_by','Registered_by')
	list_per_page = 10
	list_select_related = True
	class Meta:
		model = PotableWaterRequestCashier	

	def save_model(self, request, obj, form, change):
		if change:
			obj.Updated_by = request.user
			obj.Registered_at = datetime.now()
		obj.save()

admin.site.register(PotableWaterRequestCashier, PWRAdmin4) 

class WaterSupplyPerformedAdmin(ImportExportModelAdmin):
	pass
	fieldsets = [
        ('General information', {
            'fields': ['Dates','Planned_tasks',('First_Quarter_performed','Second_Quarter_performed'),('Forth_Quarter_performed','Third_Quarter_performed')],
        }),
			('Detail information', {
            'fields': [('First_Quarter_performance','Second_Quarter_performance'),('Third_Quarter_performance','Forth_Quarter_performance'),'Total_year_performance'],
        }),
    ]
	list_display = ['id','Planned_tasks','First_Quarter_performed','Second_Quarter_performed','Third_Quarter_performed','Forth_Quarter_performed','First_Quarter_performance','Second_Quarter_performance','Third_Quarter_performance','Forth_Quarter_performance','Total_year_performance','Registered_at','Updated_by','Registered_by']
	search_fields = ['id','Planned_tasks','First_Quarter_performed','Second_Quarter_performed','Third_Quarter_performed','Forth_Quarter_performed','First_Quarter_performance','Second_Quarter_performance','Third_Quarter_performance','Forth_Quarter_performance','Total_year_performance','Registered_at','Updated_by','Registered_by']
	list_filter = ['Total_year_performance','First_Quarter_performed','Second_Quarter_performed','Third_Quarter_performed','Forth_Quarter_performed','First_Quarter_performance','Second_Quarter_performance','Third_Quarter_performance','Forth_Quarter_performance']
	list_display_links = ['id','Planned_tasks','First_Quarter_performed','Second_Quarter_performed','Third_Quarter_performed','Forth_Quarter_performed','First_Quarter_performance','Second_Quarter_performance','Third_Quarter_performance','Forth_Quarter_performance','Total_year_performance','Registered_at','Updated_by','Registered_by']
	readonly_fields = ('id','First_Quarter_performance','Second_Quarter_performance','Third_Quarter_performance','Forth_Quarter_performance','Total_year_performance','Registered_at','Updated_by','Registered_by')
	list_per_page = 10
	list_select_related = True
	class Meta:
		model = WaterSupplyPerformed	

	def save_model(self, request, obj, form, change):
		if change:
			obj.Update_by = request.user
			obj.Registered_at = datetime.now()
		obj.save()

admin.site.register(WaterSupplyPerformed, WaterSupplyPerformedAdmin)

class PlanningAndCustomerIssuePerformedAdmin(ImportExportModelAdmin):
	pass
	fieldsets = [
        ('General information', {
            'fields': ['Dates','Planned_tasks',('First_Quarter_performed','Second_Quarter_performed'),('Forth_Quarter_performed','Third_Quarter_performed')],
        }),
			('Detail information', {
            'fields': [('First_Quarter_performance','Second_Quarter_performance'),('Third_Quarter_performance','Forth_Quarter_performance'),'Total_year_performance'],
        }),
    ]
	list_display = ['id','Planned_tasks','First_Quarter_performed','Second_Quarter_performed','Third_Quarter_performed','Forth_Quarter_performed','First_Quarter_performance','Second_Quarter_performance','Third_Quarter_performance','Forth_Quarter_performance','Total_year_performance','Registered_at','Updated_by','Registered_by']
	search_fields = ['id','Planned_tasks','First_Quarter_performed','Second_Quarter_performed','Third_Quarter_performed','Forth_Quarter_performed','First_Quarter_performance','Second_Quarter_performance','Third_Quarter_performance','Forth_Quarter_performance','Total_year_performance','Registered_at','Updated_by','Registered_by']
	list_filter = ['Total_year_performance','First_Quarter_performed','Second_Quarter_performed','Third_Quarter_performed','Forth_Quarter_performed','First_Quarter_performance','Second_Quarter_performance','Third_Quarter_performance','Forth_Quarter_performance']
	list_display_links = ['id','Planned_tasks','First_Quarter_performed','Second_Quarter_performed','Third_Quarter_performed','Forth_Quarter_performed','First_Quarter_performance','Second_Quarter_performance','Third_Quarter_performance','Forth_Quarter_performance','Total_year_performance','Registered_at','Updated_by','Registered_by']
	readonly_fields = ('id','First_Quarter_performance','Second_Quarter_performance','Third_Quarter_performance','Forth_Quarter_performance','Total_year_performance','Registered_at','Updated_by','Registered_by')
	list_per_page = 10
	list_select_related = True
	class Meta:
		model = PlanningAndCustomerIssuePerformed	

	def save_model(self, request, obj, form, change):
		if change:
			obj.Update_by = request.user
			obj.Registered_at = datetime.now()
		obj.save()

admin.site.register(PlanningAndCustomerIssuePerformed, PlanningAndCustomerIssuePerformedAdmin)

class FinanceIncomePerformedAdmin(ImportExportModelAdmin):
	pass
	fieldsets = [
        ('General information', {
            'fields': ['Dates','Planned_tasks',('First_Quarter_performed','Second_Quarter_performed'),('Forth_Quarter_performed','Third_Quarter_performed')],
        }),
			('Detail information', {
            'fields': [('First_Quarter_performance','Second_Quarter_performance'),('Third_Quarter_performance','Forth_Quarter_performance'),'Total_year_performance'],
        }),
    ]
	list_display = ['id','Planned_tasks','First_Quarter_performed','Second_Quarter_performed','Third_Quarter_performed','Forth_Quarter_performed','First_Quarter_performance','Second_Quarter_performance','Third_Quarter_performance','Forth_Quarter_performance','Total_year_performance','Registered_at','Updated_by','Registered_by']
	search_fields = ['id','Planned_tasks','First_Quarter_performed','Second_Quarter_performed','Third_Quarter_performed','Forth_Quarter_performed','First_Quarter_performance','Second_Quarter_performance','Third_Quarter_performance','Forth_Quarter_performance','Total_year_performance','Registered_at','Updated_by','Registered_by']
	list_filter = ['Total_year_performance','First_Quarter_performed','Second_Quarter_performed','Third_Quarter_performed','Forth_Quarter_performed','First_Quarter_performance','Second_Quarter_performance','Third_Quarter_performance','Forth_Quarter_performance']
	list_display_links = ['id','Planned_tasks','First_Quarter_performed','Second_Quarter_performed','Third_Quarter_performed','Forth_Quarter_performed','First_Quarter_performance','Second_Quarter_performance','Third_Quarter_performance','Forth_Quarter_performance','Total_year_performance','Registered_at','Updated_by','Registered_by']
	readonly_fields = ('id','First_Quarter_performance','Second_Quarter_performance','Third_Quarter_performance','Forth_Quarter_performance','Total_year_performance','Registered_at','Updated_by','Registered_by')
	list_per_page = 10
	list_select_related = True
	class Meta:
		model = FinanceIncomePerformed	

	def save_model(self, request, obj, form, change):
		if change:
			obj.Update_by = request.user
			obj.Registered_at = datetime.now()
		obj.save()

admin.site.register(FinanceIncomePerformed, FinanceIncomePerformedAdmin)

class FinanceCostPerformedAdmin(ImportExportModelAdmin):
	pass
	fieldsets = [
        ('General information', {
            'fields': ['Dates','Planned_tasks',('First_Quarter_performed','Second_Quarter_performed'),('Forth_Quarter_performed','Third_Quarter_performed')],
        }),
			('Detail information', {
            'fields': [('First_Quarter_performance','Second_Quarter_performance'),('Third_Quarter_performance','Forth_Quarter_performance'),'Total_year_performance'],
        }),
    ]
	list_display = ['id','Planned_tasks','First_Quarter_performed','Second_Quarter_performed','Third_Quarter_performed','Forth_Quarter_performed','First_Quarter_performance','Second_Quarter_performance','Third_Quarter_performance','Forth_Quarter_performance','Total_year_performance','Registered_at','Updated_by','Registered_by']
	search_fields = ['id','Planned_tasks','First_Quarter_performed','Second_Quarter_performed','Third_Quarter_performed','Forth_Quarter_performed','First_Quarter_performance','Second_Quarter_performance','Third_Quarter_performance','Forth_Quarter_performance','Total_year_performance','Registered_at','Updated_by','Registered_by']
	list_filter = ['Total_year_performance','First_Quarter_performed','Second_Quarter_performed','Third_Quarter_performed','Forth_Quarter_performed','First_Quarter_performance','Second_Quarter_performance','Third_Quarter_performance','Forth_Quarter_performance']
	list_display_links = ['id','Planned_tasks','First_Quarter_performed','Second_Quarter_performed','Third_Quarter_performed','Forth_Quarter_performed','First_Quarter_performance','Second_Quarter_performance','Third_Quarter_performance','Forth_Quarter_performance','Total_year_performance','Registered_at','Updated_by','Registered_by']
	readonly_fields = ('id','First_Quarter_performance','Second_Quarter_performance','Third_Quarter_performance','Forth_Quarter_performance','Total_year_performance','Registered_at','Updated_by','Registered_by')
	list_per_page = 10
	list_select_related = True
	class Meta:
		model = FinanceCostPerformed	

	def save_model(self, request, obj, form, change):
		if change:
			obj.Update_by = request.user
			obj.Registered_at = datetime.now()
		obj.save()

admin.site.register(FinanceCostPerformed, FinanceCostPerformedAdmin) 

class HumanResourcePerformedAdmin(ImportExportModelAdmin):
	pass
	fieldsets = [
        ('General information', {
            'fields': ['Dates','Planned_tasks',('First_Quarter_performed','Second_Quarter_performed'),('Forth_Quarter_performed','Third_Quarter_performed')],
        }),
			('Detail information', {
            'fields': [('First_Quarter_performance','Second_Quarter_performance'),('Third_Quarter_performance','Forth_Quarter_performance'),'Total_year_performance'],
        }),
    ]
	list_display = ['id','Planned_tasks','First_Quarter_performed','Second_Quarter_performed','Third_Quarter_performed','Forth_Quarter_performed','First_Quarter_performance','Second_Quarter_performance','Third_Quarter_performance','Forth_Quarter_performance','Total_year_performance','Registered_at','Updated_by','Registered_by']
	search_fields = ['id','Planned_tasks','First_Quarter_performed','Second_Quarter_performed','Third_Quarter_performed','Forth_Quarter_performed','First_Quarter_performance','Second_Quarter_performance','Third_Quarter_performance','Forth_Quarter_performance','Total_year_performance','Registered_at','Updated_by','Registered_by']
	list_filter = ['Total_year_performance','First_Quarter_performed','Second_Quarter_performed','Third_Quarter_performed','Forth_Quarter_performed','First_Quarter_performance','Second_Quarter_performance','Third_Quarter_performance','Forth_Quarter_performance']
	list_display_links = ['id','Planned_tasks','First_Quarter_performed','Second_Quarter_performed','Third_Quarter_performed','Forth_Quarter_performed','First_Quarter_performance','Second_Quarter_performance','Third_Quarter_performance','Forth_Quarter_performance','Total_year_performance','Registered_at','Updated_by','Registered_by']
	readonly_fields = ('id','First_Quarter_performance','Second_Quarter_performance','Third_Quarter_performance','Forth_Quarter_performance','Total_year_performance','Registered_at','Updated_by','Registered_by')
	list_per_page = 10
	list_select_related = True
	class Meta:
		model = HumanResourcePerformed	

	def save_model(self, request, obj, form, change):
		if change:
			obj.Update_by = request.user
			obj.Registered_at = datetime.now()
		obj.save()

admin.site.register(HumanResourcePerformed, HumanResourcePerformedAdmin)

class DetailCostRequestAdmin(ImportExportModelAdmin):
	pass
	fieldsets = [
        ('General informations', {
            'fields': [('Full_name','Kebele'),('House_number','Customer_neighbor'),('Service_type')],
        }),
		('Detail information', {
			'fields': [('Deposite','For_Digging','For_Rope','For_Agreement','For_Forms','For_consultation','For_information')],
		}),
		('Materials information', {
			'fields': [('Pipe_Quantity','Pipe_Single_price','Pipe_inch'),('HDP_tube_Quantity','HDP_Single_price','HDP_tube_inch'),('Elbow_Quantity','Elbow_Single_price','Elbow_inch'),('Naples_Quantity','Naples_Single_price','Naples_inch'),('Reducer_Quantity','Reducer_Single_price','Reducer_inch'),('Adapter_Quantity','Adapter_Single_price','Adapter_inch'),('Union_metal_Quantity','Union_metal_Single_price','Union_metal_inch'),('Union_HDP_Quantity','Union_HDP_Single_price','Union_HDP_inch'),('Get_valve_Quantity','Get_valve_Single_price','Get_valve_inch'),('Foss_set_Quantity','Foss_set_Single_price','Foss_set_inch'),('T_metal_Quantity','T_metal_Single_price','T_metal_inch'),('T_HDP_Quantity','T_HDP_Single_price','T_HDP_inch'),('Tape_Quantity','Tape_Single_price','Tape_inch'),('Water_meter_Quantity','Water_meter_Single_price','Water_meter_inch'),('Socket_Quantity','Socket_Single_price','Socket_inch'),'Grand_total'],
		}),
        ('Approval Requests', {
            'fields': ['Potable_water','Income_office','Amount','Cashier'],
        }),
    ]
	list_display = ['id','Full_name','Kebele','House_number','Service_type','Customer_neighbor','Total_55','Deposite','For_Digging','For_Rope','For_Agreement','For_Forms','Total_Form','Grand_total','Potable_water','Income_office','Amount','Cashier','Requested_at','Updated_by','Registered_by']
	search_fields = ['id','Full_name','Kebele','House_number','Service_type','Customer_neighbor','Total_55','Deposite','For_Digging','For_Rope','For_Agreement','For_Forms','Total_Form','Grand_total','Potable_water','Income_office','Amount','Cashier','Requested_at','Updated_by','Registered_by']
	list_filter = ['Service_type']
	list_display_links = ['id','Full_name','Kebele','House_number','Service_type','Customer_neighbor','Total_55','Deposite','For_Digging','For_Rope','For_Agreement','For_Forms','Total_Form','Grand_total','Potable_water','Income_office','Amount','Cashier','Requested_at','Updated_by','Registered_by']
	readonly_fields = ('id','Grand_total','Requested_at','Updated_by','Registered_by')
	list_per_page = 10
	list_select_related = True
	class Meta:
		model = DetailCostRequest	

	def save_model(self, request, obj, form, change):
		if change:
			obj.Update_by = request.user
			obj.Requested_at = datetime.now()
		obj.save()

admin.site.register(DetailCostRequest, DetailCostRequestAdmin)

class DetailCostRequestAdmin1(admin.ModelAdmin):
	fieldsets = [
        ('General informations', {
            'fields': [('Full_name','Kebele'),('House_number','Customer_neighbor'),('Service_type')],
        }),
		('Detail information', {
			'fields': [('Deposite','For_Digging','For_Rope','For_Agreement','For_Forms','For_consultation','For_information')],
		}),
		('Materials information', {
			'fields': [('Pipe_Quantity','Pipe_Single_price','Pipe_inch'),('HDP_tube_Quantity','HDP_Single_price','HDP_tube_inch'),('Elbow_Quantity','Elbow_Single_price','Elbow_inch'),('Naples_Quantity','Naples_Single_price','Naples_inch'),('Reducer_Quantity','Reducer_Single_price','Reducer_inch'),('Adapter_Quantity','Adapter_Single_price','Adapter_inch'),('Union_metal_Quantity','Union_metal_Single_price','Union_metal_inch'),('Union_HDP_Quantity','Union_HDP_Single_price','Union_HDP_inch'),('Get_valve_Quantity','Get_valve_Single_price','Get_valve_inch'),('Foss_set_Quantity','Foss_set_Single_price','Foss_set_inch'),('T_metal_Quantity','T_metal_Single_price','T_metal_inch'),('T_HDP_Quantity','T_HDP_Single_price','T_HDP_inch'),('Tape_Quantity','Tape_Single_price','Tape_inch'),('Water_meter_Quantity','Water_meter_Single_price','Water_meter_inch'),('Socket_Quantity','Socket_Single_price','Socket_inch'),'Grand_total'],
		}),
        ('Approval Requests', {
            'fields': ['Potable_water','Income_office','Amount','Cashier'],
        }),
    ]
	list_display = ['id','Full_name','Kebele','House_number','Service_type','Customer_neighbor','Total_55','Deposite','For_Digging','For_Rope','For_Agreement','For_Forms','Total_Form','Grand_total','Potable_water','Income_office','Amount','Cashier','Requested_at','Updated_by','Registered_by']
	search_fields = ['id','Full_name','Kebele','House_number','Service_type','Customer_neighbor','Total_55','Deposite','For_Digging','For_Rope','For_Agreement','For_Forms','Total_Form','Grand_total','Potable_water','Income_office','Amount','Cashier','Requested_at','Updated_by','Registered_by']
	list_filter = ['Service_type']
	list_display_links = ['id','Full_name','Kebele','House_number','Service_type','Customer_neighbor','Total_55','Deposite','For_Digging','For_Rope','For_Agreement','For_Forms','Total_Form','Grand_total','Potable_water','Income_office','Amount','Cashier','Requested_at','Updated_by','Registered_by']
	readonly_fields = ('id','Grand_total','Full_name','Kebele','House_number','Service_type','Customer_neighbor','Total_55','Deposite','For_Digging','For_Rope','For_Agreement','For_Forms','Total_Form','Grand_total','Income_office','Amount','Cashier','Requested_at','Updated_by','Registered_by')
	list_per_page = 10
	list_select_related = True
	class Meta:
		model = DetailCostRequestPotableWater	

	def save_model(self, request, obj, form, change):
		if change:
			obj.Update_by = request.user
			obj.Requested_at = datetime.now()
		obj.save()

admin.site.register(DetailCostRequestPotableWater, DetailCostRequestAdmin1)

class DetailCostRequestAdmin2(admin.ModelAdmin):
	fieldsets = [
        ('General informations', {
            'fields': [('Full_name','Kebele'),('House_number','Customer_neighbor'),('Service_type')],
        }),
		('Detail information', {
			'fields': [('Deposite','For_Digging','For_Rope','For_Agreement','For_Forms','For_consultation','For_information')],
		}),
		('Materials information', {
			'fields': [('Pipe_Quantity','Pipe_Single_price','Pipe_inch'),('HDP_tube_Quantity','HDP_Single_price','HDP_tube_inch'),('Elbow_Quantity','Elbow_Single_price','Elbow_inch'),('Naples_Quantity','Naples_Single_price','Naples_inch'),('Reducer_Quantity','Reducer_Single_price','Reducer_inch'),('Adapter_Quantity','Adapter_Single_price','Adapter_inch'),('Union_metal_Quantity','Union_metal_Single_price','Union_metal_inch'),('Union_HDP_Quantity','Union_HDP_Single_price','Union_HDP_inch'),('Get_valve_Quantity','Get_valve_Single_price','Get_valve_inch'),('Foss_set_Quantity','Foss_set_Single_price','Foss_set_inch'),('T_metal_Quantity','T_metal_Single_price','T_metal_inch'),('T_HDP_Quantity','T_HDP_Single_price','T_HDP_inch'),('Tape_Quantity','Tape_Single_price','Tape_inch'),('Water_meter_Quantity','Water_meter_Single_price','Water_meter_inch'),('Socket_Quantity','Socket_Single_price','Socket_inch'),'Grand_total'],
		}),
        ('Approval Requests', {
            'fields': ['Potable_water','Income_office','Amount','Cashier'],
        }),
    ]
	list_display = ['id','Full_name','Kebele','House_number','Service_type','Customer_neighbor','Total_55','Deposite','For_Digging','For_Rope','For_Agreement','For_Forms','Total_Form','Grand_total','Potable_water','Income_office','Amount','Cashier','Requested_at','Updated_by','Registered_by']
	search_fields = ['id','Full_name','Kebele','House_number','Service_type','Customer_neighbor','Total_55','Deposite','For_Digging','For_Rope','For_Agreement','For_Forms','Total_Form','Grand_total','Potable_water','Income_office','Amount','Cashier','Requested_at','Updated_by','Registered_by']
	list_filter = ['Service_type']
	list_display_links = ['id','Full_name','Kebele','House_number','Service_type','Customer_neighbor','Total_55','Deposite','For_Digging','For_Rope','For_Agreement','For_Forms','Total_Form','Grand_total','Potable_water','Income_office','Amount','Cashier','Requested_at','Updated_by','Registered_by']
	readonly_fields = ('id','Grand_total','Full_name','Kebele','House_number','Service_type','Customer_neighbor','Total_55','Deposite','For_Digging','For_Rope','For_Agreement','For_Forms','Total_Form','Grand_total','Potable_water','Amount','Cashier','Requested_at','Updated_by','Registered_by')
	list_per_page = 10
	list_select_related = True
	class Meta:
		model = DetailCostRequestIncomeOfficer	

	def save_model(self, request, obj, form, change):
		if change:
			obj.Update_by = request.user
			obj.Requested_at = datetime.now()
		obj.save()

admin.site.register(DetailCostRequestIncomeOfficer, DetailCostRequestAdmin2)

class DetailCostRequestAdmin3(admin.ModelAdmin):
	fieldsets = [
        ('General informations', {
            'fields': [('Full_name','Kebele'),('House_number','Customer_neighbor'),('Service_type')],
        }),
		('Detail information', {
			'fields': [('Deposite','For_Digging','For_Rope','For_Agreement','For_Forms','For_consultation','For_information')],
		}),
		('Materials information', {
			'fields': [('Pipe_Quantity','Pipe_Single_price','Pipe_inch'),('HDP_tube_Quantity','HDP_Single_price','HDP_tube_inch'),('Elbow_Quantity','Elbow_Single_price','Elbow_inch'),('Naples_Quantity','Naples_Single_price','Naples_inch'),('Reducer_Quantity','Reducer_Single_price','Reducer_inch'),('Adapter_Quantity','Adapter_Single_price','Adapter_inch'),('Union_metal_Quantity','Union_metal_Single_price','Union_metal_inch'),('Union_HDP_Quantity','Union_HDP_Single_price','Union_HDP_inch'),('Get_valve_Quantity','Get_valve_Single_price','Get_valve_inch'),('Foss_set_Quantity','Foss_set_Single_price','Foss_set_inch'),('T_metal_Quantity','T_metal_Single_price','T_metal_inch'),('T_HDP_Quantity','T_HDP_Single_price','T_HDP_inch'),('Tape_Quantity','Tape_Single_price','Tape_inch'),('Water_meter_Quantity','Water_meter_Single_price','Water_meter_inch'),('Socket_Quantity','Socket_Single_price','Socket_inch'),'Grand_total'],
		}),
        ('Approval Requests', {
            'fields': ['Potable_water','Income_office','Amount','Cashier'],
        }),
    ]
	list_display = ['id','Full_name','Kebele','House_number','Service_type','Customer_neighbor','Total_55','Deposite','For_Digging','For_Rope','For_Agreement','For_Forms','Total_Form','Grand_total','Potable_water','Income_office','Amount','Cashier','Requested_at','Updated_by','Registered_by']
	search_fields = ['id','Full_name','Kebele','House_number','Service_type','Customer_neighbor','Total_55','Deposite','For_Digging','For_Rope','For_Agreement','For_Forms','Total_Form','Grand_total','Potable_water','Income_office','Amount','Cashier','Requested_at','Updated_by','Registered_by']
	list_filter = ['Service_type']
	list_display_links = ['id','Full_name','Kebele','House_number','Service_type','Customer_neighbor','Total_55','Deposite','For_Digging','For_Rope','For_Agreement','For_Forms','Total_Form','Grand_total','Potable_water','Income_office','Amount','Cashier','Requested_at','Updated_by','Registered_by']
	readonly_fields = ('id','Grand_total','Full_name','Kebele','House_number','Service_type','Customer_neighbor','Total_55','Deposite','For_Digging','For_Rope','For_Agreement','For_Forms','Total_Form','Grand_total','Potable_water','Income_office','Amount','Requested_at','Updated_by','Registered_by')
	list_per_page = 10
	list_select_related = True
	class Meta:
		model = DetailCostRequestCashier	

	def save_model(self, request, obj, form, change):
		if change:
			obj.Update_by = request.user
			obj.Requested_at = datetime.now()
		obj.save()

admin.site.register(DetailCostRequestCashier, DetailCostRequestAdmin3)

class ComplainManagementAdmin(ImportExportModelAdmin):
    pass
    fieldsets = [
        ('General informations', {
            'fields': [('Category','Sub_category','Complain_type')],
        }),
		('Detail information', {
			'fields': [('Nature_of_complaint','Complain_details','Complain_related')],
		}),
    ]
    # fields = ['Category','Sub_category','Complain_type','Nature_of_complaint','Complain_details','Complain_related']
    list_display = ['id','Category','Sub_category','Complain_type','Nature_of_complaint','Complain_details','Complain_related','Complained_at','Updated_by','Registered_by']
    search_fields = ['id','Category','Sub_category','Complain_type','Nature_of_complaint','Complain_details','Complain_related','Complained_at','Updated_by','Registered_by']
    list_filter = ['Category']
    list_display_links = ['id','Category','Sub_category','Complain_type','Nature_of_complaint','Complain_details','Complain_related','Complained_at','Updated_by','Registered_by']
    readonly_fields = ('id','Complained_at','Updated_by','Registered_by')
    list_per_page = 10
    list_select_related = True
    class Meta:
	    model = ComplainManagement	

    def save_model(self, request, obj, form, change):
	    if change:
		    obj.Update_by = request.user
		    obj.Complained_at = datetime.now()
	    obj.save()

admin.site.register(ComplainManagement, ComplainManagementAdmin)

class GeneralLeisureAdmin(ImportExportModelAdmin):
    pass
    fieldsets = [
        ('General informations', {
            'fields': [('Tasks','Dates'),('General','Check_no','Check_payable','Receipt_no')],
        }), 
		('Detail information', {
			'fields': [('Deposit','Withdraw','Balance')],
		}),
    ]
    list_display = ['id','Dates','Tasks','General','Check_no','Receipt_no','Deposit','Withdraw','Balance']
    search_fields = ['id','Dates','Tasks','General','Check_no','Receipt_no','Deposit','Withdraw','Balance']
    list_filter = ['Dates']
    list_display_links = ['id','Dates','Tasks','General','Check_no','Receipt_no','Deposit','Withdraw','Balance']
    readonly_fields = ('id','Balance','Registered_date','Updated_by','Registered_by')
    list_per_page = 10
    list_select_related = True
    class Meta:
	    model = GeneralLeisure	

    def save_model(self, request, obj, form, change):
	    if change:
		    obj.Update_by = request.user
		    obj.Registered_date = datetime.now()
	    obj.save()

admin.site.register(GeneralLeisure, GeneralLeisureAdmin)

class GeneralReportTotalBalanceAdmin(ImportExportModelAdmin):
    pass
    fieldsets = [
        ('General informations', {
            'fields': [('Date'),('Total_deposite'),('Total_withdrawal')],
        }), 
		('Detail information', {
			'fields': [('Total_balance')],
		}),
    ]
    list_display = ['Date','Total_deposite','Total_withdrawal','Total_balance']
    search_fields = ['Date','Total_deposite','Total_withdrawal','Total_balance']
    list_filter = ['Date']
    list_display_links = ['Date','Total_deposite','Total_withdrawal','Total_balance']
    readonly_fields = ('Date','Total_deposite','Total_withdrawal','Total_balance')
    list_per_page = 10
    list_select_related = True
    class Meta:
	    model = GeneralReportTotalBalance	

    def save_model(self, request, obj, form, change):
	    if change:
		    obj.Update_by = request.user
		    obj.Registered_date = datetime.now()
	    obj.save()

admin.site.register(GeneralReportTotalBalance, GeneralReportTotalBalanceAdmin)

class GeneralReportBalanceDateAdmin(ImportExportModelAdmin):
    pass
    fieldsets = [
        ('General informations', {
            'fields': [('Id'),('Date'),('Total_deposite'),('Total_withdrawal')],
        }), 
		('Detail information', {
			'fields': [('Total_balance')],
		}),
    ]
    list_display = ['Id','Date','Total_deposite','Total_withdrawal','Total_balance']
    search_fields = ['Id','Date','Total_deposite','Total_withdrawal','Total_balance']
    list_filter = ['Date']
    list_display_links = ['Id','Date','Total_deposite','Total_withdrawal','Total_balance']
    readonly_fields = ('Id','Date','Total_deposite','Total_withdrawal','Total_balance')
    list_per_page = 10
    list_select_related = True
    class Meta:
	    model = GeneralReportBalanceDate	

    def save_model(self, request, obj, form, change):
	    if change:
		    obj.Update_by = request.user
		    obj.Registered_date = datetime.now()
	    obj.save()

admin.site.register(GeneralReportBalanceDate, GeneralReportBalanceDateAdmin)

class RevenueTypeAdmin(ImportExportModelAdmin):
    pass
    fieldsets = [
        ('General informations', {
            'fields': [('Dates','Code')],
        }), 
		('Detail information', {
			'fields': [('Revenue_title_amharic','Revenue_title_english')],
		}),
    ]
    list_display = ['id','Dates','Code','Revenue_title_amharic','Revenue_title_english']
    search_fields = ['id','Dates','Code','Revenue_title_amharic','Revenue_title_english']
    list_filter = ['Code']
    list_display_links = ['id','Dates','Code','Revenue_title_amharic','Revenue_title_english']
    readonly_fields = ('id','Registered_date','Updated_by','Registered_by')
    list_per_page = 10
    list_select_related = True
    class Meta:
	    model = RevenueType	

    def save_model(self, request, obj, form, change):
	    if change:
		    obj.Update_by = request.user
		    obj.Registered_date = datetime.now()
	    obj.save()

admin.site.register(RevenueType, RevenueTypeAdmin)

class ExpenseTypeAdmin(ImportExportModelAdmin):
    pass
    fieldsets = [
        ('General informations', {
            'fields': [('Dates','Code')],
        }), 
		('Detail information', {
			'fields': [('Expense_title_amharic','Expense_title_english')],
		}),
    ]
    list_display = ['id','Dates','Code','Expense_title_amharic','Expense_title_english']
    search_fields = ['id','Dates','Code','Expense_title_amharic','Expense_title_english']
    list_filter = ['Code']
    list_display_links = ['id','Dates','Code','Expense_title_amharic','Expense_title_english']
    readonly_fields = ('id','Registered_date','Updated_by','Registered_by')
    list_per_page = 10
    list_select_related = True
    class Meta:
	    model = ExpenseType	

    def save_model(self, request, obj, form, change):
	    if change:
		    obj.Update_by = request.user
		    obj.Registered_date = datetime.now()
	    obj.save()

admin.site.register(ExpenseType, ExpenseTypeAdmin)

class RevenueAdmin(ImportExportModelAdmin):
    pass
    fieldsets = [
        ('General informations', {
            'fields': [('Dates','Code')],
        }), 
		('Detail information', {
			'fields': ['Amount','Balance'],
		}),
    ]
    list_display = ['id','Dates','Code','Amount','Balance']
    search_fields = ['id','Dates','Code','Amount','Balance']
    list_filter = ['Code']
    list_display_links = ['id','Balance','Dates','Code','Amount','Balance']
    readonly_fields = ('id','Balance','Registered_date','Updated_by','Registered_by')
    list_per_page = 10
    list_select_related = True
    class Meta:
	    model = AllRevenue	

    def save_model(self, request, obj, form, change):
	    if change:
		    obj.Update_by = request.user
		    obj.Registered_date = datetime.now()
	    obj.save()

admin.site.register(AllRevenue, RevenueAdmin)

class ExpenseAdmin(ImportExportModelAdmin):
    pass
    fieldsets = [
        ('General informations', {
            'fields': [('Dates','Code')],
        }), 
		('Detail information', {
			'fields': ['Amount','Balance'],
		}),
    ]
    list_display = ['id','Dates','Code','Amount','Balance']
    search_fields = ['id','Dates','Code','Amount','Balance']
    list_filter = ['Code']
    list_display_links = ['id','Balance','Dates','Code','Amount','Balance']
    readonly_fields = ('id','Balance','Registered_date','Updated_by','Registered_by')
    list_per_page = 10
    list_select_related = True
    class Meta:
	    model = AllExpense	

    def save_model(self, request, obj, form, change):
	    if change:
		    obj.Update_by = request.user
		    obj.Registered_date = datetime.now()
	    obj.save()

admin.site.register(AllExpense, ExpenseAdmin)

class ExpenseReportAdmin(ImportExportModelAdmin):
    pass
    fieldsets = [
        ('General informations', {
            'fields': [('Code_id'),('Code')],
        }), 
		('Detail information', {
			'fields': [('Balances')],
		}),
    ]
    list_display = ['id','Dates','Code','Balances','Code_id']
    search_fields = ['id','Dates','Code','Balances','Code_id']
    list_filter = ['Code']
    list_display_links = ['id','Dates','Code','Balances','Code_id']
    readonly_fields = ('id','Dates','Code','Balances','Code_id')
    list_per_page = 10
    list_select_related = True
    class Meta:
	    model = ExpenseReport	

    def save_model(self, request, obj, form, change):
	    if change:
		    obj.Update_by = request.user
		    obj.Registered_date = datetime.now()
	    obj.save()

admin.site.register(ExpenseReport, ExpenseReportAdmin)

class ExpenseReportDateAdmin(ImportExportModelAdmin):
    pass
    fieldsets = [
        ('General informations', {
            'fields': [('Code_id'),('Code')],
        }), 
		('Detail information', {
			'fields': [('Balances')],
		}),
    ]
    list_display = ['id','Dates','Code','Balances','Code_id']
    search_fields = ['id','Dates','Code','Balances','Code_id']
    list_filter = ['Code']
    list_display_links = ['id','Dates','Code','Balances','Code_id']
    readonly_fields = ('id','Dates','Code','Balances','Code_id')
    list_per_page = 10
    list_select_related = True
    class Meta:
	    model = ExpenseReportDate	

    def save_model(self, request, obj, form, change):
	    if change:
		    obj.Update_by = request.user
		    obj.Registered_date = datetime.now()
	    obj.save()

admin.site.register(ExpenseReportDate, ExpenseReportDateAdmin)

class RevenueReportAdmin(ImportExportModelAdmin):
    pass
    fieldsets = [
        ('General informations', {
            'fields': [('Code_id'),('Code')],
        }), 
		('Detail information', {
			'fields': [('Balances')],
		}),
    ]
    list_display = ['id','Dates','Code','Balances','Code_id']
    search_fields = ['id','Dates','Code','Balances','Code_id']
    list_filter = ['Code']
    list_display_links = ['id','Dates','Code','Balances','Code_id']
    readonly_fields = ('id','Dates','Code','Balances','Code_id')
    list_per_page = 10
    list_select_related = True
    class Meta:
	    model = RevenueReport	

    def save_model(self, request, obj, form, change):
	    if change:
		    obj.Update_by = request.user
		    obj.Registered_date = datetime.now()
	    obj.save()

admin.site.register(RevenueReport, RevenueReportAdmin)

class RevenueReportDateAdmin(ImportExportModelAdmin):
    pass
    fieldsets = [
        ('General informations', {
            'fields': [('Code_id'),('Code')],
        }), 
		('Detail information', {
			'fields': [('Balances')],
		}),
    ]
    list_display = ['id','Dates','Code','Balances','Code_id']
    search_fields = ['id','Dates','Code','Balances','Code_id']
    list_filter = ['Code']
    list_display_links = ['id','Dates','Code','Balances','Code_id']
    readonly_fields = ('id','Dates','Code','Balances','Code_id')
    list_per_page = 10
    list_select_related = True
    class Meta:
	    model = RevenueReportDate	

    def save_model(self, request, obj, form, change):
	    if change:
		    obj.Update_by = request.user
		    obj.Registered_date = datetime.now()
	    obj.save()

admin.site.register(RevenueReportDate, RevenueReportDateAdmin)
