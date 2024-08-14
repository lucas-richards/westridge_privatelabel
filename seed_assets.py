import json
import os
import django
from django.utils.dateparse import parse_datetime

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_projects.settings')
django.setup()

from workorder.models import Asset, Location, Vendor
from users.models import Department
from django.contrib.auth.models import User
from workorder.models import Asset, Location, Vendor
from users.models import Department
from django.contrib.auth.models import User

# Assume the JSON data is stored in a variable called `data`

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_projects.settings')
django.setup()


# Assume the JSON data is stored in a variable called `data`

with open('./Assets_with_code.json') as f:
    data = json.load(f)

def load_assets(data):
    for item in data:
        location, _ = Location.objects.get_or_create(name=item['location'])
        created_by, _ = User.objects.get_or_create(username=item['created_by'])
        department_in_charge = Department.objects.get_or_create(name=item['department_in_charge'])[0] if item['department_in_charge'] else None
        
        try:
            # Determine the image path
            image_path = os.path.join('media', 'downloads', 'images', item['code'])
            image = None
            if os.path.exists(image_path) and os.path.isdir(image_path):
                image_files = os.listdir(image_path)
                if image_files:  # Check if any files exist in the directory
                    first_image_file = image_files[0]  # Take the first file found
                    print(first_image_file)
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
                    with open(os.path.join(attachments_path, first_attachment_file), 'rb') as f:
                        attachments = f.read()
            
            # Create the Asset object
            Asset.objects.create(
                code=item.get('code', ''),
                name=item['name'],
                status=item['status'],
                parent=None,  # Assuming no parent data in the JSON, handle accordingly if it exists
                location=location,
                description=item.get('description', ''),
                serial_number=item.get('serial_number', ''),
                model=item.get('model', ''),
                manufacturer=item.get('manufacturer', ''),
                year=item.get('year', None),
                department_in_charge=department_in_charge,
                created_by=created_by,
                created_on=parse_datetime(item['created_on']),
                last_updated=parse_datetime(item['last_updated']),
                image=imageUrl,
                # attachments=attachments,
            )
            print(f"Asset {item['name']} created successfully")
        except Exception as e:
            print(f"Asset with code {item['name']} encountered a problem")
            print(f"Error while creating asset: {e}")

if __name__ == "__main__":
    load_assets(data)

