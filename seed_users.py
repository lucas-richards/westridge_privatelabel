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
        ('Gregg Haskell', '', '', ['ALL', 'SUP', 'ALM', 'SAA', 'PMR']),
        ('John Spielman', '', '', ['ALL', 'SUP', 'DOC', 'ALM']),
        ('Todd Haskell', 'gregg_haskell', '', ['ALL', 'SUP', 'SCS']),
        ('Tom Kelly', 'gregg_haskell', '', ['ALL', 'SCS']),
        ('Osmin Ventura', 'gregg_haskell', '', ['ALL', 'WHS', 'BFK', 'AFK', 'SUP']),
        ('Chris Roman', 'osmin_ventura', '', ['ALL', 'WHS']),
        ('Ivan Caracheo', 'osmin_ventura', '', ['ALL', 'WHS', 'BFK', 'AFK', 'TRK']),
        ('Jorge Ascencio', 'osmin_ventura', '', ['ALL', 'WHS', 'BFK', 'AFK']),
        ('Liset Marin', 'osmin_ventura', '', ['ALL', 'WHS']),
        ('Randall Martinez', 'osmin_ventura', '', ['ALL', 'WHS', 'BFK', 'AFK', 'TRK']),
        ('Robert Gantt', 'osmin_ventura', '', ['ALL', 'WHS', 'BFK', 'AFK', 'TRK']),
        ('Servando Machuca', 'osmin_ventura', '', ['ALL', 'WHS']),
        ('Jerry Araiza', 'gregg_haskell', '', ['ALL', 'SCS', 'ALM', 'SUP']),
        ('Marcelle Moraes', 'gregg_haskell', '', ['ALL', 'QAS', 'SUP']),
        ('Frederick Wade', 'marcelle_moraes', '', ['ALL', 'QAS', 'QCI']),
        ('Emilia Guerrero', 'marcelle_moraes', '', ['ALL', 'QCI']),
        ('Anthony De Nicola', 'gregg_haskell', '', ['ALL', 'SAA', 'PMR']),
        ('Cristina Ripley', 'gregg_haskell', '', ['ALL', 'PUR']),
        ('Paloma Carvajal', 'gregg_haskell', '', ['ALL', 'PUR']),
        ('Maryam Parissa', 'gregg_haskell', '', ['ALL']),
        ('Erika Larios', '', '', ['ALL']),
        ('Jia Jeng', 'gregg_haskell', '', ['ALL', 'SUP', 'PMR']),
        ('Juliet Hamby', 'jia_jeng', '', ['ALL']),
        ('Liz Garibay', 'gregg_haskell', '', ['ALL', 'SUP', 'SCS']),
        ('Edgar Torres', 'liz_garibay', '', ['ALL', 'SCS']),
        ('Rocio Lopez', 'gregg_haskell', '', ['ALL', 'SCS']),
        ('Yarely Gomez', 'gregg_haskell', '', ['ALL', 'WHS', 'BFK', 'SCS']),
        ('Robert Mason', 'gregg_haskell', '', ['ALL', 'SUP', 'SCS']),
        ('Rod Burton', 'robert_mason', '', ['ALL', 'SCS']),
        ('Scott Lamborn', 'robert_mason', '', ['ALL', 'SCS']),
        ('Ivis Beza', 'gregg_haskell', '', ['ALL', 'SUP', 'ALM', 'PRD', 'CLN', 'COM', 'FOL', 'TUB', 'ASM', 'HKP', 'LNE']),
        ('Aracely Tapia', 'ivis_beza', '', ['ALL', 'SUP', 'ALM', 'PRD', 'CLN', 'COM', 'FOL', 'TUB', 'ASM', 'HKP', 'LNE']),
        ('Claudia Berzanez', 'ivis_beza', '', ['ALL', 'PRD', 'CLN', 'FOL', 'TUB', 'ASM', 'HKP', 'LNE']),
        ('Eden Mao', 'ivis_beza', '', ['ALL', 'PRD', 'CLN', 'MCH', 'FOL', 'TUB', 'HKP', 'LNE']),
        ('Esmeralda Samano', 'ivis_beza', '', ['ALL', 'PRD', 'ASM', 'HKP', 'LNE', 'COM']),
        ('Ever Santana', 'ivis_beza', '', ['ALL', 'ALM', 'PRD', 'CLN', 'FOL', 'TUB', 'ASM', 'HKP', 'LNE']),
        ('Julio Gallegas', 'ivis_beza', '', ['ALL', 'PRD', 'COM']),
        ('Tereza Maria Bautista', 'ivis_beza', '', ['ALL', 'PRD']),
        ('Maria Bermudez', 'ivis_beza', '', ['ALL', 'PRD', 'CLN', 'TUB', 'ASM', 'LNE']),
        ('Maria Macias', 'ivis_beza', '', ['ALL', 'PRD', 'CLN', 'TUB', 'ASM', 'HKP', 'LNE']),
        ('Maria Molina', 'ivis_beza', '', ['ALL', 'PRD', 'CLN', 'FOL', 'ASM', 'HKP', 'LNE']),
        ('Olga L Guerrero', 'ivis_beza', '', ['ALL', 'PRD', 'CLN', 'ASM', 'HKP', 'LNE']),
        ('Rafael Rojas', 'ivis_beza', '', ['ALL', 'PRD']),
        ('Thy Chan', 'ivis_beza', '', ['ALL', 'PRD', 'CLN', 'MCH', 'FOL', 'TUB', 'LNE']),
        ('Yesenia Merin', 'ivis_beza', '', ['ALL', 'PRD', 'ASM', 'HKP', 'LNE']),
        ('Maria Garcia', 'ivis_beza', '', ['ALL', 'PRD', 'ASM', 'HKP', 'LNE']),
        ('Nancy Teran', 'ivis_beza', '', ['ALL', 'PRD', 'ASM', 'HKP', 'LNE']),
        ('Mayra Jimenez', 'ivis_beza', '', ['ALL', 'PRD', 'ASM', 'HKP', 'LNE']),
        ('Dayrin Miranda', 'ivis_beza', '', ['ALL', 'PRD', 'ASM', 'HKP', 'LNE']),
        ('Gabriela Rodriguez', 'ivis_beza', '', ['ALL', 'PRD', 'ASM', 'HKP', 'LNE']),
        ('Haidee Esparza', 'ivis_beza', '', ['ALL', 'PRD', 'ASM', 'HKP', 'LNE']),
        ('Carmen Rojo', 'ivis_beza', '', ['ALL', 'PRD', 'ASM', 'HKP', 'LNE'])


    ]

    # Loop through the data and create users with roles
    for username, supervisor, email, roles_names in users_roles_data:
        # replace spaces with underscores and make lowercase in username
        first_name = username.split(' ')[0]
        if len(username.split(' ')) > 2:
            first_name = username.split(' ')[0] + ' ' + username.split(' ')[1]
            last_name = username.split(' ')[2]
        else:
            last_name = username.split(' ')[1]
        
        username = username.replace(" ", "_").lower()
        user, created = User.objects.get_or_create(first_name=first_name,last_name=last_name,username=username, email=email)  # Assuming User model has username and email fields
        roles = Role.objects.filter(name__in=roles_names)
        profile, created = Profile.objects.get_or_create(user=user)
        profile.roles.add(*roles)
        if profile:
            profileTraining, created = ProfileTrainingEvents.objects.get_or_create(profile=profile)
            profileTraining.update_row()
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