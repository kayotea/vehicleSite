# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt

# Create your models here.
USERNAME_REGEX = re.compile(r'[a-zA-Z0-9.+_-]{3,50}')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PWD_REGEX = re.compile(r'^.{8,50}$')
DATE_REGEX = re.compile(r'^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$')

ITEM_REGEX = re.compile(r'^.{3,50}$')
DEFAULT_USER = 1

class UserManager(models.Manager):
    def add_user(self, postData):
        username = postData['username']
        pwd = postData['password']
        c_pwd = postData['confirm_password']


        error = []
        #input validations
        if not USERNAME_REGEX.match(username):
            error.append('Username must be at least 3 characters.')
        if User.objects.filter(username=username):
            error.append('User with that username already exists')
        if not PWD_REGEX.match(pwd):
            error.append('Password must be at least 8 characters')
        if pwd != c_pwd:
            error.append('Passwords do not match!')
        #check that username does not already exist
        
        #if no errors, create user
        if len(error) == 0:
            pwd = pwd.encode('utf-8')
            hashed_pwd = bcrypt.hashpw(pwd, bcrypt.gensalt())
            u = User.objects.create(username=username, password=hashed_pwd)
            return [True, u]
        #else don't create user, return errors
        else:
            return [False, error]

    def login_user(self, postData):
        username = postData['username']
        pwd = postData['password'].encode('utf-8')
        #look for match in registered usersd
        users = User.objects.all()
        for user in users:
            user.password = user.password.encode('utf-8')
            if username == user.username and bcrypt.hashpw(pwd, user.password) == user.password:
                return [True, user.id]
        return [False, False]

class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __unicode__(self):
        return 'id: '+str(self.id)