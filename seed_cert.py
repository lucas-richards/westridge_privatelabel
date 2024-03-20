import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_projects.settings')
django.setup()

# Import your Django models
from training.models import Certification
from users.models import Role  # Adjust 'your_app' and import statement according to your Django app structure

# Define the certificates data array
certificates_data = [
    {
        "name": "TM000",
        "description": "",
        "roles": ["ALL"]
    },
    {
        "name": "TM002",
        "description": "Facilities and Safety",
        "roles": ["ALL"]
    },
    {
        "name": "TM003",
        "description": "Special Access Areas",
        "roles": ["ALM", "SAA", "PRD", "WHS","QCI","QAS"]
    },
    {
        "name": "TM004",
        "description": "Building Opening and Closing",
        "roles": ["ALM"]
    },
    {
        "name": "TM005",
        "description": "Employee Training Program",
        "roles": ["SUP","QCI","QAS"]
    },
    {
        "name": "TM100",
        "description": "Production Operations",
        "roles": ["PRD","CLN","COM","FOL","TUB","ASM","MCH","HKP","LNE","QCI","QAS"]
    },
    {
        "name": "TM101",
        "description": "Equipment Cleaning",
        "roles": ["CLN","COM","QCI","QAS"]
    },
    {
        "name": "TM103",
        "description": "Foil Machine Operation",
        "roles": ["FOL"]
    },
    {
        "name": "TM104",
        "description": "Tube Filler Operation",
        "roles": ["PRD", "FOL"]
    },
    {
        "name": "TM105",
        "description": "Production Assembly",
        "roles": ["TUB"]
    },
    {
        "name": "TM106",
        "description": "Mechanic",
        "roles": [ "MCH"]
    },
    {
        "name": "TM107",
        "description": "Reserved",
        "roles": []
    },
    {
        "name": "TM108",
        "description": "Production Line Operations",
        "roles": ["LNE"]
    },
    {
        "name": "TM200",
        "description": "Warehouse Operations",
        "roles": ["WHS", "BFK", "AFK", "TRK","QAS"]
    },
    {
        "name": "TM203",
        "description": "Truck Driver",
        "roles": ["TRK"]
    },
    {
        "name": "TM301",
        "description": "Design Control",
        "roles": ["TRK","QAS","PUR","SCS","PMR"]
                  
    },
    {
        "name": "TM302",
        "description": "Documentation Architecture",
        "roles": ["TRK","QCI","QAS","PUR","SCS","PMR"]
    },
    {
        "name": "TM401",
        "description": "Purchasing Operations",
        "roles": ["QAS","PUR"]
    },
    {
        "name": "TM001",
        "description": "Quality System and GMP",
        "roles": ["ALL"]
    },
    {
        "name": "TM040",
        "description": "Customer Complaints",
        "roles": ["QCI","SUP","QCI","QAS","SCS"]
                
    },
    {
        "name": "TM102",
        "description": "Compounding",
        "roles": ["COM","QCI", "QAS"]
    },
    {
        "name": "TM201",
        "description": "Forklift",
        "roles": ["BFK"]
    },
    {
        "name": "TM202",
        "description": "Advanced Forklift",
        "roles": ["AFK"]
    },
    {
        "name": "TM303",
        "description": "Quality Inspection",
        "roles": ["QCI", "QAS"]
    }
]

# Define a function to seed the database with certificates and roles
def seed_certificates_roles():
    for certificate_data in certificates_data:
        # Create the certification
        certification = Certification.objects.create(
            name=certificate_data["name"],
            description=certificate_data["description"]
        )

        # Get or create roles and associate them with the certification
        for role_name in certificate_data["roles"]:
            role, created = Role.objects.get_or_create(name=role_name)
            role.certifications.add(certification)

# Call the function to seed the database with certificates and roles
if __name__ == '__main__':
    seed_certificates_roles()
