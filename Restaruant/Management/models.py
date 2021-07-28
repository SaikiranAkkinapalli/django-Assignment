from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.db.models.fields import BooleanField
class foodtype(models.Model):
    type=models.CharField(primary_key=True,max_length=255)
class item(models.Model):
    id=models.CharField(primary_key=True,max_length=255);
    Name=models.CharField(max_length=255);
    Remaining=models.IntegerField();
    price=models.FloatField();
    type=models.ForeignKey(foodtype,on_delete=models.CASCADE)
class table(models.Model):
    id=models.IntegerField(primary_key=True);
    Seating_Capacity=models.IntegerField();
    Available=models.BooleanField(default=True)
    presentbill=models.FloatField(default=0);
    totalbill=models.FloatField(default=0);
class UserManager(BaseUserManager):
    def create_user(self,first_name,last_name,Email,phonenumber,password):
        if not Email:
            return ValueError("User Must have an valid Email Address")
        if not phonenumber:
            return ValueError("User Must have an phonenumber")
        user=self.model(
            first_name=first_name,
            last_name=last_name,
            phonenumber=phonenumber,
            Email=self.normalize_email(Email))
        user.set_password(password)
        user.save(using=self.db)
        return user
    def create_superuser(self,first_name,last_name,Email,password,phonenumber):
        user=self.create_user(first_name,last_name,Email,phonenumber,password)
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self.db)
        return user
class UserModel(AbstractBaseUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    Email = models.EmailField(max_length=100,unique=True)
    phonenumber = models.CharField(max_length=20,primary_key=True)
    password = models.CharField(max_length=200)
    is_admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_superuser=models.BooleanField(default=False)
    objects=UserManager()
    USERNAME_FIELD='Email'
    REQUIRED_FIELDS=['phonenumber','password','first_name','last_name']
    def __str__(self):
        return self.first_name+self.last_name
    def has_perm(self,perm,obj=None):
        return self.is_admin
    def has_module_perms(self,app_label):
        return True





