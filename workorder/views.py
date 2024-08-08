from django.shortcuts import render
from .models import Asset, Vendor, WorkOrder, Location, WorkOrderRecord
from users.models import Department
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect
import json
from .forms import AssetEditForm, WorkOrderEditForm, WorkOrderRecordForm, WorkOrderRecordEditForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import datetime
from users.models import User

# Create your views here.

def dashboard(request):
    # get the work orders records status and count
    work_orders_records = WorkOrderRecord.objects.all()
    work_orders_records_status = {
        'done': work_orders_records.filter(status='done').count(),
        'in_progress': work_orders_records.filter(status='in_progress').count(),
        'on_hold': work_orders_records.filter(status='on_hold').count(),
        'scheduled': work_orders_records.filter(status='scheduled').count(),
        'cancelled': work_orders_records.filter(status='cancelled').count(),
    }
    print(work_orders_records_status)


    context = {
        'title': 'Dashboard',
        'work_orders_records_status': work_orders_records_status,
        
    }
    return render(request, 'workorder/dashboard.html', context)

@csrf_exempt
@require_http_methods(["GET", "PUT"])
def asset(request, id):
    try:
        asset = Asset.objects.get(id=id)
        if request.method == "GET":
            data = {
                'code': asset.code,
                'name': asset.name,
                'status': asset.status,
                'description': asset.description,
                'image_url': asset.image.url if asset.image else '',
                'serial_number': asset.serial_number,
                'model': asset.model,
                'manufacturer': asset.manufacturer,
                'year': asset.year,
                'location': asset.location.name if asset.location else '',
                'parent': asset.parent.name if asset.parent else '',
                'department_in_charge': asset.department_in_charge.name if asset.department_in_charge else '',
                'vendors': asset.vendors.name if asset.vendors else '',
                'created_by': asset.created_by.username if asset.created_by else '',
                'created_on': asset.created_on.strftime('%Y-%m-%d %H:%M:%S'),
                'last_updated': asset.last_updated.strftime('%Y-%m-%d %H:%M:%S'),
                'criticality': asset.criticality,
                'attachments': asset.attachments.url if asset.attachments else '',
            }
            return JsonResponse(data)
    except Asset.DoesNotExist:
        return JsonResponse({'error': 'Asset not found'}, status=404)
    except (Location.DoesNotExist, Asset.DoesNotExist, Department.DoesNotExist, Vendor.DoesNotExist):
        return JsonResponse({'error': 'Related entity not found'}, status=404)

def assets(request):
    assets = Asset.objects.all().order_by('code')
    context = {
        'title': 'Assets',
        'assets': assets,
    }

    return render(request, 'workorder/assets.html', context)

@login_required
def add_asset(request):
    if request.method == 'POST':
        form = AssetEditForm(request.POST, request.FILES)
        # add created by
        form.instance.created_by = request.user
        if form.is_valid():
            form.save()
            return redirect('workorder-assets')
    else:
        form = AssetEditForm()
    context = {
        'title': 'Add Asset',
        'form': form,
    }
    return render(request, 'workorder/new_asset.html', context)

@login_required
def edit_asset(request, id):
    assets = Asset.objects.all().order_by('code')
    asset = Asset.objects.get(id=id)

    if request.method == 'POST':
        form = AssetEditForm(request.POST, request.FILES, instance=asset)
        if form.is_valid():
            form.save()
            return redirect('workorder-assets')
    else:
        form = AssetEditForm(instance=asset)
    context = {
        'title': 'Edit Asset',
        'asset': asset,
        'form': form,
    }
    return render(request, 'workorder/edit_asset.html', context) 

@login_required
def delete_asset(request, id):
    asset = Asset.objects.get(id=id)
    try:
        asset.delete()
        messages.success(request, 'Asset deleted successfully')
    except Exception as e:
        messages.error(request, 'Error deleting asset')
    return redirect('workorder-assets')

def asset_workorders_new(request, id):
    asset = Asset.objects.get(id=id)
    if request.method == 'POST':
        form = WorkOrderEditForm(request.POST, request.FILES)
        # add created by
        form.instance.asset = asset
        form.instance.created_by = request.user
        if form.is_valid():
            form.save()
            return redirect('workorder-workorders')
    else:
        form = WorkOrderEditForm()
        form.fields['asset'].initial = asset
    context = {
        'title': 'Add Work Order',
        'form': form,
    }
    return render(request, 'workorder/new_workorder.html', context)

@login_required
def vendors(request):
    vendors = Vendor.objects.all()
    context = {
        'title': 'Vendors',
        'vendors': vendors,
    }

    return render(request, 'workorder/vendors.html', context)

@login_required
def vendor(request, id):
    vendor = Vendor.objects.get(id=id)
    context = {
        'title': 'Vendor',
        'vendor': vendor,
    }

    return render(request, 'workorder/vendor.html', context)

@login_required
def add_vendor(request):
    if request.method == 'POST':
        pass
    context = {
        'title': 'Add Vendor',
    }

    return render(request, 'workorder/add_vendor.html', context)

@login_required
def edit_vendor(request, id):
    vendor = Vendor.objects.get(id=id)
    context = {
        'title': 'Edit Vendor',
        'vendor': vendor,
    }

    return render(request, 'workorder/edit_vendor.html', context)

@login_required
def delete_vendor(request, id):
    vendor = Vendor.objects.get(id=id)
    vendor.delete()
    return redirect('workorder-vendors')

def workorders(request):
    workorders = WorkOrder.objects.all()
    workorders_with_last_record = []
    form = WorkOrderEditForm()
    if request.method == 'POST':
        form = WorkOrderEditForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('workorder-workorders')
        else:
            print(form.errors)


    for workorder in workorders:
        last_record = workorder.workorderrecord_set.order_by('-created_on').first()
        workorders_with_last_record.append({
            'workorder': workorder,
            'last_record': last_record
        })
    
    context = {
        'title': 'Work Orders',
        'workorders': workorders_with_last_record,
        'form': form,
    }

    return render(request, 'workorder/workorders.html', context)

@login_required
@csrf_exempt
@require_http_methods(["GET", "PUT"])
def workorder(request, id):
    try:
        workorder = WorkOrder.objects.get(id=id)
        # workorder records
        records = WorkOrderRecord.objects.filter(workorder=workorder).order_by('-due_date')
        last_record = records.first()

        if request.method == "GET":
            data = {
                'title': workorder.title,
                'priority': workorder.priority,
                'description': workorder.description,
                'assigned_to': workorder.assigned_to.username if workorder.assigned_to else '',
                'department_assigned_to': workorder.department_assigned_to.name if workorder.department_assigned_to else '',
                'created_by': workorder.created_by.username if workorder.created_by else '',
                'created_on': workorder.created_on.strftime('%Y-%m-%d %H:%M:%S'),
                # time until the due date in days
                'last_updated': workorder.last_updated.strftime('%Y-%m-%d %H:%M:%S'),
                'recurrence': workorder.get_recurrence_display(),
                'asset': workorder.asset.name if workorder.asset else '',
                'image_url': workorder.image.url if workorder.image else '',
                'attachments': workorder.attachments.url if workorder.attachments else '',
                'time_until_due': (last_record.due_date - last_record.created_on).days if last_record.due_date else '',
                'records': [{'id': record.id, 'created_on': record.created_on.strftime('%Y-%m-%d'), 'status': record.status, 'due_date': record.due_date.strftime('%Y-%m-%d'), 'completed_on': record.completed_on.strftime('%Y-%m-%d') if record.completed_on else '', 'completed_by': record.completed_by.username if record.completed_by else '', 'time_to_complete': record.time_to_complete.total_seconds() if record.time_to_complete else '', 'attachments': record.attachments.url if record.attachments else '', 'comments': record.comments} for record in records],
                'last_record_status': last_record.status if last_record else '',
            }
            return JsonResponse(data)
    except WorkOrder.DoesNotExist:
        return JsonResponse({'error': 'workorder not found'}, status=404)
    except (Location.DoesNotExist, WorkOrder.DoesNotExist, Department.DoesNotExist, Vendor.DoesNotExist):
        return JsonResponse({'error': 'Related entity not found'}, status=404)

@login_required
def add_workorder(request):
    if request.method == 'POST':
        form = WorkOrderEditForm(request.POST, request.FILES)
        # add created by
        form.instance.created_by = request.user
        if form.is_valid():
            form.save()
            return redirect('workorder-workorders')
    else:
        form = WorkOrderEditForm()
    context = {
        'title': 'Add Work Order',
        'form': form,
    }
    return render(request, 'workorder/new_workorder.html', context)

@login_required
def edit_workorder(request, id):
    workorders = WorkOrder.objects.all().order_by('created_on')
    workorder = WorkOrder.objects.get(id=id)

    if request.method == 'POST':
        form = WorkOrderEditForm(request.POST, request.FILES, instance=workorder)
        if form.is_valid():
            form.save()
            return redirect('workorder-workorders')
    else:
        form = WorkOrderEditForm(instance=workorder)
    context = {
        'title': 'Edit workorder',
        'workorder': workorder,
        'form': form,
    }
    return render(request, 'workorder/edit_workorder.html', context) 

@login_required
def delete_workorder(request, id):
    workorder = WorkOrder.objects.get(id=id)
    workorder.delete()
    return redirect('workorder-workorders')

@login_required
def workorder_records(request):
    records = WorkOrderRecord.objects.all().order_by('-due_date')
    # add this to each record 'time_until_due': (record.due_date - timezone.now() ).days if record.due_date else '',
    for record in records:
        record.time_until_due = (record.due_date - timezone.now() ).days if record.due_date else ''

    context = {
        'title': 'Work Order Records',
        'records': records,
    }

    return render(request, 'workorder/workorder_records.html', context)

@login_required
@csrf_exempt
@require_http_methods(["GET", "PUT"])
def workorder_record(request, id):
    try:
        record = WorkOrderRecord.objects.get(id=id)
        
        data = {
                'id': record.id,
                'status': record.status,
                'due_date': record.due_date.strftime('%Y-%m-%d') if record.due_date else '',
                'completed_on': record.completed_on.strftime('%Y-%m-%d') if record.completed_on else '',
                'attachments': record.attachments.url if record.attachments else '',
                'comments': record.comments if record.comments else '',
                'time_until_due': (record.due_date - timezone.now() ).days if record.due_date else '',
        }        
        status = request.GET.get('status')

        if status:
            # get user
            user = User.objects.get(username=request.user)
            record.completed_by = user
            record.status = status
            completed_on = request.GET.get('completed_on')
            if completed_on:
                # Convert string to a timezone-aware datetime
                record.completed_on = timezone.make_aware(
                    timezone.datetime.strptime(completed_on, '%Y-%m-%d')
                )
            record.attachments = request.GET.get('attachments')
            record.comments = request.GET.get('comments')
            record.save()
            messages.success(request, 'Record updated successfully')
            return redirect('workorder-workorder-records')

            
        if request.method == "GET":
            return JsonResponse(data)

    except WorkOrder.DoesNotExist:
        return JsonResponse({'error': 'workorder not found'}, status=404)
    except (Location.DoesNotExist, WorkOrder.DoesNotExist, Department.DoesNotExist, Vendor.DoesNotExist):
        return JsonResponse({'error': 'Related entity not found'}, status=404)

def add_workorder_record(request):
    if request.method == 'POST':
        form = WorkOrderRecordForm(request.POST, request.FILES)
        # add created by
        form.instance.created_by = request.user
        if form.is_valid():
            form.save()
            return redirect('workorder-workorder-records')
    else:
        form = WorkOrderRecordForm()
    context = {
        'title': 'Add Work Order Record',
        'form': form,
    }
    return render(request, 'workorder/new_workorder_record.html', context)