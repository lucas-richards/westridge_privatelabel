from django.shortcuts import render
from .models import Asset, Vendor, WorkOrder
from django.http import JsonResponse

# Create your views here.

def dashboard(request):
    

    context = {
        'title': 'Dashboard',
        
    }

    return render(request, 'workorder/dashboard.html', context)

def asset(request, id):
    try:
        asset = Asset.objects.get(id=id)
        print('this is asset',asset)
        data = {
            'code': asset.code,
            'name': asset.name,
            'status': asset.status,
            'description': asset.description,
            'image_url': asset.image.url, 
            'serial_number': asset.serial_number,
            'model': asset.model,
            'manufacturer': asset.manufacturer,
            'year': asset.year,
        }
        return JsonResponse(data)
    except Asset.DoesNotExist:
        return JsonResponse({'error': 'Asset not found'}, status=404)

def assets(request):
    assets = Asset.objects.all()
    context = {
        'title': 'Assets',
        'assets': assets,
    }

    return render(request, 'workorder/assets.html', context)

# def asset(request, id):
#     asset = Asset.objects.get(id=id)
#     context = {
#         'title': 'Asset',
#         'asset': asset,
#     }

#     return render(request, 'workorder/asset.html', context)

def add_asset(request):
    if request.method == 'POST':
        pass
    context = {
        'title': 'Add Asset',
    }

    return render(request, 'workorder/add_asset.html', context)

def edit_asset(request, id):
    asset = Asset.objects.get(id=id)
    context = {
        'title': 'Edit Asset',
        'asset': asset,
    }

    return render(request, 'workorder/edit_asset.html', context)

def delete_asset(request, id):
    asset = Asset.objects.get(id=id)
    asset.delete()
    return redirect('workorder-assets')

def vendors(request):
    vendors = Vendor.objects.all()
    context = {
        'title': 'Vendors',
        'vendors': vendors,
    }

    return render(request, 'workorder/vendors.html', context)

def vendor(request, id):
    vendor = Vendor.objects.get(id=id)
    context = {
        'title': 'Vendor',
        'vendor': vendor,
    }

    return render(request, 'workorder/vendor.html', context)

def add_vendor(request):
    if request.method == 'POST':
        pass
    context = {
        'title': 'Add Vendor',
    }

    return render(request, 'workorder/add_vendor.html', context)

def edit_vendor(request, id):
    vendor = Vendor.objects.get(id=id)
    context = {
        'title': 'Edit Vendor',
        'vendor': vendor,
    }

    return render(request, 'workorder/edit_vendor.html', context)

def delete_vendor(request, id):
    vendor = Vendor.objects.get(id=id)
    vendor.delete()
    return redirect('workorder-vendors')

def workorders(request):
    workorders = WorkOrder.objects.all()
    context = {
        'title': 'Work Orders',
        'workorders': workorders,
    }

    return render(request, 'workorder/workorders.html', context)

def workorder(request, id):
    workorder = WorkOrder.objects.get(id=id)
    context = {
        'title': 'Work Order',
        'workorder': workorder,
    }

    return render(request, 'workorder/workorder.html', context)

def add_workorder(request):
    if request.method == 'POST':
        pass
    context = {
        'title': 'Add Work Order',
    }

    return render(request, 'workorder/add_workorder.html', context)

def edit_workorder(request, id):
    workorder = WorkOrder.objects.get(id=id)
    context = {
        'title': 'Edit Work Order',
        'workorder': workorder,
    }

    return render(request, 'workorder/edit_workorder.html', context)

def delete_workorder(request, id):
    workorder = WorkOrder.objects.get(id=id)
    workorder.delete()
    return redirect('workorder-workorders')

