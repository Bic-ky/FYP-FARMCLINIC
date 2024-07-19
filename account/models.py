from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password 
from django.contrib.auth.models import PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, role=None):
        if not phone_number:
            raise ValueError('The Phone Number field must be set')

        user = self.model(phone_number=phone_number, role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, phone_number, password=None):
        # Create and save a new superuser with the given phone number and password
        user = self.create_user(phone_number, password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser , PermissionsMixin):
    EXPERT = 1
    FARMER = 2

    ROLE_CHOICES = (
        (EXPERT, 'EXPERT'),
        (FARMER, 'FARMER'),
    )
    phone_number = models.CharField(max_length=50,unique=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)
    full_name = models.CharField(max_length=50,blank=True)
    email = models.EmailField(max_length=100, unique=False, default="")

    address = models.CharField(max_length=50,blank=True)
    city = models.CharField(max_length=50,blank=True)
    country = models.CharField(max_length=50,blank=True)
    latitude = models.CharField(max_length=50,blank=True)
    longitude = models.CharField(max_length=50,blank=True)
    
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "phone_number"
    objects = UserManager()
    
    def __str__(self):
        return str(self.phone_number)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def get_role(self):
        if self.role == 1:
            user_role = 'EXPERT'
        elif self.role == 2:
            user_role = 'FARMER'
        return user_role
    




class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE ,  related_name='user_profile')
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)

    profile_picture = models.ImageField(
        upload_to='users/profile_pictures', blank=True, null=True)
    

    facebook = models.URLField(max_length=200, blank=True, null=True)
    linkedin = models.URLField(max_length=200, blank=True, null=True)
    twitter = models.URLField(max_length=200, blank=True, null=True)
    instagram = models.URLField(max_length=200, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user.phone_number)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    

@receiver(post_save , sender=User)
def post_save_create_profile(sender , instance , created , **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        print("Userprofile was created.")
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            print("Userprofile was updated.")
            profile.save()
        except:
            UserProfile.objects.create(user=instance)
            print("Userprofile was not found so created.")
    
from account.models import User
from appointment.models import Expert

@receiver(post_save, sender=User)
def create_expert(sender, instance, created, **kwargs):
    if created and instance.role == User.EXPERT:
        Expert.objects.create(user=instance)
        print("Expert was created.")
    else:
        try:
            expert = Expert.objects.get(user=instance)
            print("Expert was updated.")
            expert.save()
        except:
            Expert.objects.create(user=instance)
            print("Expert was not found so created.")


class Enquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email