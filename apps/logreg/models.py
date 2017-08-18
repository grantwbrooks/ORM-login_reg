from __future__ import unicode_literals
from django.db import models
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'[0-9]')
PASS_REGEX = re.compile(r'.*[A-Z].*[0-9]')

class RegistrationManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        if len(postData['f_name']) < 2:
            errors["fname"] = "First name should be more than 2 characters"
        if len(postData['l_name']) < 2:
            errors["lname"] = "Last name should be more than 2 characters"
        if NAME_REGEX.search(postData['f_name']):
            errors["fname_numb"] = "First name cannot contain any numbers"
        if NAME_REGEX.search(postData['l_name']):
            errors["lname_numb"] = "Last name cannot contain any numbers"
        
        if len(postData['user_email']) < 1:
            errors["email_len"] = "Email is required"
        if len(postData['user_email']) > 0 and not EMAIL_REGEX.match(postData['user_email']):
            errors["email_format"] = "Email must be a valid email"
        try:
            user_record = User.objects.get(email = postData['user_email'])
            errors["email_exist"] = "Email already exists"
        except:
            pass

        
        if len(postData['pass']) < 1:
            errors["pass_len"] = "Password is required"
        if len(postData['pass']) > 0 and not PASS_REGEX.search(postData["pass"]):
            errors["pass_format"] = "Password must have a number and an uppercase letter"
    
        if postData["pass"] != postData["confirm_password"]:
            errors["pass_confirm"] = "Password and Password Confirmation should match"
        
        return errors



    def login_validator(self, postData):
        errors = {}
        try:
            user_record = User.objects.get(email = postData['user_email'])
            if not bcrypt.checkpw(postData['pass'].encode(), user_record.password.encode()):
                errors["pass_invalid"] = "Wrong Password"
        except:
            errors["email_not"] = "User does not exist"

        return errors



class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = RegistrationManager()
    # def __str__(self):         # provides human readable version of output
    #     return self.email
