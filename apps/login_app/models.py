from __future__ import unicode_literals
from django.db import models
import bcrypt
import re	# the regex module

# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class UserManager(models.Manager):
    def register_validator(self,postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First Name should be atleast 2 characters"
        elif not postData['first_name'].isalpha():
            errors['first_name'] = "First Name should be alphabets only"

        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last Name should be atleast 2 characters"
        elif not postData['last_name'].isalpha():
            errors['last_name'] = "Last Name should be alphabets only"

        if len(postData['email']) < 1:
            errors['email'] = "Email should not be empty"
        elif not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern
            errors['email'] = "Invalid Email"
        elif User.objects.filter(email = postData['email']):
            errors['email'] = "Email address already exists. Choose a different email id"

        if len(postData['password']) < 8:
            errors['password'] = "Password should be atleast 8 characters"

        if len(postData['confirm_password']) < 8:
            errors['confirm_password'] = "Confirm Password should be atleast 8 characters"
        elif postData['confirm_password'] != postData['password']:
            errors['confirm_password'] = "Confirm Password should be match Password entered"

        return errors
        

    def login_validator(self,postData):
        user = User.objects.filter(email = postData['login_email'])
        errors = {}

        if len(postData['login_email']) < 1:
            errors['email'] = "Email should not be empty"
        elif not EMAIL_REGEX.match(postData['login_email']):    # test whether a field matches the pattern
            errors['email'] = "Invalid Email address"
        elif not user:
            errors['email'] = "No account found with the given email address! Please register to create an account."

        if len(postData['login_password']) < 8:
            errors['password'] = "Password should be atleast 8 characters"
        elif user and not bcrypt.checkpw(postData['login_password'].encode(), user[0].pass_hash.encode()):
            errors['password'] = "Password doesn't match"
        
        return errors

   
class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    pass_hash = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

    def __repr__(self):
        return f"User: {self.first_name}"

