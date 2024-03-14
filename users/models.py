from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone

class Department(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{self.name}"
    
# role model
class Role(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{self.name}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(null=True, blank=True)
    # use this image url as a default https://img.freepik.com/free-vector/man-profile-account-picture_24908-81754.jpg?w=826&t=st=1710450387~exp=1710450987~hmac=5371500fb04f8770784bc3b434179fc06ff8ae0bd7d4fe480f3358bdb53f62bf
    image = models.ImageField(default='default.webp', upload_to='profile_pics')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    # each profile can have multiple roles
    roles = models.ManyToManyField(Role, related_name='profiles', blank=True)
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
        percentage = round(self.certificationstatus_set.filter(status='Completed').count() / (self.certifications.count() or 1) * 100)
        return percentage if percentage != 0 else 0

    # function that returns all certification status
    def get_certification_status(self, certification):
        return self.certificationstatus_set.filter(certification=certification).first()
    

    # write a function that tells you if the user has all the certifications in status 'completed'
    def has_all_certifications_completed(self):
        return self.certificationstatus_set.filter(status='Completed').count() == self.certifications.count()
    
    # function that returns true if user birthday is today or timeuntil if is not today
    def birthday_today(self):
        return self.birthday == timezone.now().date()
    
    # get user tasks
  
    def get_tasks_assigned(self):
        return self.tasks_asignee.all()
   
    def get_tasks_created(self):
        return self.tasks_created.all()
    
    #  get user roles
    def get_roles(self):
        return self.roles.all()
    
    # must have certification is a function that receives a certification and returns true if the user has the role required for that certification
    def must_have_certification(self, certification):
        return certification.roles.filter(profiles=self).exists()
