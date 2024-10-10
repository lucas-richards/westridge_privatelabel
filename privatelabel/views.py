from django.shortcuts import render
from .models import Customer, Order, Product
from .forms import OrderForm, CustomerForm, ProductForm
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone

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

def customer(request, pk):
    customer = get_object_or_404(Customer, id=pk)
    productForm = ProductForm()

    
    context = {
        'title':'Customer',
        'customer':customer,
        'form':productForm,
    }

    return render(request, 'privatelabel/customer.html', context)

def new_customer(request):
    customerForm = CustomerForm()
    
    if request.method == 'POST':
        customerForm = CustomerForm(request.POST)
        if customerForm.is_valid():
            customerForm.save()
            return redirect('privatelabel-customers')
        
    context = {
        'title':'New Customer',
        'form':customerForm,
    }

    return render(request, 'privatelabel/new_customer.html', context)

def orders(request):
    
    orders = Order.objects.all().order_by('due_date')
    # make the percentage progress of each order
    for order in orders:
        total_steps = 7
        completed_steps = sum([
            order.deposit_stat,
            order.ingredients_stat,
            order.spec_stat,
            order.package_stat,
            order.cap_stat,
            order.label_stat,
            order.box_stat
        ])
        order.progress = round((completed_steps / total_steps) * 100)
        order.progress = order.progress
        order.save()
        
    context = {
        'title':'Orders',
        'orders':orders,
    }

    return render(request, 'privatelabel/orders.html', context)

def order(request, pk):
    order = get_object_or_404(Order, id=pk)
    
    if request.method == 'POST':
        # Updating the order's status fields based on form data
        order.deposit_stat = 'order.deposit_stat' in request.POST
        order.ingredients_stat = 'order.ingredients_stat' in request.POST
        order.spec_stat = 'order.spec_stat' in request.POST
        order.package_stat = 'order.package_stat' in request.POST
        order.cap_stat = 'order.cap_stat' in request.POST
        order.label_stat = 'order.label_stat' in request.POST
        order.box_stat = 'order.box_stat' in request.POST
        coordinator_notes = request.POST.get('order.coordinator_notes')
        planning_notes = request.POST.get('order.planning_notes')
        if coordinator_notes is not None:
            order.coordinator_notes = coordinator_notes
        if planning_notes is not None:
            order.planning_notes = planning_notes
        
        order.last_updated = timezone.now()  # Update the last_updated field
        
        order.save()  # Save the updated order
        
        # Redirect or render after saving
        return redirect('privatelabel-orders')

    context = {
        'title':'Order',
        'order':order,
        'orderForm':orderForm,
    }

    return redirect('privatelabel-orders')
            
def new_order(request):   
    orderForm = OrderForm()
    
    if request.method == 'POST':
        orderForm = OrderForm(request.POST)
        if orderForm.is_valid():
            orderForm.save()
            return redirect('privatelabel-orders')
        
    context = {
        'title':'New Order',
        'form':orderForm,
    }

    return render(request, 'privatelabel/new_order.html', context)

def new_product(request, pk):
    customer = get_object_or_404(Customer, id=pk)
    productForm = ProductForm()

    if request.method == 'POST':
        productForm = ProductForm(request.POST)
        if productForm.is_valid():
            productForm.save()
            return redirect('privatelabel-customer', pk=pk)
        
    context = {
        'title':'New Product',
        'form':productForm,
        'customer':customer,
    }