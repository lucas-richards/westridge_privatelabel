import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_projects.settings')
django.setup()

# Import your Django models
from users.models import User, Role, Profile
from training.models import ProfileTrainingEvents
# Define a function to seed the database with users and their roles
def seed_users_roles():
    users_roles_data = [
        ('Gregg Haskell', '', '', ['ALL', 'SUP', 'ALM', 'SAA', 'PMR'], True),
        ('John Spielman', '', '', ['ALL', 'SUP', 'DOC', 'ALM'], True),
        ('Todd Haskell', 'gregg_haskell', '', ['ALL', 'SUP', 'SCS'], True),
        ('Tom Kelly', 'gregg_haskell', '', ['ALL', 'SCS'], True),
        ('Osmin Ventura', 'gregg_haskell', '', ['ALL', 'WHS', 'BFK', 'AFK', 'SUP'], True),
        ('Chris Roman', 'osmin_ventura', '', ['ALL', 'WHS'], True),
        ('Ivan Caracheo', 'osmin_ventura', '', ['ALL', 'WHS', 'BFK', 'AFK', 'TRK'], True),
        ('Jorge Ascencio', 'osmin_ventura', '', ['ALL', 'WHS', 'BFK', 'AFK'], True),
        ('Liset Marin', 'osmin_ventura', '', ['ALL', 'WHS'], True),
        ('Randall Martinez', 'osmin_ventura', '', ['ALL', 'WHS', 'BFK', 'AFK', 'TRK'], True),
        ('Robert Gantt', 'osmin_ventura', '', ['ALL', 'WHS', 'BFK', 'AFK', 'TRK'], True),
        ('Servando Machuca', 'osmin_ventura', '', ['ALL', 'WHS'], True),
        ('Jerry Araiza', 'gregg_haskell', '', ['ALL', 'SCS', 'ALM', 'SUP'], True),
        ('Marcelle Moraes', 'gregg_haskell', '', ['ALL', 'QAS', 'SUP'], True),
        ('Frederick Wade', 'marcelle_moraes', '', ['ALL', 'QAS', 'QCI'], True),
        ('Emilia Guerrero', 'marcelle_moraes', '', ['ALL', 'QCI'], True),
        ('Anthony De Nicola', 'gregg_haskell', '', ['ALL', 'SAA', 'PMR'], True),
        ('Cristina Ripley', 'gregg_haskell', '', ['ALL', 'PUR'], True),
        ('Paloma Carvajal', 'gregg_haskell', '', ['ALL', 'PUR'], True),
        ('Maryam Parissa', 'gregg_haskell', '', ['ALL'], True),
        ('Erika Larios', '', '', ['ALL'], True),
        ('Jia Jeng', 'gregg_haskell', '', ['ALL', 'SUP', 'PMR'], True),
        ('Juliet Hamby', 'jia_jeng', '', ['ALL'], True),
        ('Liz Garibay', 'gregg_haskell', '', ['ALL', 'SUP', 'SCS'], True),
        ('Edgar Torres', 'liz_garibay', '', ['ALL', 'SCS'], True),
        ('Rocio Lopez', 'gregg_haskell', '', ['ALL', 'SCS'], True),
        ('Yarely Gomez', 'gregg_haskell', '', ['ALL', 'WHS', 'BFK', 'SCS'], True),
        ('Robert Mason', 'gregg_haskell', '', ['ALL', 'SUP', 'SCS'], True),
        ('Rod Burton', 'robert_mason', '', ['ALL', 'SCS'], True),
        ('Scott Lamborn', 'robert_mason', '', ['ALL', 'SCS'], True),
        ('Ivis Beza', 'gregg_haskell', '', ['ALL', 'SUP', 'ALM', 'PRD', 'CLN', 'COM', 'FOL', 'TUB', 'ASM', 'HKP', 'LNE'], True),
        ('Aracely Tapia', 'ivis_beza', '', ['ALL', 'SUP', 'ALM', 'PRD', 'CLN', 'COM', 'FOL', 'TUB', 'ASM', 'HKP', 'LNE'], True),
        ('Claudia Berzanez', 'ivis_beza', '', ['ALL', 'PRD', 'CLN', 'FOL', 'TUB', 'ASM', 'HKP', 'LNE'], True),
        ('Eden Mao', 'ivis_beza', '', ['ALL', 'PRD', 'CLN', 'MCH', 'FOL', 'TUB', 'HKP', 'LNE'], True),
        ('Esmeralda Samano', 'ivis_beza', '', ['ALL', 'PRD', 'ASM', 'HKP', 'LNE', 'COM'], True),
        ('Ever Santana', 'ivis_beza', '', ['ALL', 'ALM', 'PRD', 'CLN', 'FOL', 'TUB', 'ASM', 'HKP', 'LNE'], True),
        ('Julio Gallegas', 'ivis_beza', '', ['ALL', 'PRD', 'COM'], True),
        ('Tereza Maria Bautista', 'ivis_beza', '', ['ALL', 'PRD'], True),
        ('Maria Bermudez', 'ivis_beza', '', ['ALL', 'PRD', 'CLN', 'TUB', 'ASM', 'LNE'], True),
        ('Maria Macias', 'ivis_beza', '', ['ALL', 'PRD', 'CLN', 'TUB', 'ASM', 'HKP', 'LNE'], True),
        ('Maria Molina', 'ivis_beza', '', ['ALL', 'PRD', 'CLN', 'FOL', 'ASM', 'HKP', 'LNE'], True),
        ('Olga L Guerrero', 'ivis_beza', '', ['ALL', 'PRD', 'CLN', 'ASM', 'HKP', 'LNE'], True),
        ('Rafael Rojas', 'ivis_beza', '', ['ALL', 'PRD'], True),
        ('Thy Chan', 'ivis_beza', '', ['ALL', 'PRD', 'CLN', 'MCH', 'FOL', 'TUB', 'LNE'], True),
        ('Yesenia Merin', 'ivis_beza', '', ['ALL', 'PRD', 'ASM', 'HKP', 'LNE'], True),
        ('Maria Garcia', 'ivis_beza', '', ['ALL', 'PRD', 'ASM', 'HKP', 'LNE'], True),
        ('Nancy Teran', 'ivis_beza', '', ['ALL', 'PRD', 'ASM', 'HKP', 'LNE'], True),
        ('Mayra Jimenez', 'ivis_beza', '', ['ALL', 'PRD', 'ASM', 'HKP', 'LNE'], True),
        ('Dayrin Miranda', 'ivis_beza', '', ['ALL', 'PRD', 'ASM', 'HKP', 'LNE'], True),
        ('Gabriela Rodriguez', 'ivis_beza', '', ['ALL', 'PRD', 'ASM', 'HKP', 'LNE'], True),
        ('Haidee Esparza', 'ivis_beza', '', ['ALL', 'PRD', 'ASM', 'HKP', 'LNE'], True),
        ('Carmen Rojo', 'ivis_beza', '', ['ALL', 'PRD', 'ASM', 'HKP', 'LNE'], True),
        ('Zaida Melendez', '', '', [], False),
        ('Charmaine Watson', '', '', [], False),
        ('Cesar Campos', '', '', [], False),
        ('Luis Roman', '', '', [], False),
        ('Albert Catalan', '', '', [], False),
        ('Shawny Mitchell', '', '', [], False),
        ('Lucas Richards', '', '', [], False),
        ('Gabriel Martinez', '', '', [], False),
        ('Miguel Caballero', '', '', [], False),
        ('Sirivan Min', '', '', [], False),
        ('Margarita Lopez', '', '', [], False),
        ('Ray Albrechtsen', '', '', [], False),
        ('Anthony De Nicola', '', '', [], False),
        ('Jorge Ascencio', '', '', [], False),
        ('Sergio Rangel', '', '', [], False),
        ('Jennifer Flores', '', '', [], False),
        ('Stephanie Cazarin [C]', '', '', [], False),
        ('Linda Weiler [C]', '', '', [], False),


    ]

    # Loop through the data and create users with roles
    for username, supervisor, email, roles_names, active in users_roles_data:
        # replace spaces with underscores and make lowercase in username
        first_name = username.split(' ')[0]
        if len(username.split(' ')) > 2:
            first_name = username.split(' ')[0] + ' ' + username.split(' ')[1]
            last_name = username.split(' ')[2]
        else:
            last_name = username.split(' ')[1]
        
        username = username.replace(" ", "_").lower()
        # if user already exists skip
        if User.objects.filter(username=username).exists():
            print(f'User {username} already exists')
            continue
        user, created = User.objects.get_or_create(first_name=first_name,last_name=last_name,username=username, email=email)  # Assuming User model has username and email fields
        roles = Role.objects.filter(name__in=roles_names)
        profile, created = Profile.objects.get_or_create(user=user)
        # if not active
        
        profile.roles.add(*roles)
        if profile:
            profileTraining, created = ProfileTrainingEvents.objects.get_or_create(profile=profile)
            profileTraining.update_row()
            profile.active = active
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