from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone

class Department(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{self.name}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(null=True, blank=True)
    image = models.ImageField(default='default.webp', upload_to='profile_pics')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    certifications = models.ManyToManyField('training.Certification', related_name='profiles', through='training.CertificationStatus')

    def __str__(self):
        return f'{self.user.username} Profile'
    
    #resize the image to save space
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width >300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
    
    # write a function that returns all the user's certifications and their status
    def get_certifications(self):
        return self.certifications.all()
    
    # wtire a function that returns the percentage of certifications completed
    def get_certifications_percentage(self):
        return round(self.certificationstatus_set.filter(status='Completed').count() / self.certifications.count() * 100)
    
    # write a function that returns all the user's certifications and their status
    def get_certification_status(self):
        return self.certificationstatus_set.all()
    
    # write a function that tells you if the user has all the certifications in status 'completed'
    def has_all_certifications_completed(self):
        return self.certificationstatus_set.filter(status='Completed').count() == self.certifications.count()
    
    # function that returns true if user birthday is today or timeuntil if is not today
    def birthday_today(self):
        return self.birthday == timezone.now().date()
    
    # get user tasks
    @property
    def get_tasks_assigned(self):
        return self.tasks_asignee.all()
    
    @property
    def get_tasks_created(self):
        return self.tasks_created.all()
