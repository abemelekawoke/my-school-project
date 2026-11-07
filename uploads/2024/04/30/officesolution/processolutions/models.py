from import_export import resources
from django.db.models import Subquery, OuterRef
from django.db import connection
from django.db import models
from django.utils import timezone
import datetime
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)
from django_currentuser.db.models import CurrentUserField
from django.urls import reverse
from django.http import HttpResponse

class WaterSupplyPlan(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    Dates = models.CharField(max_length=100)
    Tasks = models.CharField(max_length = 150)
    Measurement = models.CharField(max_length=150)
    First_Quarter_Plan = models.DecimalField(max_digits=30, decimal_places=2)
    Second_Quarter_Plan = models.DecimalField(max_digits=30, decimal_places=2)
    Third_Quarter_Plan = models.DecimalField(max_digits=30, decimal_places=2)
    Forth_Quarter_Plan = models.DecimalField(max_digits=30, decimal_places=2)
    Total_budget = models.DecimalField(max_digits=30, decimal_places=2)
    Planned_at = models.DateTimeField(auto_now=True, verbose_name="Planned at")
    Updated_by = CurrentUserField(related_name="up_by")
    Planned_by = CurrentUserField(related_name="pl_by")

    def __str__(self):
        return "%s%s" % (self.id,self.Tasks)
    def save(self, *args, **kwargs):
        self.Total_budget = self.First_Quarter_Plan + self.Second_Quarter_Plan + self.Third_Quarter_Plan + self.Forth_Quarter_Plan
        super(WaterSupplyPlan, self).save(*args, **kwargs)

class FinanceIncomePlan(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    Dates = models.CharField(max_length=100)
    # Year = models.DateField()
    Tasks = models.CharField(max_length = 150)
    Measurement = models.CharField(max_length=150)
    # Month = models.DateField()
    First_Quarter_Plan = models.DecimalField(max_digits=30, decimal_places=2)
    Second_Quarter_Plan = models.DecimalField(max_digits=30, decimal_places=2)
    Third_Quarter_Plan = models.DecimalField(max_digits=30, decimal_places=2)
    Forth_Quarter_Plan = models.DecimalField(max_digits=30, decimal_places=2)
    Total_budget = models.DecimalField(max_digits=30, decimal_places=2)
    Planned_at = models.DateTimeField(auto_now=True, verbose_name="Planned at")
    Updated_by = CurrentUserField(related_name="up_by1")
    Planned_by = CurrentUserField(related_name="pl_by1")

    def __str__(self):
        return "%s%s" % (self.id,self.Tasks)
    def save(self, *args, **kwargs):
        self.Total_budget = self.First_Quarter_Plan + self.Second_Quarter_Plan + self.Third_Quarter_Plan + self.Forth_Quarter_Plan
        super(FinanceIncomePlan, self).save(*args, **kwargs)
        
class FinanceCostPlan(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    Dates = models.CharField(max_length=100)
    # Year = models.DateField()
    Tasks = models.CharField(max_length = 150)
    Measurement = models.CharField(max_length=150)
    # Month = models.DateField()
    First_Quarter_Plan = models.DecimalField(max_digits=30, decimal_places=2)
    Second_Quarter_Plan = models.DecimalField(max_digits=30, decimal_places=2)
    Third_Quarter_Plan = models.DecimalField(max_digits=30, decimal_places=2)
    Forth_Quarter_Plan = models.DecimalField(max_digits=30, decimal_places=2)
    Total_budget = models.DecimalField(max_digits=30, decimal_places=2)
    Planned_at = models.DateTimeField(auto_now=True, verbose_name="Planned at")
    Updated_by = CurrentUserField(related_name="up_by2")
    Planned_by = CurrentUserField(related_name="pl_by2")

    def __str__(self):
        return "%s%s" % (self.id,self.Tasks)
    def save(self, *args, **kwargs):
        self.Total_budget = self.First_Quarter_Plan + self.Second_Quarter_Plan + self.Third_Quarter_Plan + self.Forth_Quarter_Plan
        super(FinanceExpenditurePlan, self).save(*args, **kwargs)

class HumanResourcePlan(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    Dates = models.CharField(max_length=100)
    # Year = models.DateField()
    Tasks = models.CharField(max_length = 150)
    Measurement = models.CharField(max_length=150)
    # Month = models.DateField()
    First_Quarter_Plan = models.DecimalField(max_digits=30, decimal_places=2)
    Second_Quarter_Plan = models.DecimalField(max_digits=30, decimal_places=2)
    Third_Quarter_Plan = models.DecimalField(max_digits=30, decimal_places=2)
    Forth_Quarter_Plan = models.DecimalField(max_digits=30, decimal_places=2)
    Total_budget = models.DecimalField(max_digits=30, decimal_places=2)
    Planned_at = models.DateTimeField(auto_now=True, verbose_name="Planned at")
    Updated_by = CurrentUserField(related_name="up_by3")
    Planned_by = CurrentUserField(related_name="pl_by3")

    def __str__(self):
        return "%s%s" % (self.id,self.Tasks)
    def save(self, *args, **kwargs):
        self.Total_budget = self.First_Quarter_Plan + self.Second_Quarter_Plan + self.Third_Quarter_Plan + self.Forth_Quarter_Plan
        super(HumanResourcePlan, self).save(*args, **kwargs)

class PlanningAndCustomerIssuePlan(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    Dates = models.CharField(max_length=100)
    # Year = models.DateField()
    Tasks = models.CharField(max_length = 150)
    Measurement = models.CharField(max_length=150)
    # Month = models.DateField()
    First_Quarter_Plan = models.DecimalField(max_digits=30, decimal_places=2)
    Second_Quarter_Plan = models.DecimalField(max_digits=30, decimal_places=2)
    Third_Quarter_Plan = models.DecimalField(max_digits=30, decimal_places=2)
    Forth_Quarter_Plan = models.DecimalField(max_digits=30, decimal_places=2)
    
    Total_budget = models.DecimalField(max_digits=30, decimal_places=2)
    Planned_at = models.DateTimeField(auto_now=True, verbose_name="Planned at")
    Updated_by = CurrentUserField(related_name="up_by12")
    Planned_by = CurrentUserField(related_name="pl_by12")

    def __str__(self):
        return "%s%s" % (self.id,self.Tasks)
    def save(self, *args, **kwargs):
        self.Total_budget = self.First_Quarter_Plan + self.Second_Quarter_Plan + self.Third_Quarter_Plan + self.Forth_Quarter_Plan
        super(HumanResourcePlan, self).save(*args, **kwargs)

class PlanningAndCustomerIssuePerformed(models.Model):
    THEME_CHOICES = (
		('First', 'First Quarter'),
		('Second', 'Second Quarter'),
		('Third', 'Third Quarter'),
		('Forth', 'Forth Quarter'),
	)
    id = models.AutoField(primary_key = True, unique = True)
    Dates = models.CharField(max_length=100)
    Planned_tasks = models.ForeignKey(PlanningAndCustomerIssuePlan, on_delete=models.CASCADE)

    First_Quarter_performed = models.DecimalField(max_digits=30, decimal_places=2, default=0)
    Second_Quarter_performed = models.DecimalField(max_digits=30, decimal_places=2, default=0)
    Third_Quarter_performed = models.DecimalField(max_digits=30, decimal_places=2, default=0)
    Forth_Quarter_performed = models.DecimalField(max_digits=30, decimal_places=2, default=0)

    First_Quarter_performance = models.DecimalField(max_digits=30, decimal_places=2, default=0)
    Second_Quarter_performance = models.DecimalField(max_digits=30, decimal_places=2, default=0)
    Third_Quarter_performance = models.DecimalField(max_digits=30, decimal_places=2, default=0)
    Forth_Quarter_performance = models.DecimalField(max_digits=30, decimal_places=2, default=0)

    Total_year_performance = models.DecimalField(max_digits=50, decimal_places=2, default=0)

    Registered_at = models.DateTimeField(auto_now=True, verbose_name="Registered at")
    Updated_by = CurrentUserField(related_name="up_by77")
    Registered_by = CurrentUserField(related_name="pl_by77")

    def __str__(self):
        return "%s" % (self.id)
    class Meta:
        verbose_name="Planning And Customer Issue Performed"
        verbose_name_plural="Planning And Customer Issue Performed"

    def save(self, *args, **kwargs):
    	plan = PlanningAndCustomerIssuePlan.objects.get(id=self.Planned_tasks_id)
    	p1 = plan.First_Quarter_Plan
    	p2 = plan.Second_Quarter_Plan
    	p3 = plan.Third_Quarter_Plan
    	p4 = plan.Forth_Quarter_Plan

    	self.First_Quarter_performance = (self.First_Quarter_performed/p1)*100
    	self.Second_Quarter_performance = (self.Second_Quarter_performed/p2)*100
    	self.Third_Quarter_performance = (self.Third_Quarter_performed/p3)*100
    	self.Forth_Quarter_performance = (self.Forth_Quarter_performed/p4)*100

    	self.Total_year_performance = (self.First_Quarter_performed/p1)*100 + (self.Second_Quarter_performed/p2)*100 + (self.Third_Quarter_performed/p3)*100 + (self.Forth_Quarter_performed/p4)*100
    	super(PlanningAndCustomerIssuePerformed, self).save(*args, **kwargs)


class MaintenanceRequest(models.Model):
    THEME_CHOICES = (
		('1/2', '1/2'),
		('3/4', '3/4'),
		('1', '1'),
		('1 1/2', '1 1/2'),
        ('2', '2'),
        ('2 1/2', '2 1/2'),
        ('3', '3'),
        ('3 1/2', '3 1/2'),
        ('4', '4'),
	)
    THEME_CHOICES1 = (
        ('Residence', 'Residence'),
        ('Trade_organization', 'Trade organization'),
        ('Public_government', 'Public government'),
	)
    THEME_CHOICES2 = (
		('2 1/2 - 2', '2 1/2 - 2'),
		('2 1/2 - 1 1/2', '2 1/2 - 1 1/2'),
		('2 1/2 - 1', '2 1/2 - 1'),
		('2 1/2 - 3/4', '2 1/2 - 3/4'),
        ('2 1/2 - 1/2', '2 1/2 - 1/2'),
        ('2 - 1 1/2', '2 - 1 1/2'),
        ('2 - 1', '2 - 1'),
        ('2 - 3/4', '2 - 3/4'),
        ('2 - 1/2', '2 - 1/2'),
        ('1 1/2 - 1', '1 1/2 - 1'),
        ('1 1/2 - 3/4', '1 1/2 - 3/4'),
        ('1 1/2 - 1/2', '1 1/2 - 1/2'),
        ('1 - 3/4', '1 - 3/4'),
        ('1 - 1/2', '1 - 1/2'),
	)
    id = models.AutoField(primary_key = True, unique = True)
    Full_name = models.CharField(max_length = 150)
    Address = models.CharField(max_length = 150, blank=True)
    Kebele = models.CharField(max_length = 150)
    Service_type = models.CharField(max_length = 150, choices=THEME_CHOICES1, blank=True)

    Simple_maintenance  = models.PositiveIntegerField(default=175, blank=True)
    Water_meter_transfer = models.PositiveIntegerField(default=175, blank=True)
    Water_meter_change = models.PositiveIntegerField(blank=True, default=0)
    Examine_or_clean_up = models.PositiveIntegerField(default=40, blank=True)
    Water_meter_openning = models.PositiveIntegerField(default=60, blank=True)
    Get_valve_change = models.PositiveIntegerField(blank=True, default=0)
    For_waste = models.PositiveIntegerField(blank=True, default=0)
    For_Digging = models.PositiveIntegerField(blank=True, default=0)

    House_number = models.CharField(max_length = 150, blank=True)
    Phone_number = models.CharField(max_length = 150)
    Place = models.CharField(max_length = 150)
    Pipe_Quantity = models.PositiveIntegerField(blank=True, default=0)
    Pipe_Single_price = models.PositiveIntegerField(blank=True, default=0)
    Pipe_inch = models.CharField(max_length = 150, choices = THEME_CHOICES,blank=True)
    HDP_tube_Quantity = models.PositiveIntegerField(blank=True, default=0)
    HDP_Single_price = models.PositiveIntegerField(blank=True, default=0)
    HDP_tube_inch = models.CharField(max_length = 150, choices = THEME_CHOICES,blank=True)
    Elbow_Quantity = models.PositiveIntegerField(blank=True, default=0)
    Elbow_Single_price = models.PositiveIntegerField(blank=True, default=0)
    Elbow_inch = models.CharField(max_length = 150, choices = THEME_CHOICES,blank=True)
    Naples_Quantity = models.PositiveIntegerField(blank=True, default=0)
    Naples_Single_price = models.PositiveIntegerField(blank=True, default=0)
    Naples_inch = models.CharField(max_length = 150, choices = THEME_CHOICES,blank=True)
    Reducer_Quantity = models.PositiveIntegerField(blank=True, default=0)
    Reducer_Single_price = models.PositiveIntegerField(blank=True, default=0)
    Reducer_inch = models.CharField(max_length = 150, choices = THEME_CHOICES2,blank=True)

    Adapter_Quantity = models.PositiveIntegerField(blank=True, default=0)
    Adapter_Single_price = models.PositiveIntegerField(blank=True, default=0)
    Adapter_inch = models.CharField(max_length = 150, choices = THEME_CHOICES,blank=True)
    Union_metal_Quantity = models.PositiveIntegerField(blank=True, default=0)
    Union_metal_Single_price = models.PositiveIntegerField(blank=True, default=0)
    Union_metal_inch = models.CharField(max_length = 150, choices = THEME_CHOICES,blank=True)
    Union_HDP_Quantity = models.PositiveIntegerField(blank=True, default=0)
    Union_HDP_Single_price = models.PositiveIntegerField(blank=True, default=0)
    Union_HDP_inch = models.CharField(max_length = 150, choices = THEME_CHOICES,blank=True)
    Get_valve_Quantity = models.PositiveIntegerField(blank=True, default=0)
    Get_valve_Single_price = models.PositiveIntegerField(blank=True, default=0)
    Get_valve_inch = models.CharField(max_length = 150, choices = THEME_CHOICES,blank=True)
    Foss_set_Quantity = models.PositiveIntegerField(blank=True, default=0)
    Foss_set_Single_price = models.PositiveIntegerField(blank=True, default=0)
    Foss_set_inch = models.CharField(max_length = 150, choices = THEME_CHOICES,blank=True)
    
    T_metal_Quantity = models.PositiveIntegerField(blank=True, default=0)
    T_metal_Single_price = models.PositiveIntegerField(blank=True, default=0)
    T_metal_inch = models.CharField(max_length = 150, choices = THEME_CHOICES,blank=True)
    T_HDP_Quantity = models.PositiveIntegerField(blank=True, default=0)
    T_HDP_Single_price = models.PositiveIntegerField(blank=True, default=0)
    T_HDP_inch = models.CharField(max_length = 150, choices = THEME_CHOICES,blank=True)
    Tape_Quantity = models.PositiveIntegerField(blank=True, default=0)
    Tape_Single_price = models.PositiveIntegerField(blank=True, default=0)
    Tape_inch = models.CharField(max_length = 150, choices = THEME_CHOICES,blank=True)
    Water_meter_Quantity = models.PositiveIntegerField(blank=True, default=0)
    Water_meter_Single_price = models.PositiveIntegerField(blank=True, default=0)
    Water_meter_inch = models.CharField(max_length = 150, choices = THEME_CHOICES,blank=True)
    Socket_Quantity = models.PositiveIntegerField(blank=True, default=0)
    Socket_Single_price = models.PositiveIntegerField(blank=True, default=0)
    Socket_inch = models.CharField(max_length = 150, choices = THEME_CHOICES,blank=True)

    Total_55 = models.FloatField(blank=True, default=0)
    Grand_total = models.FloatField(blank=True, default=0)
    Water_supply = models.TextField(max_length = 250, blank=True, default="To Income Officer")
    Income_office = models.TextField(max_length = 250, blank=True, default="To Finance Officer")
    Amount = models.PositiveIntegerField(blank=True, default=0)
    Cashier = models.TextField(blank=True, default="በገቢ ደረሰኝ ቁጥር       ብር ስለከፈለ ቀሪው ስራ ታይቶ ይሰራለት፡፡")
    Requested_at = models.DateTimeField(auto_now=True, verbose_name="Requested at")
    Updated_by = CurrentUserField(related_name="up_by11")
    Registered_by = CurrentUserField(related_name="pl_by11")

    def save(self, *args, **kwargs):
        self.Total_55 = (
            (self.Pipe_Quantity * self.Pipe_Single_price)+
            (self.HDP_tube_Quantity * self.HDP_Single_price)+
            (self.Elbow_Quantity * self.Elbow_Single_price)+
            (self.Naples_Quantity * self.Naples_Single_price)+
            (self.Reducer_Quantity * self.Reducer_Single_price)+
            (self.Adapter_Quantity * self.Adapter_Single_price)+
            (self.Union_metal_Quantity * self.Union_metal_Single_price)+
            (self.Union_HDP_Quantity * self.Union_HDP_Single_price)+
            (self.Get_valve_Quantity * self.Get_valve_Single_price)+
            (self.Foss_set_Quantity * self.Foss_set_Single_price)+
            (self.T_metal_Quantity * self.T_metal_Single_price)+
            (self.T_HDP_Quantity * self.T_HDP_Single_price)+
            (self.Tape_Quantity * self.Tape_Single_price)+
            (self.Water_meter_Quantity * self.Water_meter_Single_price)+
            (self.Socket_Quantity * self.Socket_Single_price)
            
            ) * 0.55
        self.Grand_total = self.Total_55 + self.Simple_maintenance + self.Water_meter_transfer + self.For_Digging + self.Water_meter_change + self.Examine_or_clean_up + self.Water_meter_openning + self.Get_valve_change + self.For_waste
        super(MaintenanceRequest, self).save(*args, **kwargs)

    def __str__(self):
        return "%s" % (self.id)
    class Meta():
        verbose_name_plural='የጥገና ጥያቄ'        
            

class MaintenanceRequestPotableWater(MaintenanceRequest):

    class Meta:
        proxy = True
        verbose_name_plural='ለመጠጥ ዉኃ የስራ ሂደት የጥገና ጥያቄ'

class MaintenanceRequestIncomeOfficer(MaintenanceRequest):

    class Meta:
        proxy = True
        verbose_name_plural='ለገቢ ግዥ ፋይናንስ የስራ ሂደት የጥገና ጥያቄ'

class MaintenanceRequestCashier(MaintenanceRequest):

    class Meta:
        proxy = True
        verbose_name_plural='ለንብረትና ገንዘብ ያዥ የስራ ሂደት የጥገና ጥያቄ'

class NameChangeRequest(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    Full_name = models.CharField(max_length = 150)
    Address = models.CharField(max_length = 150)
    Kebele = models.CharField(max_length = 150)
    Service_type = models.CharField(max_length = 150)
    # Maintenance_type  = models.CharField(max_length = 150)
    House_number = models.CharField(max_length = 150)
    Phone_number = models.CharField(max_length = 150)
    Place = models.CharField(max_length = 150)
    Income_office = models.TextField(max_length = 250, blank=True, default="To Finance Officer")
    Amount = models.PositiveIntegerField()
    Cashier = models.TextField(max_length = 250, blank=True, default="በገቢ ደረሰኝ ቁጥር       ብር ስለከፈለ ቀሪው ስራ ታይቶ ይሰራለት፡፡")
    Bill_processor  = models.TextField(max_length = 250, blank=True, default="To the organization ")
    Requested_at = models.DateTimeField(auto_now=True, verbose_name="Requested at")
    Updated_by = CurrentUserField(related_name="up_bypp")
    Registered_by = CurrentUserField(related_name="pl_bypp")

    class Meta():
        verbose_name_plural='የስም ለውጥ ጥያቄ'
             

    def __str__(self):
        return "%s" % (self.id)

class NameChangeRequestIncomeOfficer(NameChangeRequest):

    class Meta:
        proxy = True
        verbose_name_plural='ለገቢ ግዥ ፋይናንስ የስራ ሂደት የስም ለውጥ ጥያቄ'
# Water_meter_Single_price
class NameChangeRequestCashier(NameChangeRequest):

    class Meta:
        proxy = True
        verbose_name_plural='ለንብረትና ገንዘብ ያዥ የስራ ሂደት የስም ለውጥ ጥያቄ'

class NameChangeRequestBillProcessor(NameChangeRequest):

    class Meta:
        proxy = True
        verbose_name_plural='ለቢልና ግምት ክፍል የስራ ሂደት የስም ለውጥ ጥያቄ'

class PotableWaterRequest(models.Model):
    THEME_CHOICES1 = (
        ('Residence', 'Residence'),
        ('Trade_organization', 'Trade organization'),
        ('Public_government', 'Public government'),
	)
    id = models.AutoField(primary_key = True, unique = True)
    Full_name = models.CharField(max_length = 150)
    Address = models.CharField(max_length = 150)
    Kebele = models.CharField(max_length = 150)
    House_number  = models.CharField(max_length = 150)
    Phone_number = models.CharField(max_length = 150)
    Place = models.CharField(max_length = 150)
    Service_type = models.CharField(max_length = 150, choices=THEME_CHOICES1)
    Line_joined = models.CharField(max_length = 150)
    Water_supply = models.TextField(blank=True, default="To Income Officer")
    Income_office = models.TextField(blank=True, default="To Finance Officer")
    Amount = models.PositiveIntegerField()
    Cashier = models.TextField(blank=True, default="በገቢ ደረሰኝ ቁጥር       ብር ስለከፈለ ቀሪው ስራ ታይቶ ይሰራለት፡፡")
    Requested_at = models.DateTimeField(auto_now=True, verbose_name="Requested at")
    Updated_by = CurrentUserField(related_name="up_by6")
    Registered_by = CurrentUserField(related_name="pl_by6")

    def __str__(self):
        return "%s" % (self.id)
    class Meta():
        verbose_name_plural='የአዲስ ደንበኛ ጥያቄ'
            

class PotableWaterRequestPotableWater(PotableWaterRequest):

    class Meta:
        proxy = True
        verbose_name_plural='ለመጠጥ ዉኃ የስራ ሂደት የአዲስ ደንበኛ ጥያቄ'

class PotableWaterRequestIncomeOfficer(PotableWaterRequest):

    class Meta:
        proxy = True
        verbose_name_plural='ለገቢ ግዥ ፋይናንስ የስራ ሂደት  የአዲስ ደንበኛ ጥያቄ'

class PotableWaterRequestCashier(PotableWaterRequest):

    class Meta:
        proxy = True
        verbose_name_plural='ለንብረትና ገንዘብ ያዥ የስራ ሂደት የአዲስ ደንበኛ ጥያቄ'


class DetailCostRequest(models.Model):
    THEME_CHOICES = (
		('1/2', '1/2'),
		('3/4', '3/4'),
		('1', '1'),
		('1 1/2', '1 1/2'),
        ('2', '2'),
        ('2 1/2', '2 1/2'),
        ('3', '3'),
        ('3 1/2', '3 1/2'),
        ('4', '4'),
	)
    THEME_CHOICES1 = (
        ('Residence', 'Residence'),
        ('Trade_organization', 'Trade organization'),
        ('Public_government', 'Public government'),
	)
    THEME_CHOICES2 = (
		('2 1/2 - 2', '2 1/2 - 2'),
		('2 1/2 - 1 1/2', '2 1/2 - 1 1/2'),
		('2 1/2 - 1', '2 1/2 - 1'),
		('2 1/2 - 3/4', '2 1/2 - 3/4'),
        ('2 1/2 - 1/2', '2 1/2 - 1/2'),
        ('2 - 1 1/2', '2 - 1 1/2'),
        ('2 - 1', '2 - 1'),
        ('2 - 3/4', '2 - 3/4'),
        ('2 - 1/2', '2 - 1/2'),
        ('1 1/2 - 1', '1 1/2 - 1'),
        ('1 1/2 - 3/4', '1 1/2 - 3/4'),
        ('1 1/2 - 1/2', '1 1/2 - 1/2'),
        ('1 - 3/4', '1 - 3/4'),
        ('1 - 1/2', '1 - 1/2'),
	)
    id = models.AutoField(primary_key = True, unique = True)
    Full_name = models.CharField(max_length = 150)
    Kebele = models.CharField(max_length = 150)
    House_number  = models.CharField(max_length = 150,blank=True)
    Service_type = models.CharField(max_length = 150, choices=THEME_CHOICES1)
    Customer_neighbor = models.CharField(max_length=150,blank=True)
    For_consultation = models.PositiveIntegerField(blank=True, default=0)
    For_information = models.PositiveIntegerField(blank=True, default=0)

    Pipe_Quantity = models.PositiveIntegerField(blank=True, default=0)
    Pipe_Single_price = models.PositiveIntegerField(blank=True, default=0)
    Pipe_inch = models.CharField(max_length = 150, choices = THEME_CHOICES,blank=True)
    HDP_tube_Quantity = models.PositiveIntegerField(blank=True, default=0)
    HDP_Single_price = models.PositiveIntegerField(blank=True, default=0)
    HDP_tube_inch = models.CharField(max_length = 150, choices = THEME_CHOICES,blank=True)
    Elbow_Quantity = models.PositiveIntegerField(blank=True, default=0)
    Elbow_Single_price = models.PositiveIntegerField(blank=True, default=0)
    Elbow_inch = models.CharField(max_length = 150, choices = THEME_CHOICES,blank=True)
    Naples_Quantity = models.PositiveIntegerField(blank=True, default=0)
    Naples_Single_price = models.PositiveIntegerField(blank=True, default=0)
    Naples_inch = models.CharField(max_length = 150, choices = THEME_CHOICES,blank=True)
    Reducer_Quantity = models.PositiveIntegerField(blank=True, default=0)
    Reducer_Single_price = models.PositiveIntegerField(blank=True, default=0)
    Reducer_inch = models.CharField(max_length = 150, choices = THEME_CHOICES2,blank=True)

    Adapter_Quantity = models.PositiveIntegerField(blank=True, default=0)
    Adapter_Single_price = models.PositiveIntegerField(blank=True, default=0)
    Adapter_inch = models.CharField(max_length = 150, choices = THEME_CHOICES,blank=True)
    Union_metal_Quantity = models.PositiveIntegerField(blank=True, default=0)
    Union_metal_Single_price = models.PositiveIntegerField(blank=True, default=0)
    Union_metal_inch = models.CharField(max_length = 150, choices = THEME_CHOICES,blank=True)
    Union_HDP_Quantity = models.PositiveIntegerField(blank=True, default=0)
    Union_HDP_Single_price = models.PositiveIntegerField(blank=True, default=0)
    Union_HDP_inch = models.CharField(max_length = 150, choices = THEME_CHOICES,blank=True)
    Get_valve_Quantity = models.PositiveIntegerField(blank=True, default=0)
    Get_valve_Single_price = models.PositiveIntegerField(blank=True, default=0)
    Get_valve_inch = models.CharField(max_length = 150, choices = THEME_CHOICES,blank=True)
    Foss_set_Quantity = models.PositiveIntegerField(blank=True, default=0)
    Foss_set_Single_price = models.PositiveIntegerField(blank=True, default=0)
    Foss_set_inch = models.CharField(max_length = 150, choices = THEME_CHOICES,blank=True)
    
    T_metal_Quantity = models.PositiveIntegerField(blank=True, default=0)
    T_metal_Single_price = models.PositiveIntegerField(blank=True, default=0)
    T_metal_inch = models.CharField(max_length = 150, choices = THEME_CHOICES,blank=True)
    T_HDP_Quantity = models.PositiveIntegerField(blank=True, default=0)
    T_HDP_Single_price = models.PositiveIntegerField(blank=True, default=0)
    T_HDP_inch = models.CharField(max_length = 150, choices = THEME_CHOICES,blank=True)
    Tape_Quantity = models.PositiveIntegerField(blank=True, default=0)
    Tape_Single_price = models.PositiveIntegerField(blank=True, default=0)
    Tape_inch = models.CharField(max_length = 150, choices = THEME_CHOICES,blank=True)
    Water_meter_Quantity = models.PositiveIntegerField(blank=True, default=0)
    Water_meter_Single_price = models.PositiveIntegerField(blank=True, default=0)
    Water_meter_inch = models.CharField(max_length = 150, choices = THEME_CHOICES,blank=True)
    Socket_Quantity = models.PositiveIntegerField(blank=True, default=0)
    Socket_Single_price = models.PositiveIntegerField(blank=True, default=0)
    Socket_inch = models.CharField(max_length = 150, choices = THEME_CHOICES,blank=True)
     # Total_price = models.PositiveIntegerField(blank=True)
    Total_55 = models.FloatField(blank=True, default=0)
    Deposite=models.PositiveIntegerField(blank=True, default=100, help_text="ድርጅት ብር 350")
    For_Digging = models.PositiveIntegerField(default=0)
    For_Rope = models.PositiveIntegerField(blank=True, default=60)
    For_Agreement = models.PositiveIntegerField(blank=True, default=30)
    For_Forms = models.PositiveIntegerField(default=0)
    Total_Form = models.PositiveIntegerField(blank=True, default=0)
    Grand_total = models.FloatField(blank=True, default=0)

    Potable_water = models.TextField(blank=True, default="To Income Officer")
    Income_office = models.TextField(blank=True, default="To Finance Officer")
    Amount = models.PositiveIntegerField(blank=True, default=0)
    Cashier = models.TextField(blank=True, default="በገቢ ደረሰኝ ቁጥር       ብር ስለከፈለ ቀሪው ስራ ታይቶ ይሰራለት፡፡")
    Requested_at = models.DateTimeField(auto_now=True, verbose_name="Requested at")
    Updated_by = CurrentUserField(related_name="up_by61")
    Registered_by = CurrentUserField(related_name="pl_by61")

    def __str__(self):
        return "%s" % (self.id)

    class Meta():
        verbose_name_plural='የ55% አገልግሎት ክፍያ ጥያቄ'
    
    def save(self, *args, **kwargs):
        self.Total_55 = (
            (self.Pipe_Quantity * self.Pipe_Single_price)+
            (self.HDP_tube_Quantity * self.HDP_Single_price)+
            (self.Elbow_Quantity * self.Elbow_Single_price)+
            (self.Naples_Quantity * self.Naples_Single_price)+
            (self.Reducer_Quantity * self.Reducer_Single_price)+
            (self.Adapter_Quantity * self.Adapter_Single_price)+
            (self.Union_metal_Quantity * self.Union_metal_Single_price)+
            (self.Union_HDP_Quantity * self.Union_HDP_Single_price)+
            (self.Get_valve_Quantity * self.Get_valve_Single_price)+
            (self.Foss_set_Quantity * self.Foss_set_Single_price)+
            (self.T_metal_Quantity * self.T_metal_Single_price)+
            (self.T_HDP_Quantity * self.T_HDP_Single_price)+
            (self.Tape_Quantity * self.Tape_Single_price)+
            (self.Water_meter_Quantity * self.Water_meter_Single_price)+
            (self.Socket_Quantity * self.Socket_Single_price)
            
            ) * 0.55
        self.Total_Form = self.For_Forms * 2
        self.Grand_total = self.Total_55 + self.Deposite + self.For_Digging + self.For_Rope + self.For_Agreement + (self.For_Forms) * 2
        super(DetailCostRequest, self).save(*args, **kwargs)



class DetailCostRequestPotableWater(DetailCostRequest):

    class Meta:
        proxy = True
        verbose_name_plural='ለመጠጥ ዉኃ የስራ ሂደት 55% አገልግሎት ክፍያ ጥያቄ'

class DetailCostRequestIncomeOfficer(DetailCostRequest):

    class Meta:
        proxy = True
        verbose_name_plural='ለገቢ ግዥ ፋይናንስ የስራ ሂደት 55% አገልግሎት ክፍያ ጥያቄ'

class DetailCostRequestCashier(DetailCostRequest):

    class Meta:
        proxy = True
        verbose_name_plural='ለንብረትና ገንዘብ ያዥ የስራ ሂደት 55% አገልግሎት ክፍያ ጥያቄ'

class WaterSupplyPerformed(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    Planned_tasks = models.ForeignKey(WaterSupplyPlan, on_delete=models.CASCADE)
    Dates = models.CharField(max_length=100)

    First_Quarter_performed = models.DecimalField(max_digits=30, decimal_places=2, default=0)
    Second_Quarter_performed = models.DecimalField(max_digits=30, decimal_places=2, default=0)
    Third_Quarter_performed = models.DecimalField(max_digits=30, decimal_places=2, default=0)
    Forth_Quarter_performed = models.DecimalField(max_digits=30, decimal_places=2, default=0)

    First_Quarter_performance = models.DecimalField(max_digits=30, decimal_places=2, default=0)
    Second_Quarter_performance = models.DecimalField(max_digits=30, decimal_places=2, default=0)
    Third_Quarter_performance = models.DecimalField(max_digits=30, decimal_places=2, default=0)
    Forth_Quarter_performance = models.DecimalField(max_digits=30, decimal_places=2, default=0)

    Total_year_performance = models.DecimalField(max_digits=50, decimal_places=2, default=0)

    Registered_at = models.DateTimeField(auto_now=True, verbose_name="Registered at")
    Updated_by = CurrentUserField(related_name="up_by7")
    Registered_by = CurrentUserField(related_name="pl_by7")

    def __str__(self):
        return "%s" % (self.id)
    class Meta:
        verbose_name="Water Supply Performed"
        verbose_name_plural="Water Supply Performed"

    def save(self, *args, **kwargs):
    	plan = WaterSupplyPlan.objects.get(id=self.Planned_tasks_id)
    	p1 = plan.First_Quarter_Plan
    	p2 = plan.Second_Quarter_Plan
    	p3 = plan.Third_Quarter_Plan
    	p4 = plan.Forth_Quarter_Plan

    	self.First_Quarter_performance = (self.First_Quarter_performed/p1)*100
    	self.Second_Quarter_performance = (self.Second_Quarter_performed/p2)*100
    	self.Third_Quarter_performance = (self.Third_Quarter_performed/p3)*100
    	self.Forth_Quarter_performance = (self.Forth_Quarter_performed/p4)*100

    	self.Total_year_performance = ((self.First_Quarter_performed/p1)*100 + (self.Second_Quarter_performed/p2)*100 + (self.Third_Quarter_performed/p3)*100 + (self.Forth_Quarter_performed/p4)*100)/4
    	super(WaterSupplyPerformed, self).save(*args, **kwargs)

class FinanceIncomePerformed(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    Dates = models.CharField(max_length=100)
    Planned_tasks = models.ForeignKey(FinanceIncomePlan, on_delete=models.CASCADE)

    First_Quarter_performed = models.DecimalField(max_digits=30, decimal_places=2, default=0)
    Second_Quarter_performed = models.DecimalField(max_digits=30, decimal_places=2, default=0)
    Third_Quarter_performed = models.DecimalField(max_digits=30, decimal_places=2, default=0)
    Forth_Quarter_performed = models.DecimalField(max_digits=30, decimal_places=2, default=0)

    First_Quarter_performance = models.DecimalField(max_digits=30, decimal_places=2, default=0)
    Second_Quarter_performance = models.DecimalField(max_digits=30, decimal_places=2, default=0)
    Third_Quarter_performance = models.DecimalField(max_digits=30, decimal_places=2, default=0)
    Forth_Quarter_performance = models.DecimalField(max_digits=30, decimal_places=2, default=0)

    Total_year_performance = models.DecimalField(max_digits=50, decimal_places=2, default=0)

    Registered_at = models.DateTimeField(auto_now=True, verbose_name="Registered at")
    Updated_by = CurrentUserField(related_name="up_by8")
    Registered_by = CurrentUserField(related_name="pl_by8")

    def __str__(self):
        return "%s" % (self.id)
    class Meta:
        verbose_name="Finance Income Performed"
        verbose_name_plural="Finance Income Performed"

    def save(self, *args, **kwargs):
        plan = FinanceIncomePlan.objects.get(id=self.Planned_tasks_id)
        p1 = plan.First_Quarter_Plan
        p2 = plan.Second_Quarter_Plan
        p3 = plan.Third_Quarter_Plan
        p4 = plan.Forth_Quarter_Plan

        self.First_Quarter_performance = (self.First_Quarter_performed/p1)*100
        self.Second_Quarter_performance = (self.Second_Quarter_performed/p2)*100
        self.Third_Quarter_performance = (self.Third_Quarter_performed/p3)*100
        self.Forth_Quarter_performance = (self.Forth_Quarter_performed/p4)*100

        self.Total_year_performance = ((self.First_Quarter_performed/p1)*100 + (self.Second_Quarter_performed/p2)*100 + (self.Third_Quarter_performed/p3)*100 + (self.Forth_Quarter_performed/p4)*100)/4

        super(FinanceIncomePerformed, self).save(*args, **kwargs)

class FinanceCostPerformed(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    Dates = models.CharField(max_length=100)
    Planned_tasks = models.ForeignKey(FinanceCostPlan, on_delete=models.CASCADE)

    First_Quarter_performed = models.DecimalField(max_digits=30, decimal_places=2, default=0)
    Second_Quarter_performed = models.DecimalField(max_digits=30, decimal_places=2, default=0)
    Third_Quarter_performed = models.DecimalField(max_digits=30, decimal_places=2, default=0)
    Forth_Quarter_performed = models.DecimalField(max_digits=30, decimal_places=2, default=0)

    First_Quarter_performance = models.DecimalField(max_digits=30, decimal_places=2, default=0)
    Second_Quarter_performance = models.DecimalField(max_digits=30, decimal_places=2, default=0)
    Third_Quarter_performance = models.DecimalField(max_digits=30, decimal_places=2, default=0)
    Forth_Quarter_performance = models.DecimalField(max_digits=30, decimal_places=2, default=0)

    Total_year_performance = models.DecimalField(max_digits=50, decimal_places=2, default=0)

    Registered_at = models.DateTimeField(auto_now=True, verbose_name="Registered at")
    Updated_by = CurrentUserField(related_name="up_by9")
    Registered_by = CurrentUserField(related_name="pl_by9")

    def __str__(self):
        return "%s" % (self.id)
    class Meta:
        verbose_name="Finance Cost Performed"
        verbose_name_plural="Finance Cost Performed"

    def save(self, *args, **kwargs):
    	plan = FinanceCostPlan.objects.get(id=self.Planned_tasks_id)
    	p1 = plan.First_Quarter_Plan
    	p2 = plan.Second_Quarter_Plan
    	p3 = plan.Third_Quarter_Plan
    	p4 = plan.Forth_Quarter_Plan

    	self.First_Quarter_performance = (self.First_Quarter_performed/p1)*100
    	self.Second_Quarter_performance = (self.Second_Quarter_performed/p2)*100
    	self.Third_Quarter_performance = (self.Third_Quarter_performed/p3)*100
    	self.Forth_Quarter_performance = (self.Forth_Quarter_performed/p4)*100

    	self.Total_year_performance = ((self.First_Quarter_performed/p1)*100 + (self.Second_Quarter_performed/p2)*100 + (self.Third_Quarter_performed/p3)*100 + (self.Forth_Quarter_performed/p4)*100)/4
    	super(FinanceCostPerformed, self).save(*args, **kwargs)

class HumanResourcePerformed(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    Dates = models.CharField(max_length=100)
    Planned_tasks = models.ForeignKey(HumanResourcePlan, on_delete=models.CASCADE)

    First_Quarter_performed = models.DecimalField(max_digits=30, decimal_places=2, default=0)
    Second_Quarter_performed = models.DecimalField(max_digits=30, decimal_places=2, default=0)
    Third_Quarter_performed = models.DecimalField(max_digits=30, decimal_places=2, default=0)
    Forth_Quarter_performed = models.DecimalField(max_digits=30, decimal_places=2, default=0)

    First_Quarter_performance = models.DecimalField(max_digits=30, decimal_places=2, default=0)
    Second_Quarter_performance = models.DecimalField(max_digits=30, decimal_places=2, default=0)
    Third_Quarter_performance = models.DecimalField(max_digits=30, decimal_places=2, default=0)
    Forth_Quarter_performance = models.DecimalField(max_digits=30, decimal_places=2, default=0)

    Total_year_performance = models.DecimalField(max_digits=50, decimal_places=2, default=0)

    Registered_at = models.DateTimeField(auto_now=True, verbose_name="Registered at")
    Updated_by = CurrentUserField(related_name="up_by10")
    Registered_by = CurrentUserField(related_name="pl_by10")

    def __str__(self):
        return "%s" % (self.id)
    class Meta:
        verbose_name="Human Resource Performed"
        verbose_name_plural="Human Resource Performed"

    def save(self, *args, **kwargs):
    	plan = HumanResourcePlan.objects.get(id=self.Planned_tasks_id)
    	p1 = plan.First_Quarter_Plan
    	p2 = plan.Second_Quarter_Plan
    	p3 = plan.Third_Quarter_Plan
    	p4 = plan.Forth_Quarter_Plan

    	self.First_Quarter_performance = (self.First_Quarter_performed/p1)*100
    	self.Second_Quarter_performance = (self.Second_Quarter_performed/p2)*100
    	self.Third_Quarter_performance = (self.Third_Quarter_performed/p3)*100
    	self.Forth_Quarter_performance = (self.Forth_Quarter_performed/p4)*100

    	self.Total_year_performance = ((self.First_Quarter_performed/p1)*100 + (self.Second_Quarter_performed/p2)*100 + (self.Third_Quarter_performed/p3)*100 + (self.Forth_Quarter_performed/p4)*100)/4
    	super(HumanResourcePerformed, self).save(*args, **kwargs)

class ComplainManagement(models.Model):
    THEME_CHOICES1 = (
		('1', 'First type'),
		('2', 'Second type'),
		('3', 'Third type'),
		('4', 'Forth type'),
	)
    THEME_CHOICES2 = (
		('1', 'First type'),
		('2', 'Second type'),
		('3', 'Third type'),
		('4', 'Forth type'),
	)
    THEME_CHOICES3 = (
		('1', 'First type'),
		('2', 'Second type'),
		('3', 'Third type'),
		('4', 'Forth type'),
	)
    id = models.AutoField(primary_key = True, unique = True)
    Category = models.CharField(max_length = 150, choices = THEME_CHOICES1)
    Sub_category = models.CharField(max_length = 150, choices = THEME_CHOICES2)
    Complain_type = models.CharField(max_length = 150, choices = THEME_CHOICES3)
    Nature_of_complaint = models.CharField(max_length = 150)
    Complain_details = models.TextField(max_length = 250)
    Complain_related = models.FileField(upload_to='documents/%Y/%m/%d', max_length=254)
    Complained_at = models.DateTimeField(auto_now=True, verbose_name="Registered at")
    Updated_by = CurrentUserField(related_name="up_by111")
    Registered_by = CurrentUserField(related_name="pl_by111")

    def __str__(self):
        return "%s" % (self.id)
    class Meta:
        verbose_name="Complain management system"
        verbose_name_plural="Complain management systems"
class GeneralReportTotalBalance(models.Model):
    Date = models.DateField('Date')
    Total_deposite = models.DecimalField(decimal_places=2, max_digits=250)
    Total_withdrawal = models.DecimalField(decimal_places=2, max_digits=250)
    Total_balance = models.DecimalField(decimal_places=2, max_digits=250)
    
    class Meta:
        managed = False
        db_table = "GeneralReportTotalBalance"

class GeneralLeisure(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    Dates = models.DateField('Date')
    Tasks = models.CharField(max_length = 150)
    General = models.PositiveIntegerField(default=0)
    Check_no = models.PositiveIntegerField(default=0)
    Check_payable = models.PositiveIntegerField(default=0)
    Receipt_no = models.CharField(max_length = 250,default=0)
    Deposit = models.DecimalField(decimal_places=2, max_digits=250, default=0)
    Withdraw = models.DecimalField(decimal_places=2, max_digits=250, default=0)
    Balance = models.DecimalField(decimal_places=2, max_digits=250, default=0)
    Registered_date = models.CharField(max_length=150,verbose_name="Registered at")
    Updated_by = CurrentUserField(related_name="up_by1111")
    Registered_by = CurrentUserField(related_name="pl_by1111")
    def __str__(self):
        return "%s" % (self.id)
    class Meta:
        verbose_name="General leisure management"
        verbose_name_plural="General leisure management"

    def save(self, *args, **kwargs):
    	br = GeneralReportTotalBalance.objects.get()
    	getbal = br.Total_balance
    	if getbal == None:
    		getbal=0
    	self.Balance = getbal + self.Deposit - self.Withdraw
    	super(GeneralLeisure, self).save(*args, **kwargs)

class GeneralReportBalanceDate(models.Model):
    Id = models.AutoField(primary_key=True)
    Date = models.DateField('Date')
    Total_deposite = models.DecimalField(decimal_places=2, max_digits=250)
    Total_withdrawal = models.DecimalField(decimal_places=2, max_digits=250)
    Total_balance = models.DecimalField(decimal_places=2, max_digits=250)
    
    class Meta:
        managed = False
        db_table = "GeneralReportBalanceDate"	

class RevenueType(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    Dates = models.DateField('Date')
    Code = models.CharField(max_length = 150)
    Revenue_title_amharic = models.CharField(max_length = 150)
    Revenue_title_english = models.CharField(max_length = 150)
    Registered_date = models.CharField(max_length=150,verbose_name="Registered at")
    Updated_by = CurrentUserField(related_name="up_by11111")
    Registered_by = CurrentUserField(related_name="pl_by11111")

    def __str__(self):
        return "%s" % (self.Code)

    class Meta:
        verbose_name="Revenue type management"
        verbose_name_plural="Revenue type management"

class ExpenseType(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    Dates = models.DateField('Date')
    Code = models.CharField(max_length = 150)
    Expense_title_amharic = models.CharField(max_length = 150)
    Expense_title_english = models.CharField(max_length = 150)
    Registered_date = models.CharField(max_length=150,verbose_name="Registered at")
    Updated_by = CurrentUserField(related_name="up_by1111111")
    Registered_by = CurrentUserField(related_name="pl_by1111111")

    def __str__(self):
        return "%s" % (self.Code)

    class Meta:
        verbose_name="Expense type management"
        verbose_name_plural="Expense type management"

class RevenueReport(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    Dates = models.DateField('Date')
    Code_id = models.CharField(max_length = 150)
    Code = models.CharField(max_length = 150)
    Balances = models.DecimalField(decimal_places=2, max_digits=250, default=0)

    def __str__(self):
        return "%s" % (self.id)

    class Meta:
        verbose_name="All Revenue Report"
        verbose_name_plural="All Revenue Report" 
    class Meta:
        managed = False
        db_table = "RevenueReport"

class RevenueReportDate(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    Dates = models.DateField('Date')
    Code_id = models.CharField(max_length = 150)
    Code = models.CharField(max_length = 150)
    Balances = models.DecimalField(decimal_places=2, max_digits=250, default=0)

    def __str__(self):
        return "%s" % (self.id)

    class Meta:
        verbose_name="Revenue Report Date"
        verbose_name_plural="Revenue Report Date" 
    class Meta:
        managed = False
        db_table = "RevenueReportDate"

class ExpenseReport(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    Dates = models.DateField('Date')
    Code_id = models.CharField(max_length = 150)
    Code = models.CharField(max_length = 150)
    Balances = models.DecimalField(decimal_places=2, max_digits=250, default=0)

    def __str__(self):
        return "%s" % (self.id)

    class Meta:
        verbose_name="All Expense Report"
        verbose_name_plural="All Expense Report" 
    class Meta:
        managed = False
        db_table = "ExpenseReport"

class ExpenseReportDate(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    Dates = models.DateField('Date')
    Code_id = models.CharField(max_length = 150)
    Code = models.CharField(max_length = 150)
    Balances = models.DecimalField(decimal_places=2, max_digits=250, default=0)

    def __str__(self):
        return "%s" % (self.id)

    class Meta:
        verbose_name="Expense Report Date"
        verbose_name_plural="Expense Report Date" 
    class Meta:
        managed = False
        db_table = "ExpenseReportDate"

class AllRevenue(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    Dates = models.DateField('Date')
    Code = models.ForeignKey(RevenueType, on_delete=models.CASCADE)
    Amount = models.DecimalField(decimal_places=2, max_digits=250, default=0)
    Balance = models.DecimalField(decimal_places=2, max_digits=250, default=0)
    Registered_date = models.CharField(max_length=150,verbose_name="Registered at")
    Updated_by = CurrentUserField(related_name="up_by111111")
    Registered_by = CurrentUserField(related_name="pl_by111111")

    def __str__(self):
        return "%s" % (self.id)

    class Meta:
        verbose_name="All Revenue management"
        verbose_name_plural="All Revenue management"

    def save(self, *args, **kwargs):
    	br = RevenueReport.objects.get(id=self.Code_id)
    	getbal = br.Balances
    	if getbal == None:
    		getbal=0
    	self.Balance = getbal + self.Amount
    	super(AllRevenue, self).save(*args, **kwargs)

class AllExpense(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    Dates = models.DateField('Date')
    Code = models.ForeignKey(ExpenseType, on_delete=models.CASCADE)
    Amount = models.DecimalField(decimal_places=2, max_digits=250, default=0)
    Balance = models.DecimalField(decimal_places=2, max_digits=250, default=0)
    Registered_date = models.CharField(max_length=150, verbose_name="Registered at")
    Updated_by = CurrentUserField(related_name="up_by11111111")
    Registered_by = CurrentUserField(related_name="pl_by11111111")

    def __str__(self):
        return "%s" % (self.id)

    class Meta:
        verbose_name="All Expense management"
        verbose_name_plural="All Expense management" 

    def save(self, *args, **kwargs):
    	br = ExpenseReport.objects.get(id=self.Code_id)
    	getbal = br.Balances
    	if getbal == None:
    		getbal=0
    	self.Balance = getbal + self.Amount
    	super(AllExpense, self).save(*args, **kwargs)



