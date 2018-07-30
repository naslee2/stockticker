from __future__ import unicode_literals
from django.db import models
from datetime import datetime
from time import gmtime, strftime
import re, bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX=re.compile(r'^[a-zA-Z0-9]+$')

class UserManager(models.Manager):
    def validator(self, postData): #registeration validator
        errors={}
        #Username checker
        if len(postData['username']) < 3:
            errors['username'] = "Name should be at least 4 characters long!"
        else:
            username_dup = User.objects.filter(username=postData['username'])
            if len(username_dup) > 0:
                errors['username'] = "That username is already registered!"
        
        #Email checker
        if EMAIL_REGEX.match(postData['email']):
            duplicate = User.objects.filter(email=postData['email'])
            if len(duplicate) > 0:
                errors['email'] = "That email is already registered!"
        else:
            errors['email'] = "Must put in a valid email!"

        #password checker
        if len(postData['password']) < 7:
            errors['password'] = "Password should be at least 8 characters long!"
        elif not PASSWORD_REGEX.match(postData['password']):
            errors['password'] = "Password must have numbers and letters!"
        
        #confirm password checker
        if len(postData['confirm_password']) < 7:
            errors['confirm_password'] = "Passwords must both be the same!"
        elif not PASSWORD_REGEX.match(postData['confirm_password']):
            errors['confirm_password'] = "Passwords must both be the same!"
        elif not postData['password'] == postData['confirm_password']:
            errors['confirm_password'] = "Passwords must both be the same!"
        if len(errors) < 1:
            reg_hash = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            reg_user = User.objects.create(username=postData['username'], email=postData['email'], password=reg_hash)
            errors['valid_user'] = reg_user

        return errors
    
    def validator2(self, postData):
        errors2= {}
        login_check = User.objects.filter(username=postData['login_username'])
        if login_check:
            email_check = login_check[0].email
            password_check = login_check[0].password
            if bcrypt.checkpw(postData['login_password'].encode(), password_check.encode()):
                errors2['success'] = login_check[0]
                return errors2
            else:
                errors2['login_password'] = "Incorrect Login and/or Password"
                return errors2
        else:
            errors2['login_password'] = "Incorrect Login and/or Password"
            return errors2

class User(models.Model):
    username=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=45)
    date_added = models.DateTimeField(auto_now_add = True)
    objects= UserManager()
