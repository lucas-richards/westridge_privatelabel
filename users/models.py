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
    
    # filter trainingmodules that have this role
    def get_training_modules(self):
        return self.TrainingModules.all()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #  this profile supervisor
    supervisor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='supervisor_profiles')
    birthday = models.DateField(null=True, blank=True)
    # use this image url as a default https://img.freepik.com/free-vector/man-profile-account-picture_24908-81754.jpg?w=826&t=st=1710450387~exp=1710450987~hmac=5371500fb04f8770784bc3b434179fc06ff8ae0bd7d4fe480f3358bdb53f62bf
    image = models.ImageField(default='profile_pics/default.webp', upload_to='profile_pics')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    # each profile can have multiple roles
    roles = models.ManyToManyField(Role, related_name='profiles', blank=True)
    training_modules = models.ManyToManyField('training.TrainingModule', related_name='profiles', through='training.TrainingEvent')

    def __str__(self):
        return f'{self.user.username} Profile'
    
    #resize the image to save space
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

    #     img = Image.open(self.image.path)

    #     if img.height > 300 or img.width >300:
    #         output_size = (300,300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)
    
    # write a function that returns all the user's training_events and their status
    def get_training_modules(self):
        return self.training_modules.all()
    
    # wtire a function that returns the percentage of training_events completed
    
    def get_training_modules_percentage(self):
        # save in a list the modules that this profiles must have
        must_have = self.must_have_training_modules()
        print(f'{self.user.username} must have {must_have} training modules')
        if not must_have:
            return 0
        # for loop must_have and get the status of each module
        completed = 0
        expired = 0
        for module in must_have:
            training_event = module.get_training_events().filter(profile=self).first()
            print(f'{self.user.username} - {module.name} - {training_event}')
            status = training_event.status() if training_event else None
            if status is None:
                continue
            else:
                completed += 1
                if status == 'Expired':
                    expired += 1
        completed -= expired
        
        print(f'{self.user.username} has completed {completed} out of {len(must_have)} training modules')
        return round(completed/len(must_have) * 100)
        
    
    
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
    
    # function that ruturns a list of modules that the user must have based on the roles
    def must_have_training_modules(self):
        required_modules = []
        # Iterate over each role associated with the profile
        for role in self.roles.all():
            # Add training modules associated with the current role to the array
            required_modules.extend(role.get_training_modules())
        return required_modules
