from django.shortcuts import render
from .models import Customer, Order, Product

# Create your views here.

def dashboard(request):

    context = {
        'title':'Dashboard',
    }

    return render(request, 'privatelabel/dashboard.html', context)

def customers(request):

    customers = Customer.objects.all()

    context = {
        'title':'Customers',
        'customers':customers,
    }

    return render(request, 'privatelabel/customers.html', context)

def orders(request):
    
        orders = Order.objects.all()
    
        context = {
            'title':'Orders',
            'orders':orders,
        }
    
        return render(request, 'privatelabel/orders.html', context)
    