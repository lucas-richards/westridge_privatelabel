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
        ('Gregg Haskell', '' , 'lucasrichardsdev@gmail.com', ['ALL', 'SUP', 'ALM', 'SAA', 'PMR']),
        ('John Spielman', '' , 'lucasrichardsdev@gmail.com', ['ALL', 'SUP', 'DOC', 'ALM']),
        ('Todd Haskell', 'Gregg Haskell' , 'lucasrichardsdev@gmail.com', ['ALL', 'SUP', 'SCS']),
        ('Tom Kelly', 'Gregg Haskell' , 'lucasrichardsdev@gmail.com', ['ALL', 'SCS']),
        ('Osmin Ventura', 'Gregg Haskell' , 'lucasrichardsdev@gmail.com', ['ALL', 'WHS', 'BFK', 'AFK', 'SUP']),
        ('Chris Roman', 'Osmin Ventura' , 'lucasrichardsdev@gmail.com', ['ALL', 'WHS']),
        ('Ivan Caracheo', 'Osmin Ventura' , 'lucasrichardsdev@gmail.com', ['ALL', 'WHS', 'BFK', 'AFK', 'TRK']),
        ('Jorge Ascencio', 'Osmin Ventura' , 'lucasrichardsdev@gmail.com', ['ALL', 'WHS', 'BFK', 'AFK']),
        ('Liset Marin', 'Osmin Ventura' , 'lucasrichardsdev@gmail.com', ['ALL', 'WHS']),
        ('Randall Martinez', 'Osmin Ventura' , 'lucasrichardsdev@gmail.com', ['ALL', 'WHS', 'BFK', 'AFK', 'TRK']),
        ('Robert Gantt', 'Osmin Ventura' , 'lucasrichardsdev@gmail.com', ['ALL', 'WHS', 'BFK', 'AFK', 'TRK']),
        ('Servando Machuca', 'Osmin Ventura' , 'lucasrichardsdev@gmail.com', ['ALL', 'WHS']),
        ('Jerry Araiza', 'Gregg Haskell' , 'lucasrichardsdev@gmail.com', ['ALL', 'SCS', 'ALM', 'SUP']),
        ('Marcelle Moraes', 'Gregg Haskell' , 'lucasrichardsdev@gmail.com', ['ALL', 'QAS', 'SUP']),
        ('Frederick Wade', 'Marcelle Moraes' , 'lucasrichardsdev@gmail.com', ['ALL', 'QAS', 'QCI']),
        ('Emilia Guerrero', 'Marcelle Moraes' , 'lucasrichardsdev@gmail.com', ['ALL', 'QCI']),
        # ('Anthony De Nicola', 'Gregg Haskell' , 'lucasrichardsdev@gmail.com', ['ALL', 'SAA', 'PMR']),
        # ('Cristina Ripley', 'Gregg Haskell' , 'lucasrichardsdev@gmail.com', ['ALL', 'PUR']),
        # ('Paloma Carvajal', 'Gregg Haskell' , 'lucasrichardsdev@gmail.com', ['ALL', 'PUR']),
        # ('Maryam Parissa', 'Gregg Haskell' , 'lucasrichardsdev@gmail.com', ['ALL']),
        # ('Erika Larios',  'Jia Jeng' ,'lucasrichardsdev@gmail.com', ['ALL']),
        # ('Jia Jeng', 'Gregg Haskell' , 'lucasrichardsdev@gmail.com', ['ALL', 'SUP', 'PMR']),
        # ('Juliet Hamby', 'Jia Jeng' , 'lucasrichardsdev@gmail.com', ['ALL']),
        # ('Liz Garibay', 'Gregg Haskell' , 'lucasrichardsdev@gmail.com', ['ALL', 'SCS']),
        # ('Edgar Torres', 'Liz Garibay' , 'lucasrichardsdev@gmail.com', ['ALL', 'SCS']),
        # ('Rocio Lopez', 'Gregg Haskell' , 'lucasrichardsdev@gmail.com', ['ALL', 'SCS']),
        # ('Yarely Gomez', 'Gregg Haskell' , 'lucasrichardsdev@gmail.com', ['ALL', 'WHS', 'BFK', 'SCS']),
        # ('Robert Mason', 'Gregg Haskell' , 'lucasrichardsdev@gmail.com', ['ALL', 'SUP', 'SCS']),
        # ('Rod Burton',  'Gregg Haskell' ,'lucasrichardsdev@gmail.com', ['ALL', 'SCS', 'SUP']),
        # ('Scott Lamborn',  'Gregg Haskell' ,'lucasrichardsdev@gmail.com', ['ALL', 'SCS']),
        # ('Ivis Beza', 'Gregg Haskell' , 'lucasrichardsdev@gmail.com', ['ALL', 'SUP', 'ALM', 'PRD', 'CLN', 'COM', 'FOL', 'TUB', 'ASM', 'HKP', 'LNE']),
        # ('Aracely Tapia', 'Ivis Beza' , 'lucasrichardsdev@gmail.com', ['ALL', 'SUP', 'ALM', 'PRD', 'CLN', 'COM', 'FOL', 'TUB', 'ASM', 'HKP', 'LNE']),
        # ('Claudia Berzanez', 'Ivis Beza' , 'lucasrichardsdev@gmail.com', ['ALL', 'PRD', 'CLN', 'FOL', 'TUB', 'ASM', 'HKP', 'LNE']),
        # ('Eden Mao',  'Ivis Beza' ,'lucasrichardsdev@gmail.com', ['ALL', 'PRD', 'CLN', 'MCH', 'FOL', 'TUB', 'HKP', 'LNE']),
        # ('Esmeralda Samano',  'Ivis Beza' ,'lucasrichardsdev@gmail.com', ['ALL', 'PRD', 'ASM', 'HKP', 'LNE', 'COM']),
        # ('Ever Santana', 'Ivis Beza' , 'lucasrichardsdev@gmail.com', ['ALL', 'ALM', 'PRD', 'CLN', 'FOL', 'TUB', 'ASM', 'HKP', 'LNE']),
        # ('Julio Gallegas', 'Ivis Beza','lucasrichardsdev@gmail.com', ['ALL', 'PRD', 'COM']),
        # ('Tereza Maria Bautista','Ivis Beza', 'lucasrichardsdev@gmail.com', ['ALL', 'PRD']),
        # ('Maria Bermudez', 'Ivis Beza','lucasrichardsdev@gmail.com', ['ALL', 'PRD', 'CLN', 'TUB', 'ASM', 'LNE']),
        # ('Maria Macias','Ivis Beza', 'lucasrichardsdev@gmail.com', ['ALL', 'PRD', 'CLN', 'TUB', 'ASM', 'HKP', 'LNE']),
        # ('Maria Molina','Ivis Beza', 'lucasrichardsdev@gmail.com', ['ALL', 'PRD', 'CLN', 'FOL', 'ASM', 'HKP', 'LNE']),
        # ('Olga L Guerrero','Ivis Beza', 'lucasrichardsdev@gmail.com', ['ALL', 'PRD', 'CLN', 'ASM', 'HKP', 'LNE']),
        # ('Rafael Rojas', 'Ivis Beza','lucasrichardsdev@gmail.com', ['ALL', 'PRD']),
        # ('Thy Chan', 'Ivis Beza','lucasrichardsdev@gmail.com', ['ALL', 'PRD', 'CLN', 'MCH', 'FOL', 'TUB', 'LNE']),
        # ('Yesenia Merin','Ivis Beza', 'lucasrichardsdev@gmail.com', ['ALL', 'PRD', 'ASM', 'HKP', 'LNE']),
        # ('Maria Garcia', 'Ivis Beza','lucasrichardsdev@gmail.com', ['ALL', 'PRD', 'ASM', 'HKP', 'LNE']),
        # ('Nancy Teran', 'Ivis Beza','lucasrichardsdev@gmail.com', ['ALL', 'PRD', 'ASM', 'HKP', 'LNE']),
        # ('Mayra Jimenez','Ivis Beza', 'lucasrichardsdev@gmail.com', ['ALL', 'PRD', 'ASM', 'HKP', 'LNE']),
        # ('Dayrin Miranda','Ivis Beza', 'lucasrichardsdev@gmail.com', ['ALL', 'PRD', 'ASM', 'HKP', 'LNE']),
        # ('Gabriela Rodriguez','Ivis Beza', 'lucasrichardsdev@gmail.com', ['ALL', 'PRD', 'ASM', 'HKP', 'LNE']),
        # ('Haidee Esparza','Ivis Beza', 'lucasrichardsdev@gmail.com', ['ALL', 'PRD', 'ASM', 'HKP', 'LNE']),
        # ('Carmen Rojo','Ivis Beza', 'lucasrichardsdev@gmail.com', ['ALL', 'PRD', 'ASM', 'HKP', 'LNE']),


    ]

    # Loop through the data and create users with roles
    for username, supervisor, email, roles_names in users_roles_data:
        user, created = User.objects.get_or_create(username=username, email=email)  # Assuming User model has username and email fields
        roles = Role.objects.filter(name__in=roles_names)
        profile, created = Profile.objects.get_or_create(user=user)
        profile.roles.add(*roles)
        if supervisor:
            try:
                profile.supervisor = User.objects.get(username=supervisor)
                profile.save()
            except User.DoesNotExist:
                print(f'User {username} supervisor {supervisor} does not exist')
    
        print(f'User {username} created or updated with roles {roles_names}')

# Call the function to seed the database with users and their roles
if __name__ == '__main__':
    seed_users_roles()