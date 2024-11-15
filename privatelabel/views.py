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
    
    orders = Order.objects.all().prefetch_related('notes').order_by('due_date')


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
        print('request.post',request.FILES)
        order.number = request.POST.get('order.number') if request.POST.get('order.number') else order.number
        order.qty = request.POST.get('order.qty') if request.POST.get('order.qty') else order.qty
        order.product.name = request.POST.get('order.product.name') if request.POST.get('order.product.name') else order.product.name
        order.due_date = request.POST.get('order.due_date') if request.POST.get('order.due_date') else None
        order.last_component_eta = request.POST.get('order.last_component_eta') if request.POST.get('order.last_component_eta') else None
        order.date_received = request.POST.get('order.date_received') if request.POST.get('order.date_received') else None
        order.expected_ship_date = request.POST.get('order.expected_ship_date') if request.POST.get('order.expected_ship_date') else None
        order.scheduled_date = request.POST.get('order.scheduled_date') if request.POST.get('order.scheduled_date') else None
        order.deposit_stat = 'order.deposit_stat' in request.POST
        order.ingredients_stat = 'order.ingredients_stat' in request.POST
        order.spec_stat = 'order.spec_stat' in request.POST
        order.package_stat = 'order.package_stat' in request.POST
        order.cap_stat = 'order.cap_stat' in request.POST
        order.label_stat = 'order.label_stat' in request.POST
        order.box_stat = 'order.box_stat' in request.POST
        order.status  = request.POST.get('order.status') if request.POST.get('order.status') else order.status
        first_name = request.POST.get('order.take_action_user')
        if first_name:
            try:
                user = User.objects.get(first_name=first_name)
                order.take_action_user = user
            except User.DoesNotExist:
                order.take_action_user = None

        # Attachments
        if 'order.customer_po' in request.FILES:
            order.customer_po = request.FILES['order.customer_po']
        if 'order.quality_agreement' in request.FILES:
            order.quality_agreement = request.FILES['order.quality_agreement']
        if 'order.terms_and_conditions' in request.FILES:
            order.terms_and_conditions = request.FILES['order.terms_and_conditions']
        if 'order.official_quote' in request.FILES:
            order.official_quote = request.FILES['order.official_quote']
        print('order:', order.__dict__)
        print('order.product:', order.product.__dict__)
        order.last_updated = timezone.now()  # Update the last_updated field
        
        order.save()  # Save the updated order
        order.product.save()  # Save the updated product
        
        # Redirect or render after saving
        return redirect('privatelabel-orders')

    context = {
        'title':'Order',
        'order':order,
        'orderForm':orderForm,
        'orderAttachmentsForm':orderAttachmentsForm,
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