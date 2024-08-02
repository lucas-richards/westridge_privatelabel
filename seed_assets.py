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
import json
import os
import django
from django.utils.dateparse import parse_datetime
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
            
            Asset.objects.create(
                code=item.get('code', ''),
                name=item['name'],
                status=item['status'],
                parent=None,  # Assuming no parent data in the JSON, handle accordingly if exists
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
                image=item.get('image', ''),
            )
            print(f"Asset {item['name']} created successfully")
        except Exception as e:
            print(f"asset with code {item['name']} got a problem")
            print(f"Error while creating asset: {e}")

if __name__ == "__main__":
    load_assets(data)

