
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone
from users.models import Department, User

CRITICALITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

STATUS = [
        ('in_progress', 'In Progress'),
        ('on_hold', 'On Hold'),
        ('done', 'Done'),
        ('scheduled', 'Scheduled'),
        ('cancelled', 'Cancelled'),
    ]

STATUS2 = [
    ('online', 'Online'),
    ('offline', 'Offline'),
    ('do_not_track', 'Do Not Track'),
    ]

RECURRENCE = [
    ('once', 'Once'),
    ('daily', 'Daily'),
    ('weekly', 'Weekly'),
    ('monthly', 'Monthly'),
    ('quarterly', 'Quarterly'),
    ('biannually', 'Biannually'),
    ('yearly', 'Yearly'),
]

# KPI models
class KPI(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class KPIValue(models.Model):
    kpi = models.ForeignKey(KPI, on_delete=models.CASCADE)
    value = models.FloatField()
    date = models.DateField()

    def __str__(self):
        return f"{self.kpi.name} - {self.date}: {self.value}"


# vendor model
class Vendor(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    contact = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name

def asset_attachment_path(instance, filename):
    return f'asset_attachments/{instance.code}/{filename}'

class Asset(models.Model):
    code = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=STATUS2,
        default='online',
    )
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    location = models.CharField(
        max_length=20,
        choices=[
            ('warehouse', 'Warehouse'),
            ('office', 'Office'),
            ('quality lab', 'Quality Lab'),
            ('bulding', 'Building'),
            ('production Line #1', 'Production Line #1'),
            ('production Line #2', 'Production Line #2'),
            ('production Line #3', 'Production Line #3'),
            ('assembly', 'Assembly'),
            ('roof', 'Roof'),
            # Add more choices here
        ],
        null=False,
        blank=False,
    )
    description = models.TextField(null=True, blank=True)
    serial_number = models.CharField(max_length=255, null=True, blank=True)
    model = models.CharField(max_length=255, null=True, blank=True)
    manufacturer = models.CharField(max_length=255, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    department_in_charge = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    vendors = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='asset_images/', null=True, blank=True)
    # criticality of the asset with an array of three options low medium and high
    criticality = models.CharField(
        max_length=6,
        choices=CRITICALITY_CHOICES,
        default='medium',
    )
    attachments = models.FileField(upload_to=asset_attachment_path, null=True, blank=True)

    def __str__(self):
        return self.name

def workorder_attachment_path(instance, filename):
    return f'asset_attachments/{instance.title}/{filename}'

class WorkOrder(models.Model):
    title = models.CharField(max_length=255)
    priority = models.CharField(
        max_length=20,
        choices=CRITICALITY_CHOICES,
        default='medium',
    )
    description = models.TextField(null=True, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_workorders')
    department_assigned_to = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_workorders')
    created_on = models.DateTimeField(auto_now_add=True)
    first_due_date = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now=True)
    recurrence = models.CharField(
        max_length=20,
        choices=RECURRENCE,
        default='once',
    )
    asset = models.ForeignKey(Asset, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='wo_images/', null=True, blank=True)
    attachments = models.FileField(upload_to=workorder_attachment_path, null=True, blank=True)


    def __str__(self):
        return 'WO' + str(self.id) + '-' + self.title 

    #  when a work order is created, I want to automatically create a work order record with same due date and assigned to the same person
    def save(self, *args, **kwargs):
        super(WorkOrder, self).save(*args, **kwargs)
        if not self.workorderrecord_set.exists():
            WorkOrderRecord.objects.create(workorder=self, due_date=self.first_due_date, assigned_to=self.assigned_to)

    

class WorkOrderRecord(models.Model):
    workorder = models.ForeignKey(WorkOrder, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='scheduled',
    )
    created_on = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(default=timezone.now)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_workorders_record')
    completed_on = models.DateTimeField(null=True, blank=True)
    completed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    time_to_complete = models.DurationField(null=True, blank=True)
    attachments = models.FileField(upload_to=f'records', null=True, blank=True)
    comments = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"#{self.id} - {self.workorder.asset} - {self.workorder.title} - {self.due_date}"

    # when saved check how many records are with status done today and update the kpi
    def save(self, *args, **kwargs):
        super(WorkOrderRecord, self).save(*args, **kwargs)
        if self.status == 'done':
            kpi = KPI.objects.get(name='Productivity')
            today = timezone.now().date()
            value = WorkOrderRecord.objects.filter(status='done', completed_on__date=today).count()
            print('value:', value)
            kpi_value = KPIValue.objects.filter(kpi=kpi, date=today).first()
            if not kpi_value:
                kpi_value = KPIValue.objects.create(kpi=kpi, date=today, value=value)
            else:
                kpi_value.value = value
            kpi_value.save()
            
            
