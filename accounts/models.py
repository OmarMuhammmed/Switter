from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
# Create your models here.
from django.utils import timezone
class CustomUserManager(BaseUserManager):
    def create_user(self, first_name, last_name , username, email=None,  password=None,**extra_fields):
        # Vaildation 
        if not username:
            raise ValueError('The username field must be set')
       
        user = self.model(
                            email = self.normalize_email(email),
                            username = username,
                            first_name = first_name,
                            last_name = last_name,
                            **extra_fields 
                         )
        user.set_password(password),
        user.save(using=self._db)
        return user

    
    def create_superuser(self,username, email=None, password=None, **extra_fields):
        # Set default permissions for superuser
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_admin', True)

        # Create the user with the provided parameters
        user = self.create_user(
            first_name='Admin',
            last_name='User',
            username=username,
            email=self.normalize_email(email),
            password=password,
            **extra_fields
        )
        
        
        
        # Set the password and save the user
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False , null=True,blank=True)
    is_admin = models.BooleanField(default=False, null=True, blank=True)
    is_superuser = models.BooleanField(default=False, null=True, blank=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)
    
    USERNAME_FIELD = 'username' # to login django dash 

    objects = CustomUserManager()
    
    class Meta:
        verbose_name_plural = 'Users'

    
    def has_perm(self, perm, obj=None):
       
        return True

    def has_module_perms(self, app_label):
       
        return True

    @property
    def is_staff(self):
        
        return self.is_superuser
    

    def __str__(self):
        return self.username