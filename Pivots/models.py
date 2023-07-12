from django.test import TestCase
from django.db import models
from django.db.models import Count, Avg, Sum, Max, Min
# Create your tests here.



class Pivot(models.Model):
    pivot_id = models.SmallAutoField(db_column='PivotId', primary_key=True, editable=False)
    pivot_head = models.CharField(db_column='PivotHead', max_length=50)
    pivot_name = models.CharField(db_column='PivotName', max_length=50)
    pivot_location = models.CharField(db_column='PivotLocation', max_length=50)
    pivot_phone = models.CharField(db_column='PivotPhone', max_length=50)
    pivot_email = models.CharField(db_column='PivotEmail', max_length=50)

    def __str__(self) -> str:
        return str(self.pivot_id)

    class Meta:
        db_table = 'Pivot'

class Farmer(models.Model):
    farmer_id = models.SmallAutoField(db_column='CustomerId', primary_key=True, editable=False)
    first_name = models.CharField(db_column='FirstName', max_length=30)
    last_name = models.CharField(db_column='LastName', max_length=30)
    phone_number = models.CharField(db_column='PhoneNumber', max_length=50)
    pivot_id = models.ForeignKey(Pivot, db_column='PivotId', on_delete=models.CASCADE)
    land_size = models.IntegerField(db_column='LandSize', blank=True, null=True)
    ownership = models.CharField(db_column='Ownership', max_length=50, blank=True, null=True)
    land_owner = models.CharField(db_column='LandOwner', max_length=50, blank=True, null=True)
    land_owner_phone = models.CharField(db_column='LandOwnerPhone', max_length=50, blank=True, null=True)
    land_upi = models.CharField(db_column='LandUPI', max_length=50, blank=True, null=True)
    bank_name = models.CharField(db_column='BankName', max_length=50, blank=True, null=True)
    bank_account = models.CharField(db_column='BankAccount', max_length=50, blank=True, null=True)
    bank_account_name = models.CharField(db_column='BankAccountName', max_length=50, blank=True, null=True)
    harvest_balance = models.IntegerField(db_column='TotalHarvest', blank=True, null=True)
    input_balance = models.IntegerField(db_column="TotalInput", blank=True, null=True)

    def __str__(self) -> str:
        return str(self.full_name)
    
    @property
    def full_name(self):
        return self.first_name + " " + self.last_name
    
    @property
    def pivot_name_str(self):
        return str(self.pivot_id.pivot_id) + "-" + self.pivot_id.pivot_name

    class Meta:
        db_table = 'Farmers'

class Harvest(models.Model):
    harvest_id = models.SmallAutoField(db_column='HarvestId', primary_key=True, editable=False)
    farmer_id = models.ForeignKey(Farmer, db_column='FarmerId', on_delete=models.CASCADE)
    pivot_id = models.ForeignKey(Pivot, db_column='PivotId', on_delete=models.CASCADE)
    crop = models.CharField(db_column='Crop', max_length=50)
    quantity = models.IntegerField(db_column='Quantity')
    unit_price = models.IntegerField(db_column='UnitPrice') 
    total_value = models.IntegerField(db_column='TotalValue')
    date = models.DateField(db_column='Date')
    comments = models.CharField(db_column='Comments', max_length=100, blank=True, null=True)

    def __str__(self) -> str:
        return str(self.harvest_id) + " - " + str(self.farmer_id.full_name) + " - " + str(self.pivot_id.pivot_id) + " - " + str(self.crop)
    

    class Meta:
        db_table = 'Harvests'

class Input(models.Model):
    input_id = models.SmallAutoField(db_column='InputId', primary_key=True, editable=False)
    date = models.DateField(db_column='Date')
    pivot_id = models.ForeignKey(Pivot, db_column='PivotId', on_delete=models.CASCADE)
    farmer_id = models.ForeignKey(Farmer, db_column='CustomerId', on_delete=models.CASCADE)
    item = models.CharField(db_column='Item', max_length=50)
    description = models.CharField(db_column='Description', max_length=100)
    quantity = models.IntegerField(db_column='Quantity')
    unit_price = models.IntegerField(db_column='UnitPrice')
    total_value = models.IntegerField(db_column='TotalValue')
    payment_mode = models.CharField(db_column='PaymentMode', max_length=50)

    class Meta:
        db_table = 'Inputs'

