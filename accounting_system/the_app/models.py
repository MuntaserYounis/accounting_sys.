from django.db import models
import bcrypt
import re
from datetime import datetime, date,timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django import forms

class MerchantManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if len(postData['first_name'])< 2 or not postData['first_name'].isalpha():
            errors['first_name'] = 'first name should be more than 2 characters'
        if len(postData['last_name'])< 2 or not postData['last_name'].isalpha():
            errors['last_name'] = 'last name should be more than 2 characters'
        if len(postData['password']) < 8:
            errors['password'] = 'password should be at least 8 characters'
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if postData['password'] != postData['confirm']:
            errors['password'] = 'Passwords are not matching '
        return errors
    def login_validator(self,postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors2={}
        email2= postData['email2']
        password2 = postData['password2']
        merch = Merchant.objects.filter(email=email2)
        if len(email2)<1:
            errors2['email2'] = 'Email cannot be empty'
        elif not EMAIL_REGEX.match(email2):
            errors2['email2'] = 'Invalid email'
        elif not bcrypt.checkpw(password2.encode(), merch[0].password.encode()):
            errors2['password'] = 'incorrect password'
        return errors2

class CarManager(models.Manager):
    def car_validator(self,postData):
        errors3 = {}
        if len(postData['the_type']) < 1 : 
            errors3['the_type'] = 'Please enter a car model'
        if int(postData['man_year'])<2013:
            errors3['man_year'] = 'you can not rent a car that was manufactured before 2013'
        if int(postData['insurance']) <1:
            errors3['insurance'] = 'All cars must have insurance'
        if not postData['acquiring_date']:
            errors3['acquiring_date'] = 'Please select an acquiring date'
            
        return errors3

class ClientManager(models.Manager):
    def client_validator(self,postData):
        errors4 = {}
        if len(postData['cl_fname']) < 1:
            errors4['cl_fname'] = 'Client should have last name filled'
        if len(postData['cl_lname']) < 1:
            errors4['cl_lname'] = 'Client should have last name filled'
        if len(postData['nat_id']) < 9:
            errors4['nat_id'] = 'National ID should consist of 9 digits'
        if len(postData['cell_number'])< 10:
            errors4['cell_number'] = 'cellphone number should be 10 numbers at least'    

class Merchant(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MerchantManager()

class Car(models.Model):
    the_type = models.CharField(max_length=255)
    man_year = models.IntegerField(default= 2020,validators=[MinValueValidator(2013), MaxValueValidator(2024)])
    rent_price = models.IntegerField()
    insurance = models.IntegerField()
    maintenance = models.IntegerField(default=0)
    payments = models.IntegerField(default=0)
    acquiring_date = models.DateField()
    rent_status = models.BooleanField(default=True)
    variable_cost = models.IntegerField(default=0, editable=False)
    owned_by = models.ForeignKey(Merchant,related_name='cars_owned',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CarManager()

    def save(self, *args, **kwargs):
        self.variable_cost = (self.maintenance/30) + (self.payments/30) + (self.insurance/360)
        super().save(*args, **kwargs)


class Client(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    nat_id = models.IntegerField()
    cell_number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ClientManager()

class Rental(models.Model):
    client = models.ForeignKey(Client,on_delete=models.CASCADE)
    car = models.ForeignKey(Car,related_name = 'rental',on_delete=models.CASCADE)
    return_date =   models.DateField() 
    actual_return_date =  models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    


    # def mark_as_returned(self):
    #     self.car.rent_status = True
    #     self.car.save()
    #     self.actual_return_date = timezone.now()
    #     self.save()


    