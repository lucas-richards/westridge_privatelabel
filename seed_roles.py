import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_projects.settings')
django.setup()

# Import your Django models
from users.models import Role  # Replace 'your_app' with the description of your Django app
from training.models import TrainingModule
# Define a function to seed the database with roles
def seed_roles():
    roles_data = [
    {'name': 'ALL', 'description': 'All Employees', 'training_modules': ['TM000', 'TM001', 'TM002']},
    {'name': 'SUP', 'description': 'Supervisors', 'training_modules': ['TM005', 'TM040']},
    {'name': 'ALM', 'description': 'Alarm Access Employees', 'training_modules': ['TM003', 'TM004']},
    {'name': 'SAA', 'description': 'Special Access Area Employees', 'training_modules': ['TM003']},
    {'name': 'PRD', 'description': 'Production Staff General', 'training_modules': ['TM003', 'TM100']},
    {'name': 'WHS', 'description': 'Warehouse and Shipping Staff', 'training_modules': ['TM003','TM200']},
    {'name': 'DOC', 'description': 'Document Control Staff', 'training_modules': ['TM301', 'TM302']},
    {'name': 'QCI', 'description': 'Quality Inspector', 'training_modules': ['TM003', 'TM005', 'TM100', 'TM101', 'TM102', 'TM302', 'TM303', 'TM040']},
    {'name': 'QAS', 'description': 'Quality Assurance Staff', 'training_modules': ['TM003', 'TM005', 'TM100', 'TM101', 'TM102', 'TM200', 'TM301', 'TM302', 'TM303', 'TM401', 'TM040']},
    {'name': 'PUR', 'description': 'Purchasing Staff', 'training_modules': ['TM401']},
    {'name': 'SCS', 'description': 'Customer Service / Sales Staff', 'training_modules': ['TM040']},
    {'name': 'PMR', 'description': 'Product Manager', 'training_modules': ['TM301', 'TM302']},
    {'name': 'CLN', 'description': 'Equipment Cleaner', 'training_modules': ['TM100','TM101']},
    {'name': 'COM', 'description': 'Compounding and Mixing', 'training_modules': ['TM100','TM101', 'TM102']},
    {'name': 'FOL', 'description': 'Foil Machine Operator', 'training_modules': ['TM100', 'TM103']},
    {'name': 'TUB', 'description': 'Tube Filling Operator', 'training_modules': ['TM100', 'TM104']},
    {'name': 'ASM', 'description': 'Production Assembly', 'training_modules': ['TM100','TM105']},
    {'name': 'MCH', 'description': 'Mechanic', 'training_modules': ['TM100', 'TM106']},
    {'name': 'HKP', 'description': 'Housekeeping', 'training_modules': ['TM100']},
    {'name': 'LNE', 'description': 'Filling Line Operator', 'training_modules': ['TM100', 'TM108']},
    {'name': 'BFK', 'description': 'Sit Down Forklift Operator', 'training_modules': ['TM200', 'TM201']},
    {'name': 'AFK', 'description': 'Advanced Forklift Operator', 'training_modules': ['TM200', 'TM202']},
    {'name': 'TRK', 'description': 'Truck Driver', 'training_modules': ['TM200', 'TM203']}
]

    # Loop through the data and create roles
    for role_data in roles_data:
        # get or create
        role, _ = Role.objects.get_or_create(name=role_data['name'], description=role_data['description'])
        # add training modules
        for tm in role_data['training_modules']:
            training = TrainingModule.objects.get(name=tm)
            role.training_modules.add(training)
        

        print(f'Role {role.name} created or updated with {role.training_modules.all()}')


# Call the function to seed the database with roles
if __name__ == '__main__':
    seed_roles()