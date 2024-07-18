# Schdule this to run daily like cron, every midnight and update status
# 0 0 * * * /path/to/your/python /path/to/your/manage.py update_certification_status
import os
import django
# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_projects.settings')
django.setup()
from datetime import date
from training.models import TrainingEvent, Certification
from datetime import timedelta
from users.models import Profile



def handle():
    # Get today's date
    today = date.today()
    profiles = Profile.objects.all()
    print(f'Updating certification status for {len(profiles)} profiles')
    for profile in profiles:
        for certification in profile.certifications.all():
            certificate = Certification.objects.get(id=certification.id)
            certStatus = TrainingEvent.objects.get(profile=profile, certification=certification)
            certStatus_exp = certStatus.expiration_date()
            if certificate.retrain_months:
                if certStatus.status == 'Completed':
                    if certStatus_exp < today:
                        certStatus.status = 'Expired'
                        print(f'{certificate.name} expired for {profile.user.username}')
                        certStatus.save()
                    elif certStatus_exp > today and certStatus_exp < today + timedelta(days=90):
                        certStatus.status = 'About to Expire'
                        print(f'{certificate.name} about to expire for {profile.user.username}')
                        certStatus.save()
                elif certStatus.status == 'About to Expire':
                    if certStatus_exp < today:
                        certStatus.status = 'Expired'
                        print(f'{certificate.name} expired for {profile.user.username}')
                        certStatus.save()
                    elif certStatus_exp > today + timedelta(days=90):
                        certStatus.status = 'Completed'
                        print(f'{certificate.name} completed for {profile.user.username}')
                        certStatus.save()
                elif certStatus.status == 'Expired':
                    if certStatus_exp > today:
                        certStatus.status = 'About to Expire'
                        print(f'{certificate.name} about to expire for {profile.user.username}')
                        certStatus.save()
                    elif certStatus_exp > today + timedelta(days=90):
                        certStatus.status = 'Completed'
                        print(f'{certificate.name} completed for {profile.user.username}')
                        certStatus.save()


# Handle call
if __name__ == '__main__':
    handle()