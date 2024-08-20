import json
import os
import django
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from datetime import datetime


# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_projects.settings')
django.setup()

from workorder.models import WorkOrder, Location, Vendor, Asset
from users.models import Department
from django.contrib.auth.models import User

# Assume the JSON data is stored in a variable called `data`

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_projects.settings')
django.setup()


# Assume the JSON data is stored in a variable called `data`

with open('./work_orders_mmddyyyy.json') as f:
    data = json.load(f)

def load_workorders(data):
    for item in data:
        asset = Asset.objects.filter(code=item['code']).first()
        created_by = User.objects.filter(first_name=item['Created by'].split()[0]).first()
        assigned_to = User.objects.filter(first_name=item['Assigned to'].split()[0]).first() if item['Assigned to'] else None
        department_in_charge = Department.objects.get_or_create(name=item['Teams Assigned to'])[0] if item['Teams Assigned to'] else None
        
        try:
            # Determine the image path
            image_path = os.path.join('media', 'downloads', 'images', item['code'])
            image = None
            if os.path.exists(image_path) and os.path.isdir(image_path):
                image_files = os.listdir(image_path)
                if image_files:  # Check if any files exist in the directory
                    first_image_file = image_files[0]  # Take the first file found
                    imageUrl = os.path.join('downloads', 'images', item['code'], first_image_file)
                    with open(os.path.join(image_path, first_image_file), 'rb') as f:
                        image = f.read()
            
            # Determine the attachments path
            attachments_path = os.path.join('media', 'downloads', 'attachments', item['code'])
            attachments = None
            if os.path.exists(attachments_path) and os.path.isdir(attachments_path):
                attachment_files = os.listdir(attachments_path)
                if attachment_files:  # Check if any files exist in the directory
                    first_attachment_file = attachment_files[0]  # Take the first file found
                    attachmentUrl = os.path.join('downloads', 'attachments', item['code'], first_attachment_file)
                    with open(os.path.join(attachments_path, first_attachment_file), 'rb') as f:
                        attachments = f.read()
            
            created_on= timezone.make_aware(datetime.strptime(item['Created on'], "%m-%d-%Y")) if item['Created on'] else None
            first_due_date=  timezone.make_aware(datetime.strptime(item['Due date'], "%m-%d-%Y")) if item['Due date'] else None

            print(f"created_on: {created_on}")
            print(f"first_due_date: {first_due_date}")
            # Create the workorder object
            workorder, created = WorkOrder.objects.get_or_create(
                title=item['Title'],
                description=item.get('Description', ''),
                priority=item.get('Priority') if item.get('Priority') else 'medium',
                assigned_to=assigned_to if assigned_to else None,
                department_assigned_to=department_in_charge if department_in_charge else None,
                created_by=created_by if created_by else None,
                created_on= created_on,
                first_due_date=first_due_date,
                recurrence=item.get('recurrence') if item.get('recurrence') else 'once',
                asset=asset if asset else None,
                # image=image,
                # attachments=attachments,
            )
            
            if created:
                print(f"WorkOrder {item['Title']} created successfully")
            else:
                # update attachment
                if attachmentUrl:
                    workorder.attachments = attachmentUrl
                    workorder.save()

                print(f"workorder {item['Title']} updated successfully")
            
        except Exception as e:
            print(f"workorder with code {item['Title']} encountered a problem")
            print(f"Error while creating workorder: {e}")

if __name__ == "__main__":
    load_workorders(data)

