from django import forms
from .models import Customer, Product, Order



class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['sku', 'spec_version', 'name', 'customer', 'package', 'cap', 'label', 'lube', 'size']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'product','qty', 'due_date', 'date_received', 'deposit_stat', 'ingredients_stat', 'spec_stat', 'package_stat', 'cap_stat', 'label_stat', 'box_stat', 'customer_po', 'official_quote', 'quality_agreement','terms_and_conditions']
        widgets = {
            'due_date': forms.DateInput(attrs={'type':'date'}),
            'date_received': forms.DateInput(attrs={'type':'date'}),
        }

class OrderAttachments(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_po', 'official_quote', 'quality_agreement', 'terms_and_conditions']
        widgets = {
            'due_date': forms.DateInput(attrs={'type':'date'}),
            'date_received': forms.DateInput(attrs={'type':'date'}),
        }

