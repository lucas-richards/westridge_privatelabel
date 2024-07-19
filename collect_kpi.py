import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_projects.settings')
django.setup()

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date
from training.models import KPI, KPIValue, Profile, TrainingEvent, TrainingModule, ProfileTrainingEvents
import datetime as dt

class Command(BaseCommand):
    help = 'Calculate and save daily KPI values'
    
    def save_kpi(self, kpi_name, value):
        today = date.today()
        kpi, created = KPI.objects.get_or_create(name=kpi_name)
        KPIValue.objects.update_or_create(
            kpi=kpi,
            date=today,
            defaults={'value': value}
        )

    def handle(self, *args, **kwargs):
        profiles = Profile.objects.all()
        active_profiles = profiles.filter(active=True)
        training_modules = TrainingModule.objects.filter(other=False).order_by('name')

        training = {
            'performed': 0,
            'not_performed': 0,
            'total': 0
        }
        retraining = {
            'performed': 0,
            'overdue': 0,
            'not_performed': 0,
            'total': 0
        }
        profiles_fully_trained = 0
        training_not_performed_users = []
        retraining_not_performed_users = []
        retraining_overdue_users = []

        for profile in active_profiles:
            try:
                profile_training_events = ProfileTrainingEvents.objects.filter(profile=profile).first()
                training_events_now = profile_training_events.row.split(',')
                fully_trained = True

                for i, training_module in enumerate(training_modules):
                    if training_events_now[i] == '-':
                        continue
                    elif training_events_now[i][0] == 'T':
                        fully_trained = False
                        if training_module.retrain_months:
                            retraining['total'] += 1
                            retraining['not_performed'] += 1
                            retraining_not_performed_users.append(profile.user)
                        else:
                            training['total'] += 1
                            training['not_performed'] += 1
                            training_not_performed_users.append(profile.user)
                        continue

                    try:
                        parsed_date = dt.datetime.strptime(training_events_now[i], '%m/%d/%y')
                        current_date = dt.datetime.now()
                        delta = current_date - parsed_date
                        months_difference = delta.days // 30

                        if training_module.retrain_months:
                            if months_difference > training_module.retrain_months:
                                retraining['overdue'] += 1
                                fully_trained = False
                                retraining_overdue_users.append(profile.user)
                            else:
                                retraining['performed'] += 1
                            retraining['total'] += 1
                        else:
                            training['performed'] += 1
                            training['total'] += 1

                    except ValueError:
                        print('this is the value that couldnt convert to date', training_events_now[i])
            except:
                print('Error for:', profile.user.username)
                continue

            if fully_trained:
                profiles_fully_trained += 1
                print('Fully trained:', profile.user.username)

        perc_fully_trained = round(profiles_fully_trained / active_profiles.count() * 100) if active_profiles.count() else 0
        training_not_performed_users = list(set(training_not_performed_users))
        retraining_not_performed_users = list(set(retraining_not_performed_users))
        retraining_overdue_users = list(set(retraining_overdue_users))

        training['performed'] = round(training['performed'] / training['total'] * 100) if training['total'] else 0
        retraining['performed'] = round(retraining['performed'] / retraining['total'] * 100) if retraining['total'] else 0
        retraining['overdue'] = round(retraining['overdue'] / retraining['total'] * 100) if retraining['total'] else 0
        training['not_performed'] = round(training['not_performed'] / training['total'] * 100) if training['total'] else 0
        retraining['not_performed'] = round(retraining['not_performed'] / retraining['total'] * 100) if retraining['total'] else 0

        self.save_kpi('Training Performed', training['performed'])
        self.save_kpi('Retraining Performed', retraining['performed'])
        self.save_kpi('Retraining Overdue', retraining['overdue'])
        self.save_kpi('Training Not Performed', training['not_performed'])
        self.save_kpi('Retraining Not Performed', retraining['not_performed'])
        self.save_kpi('Percentage Fully Trained', perc_fully_trained)
        
        self.stdout.write(self.style.SUCCESS('Successfully saved daily KPI values'))

# Call the function to calculate and save daily KPI values
if __name__ == '__main__':
    Command().handle()

