from django.shortcuts import render
from .models import Customer, Order, Product, Note
from .forms import OrderForm, CustomerForm, ProductForm, OrderAttachments
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json
from django.db.models import Prefetch
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib import messages


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
    customerForm = CustomerForm(instance=customer)

    
    context = {
        'title':'Customer',
        'customer':customer,
        'formp':productForm,
        'formc':customerForm,
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
    orders = Order.objects.exclude(status__in=['Canceled', 'Completed']).prefetch_related('notes').order_by('desired_date', 'number', 'id')

    rowData = []
    total_steps = 7

    for order in orders:
        completed_steps = sum([
            order.deposit_stat,
            order.ingredients_stat,
            order.spec_stat,
            order.package_stat,
            order.cap_stat,
            order.label_stat,
            order.box_stat
        ])
        progress = round((completed_steps / total_steps) * 100)
        days_left = (order.due_date - timezone.now().date()).days if order.due_date else 'No due date'
        next_step = 'Ingredients' if not order.ingredients_stat else 'Package' if not order.package_stat else 'Cap' if not order.cap_stat else 'Label' if not order.label_stat else 'Box' if not order.box_stat else 'Completed'

        rowData.append({
            'id': order.id,
            'customer': order.customer if order.customer else '',
            'customerid': order.customerid,
            'product': order.product if order.product else '',
            'uom': order.uom,
            'qty': order.qty,
            'number': order.number,
            'status': order.status,
            'quantity': order.qty,
            'date_received': order.date_received.strftime('%m-%d-%Y') if order.date_received else '',
            'desired_date': order.desired_date.strftime('%m-%d-%Y') if order.desired_date else 'No desired date',
            'due_date': order.due_date.strftime('%m-%d-%Y') if order.due_date else order.desired_date.strftime('%m-%d-%Y') if order.desired_date else '',
            'scheduled': order.scheduled_date.strftime('%m-%d-%Y') if order.scheduled_date else '',
            'progress': f"{progress}%",
            'next_step': next_step,
            'days_till_due': days_left,
            'deposit_stat': order.deposit_stat,
            'ingredients_stat': order.ingredients_stat,
            'spec_stat': order.spec_stat,
            'package_stat': order.package_stat,
            'cap_stat': order.cap_stat,
            'label_stat': order.label_stat,
            'box_stat': order.box_stat,
        })

    context = {
        'title': 'Orders',
        'orders': orders,
        'rowData': json.dumps(rowData),
        'orders_count': orders.count(),
    }

    return render(request, 'privatelabel/orders.html', context)

def order(request, pk):
    order = get_object_or_404(Order, id=pk)

    orderForm = OrderForm(instance=order)
    
    if request.method == 'POST':
        try:
            # Updating the order's status fields based on form data
            data = json.loads(request.body.decode("utf-8"))
            field = data.get('field')
            new_value = data.get('newValue')

            # Convert date fields to date objects
            if field in ['due_date', 'desired_date', 'scheduled_date', 'date_received']:
                # identify the date format
                print('new_value1:', new_value)
                new_value = timezone.datetime.strptime(new_value, '%Y-%m-%dT%H:%M:%S.%fZ').date()
                print('new_value:', new_value)

            if field and hasattr(order, field):
                setattr(order, field, new_value)
                order.save()
            
            return JsonResponse({"message": "Order updated successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    context = {
        'title':'Order',
        'order':order,
        'form':orderForm
    }

    return render(request, 'privatelabel/order.html', context)

def order_attachments(request, pk):
    order = get_object_or_404(Order, id=pk)
    orderForm = OrderForm(instance=order)
    
    if request.method == 'POST':
        orderForm = OrderForm(request.POST, instance=order)
        if orderForm.is_valid():
            orderForm.save()
            messages.success(request, 'Order updated successfully')
            return redirect('privatelabel-orders')
        
    context = {
        'title':'Update Order',
        'form':orderForm,
    }

    return render(request, 'privatelabel/order.html', context)
            
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
        # Get the customer object or return a 404 if not found
    customer = get_object_or_404(Customer, id=pk)
    formp = ProductForm()
    formc = CustomerForm(instance=customer)
    # Initialize the forms
    if request.method == "POST":
        print('request.post:', request.POST)
        formc = CustomerForm(request.POST, instance=customer)
        if formc.is_valid():
            formc.save()
            messages.success(request, 'Customer updated successfully')
            return redirect('privatelabel-customer', pk=customer.id)
        formp = ProductForm(request.POST)
        if formp.is_valid():
            # Save the new product and associate it with the customer
            product = formp.save(commit=False)
            product.customer = customer
            product.save()
            messages.success(request, 'Product added successfully')
            return redirect('privatelabel-customer', pk=customer.id)
    else:
        # Initialize forms for GET requests
        formc = CustomerForm(instance=customer)
        formp = ProductForm()
    
    # Pass data to the template
    context = {
        'customer': customer,
        'formc': formc,
        'formp': formp,
    }
    return redirect('privatelabel-customer', pk=customer.id)
        

@require_POST
def add_note(request, pk):
    try:
        # Get the order
        order = Order.objects.get(id=pk)
        print('request.body:', request.body)

        # Get the note content from the request
        data = json.loads(request.body.decode("utf-8"))
        content = data.get('content', '')

        # Create the new note
        new_note = Note.objects.create(order=order, content=content)

        # Return success response with the new note details
        return JsonResponse({
            'success': True,
            'note': {
                'content': new_note.content
            }
        })

    except Order.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Order not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

def delete_order(request, pk):
    order = get_object_or_404(Order, id=pk)
    order.delete()
    messages.success(request, 'Order deleted successfully')
    return redirect('privatelabel-orders')