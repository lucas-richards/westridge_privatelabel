import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_projects.settings')
django.setup()

# Import your Django models
from users.models import Role  # Replace 'your_app' with the description of your Django app

# Define a function to seed the database with roles
def seed_roles():
    roles_data = [
        ('ALL', 'All Employees'),
        ('SUP', 'Supervisors'),
        ('ALM', 'Alarm Access Employees'),
        ('SAA', 'Special Access Area Employees'),
        ('PRD', 'Production Staff General'),
        ('WHS', 'Warehouse and Shipping Staff'),
        ('DOC', 'Document Control Staff'),
        ('QCI', 'Quality Inspector'),
        ('QAS', 'Quality Assurance Staff'),
        ('PUR', 'Purchasing Staff'),
        ('SCS', 'Customer Service / Sales Staff'),
        ('PMR', 'Product Manager'),
    ]

    # Loop through the data and create roles
    for name, description in roles_data:
        Role.objects.create(name=name, description=description)
        print(f'Role {name} created')

# Call the function to seed the database with roles
if __name__ == '__main__':
    seed_roles()