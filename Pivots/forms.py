from django import forms
from django.utils import timezone

from .models import *
import datetime


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control', 'id':'username', 'placeholder':'Username'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'id':'password', 'placeholder':'Password'}))
    
class FarmerForm(forms.Form):
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'class': 'form-control', 'id':'first_name', 'placeholder':'First Name'}))
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'class': 'form-control', 'id':'last_name', 'placeholder':'Last Name'}))
    phone_number = forms.CharField(label='Phone Number', widget=forms.TextInput(attrs={'class': 'form-control', 'id':'phone_number', 'placeholder':'Phone Number'}))
    land_size = forms.IntegerField(label='Land Size (Acres)', widget=forms.NumberInput(attrs={'class': 'form-control', 'id':'land_size', 'placeholder':'Land Size'}))
    ownership = forms.CharField(label='Ownership', widget=forms.TextInput(attrs={'class': 'form-control', 'id':'ownership', 'placeholder':'Ownership'}))
    land_owner = forms.CharField(label='Land Owner', widget=forms.TextInput(attrs={'class': 'form-control', 'id':'land_owner', 'placeholder':'Land Owner'}))
    land_owner_phone = forms.CharField(label='Land Owner Phone', widget=forms.TextInput(attrs={'class': 'form-control', 'id':'land_owner_phone', 'placeholder':'Land Owner Phone'}))
    land_upi = forms.CharField(label='Land UPI', widget=forms.TextInput(attrs={'class': 'form-control', 'id':'land_upi', 'placeholder':'Land UPI'}))
    bank_name = forms.CharField(label='Bank Name', widget=forms.TextInput(attrs={'class': 'form-control', 'id':'bank_name', 'placeholder':'Bank Name'}))
    bank_account = forms.CharField(label='Bank Account', widget=forms.TextInput(attrs={'class': 'form-control', 'id':'bank_account', 'placeholder':'Bank Account'}))
    bank_account_name = forms.CharField(label='Bank Account Name', widget=forms.TextInput(attrs={'class': 'form-control', 'id':'bank_account_name', 'placeholder':'Bank Account Name'}))

    def save(self, pivot_id : int):
        farmer = Farmer()
        farmer.pivot_id = Pivot.objects.filter(pivot_id=pivot_id).first()
        farmer.first_name = self.cleaned_data['first_name']
        farmer.last_name = self.cleaned_data['last_name']
        farmer.phone_number = self.cleaned_data['phone_number']
        farmer.land_size = self.cleaned_data['land_size']
        farmer.ownership = self.cleaned_data['ownership']
        farmer.land_owner = self.cleaned_data['land_owner']
        farmer.land_owner_phone = self.cleaned_data['land_owner_phone']
        farmer.land_upi = self.cleaned_data['land_upi']
        farmer.bank_name = self.cleaned_data['bank_name']
        farmer.bank_account = self.cleaned_data['bank_account']
        farmer.bank_account_name = self.cleaned_data['bank_account_name']
        farmer.harvest_balance = 0
        farmer.input_balance = 0
        farmer.save()

class HarvestForm(forms.Form):
    date = forms.DateField(label='Date',initial=datetime.date.today, widget=forms.DateInput(attrs={'class': 'form-control', 'id':'date', 'placeholder':'Date'}))
    crop_type = forms.CharField(label='Crop Type', widget=forms.TextInput(attrs={'class': 'form-control', 'id':'crop_type', 'placeholder':'Crop Type'}))
    quantity = forms.IntegerField(label='Quanitity (KGs)', widget=forms.NumberInput(attrs={'class': 'form-control', 'id':'quantity', 'placeholder':'0 Kgs'}))
    price = forms.IntegerField(label='Unit Price', widget=forms.TextInput(attrs={'class': 'form-control', 'id':'unit_price', 'placeholder':'Price'}))
    total_value = forms.IntegerField(label='Total Value', required=False,  widget=forms.TextInput(attrs={'class': 'form-control', 'id':'total_value', 'placeholder':'Total','disabled': True}))
    comment = forms.CharField(label='Comment', widget=forms.Textarea(attrs={'class': 'form-control', 'id':'comment', 'placeholder':'Comment'}))

    def save(self, farmer_id : int):
        harvest = Harvest()
        harvest.date = self.cleaned_data['date']
        harvest.farmer_id = Farmer.objects.filter(farmer_id=farmer_id).first()
        harvest.pivot_id = Farmer.objects.filter(pk=farmer_id).first().pivot_id
        harvest.crop = self.cleaned_data['crop_type']
        harvest.quantity = self.cleaned_data['quantity']
        harvest.unit_price = self.cleaned_data['price']
        harvest.total_value = self.cleaned_data['quantity'] * self.cleaned_data['price']
        harvest.comments = self.cleaned_data['comment']
        harvest.save()

        try:
            FarmerObj = Farmer.objects.get(farmer_id=farmer_id)
            FarmerObj.harvest_balance = FarmerObj.harvest_balance + (self.cleaned_data['price'] * self.cleaned_data['quantity'])
            FarmerObj.save()
        except TypeError:
            FarmerObj = Farmer.objects.get(farmer_id=farmer_id)
            FarmerObj.harvest_balance = (self.cleaned_data['price'] * self.cleaned_data['quantity'])
            FarmerObj.save()

class InputForm(forms.Form):
    PAYMENT_CHOICES = [
    ('Credit', 'Credit'),
    ('Cash Payment', 'Cash Payment'),]

    pivot_id = forms.CharField(label='Pivot ID',required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'id':'pivot_id', 'placeholder':'Pivot ID', 'disabled':True}))
    farmer_name = forms.CharField(label='Farmer Name', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'id':'farmer_name', 'placeholder':'Farmer Name', 'disabled':True}))
    date = forms.DateField(label='Date',initial=datetime.date.today, widget=forms.DateInput(attrs={'class': 'form-control', 'id':'date', 'placeholder':'Date'}))
    item = forms.CharField(label='Item', widget=forms.TextInput(attrs={'class': 'form-control', 'id':'item', 'placeholder':'Item'}))
    description = forms.CharField(label='Description', widget=forms.Textarea(attrs={'class': 'form-control', 'id':'description', 'placeholder':'Description'}))
    quantity = forms.IntegerField(label='Quantity', widget=forms.NumberInput(attrs={'class': 'form-control', 'id':'quantity', 'placeholder':'Quantity'}))
    unit_price = forms.IntegerField(label='Unit Price', widget=forms.NumberInput(attrs={'class': 'form-control', 'id':'unit_price', 'placeholder':'Unit Price'}))
    total_value = forms.IntegerField(label='Total Value', required=False,widget=forms.TextInput(attrs={'class': 'form-control', 'id':'total_value', 'placeholder':'Total', 'disabled': True}))
    payment_method = forms.ChoiceField(label='Payment Method',choices=PAYMENT_CHOICES,widget=forms.Select(attrs={'class': 'form-control', 'id': 'payment_method'}),)

    def save(self, farmer_id : int):
        input = Input()
        input.date = self.cleaned_data['date']
        input.farmer_id = Farmer.objects.filter(farmer_id=farmer_id).first()
        input.pivot_id = Farmer.objects.filter(farmer_id=farmer_id).first().pivot_id
        input.item = self.cleaned_data['item']
        input.description = self.cleaned_data['description']
        input.quantity = self.cleaned_data['quantity']
        input.unit_price = self.cleaned_data['unit_price']
        input.total_value = self.cleaned_data['unit_price'] * self.cleaned_data['quantity']
        input.payment_mode = self.cleaned_data['payment_method']
        input.save()

        #Update the Input Balance on the Farmer Model
        try:
            FarmerObj = Farmer.objects.get(farmer_id=farmer_id)
            FarmerObj.input_balance = FarmerObj.input_balance + (self.cleaned_data['unit_price'] * self.cleaned_data['quantity'])
            FarmerObj.save()
        except TypeError:
            FarmerObj = Farmer.objects.get(farmer_id=farmer_id)
            FarmerObj.input_balance = (self.cleaned_data['unit_price'] * self.cleaned_data['quantity'])
            FarmerObj.save()


