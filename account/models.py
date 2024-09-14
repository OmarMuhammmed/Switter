from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
# Create your models here.

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
        
        # Create the user with the provided parameters
        user = self.create_user(
            first_name='Admin',
            last_name='User',
            username=username,
            email=self.normalize_email(email),
            password=password,
            **extra_fields
        )
        # Set default permissions for superuser
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        # Set the password and save the user
        user.set_password(password)
        user.save(using=self._db)
        return user



class CustomUser(AbstractBaseUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'username' # to login django dash 

    objects = CustomUserManager()
    
    class Meta:
        verbose_name_plural = 'Users'
    

    def __str__(self):
        return self.username