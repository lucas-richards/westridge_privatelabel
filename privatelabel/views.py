import acumatica.AliveDataTools_v105 as AliveDataTools
import xml.etree.ElementTree as ET
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
import os
from django.core.mail import send_mail
from datetime import date

email_user = os.environ.get('EMAIL_USER')
email_password = os.environ.get('EMAIL_PASS')
author_email = 'lrichards@westridgelabs.com'
recipients = ['lrichards@westridgelabs.com' ]


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
            'expected_ship_date': order.expected_ship_date.strftime('%m-%d-%Y') if order.expected_ship_date else '',
            'scheduled_date': order.scheduled_date.strftime('%m-%d-%Y') if order.scheduled_date else '',
            'progress': f"{progress}%",
            'next_step': next_step,
            'days_left': days_left,
            'deposit_stat': order.deposit_stat,
            'ingredients_stat': order.ingredients_stat,
            'spec_stat': order.spec_stat,
            'package_stat': order.package_stat,
            'cap_stat': order.cap_stat,
            'label_stat': order.label_stat,
            'box_stat': order.box_stat,
            'customer_po': 'In File' if order.customer_po else '',
            'official_quote': 'In File' if order.official_quote else '',
            'quality_agreement': 'In File' if order.quality_agreement else '',
            'terms_and_conditions': 'In File' if order.terms_and_conditions else '',
        })

    context = {
        'title': 'Orders',
        'orders': orders,
        'rowData': json.dumps(rowData),
        'orders_count': orders.count(),
    }

    return render(request, 'privatelabel/orders.html', context)

def orders_accounting(request):
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
            'expected_ship_date': order.expected_ship_date.strftime('%m-%d-%Y') if order.expected_ship_date else '',
            'scheduled_date': order.scheduled_date.strftime('%m-%d-%Y') if order.scheduled_date else '',
            'progress': f"{progress}%",
            'next_step': next_step,
            'days_left': days_left,
            'deposit_stat': order.deposit_stat,
            'ingredients_stat': order.ingredients_stat,
            'spec_stat': order.spec_stat,
            'package_stat': order.package_stat,
            'cap_stat': order.cap_stat,
            'label_stat': order.label_stat,
            'box_stat': order.box_stat,
            'deposit_amount': order.deposit_amount,
            'deposit_date': order.deposit_date.strftime('%m-%d-%Y') if order.deposit_date else '',
            'deposit_notes': order.deposit_notes,
        })

    context = {
        'title': 'Accounting',
        'orders': orders,
        'rowData': json.dumps(rowData),
        'orders_count': orders.count(),
    }

    return render(request, 'privatelabel/orders_accounting.html', context)

def orders_gregg(request):
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
            'expected_ship_date': order.expected_ship_date.strftime('%m-%d-%Y') if order.expected_ship_date else '',
            'scheduled_date': order.scheduled_date.strftime('%m-%d-%Y') if order.scheduled_date else '',
            'progress': f"{progress}%",
            'next_step': next_step,
            'days_left': days_left,
            'deposit_stat': order.deposit_stat,
            'ingredients_stat': order.ingredients_stat,
            'spec_stat': order.spec_stat,
            'package_stat': order.package_stat,
            'cap_stat': order.cap_stat,
            'label_stat': order.label_stat,
            'box_stat': order.box_stat,
            'deposit_amount': order.deposit_amount,
            'deposit_date': order.deposit_date.strftime('%m-%d-%Y') if order.deposit_date else '',
            'deposit_notes': order.deposit_notes,
        })

    context = {
        'title': 'Gregg',
        'orders': orders,
        'rowData': json.dumps(rowData),
        'orders_count': orders.count(),
    }

    return render(request, 'privatelabel/orders_gregg.html', context)

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
            if field in ['due_date', 'desired_date', 'scheduled_date', 'date_received','expected_ship_date','last_component_eta','deposit_date']:
                # identify the date format
                print('new_value1:', new_value)
                new_value = timezone.datetime.strptime(new_value, '%Y-%m-%dT%H:%M:%S.%fZ').date()
                print('new_value:', new_value)

            if field and hasattr(order, field):
                setattr(order, field, new_value)
                order.save()

            # send email to admin
            send_mail(f'Order {order.number} was updated', '', email_user, recipients, html_message=f'Field {field} was updated', auth_user=email_user, auth_password=email_password)

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
        orderForm = OrderForm(request.POST, request.FILES, instance=order)
        if orderForm.is_valid():
            orderForm.save()
            messages.success(request, 'Order updated successfully')
            send_mail(f'Order #{order.number} was updated', '', email_user, recipients, html_message=f'Order #{order.number} was updated', auth_user=email_user, auth_password=email_password)
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
    send_mail(f'Order {order.number} was deleted', '', email_user, recipients, html_message=f'Order #{order.number} was updated', auth_user=email_user, auth_password=email_password)

    return redirect('privatelabel-orders')

def backorders(request):
    # Fetch all orders with status 'Back Order' using odataquery
    
    results = getAcumatica_data(
                gi='Back order board V2', 
                # filter qtySOBackOrdered > 0
                top=0,
                debug=True,
                )
    # Filter results where 'Back Ordered (POs-available)' is greater than zero
    results = [item for item in results if float(item.get('BackOrderedPOsavailable', 0)) > 0]
    # Round the 'BackOrderedPOsavailable' value for all items without decimals
    for item in results:
        if 'BackOrderedPOsavailable' in item:
            item['BackOrderedPOsavailable'] = round(float(item['BackOrderedPOsavailable']))
    total_items = len(results)
    source_purchasing_count = sum(1 for item in results if item.get('Source') == 'Purchase')
    source_kit_assembly_count = sum(1 for item in results if item.get('Source') == 'Kit Assembly')
    total_backordered_pos_available = sum(float(item.get('Back Ordered (POs-available)', 0)) for item in results)

    # Calculate days since 10/14/2024
    start_date = date(2024, 10, 14)
    today = date.today()
    days_without_incidents = (today - start_date).days

    # Sort by 'Back Ordered (POs-available)' in descending order and get the top 5
    top_five_backordered = sorted(
        results, 
        key=lambda x: float(x.get('BackOrderedPOsavailable', 0)), 
        reverse=True
    )[:10]
    print('top_five_backordered:', top_five_backordered)
    print('total_items:', total_items)
    print('source_purchasing_count:', source_purchasing_count)
    print('source_kit_assembly_count:', source_kit_assembly_count)

    context = {
        'total_items': total_items,
        'source_purchasing_count': source_purchasing_count,
        'source_kit_assembly_count': source_kit_assembly_count,
        'total_backordered_pos_available': total_backordered_pos_available,
        'top_five_backordered': top_five_backordered,
        'days_without_incidents': days_without_incidents,
    }
    return render(request, 'privatelabel/backorders.html', context)
# A1006_Attributes,replenishmentSource,inventoryCD_description,A1011_Attributes,Back Ordered (POs-available),itemType,qtySOBackOrdered

# Input Variables:
    #   gi: The Acumatica generic inquiry where the data of interest exists. 
    #   fields: list of fields to return, odata format i.e. 'TaxID,Description,TaxSchedule'. Uses the odata select parameter.
    #   filter: return records filter parameter, odata format i.e. "startswith(Customer,'LC')"
    #   top: limit the number of records to return. If 0, top is ignored. Default is 0.
    #   html: raw html that bypasses all other variable to send in the request. 

def getAcumatica_data(gi='', fields='', filter='', top=0, html='', debug='maybe',):
    # Fetch all orders with status 'Back Order' using odataquery
    xml_content = AliveDataTools.OdataQuery(
        gi  = gi,
        fields = fields,
        filter = filter,
        top    = top,
        html   = html,
    )
    
    # Define namespaces used in the XML
    namespaces = {
        'atom': 'http://www.w3.org/2005/Atom',
        'd': 'http://schemas.microsoft.com/ado/2007/08/dataservices',
        'm': 'http://schemas.microsoft.com/ado/2007/08/dataservices/metadata',
    }

    # Parse the XML
    root = ET.fromstring(xml_content.text)

    # Extract all entries
    entries = root.findall('atom:entry', namespaces)

    # Convert each entry's properties into a dictionary
    results = []
    for entry in entries:
        props = entry.find('.//m:properties', namespaces)
        entry_dict = {}
        if props is not None:
            for elem in props:
                tag = elem.tag.split('}')[-1]  # strip namespace
                entry_dict[tag] = elem.text
        results.append(entry_dict)

    # Now 'results' is a list of dictionaries
   
    return results