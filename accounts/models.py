from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManger(BaseUserManager):
    def create_user(self,first_name,last_name,email,username,phone_number,password=None):
        if not email:
            raise ValueError("Your email is invaild !")
        if not username:
            raise ValueError("Your username is invlaid")
        user=self.model(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            username=username,
            phone_number=phone_number,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,first_name,last_name,email,username,phone_number,password):
        user=self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            phone_number=phone_number
        )
        user.is_admin=True
        user.is_active=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)

        return user

class Account(AbstractBaseUser):
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    username=models.CharField(max_length=30,unique=True,blank=True,null=True)
    email=models.EmailField(unique=True,blank=False)
    phone_number=models.CharField(max_length=12)


    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)


    objects=MyAccountManger()


    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS=('first_name','last_name','username','phone_number')


    def __str__(self):
        return self.email


    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
