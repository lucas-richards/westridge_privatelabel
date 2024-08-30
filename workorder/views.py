from django.shortcuts import render
from .models import Asset, Vendor, WorkOrder, WorkOrderRecord, KPI, KPIValue
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
        'overdue': round(work_orders_records.filter(due_date__lt=timezone.now()).exclude(status__in=['done', 'cancelled']).count(), 0),
        'on_time': round(work_orders_records.filter(due_date__gte=timezone.now()).exclude(status__in=['done', 'cancelled']).count(), 0),
        'total': work_orders_records.count(),
        'total_exclude_done_cancelled': work_orders_records.exclude(status__in=['done', 'cancelled']).count(),
    }

    # calculate the percentages
    work_orders_records_status['overdue_percentage'] = round((work_orders_records_status['overdue'] / work_orders_records_status['total_exclude_done_cancelled']) * 100) if work_orders_records_status['total_exclude_done_cancelled'] != 0 else 0
    work_orders_records_status['on_time_percentage'] = round((work_orders_records_status['on_time'] / work_orders_records_status['total_exclude_done_cancelled']) * 100) if work_orders_records_status['total_exclude_done_cancelled'] != 0 else 0
    work_orders_records_status['done_percentage'] = round((work_orders_records_status['done'] / work_orders_records_status['total']) * 100) if work_orders_records_status['total'] != 0 else 0
    work_orders_records_status['in_progress_percentage'] = round((work_orders_records_status['in_progress'] / work_orders_records_status['total']) * 100) if work_orders_records_status['total'] != 0 else 0
    work_orders_records_status['on_hold_percentage'] = round((work_orders_records_status['on_hold'] / work_orders_records_status['total']) * 100) if work_orders_records_status['total'] != 0 else 0
    work_orders_records_status['scheduled_percentage'] = round((work_orders_records_status['scheduled'] / work_orders_records_status['total']) * 100) if work_orders_records_status['total'] != 0 else 0
    work_orders_records_status['cancelled_percentage'] = round((work_orders_records_status['cancelled'] / work_orders_records_status['total']) * 100) if work_orders_records_status['total'] != 0 else 0
    print(work_orders_records_status)

    # get the KPI values
    status_kpi = KPIValue.objects.filter(kpi__name='Status Done').order_by('date')
    status_kpi_values = [value.value for value in status_kpi]
    status_kpi_dates = [value.date.strftime('%m-%d-%Y') for value in status_kpi]
    timing_kpi = KPIValue.objects.filter(kpi__name='Timing On Time').order_by('date')
    timing_kpi_values = [value.value for value in timing_kpi]
    timing_kpi_dates = [value.date.strftime('%m-%d-%Y') for value in timing_kpi]
    productivity_kpi = KPIValue.objects.filter(kpi__name='Productivity').order_by('date')
    productivity_kpi_values = [value.value for value in productivity_kpi]
    productivity_kpi_dates = [value.date.strftime('%m-%d-%Y') for value in productivity_kpi]


    context = {
        'title': 'Dashboard',
        'work_orders_records_status': work_orders_records_status,
        'status_kpi_values': status_kpi_values,
        'status_kpi_dates': status_kpi_dates,
        'timing_kpi_values': timing_kpi_values,
        'timing_kpi_dates': timing_kpi_dates,
        'productivity_kpi_values': productivity_kpi_values,
        'productivity_kpi_dates': productivity_kpi_dates,
        
    }
    return render(request, 'workorder/dashboard.html', context)

@csrf_exempt
@require_http_methods(["GET", "PUT"])
def asset(request, id):
    try:
        asset = Asset.objects.get(id=id)
        workorders_all = WorkOrder.objects.filter(asset=asset)
        workorders = []
        for wo in workorders_all:
            workorder = {
            'id': wo.id,
            'title': wo.title,
            'priority': wo.get_priority_display(),
            'recurrence': wo.get_recurrence_display(),
            'last_record_status': wo.workorderrecord_set.order_by('-created_on').first().status if wo.workorderrecord_set.order_by('-created_on').first() else '',
            }
            workorders.append(workorder)

        if request.method == "GET":
            data = {
                'id': asset.id,
                'code': asset.code,
                'name': asset.name,
                'status': asset.status,
                'description': asset.description,
                'image_url': asset.image.url if asset.image else '',
                'serial_number': asset.serial_number,
                'model': asset.model,
                'manufacturer': asset.manufacturer,
                'year': asset.year,
                'location': asset.location if asset.location else '',
                'parent': asset.parent.name if asset.parent else '',
                'department_in_charge': asset.department_in_charge.name if asset.department_in_charge else '',
                'vendors': asset.vendors.name if asset.vendors else '',
                'created_by': asset.created_by.username if asset.created_by else '',
                'created_on': asset.created_on.strftime('%m-%d-%Y %H:%M:%S'),
                'last_updated': asset.last_updated.strftime('%m-%d-%Y %H:%M:%S'),
                'criticality': asset.criticality,
                'attachments': asset.attachments.url if asset.attachments else '',
                'workorders': workorders,
            }
            return JsonResponse(data)
    except Asset.DoesNotExist:
        return JsonResponse({'error': 'Asset not found'}, status=404)
    except ( Asset.DoesNotExist, Department.DoesNotExist, Vendor.DoesNotExist):
        return JsonResponse({'error': 'Related entity not found'}, status=404)

def assets(request):
    assets = Asset.objects.all().order_by('code')
    # add an extra property to each asset 'workorders_count'
    for asset in assets:
        asset.workorders_count = WorkOrder.objects.filter(asset=asset).count()

    context = {
        'title': 'Assets',
        'assets': assets,
    }

    return render(request, 'workorder/assets.html', context)

@login_required
def add_asset(request):
    if request.method == 'POST':
        form = AssetEditForm(request.POST, request.FILES)
        # print location from request
        print('location', request.POST['location'])
        # add created by
        form.instance.created_by = request.user
        # if the location is warehouse, then find the last code that starts with W and increment it by 1. If last code is O-003 then the new code will be O-004
        if form.is_valid():
            location = request.POST['location']
            prefix = ''
            if location == 'warehouse':
                prefix = 'W'
            elif location == 'office':
                prefix = 'O'
            elif location in ['production Line #1', 'production Line #2', 'production Line #3']:
                prefix = 'P'
            elif location == 'assembly':
                prefix = 'A'
            elif location == 'building':
                prefix = 'B'
            elif location == 'roof':
                prefix = 'F'
            elif location == 'quality lab':
                prefix = 'Q'
            elif location == 'scale':
                prefix = 'SC'
            
            last_code = Asset.objects.filter(code__startswith=prefix).order_by('-code').first()
            if last_code:
                last_code = last_code.code.split('-')[1]
                form.instance.code = f'{prefix}-{str(int(last_code) + 1).zfill(3)}'
            else:
                form.instance.code = f'{prefix}-001'
            
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
    # set idwo to whatever the request has
    idwo = request.GET.get('idwo')
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
            'last_record': last_record,
            'recurrence': workorder.get_recurrence_display(),
        })

    # order workorders_by_last_record based on the last_record.due_date
    workorders_with_last_record = sorted(workorders_with_last_record, key=lambda x: x['last_record'].due_date if x['last_record'] else None)
    
    context = {
        'title': 'Work Orders',
        'workorders': workorders_with_last_record,
        'form': form,
        'idwo':idwo
    }

    return render(request, 'workorder/workorders.html', context)


@csrf_exempt
@require_http_methods(["GET", "PUT"])
def workorder(request, id):
    try:
        workorder = WorkOrder.objects.get(id=id)
        records = WorkOrderRecord.objects.filter(workorder=workorder).order_by('-due_date')
        last_record = records.first()

        if request.method == "GET":
            data = {
                'id': workorder.id,
                'code': workorder.asset.code if workorder.asset else '',
                'title': workorder.title,
                'priority': workorder.priority,
                'description': workorder.description,
                'assigned_to': workorder.assigned_to.username if workorder.assigned_to else '',
                'department_assigned_to': workorder.department_assigned_to.name if workorder.department_assigned_to else '',
                'created_by': workorder.created_by.username if workorder.created_by else '',
                'created_on': workorder.created_on.strftime('%m-%d-%Y %H:%M:%S'),
                'last_updated': workorder.last_updated.strftime('%m-%d-%Y %H:%M:%S'),
                'recurrence': workorder.get_recurrence_display(),
                'asset': workorder.asset.name if workorder.asset else '',
                'image_url': workorder.image.url if workorder.image else '',
                'attachments': workorder.attachments.url if workorder.attachments else '',
                'time_until_due': (last_record.due_date - last_record.created_on).days if last_record.due_date else '',
                'records': [{'id': record.id, 'created_on': record.created_on.strftime('%m-%d-%Y'), 'status': record.status, 'due_date': record.due_date.strftime('%m-%d-%Y'), 'completed_on': record.completed_on.strftime('%m-%d-%Y') if record.completed_on else '', 'completed_by': record.completed_by.username if record.completed_by else '', 'time_to_complete': record.time_to_complete.total_seconds() if record.time_to_complete else '', 'attachments': record.attachments.url if record.attachments else '', 'comments': record.comments} for record in records],
                'last_record_status': last_record.status if last_record else '',
            }
            return JsonResponse(data)
    except WorkOrder.DoesNotExist:
        return JsonResponse({'error': 'workorder not found'}, status=404)
    except (WorkOrder.DoesNotExist, Department.DoesNotExist, Vendor.DoesNotExist):
        return JsonResponse({'error': 'Related entity not found'}, status=404)

def workorder_page(request, id):
    # This is the view that renders the full page
    try:
        workorder = WorkOrder.objects.get(id=id)
        return redirect('workorder-workorders')
    except WorkOrder.DoesNotExist:
        return render(request, '404.html', status=404)

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


def workorder_records(request):
    idwor = request.GET.get('idwor')
    workorders = WorkOrder.objects.all()
    records = []
    for workorder in workorders:
        last_record = WorkOrderRecord.objects.filter(workorder=workorder).order_by('-due_date').first()
        if last_record:
            records.append(last_record)
    records = sorted(records, key=lambda x: x.due_date)
    # rearrange the records list so records with status cancelled or done are at the end
    records = sorted(records, key=lambda x: x.status in ['cancelled', 'done'])
    # add this to each record 'time_until_due': (record.due_date - timezone.now() ).days if record.due_date else '',
    for record in records:
        record.time_until_due = (record.due_date - timezone.now() ).days if record.due_date else ''
        record.status = record.get_status_display()

    context = {
        'title': 'Work Order Records',
        'records': records,
        'idwor':idwor
    }

    return render(request, 'workorder/workorder_records.html', context)

@login_required
@csrf_exempt
@require_http_methods(["GET", "POST", "PUT"])
def workorder_record(request, id):
    try:
        record = WorkOrderRecord.objects.get(id=id)
        
        data = {
                'id': record.id,
                'workorder_id': record.workorder.id if record.workorder else '',
                'workorder_title': record.workorder.title if record.workorder else '',
                'workorder_description': record.workorder.description if record.workorder else '',
                'workorder_asset': record.workorder.asset.code if record.workorder.asset else '',
                'status': record.status,
                'due_date': record.due_date.strftime('%m-%d-%Y') if record.due_date else '',
                'completed_on': record.completed_on.strftime('%Y-%m-%d') if record.completed_on else '',
                'attachments': record.attachments.url if record.attachments else '',
                'comments': record.comments if record.comments else '',
                'time_until_due': (record.due_date - timezone.now() ).days if record.due_date else '',
        }        
        status = request.POST.get('status')
        print('request.FILES',request.FILES)
        if request.method == "POST":
            if status:
                print(request)
                # get user
                user = User.objects.get(username=request.user)
                record.completed_by = user
                record.status = status
                completed_on = request.POST.get('completed_on')
                print(completed_on)
                if completed_on:
                    # Convert string to a timezone-aware datetime
                    record.completed_on = timezone.make_aware(
                        timezone.datetime.strptime(completed_on, '%Y-%m-%d')
                    )
                # Handle file upload
                if 'attachments' in request.FILES:
                    record.attachments = request.FILES['attachments']
                    print('attachments', record.attachments)
                record.comments = request.POST.get('comments')
                record.save()
                messages.success(request, 'Record updated successfully')
                return redirect('workorder-workorder-records')

            
        if request.method == "GET":
            return JsonResponse(data)

    except WorkOrder.DoesNotExist:
        return JsonResponse({'error': 'workorder not found'}, status=404)
    except ( WorkOrder.DoesNotExist, Department.DoesNotExist, Vendor.DoesNotExist):
        return JsonResponse({'error': 'Related entity not found'}, status=404)

def workorder_record_page(request, id):
    # This is the view that renders the full page
    try:
        record = WorkOrderRecord.objects.get(id=id)
        return redirect('workorder-workorder-records')
    except WorkOrderRecord.DoesNotExist:
        return render(request, '404.html', status=404)

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