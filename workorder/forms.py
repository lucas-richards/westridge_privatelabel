from django import forms
from workorder.models import Asset, Vendor, WorkOrder, WorkOrderRecord, STATUS, STATUS2, CRITICALITY_CHOICES
from users.models import Department, User



class AssetEditForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name','location', 'description', 'status', 'image', 'serial_number', 'model', 'manufacturer', 'year', 'parent', 'department_in_charge', 'vendors', 'criticality', 'attachments']
        widgets = {
            'status': forms.Select(choices=STATUS2),
            'location': forms.Select(choices=Asset.objects.values_list('location', 'location')),
            'parent': forms.Select(choices=Asset.objects.values_list('name', 'name')),
            'department_in_charge': forms.Select(choices=Department.objects.values_list('name', 'name')),
            'vendors': forms.Select(choices=Vendor.objects.values_list('name', 'name')),
            'criticality': forms.Select(choices=CRITICALITY_CHOICES),
            
        }

        

class WorkOrderEditForm(forms.ModelForm):
    class Meta:
        model = WorkOrder
        fields = ['recurrence','first_due_date','title','assigned_to', 'department_assigned_to','image','description','asset', 'priority', 'attachments', ]
        widgets = {
            'priority': forms.Select(choices=CRITICALITY_CHOICES),
            'first_due_date': forms.DateInput(attrs={'type': 'date'}),
            'assigned_to': forms.Select(choices=User.objects.values_list('username', 'username').order_by('username')),
        }
# form to create a work order record
class WorkOrderRecordForm(forms.ModelForm):
    class Meta:
        model = WorkOrderRecord
        fields = ['workorder', 'due_date', 'comments']
        widgets = {
            'workorder': forms.Select(choices=WorkOrder.objects.values_list('asset')),
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


# form to edit work order record
class WorkOrderRecordEditForm(forms.ModelForm):
    class Meta:
        model = WorkOrderRecord
        fields = ['status', 'completed_on', 'attachments','comments']
        widgets = {
            'status': forms.Select(choices=STATUS),
            'completed_on': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

