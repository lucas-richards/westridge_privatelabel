import os
import django
import logging


# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_projects.settings')
django.setup()

from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date
from workorder.models import WorkOrder, WorkOrderRecord

class Command(BaseCommand):
    help = 'Send maintenance email with overdue and coming up WOs'
    
    def handle(self, *args, **kwargs):
        email_user = os.environ.get('EMAIL_USER')
        email_password = os.environ.get('EMAIL_PASS')
        author_email = 'lrichards@westridgelabs.com'
        recipients = ['lrichards@westridgelabs.com' ]

        subject = 'Due Maintenance Work Orders'
        workorders = WorkOrder.objects.all()
        records = []

        for workorder in workorders:
            last_record = WorkOrderRecord.objects.filter(workorder=workorder).exclude(status__in=['done', 'cancelled']).order_by('-due_date').first()
            if last_record:
                last_record.time_until_due = (last_record.due_date - timezone.now()).days if last_record.due_date else None
                if last_record.time_until_due is not None and last_record.time_until_due <= 7:
                    records.append(last_record)
        
        records = sorted(records, key=lambda x: x.due_date)

        for record in records:
            record.status = record.get_status_display()

        # Build the message
        if records:
            message_parts = ["""
            <div style="padding-left: 16px; border: 1px solid #ddd; border-radius: 4px;">
            """]

            for data in records:
                message_parts.append(f'''
                <div style=" border-bottom: 1px solid #ddd;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="display: flex; align-items: baseline;">
                            {self.get_status_badge(data.status)}
                            <p style="min-width: 50px; margin-right: 8px; font-weight: bold;">WO{data.workorder.id}</p>
                            <p style="min-width: 250px; margin-right: 8px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{data.workorder.title}</p>
                        </div>
                        <div>
                            {self.get_due_status(data)}
                        </div>
                    </div>
                </div>
                ''')

            message_parts.append('</div>')
            message = ''.join(message_parts)
        else:
            message = '''
            <div style="padding: 8px; margin-top: 8px; border: 1px solid #ddd; border-radius: 4px;">
                <h5>No records found</h5>
            </div>
            '''

        try:
            send_mail(subject, '', email_user, recipients, html_message=message, auth_user=email_user, auth_password=email_password)
            logging.info(f'Successfully sent schedule update email to {recipients}')
            print(f'Successfully sent schedule update email to {recipients}')
        except Exception as e:
            logging.error(f'Error sending schedule update email to {recipients}: {str(e)}')
            print(f'Error sending schedule update email to {recipients}: {str(e)}')

    def get_status_badge(self, status):
        badge_styles = {
            'On Hold': 'margin-right: 8px; background-color: #ffc107; color: #fff; padding: 2px 4px; border-radius: 4px;',
            'In Progress': 'margin-right: 8px; background-color: #007bff; color: #fff; padding: 2px 4px; border-radius: 4px;',
            'Scheduled': 'margin-right: 8px; background-color: #17a2b8; color: #fff; padding: 2px 4px; border-radius: 4px;',
        }
        return f'<span style="min-width: 70px; {badge_styles.get(status, "")}">{status}</span>'

    def get_due_status(self, record):
        if record.time_until_due > 0:
            return '<p style="margin-right: 8px; color: #ffc107;font-weight:bold;">Coming up</p>'
        else:
            return '<p style="margin-right: 8px; color: #dc3545;font-weight:bold;">Overdue</p>'

# Call the function to send email
if __name__ == '__main__':
    Command().handle()
