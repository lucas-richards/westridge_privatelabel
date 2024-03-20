import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_projects.settings')
django.setup()

# Import your Django models
from users.models import User, Role, Profile  # Replace 'your_app' with the name of your Django app

# Define a function to seed the database with users and their roles
def seed_users_roles():
    users_roles_data = [
        ('Gregg Haskell', 'lucasrichardsdev@gmail.com', ['ALL', 'SUP', 'ALM', 'SAA', 'PMR']),
        ('John Spielman', 'lucasrichardsdev@gmail.com', ['ALL', 'SUP', 'DOC', 'ALM']),
        ('Todd Haskell', 'lucasrichardsdev@gmail.com', ['ALL', 'SUP', 'SCS']),
        ('Tom Kelly', 'lucasrichardsdev@gmail.com', ['ALL', 'SCS']),
        ('Osmin Ventura', 'lucasrichardsdev@gmail.com', ['ALL', 'WHS', 'BFK', 'AFK', 'SUP']),
        ('Chris Roman', 'lucasrichardsdev@gmail.com', ['ALL', 'WHS']),
        ('Ivan Caracheo', 'lucasrichardsdev@gmail.com', ['ALL', 'WHS', 'BFK', 'AFK', 'TRK']),
        ('Jorge Ascencio', 'lucasrichardsdev@gmail.com', ['ALL', 'WHS', 'BFK', 'AFK']),
        ('Liset Marin', 'lucasrichardsdev@gmail.com', ['ALL', 'WHS']),
        ('Randall Martinez', 'lucasrichardsdev@gmail.com', ['ALL', 'WHS', 'BFK', 'AFK', 'TRK']),
        ('Robert Gantt', 'lucasrichardsdev@gmail.com', ['ALL', 'WHS', 'BFK', 'AFK', 'TRK']),
        ('Servando Machuca', 'lucasrichardsdev@gmail.com', ['ALL', 'WHS']),
        ('Jerry Araiza', 'lucasrichardsdev@gmail.com', ['ALL', 'SCS', 'ALM', 'SUP']),
        ('Marcelle Moraes', 'lucasrichardsdev@gmail.com', ['ALL', 'QAS', 'SUP']),
        ('Frederick Wade', 'lucasrichardsdev@gmail.com', ['ALL', 'QAS', 'QCI']),
        ('Emilia Guerrero', 'lucasrichardsdev@gmail.com', ['ALL', 'QCI']),
        ('Anthony De Nicola', 'lucasrichardsdev@gmail.com', ['ALL', 'SAA', 'PMR']),
        ('Cristina Ripley', 'lucasrichardsdev@gmail.com', ['ALL', 'PUR']),
        ('Paloma Carvajal', 'lucasrichardsdev@gmail.com', ['ALL', 'PUR']),
        ('Maryam Parissa', 'lucasrichardsdev@gmail.com', ['ALL']),
        ('Erika Larios', 'lucasrichardsdev@gmail.com', ['ALL']),
        ('Jia Jeng', 'lucasrichardsdev@gmail.com', ['ALL', 'SUP', 'PMR']),
        ('Juliet Hamby', 'lucasrichardsdev@gmail.com', ['ALL']),
        ('Jennifer Flores', 'lucasrichardsdev@gmail.com', ['ALL', 'SCS', 'SUP']),
        ('Liz Garibay', 'lucasrichardsdev@gmail.com', ['ALL', 'SCS']),
        ('Edgar Torres', 'lucasrichardsdev@gmail.com', ['ALL', 'SCS']),
        ('Rocio Lopez', 'lucasrichardsdev@gmail.com', ['ALL', 'SCS']),
        ('Yarely Gomez', 'lucasrichardsdev@gmail.com', ['ALL', 'WHS', 'BFK', 'SCS']),
        ('Robert Mason', 'lucasrichardsdev@gmail.com', ['ALL', 'SUP', 'SCS']),
        ('Rod Burton', 'lucasrichardsdev@gmail.com', ['ALL', 'SCS', 'SUP']),
        ('Scott Lamborn', 'lucasrichardsdev@gmail.com', ['ALL', 'SCS']),
        ('Ivis Beza', 'lucasrichardsdev@gmail.com', ['ALL', 'SUP', 'ALM', 'PRD', 'CLN', 'COM', 'FOL', 'TUB', 'ASM', 'HKP', 'LNE']),
        ('Aracely Tapia', 'lucasrichardsdev@gmail.com', ['ALL', 'SUP', 'ALM', 'PRD', 'CLN', 'COM', 'FOL', 'TUB', 'ASM', 'HKP', 'LNE']),
        ('Claudia Berzanez', 'lucasrichardsdev@gmail.com', ['ALL', 'PRD', 'CLN', 'FOL', 'TUB', 'ASM', 'HKP', 'LNE']),
        ('Eden Mao', 'lucasrichardsdev@gmail.com', ['ALL', 'PRD', 'CLN', 'MCH', 'FOL', 'TUB', 'HKP', 'LNE']),
        ('Esmeralda Samano', 'lucasrichardsdev@gmail.com', ['ALL', 'PRD', 'ASM', 'HKP', 'LNE', 'COM']),
        ('Ever Santana', 'lucasrichardsdev@gmail.com', ['ALL', 'ALM', 'PRD', 'CLN', 'FOL', 'TUB', 'ASM', 'HKP', 'LNE']),
        ('Julio Gallegas', 'lucasrichardsdev@gmail.com', ['ALL', 'PRD', 'COM']),
        ('Tereza Maria Bautista', 'lucasrichardsdev@gmail.com', ['ALL', 'PRD']),
        ('Maria Bermudez', 'lucasrichardsdev@gmail.com', ['ALL', 'PRD', 'CLN', 'TUB', 'ASM', 'LNE']),
        ('Maria Macias', 'lucasrichardsdev@gmail.com', ['ALL', 'PRD', 'CLN', 'TUB', 'ASM', 'HKP', 'LNE']),
        ('Maria Molina', 'lucasrichardsdev@gmail.com', ['ALL', 'PRD', 'CLN', 'FOL', 'ASM', 'HKP', 'LNE']),
        ('Olga L Guerrero', 'lucasrichardsdev@gmail.com', ['ALL', 'PRD', 'CLN', 'ASM', 'HKP', 'LNE']),
        ('Rafael Rojas', 'lucasrichardsdev@gmail.com', ['ALL', 'PRD']),
        ('Thy Chan', 'lucasrichardsdev@gmail.com', ['ALL', 'PRD', 'CLN', 'MCH', 'FOL', 'TUB', 'LNE']),
        ('Yesenia Merin', 'lucasrichardsdev@gmail.com', ['ALL', 'PRD', 'ASM', 'HKP', 'LNE']),
    ]

    # Loop through the data and create users with roles
    for username, email, roles_names in users_roles_data:
        user, created = User.objects.get_or_create(username=username, email=email)  # Assuming User model has username and email fields
        roles = Role.objects.filter(name__in=roles_names)
        profile, created = Profile.objects.get_or_create(user=user)
        profile.roles.add(*roles)
        print(f'User {username} created with roles {roles_names}')

# Call the function to seed the database with users and their roles
if __name__ == '__main__':
    seed_users_roles()