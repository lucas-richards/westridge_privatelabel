import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_projects.settings')
django.setup()

# Import your Django models
from training.models import TrainingModule

# Define the modules data array
modules_data = [
    {'name': 'TM000', 'description': ''},
    {'name': 'TM002', 'description': 'Facilities and Safety'},
    {'name': 'TM003', 'description': 'Special Access Areas'},
    {'name': 'TM004', 'description': 'Building Opening and Closing'},
    {'name': 'TM005', 'description': 'Employee Training Program'},
    {'name': 'TM100', 'description': 'Production Operations'},
    {'name': 'TM101', 'description': 'Equipment Cleaning'},
    {'name': 'TM103', 'description': 'Foil Machine Operation'},
    {'name': 'TM104', 'description': 'Tube Filler Operation'},
    {'name': 'TM105', 'description': 'Production Assembly'},
    {'name': 'TM106', 'description': 'Mechanic'},
    {'name': 'TM107', 'description': 'Reserved'},
    {'name': 'TM108', 'description': 'Production Line Operations'},
    {'name': 'TM200', 'description': 'Warehouse Operations'},
    {'name': 'TM203', 'description': 'Truck Driver'},
    {'name': 'TM301', 'description': 'Design Control'},
    {'name': 'TM302', 'description': 'Documentation Architecture'},
    {'name': 'TM401', 'description': 'Purchasing Operations'},
    {'name': 'TM001', 'description': 'Quality System and GMP', 'retrain_months': 24},
    {'name': 'TM040', 'description': 'Customer Complaints', 'retrain_months': 24},
    {'name': 'TM102', 'description': 'Compounding', 'retrain_months': 24},
    {'name': 'TM201', 'description': 'Forklift', 'retrain_months': 24},
    {'name': 'TM202', 'description': 'Advanced Forklift', 'retrain_months': 24},
    {'name': 'TM303', 'description': 'Quality Inspection', 'retrain_months': 24}
]

# Define a function to seed the database with modules and roles
def seed_modules_roles():
    # Create modules
    for module_data in modules_data:
        module, created = TrainingModule.objects.get_or_create(
            name=module_data['name'],
            description=module_data['description']
        )

        # Add retrain_months if it exists in module_data
        if 'retrain_months' in module_data:
            module.retrain_months = module_data['retrain_months']


        print(f'Module {module.name} created')

        module.save()

    print('Modules and roles seeded successfully!')


# Call the function to seed the database with modules and roles
if __name__ == '__main__':
    seed_modules_roles()
