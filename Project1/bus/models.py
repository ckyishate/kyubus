from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
import firebase_orm,firebase_admin
from firebase_admin import firestore

cred = credentials.Certificate('firebase-sdk.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
from django.conf import settings





class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=True, is_staff=False, is_admin=False):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.staff = is_staff
        user.admin = is_admin
        user.active = is_active
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email, 
            password=password,
            is_staff = True
        )
        
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
            is_staff = True,
            is_admin = True
        )
        
        user.save(using=self._db)
        return user


    ...

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser
    first_Name = models.CharField(max_length=255 )
    last_Name = models.CharField(max_length=255)
    sex = models.CharField(max_length=12, choices=(('Male','Male'),('Female','Female')))
    contact = models.CharField(max_length=100)

    # notice the absence of a "Password field", that is built in.

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.first_Name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin


class Bus(models.Model): 
    name = models.CharField(max_length= 100)
    plate_number = models.CharField(max_length=10)
    no_of_seats = models.IntegerField()
    driver_attached  = models.CharField(max_length=100)
    mech_status = models.CharField(max_length=20, choices =(('down','down'),('good','good'), ('poor','poor')))

    def __str__(self):
        return self.name 



class Routes(models.Model):
    source = models.CharField(max_length=200)
    destination = models.CharField(max_length= 150)
    departure = models.TimeField()
    date = models.DateField()
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    fare = models.IntegerField()
    bSeats = models.IntegerField(default=0)

    def __str__(self):
        return self.source + '-'+self.destination
    


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=20, choices =(('MobileMoney','MobileMoney'), ('CreditCard', 'CreditCard')))
    time_stamp = models.TimeField(default=timezone.now)
    
    def __str__(self):
        return self.payment_method

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default = timezone.now)
    seat = models.IntegerField()
    route = models.ForeignKey(Routes, on_delete=models.CASCADE)
    



class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    comment = models.TextField()
    timestamp = models.TimeField(default = timezone.now)
    reply = models.TextField(blank=True, null=True)
    