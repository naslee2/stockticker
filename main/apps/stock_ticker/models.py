from __future__ import unicode_literals
from django.db import models
from datetime import datetime
from time import gmtime, strftime
import re, bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX=re.compile(r'^[a-zA-Z0-9]+$')

class UserManager(models.Manager):
    def validator(self, postData):
        errors={}
        #Username checker
        if len(postData['username']) < 3:
            errors['username'] = "Name should be at least 4 characters long!"
        
        #Email checker
        if EMAIL_REGEX.match(postData['email']):
            duplicate = User.objects.filter(email=postData['email'])
            if len(dup) > 0:
                errors['email'] = "Email is already registered!"
        else:
            errors['email'] = "Must put in a valid email!"

        #password checker
        if len(postData['password']) < 7:
            errors['password'] = "Password should be at least 8 characters long!"
        elif not PASSWORD_REGEX.match(postData['password']):
            error['password'] = "Password must have numbers and letters!"
        
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

        

class User(models.Model):
    username=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=45)
    date_registered = models.DateTimeField()
    date_added = models.DateTimeField(auto_now_add = True)
    objects= UserManager()
