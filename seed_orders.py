import json
import os
import django
from django.utils.dateparse import parse_datetime

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_projects.settings')
django.setup()

from privatelabel.models import Order, Customer, Product



# Assume the JSON data is stored in a variable called `data`

with open('./orders.json') as f:
    data = json.load(f)

def load_orders(data):
    for item in data:
        customer, created = Customer.objects.get_or_create(name=item['customer'])
        product, created = Product.objects.get_or_create(name=item['product'])
        
        order = Order(
            customer=customer,
            product=product,
            number=item['number'],
            qty=item['qty'],
            date_received=parse_datetime(item['date_received']) if item['date_received'] != 'tbd' else None,
            date_entered=parse_datetime(item['date_entered']) if item['date_entered'] != 'tbd' else None,
            due_date=parse_datetime(item['due_date']) if item['due_date'] != 'tbd' else None,
            desired_date=parse_datetime(item['desired_date']) if item['desired_date'] != 'tbd' else None,
            expected_ship_date=parse_datetime(item['expected_ship_date']) if item['expected_ship_date'] else None,
            deposit_stat=item['deposit_stat'],
            ingredients_stat=item['ingredients_stat'],
            spec_stat=item['spec_stat'],
            package_stat=item['package_stat'],
            cap_stat=item['cap_stat'],
            label_stat=item['label_stat'],
            box_stat=item['box_stat']
        )
        order.save()
        print(f'Order {order.number} created')
       

if __name__ == "__main__":
    load_orders(data)
    


