from django import forms
from .models import Customer, Product, Order



class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'product', 'due_date', 'date_received', 'deposit_stat', 'ingredients_stat', 'spec_stat', 'package_stat', 'cap_stat', 'label_stat', 'box_stat']
        widgets = {
            'due_date': forms.DateInput(attrs={'type':'date'}),
            'date_received': forms.DateInput(attrs={'type':'date'}),
        }