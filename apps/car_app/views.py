# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect #HttpResponse
from django.contrib import messages
from .models import User

def index(request):
    return render(request, 'car_app/index.html')

def home(request):
    print "reached home"
    return render(request, 'car_app/home.html')

#create user POST 
def register_process(request):
    if request.method == "POST":
        postData = {
            'username' : request.POST['username'],
            'password' : request.POST['password'],
            'confirm_password' : request.POST['confirm_password'],
        }
        #validate and add user
        user = User.objects.add_user(postData)
        #if user added
        if user[0]:
            request.session['login'] = user[1].id
        else:
            errors = user[1]
            for error in errors:
                messages.add_message(request, messages.INFO, error)
            return redirect('/')

        #if user created
        if user[0] == True:
            request.session['login'] = user[1].id
            return redirect('/home')
        #if user was not created
        else:
            errors = user[1]
            for error in errors:
                messages.add_message(request, messages.INFO, error)
            return redirect('/')

def login(request):
    if request.method == "POST":
        postData = {
            'username' : request.POST.get('username', False),
            'password' : request.POST['password']
        }
        #check for user and login
        user = User.objects.login_user(postData)
        #if login was successful
        if user[0]:
            request.session['login'] = user[1]
            return redirect('/home')
        else:
            messages.add_message(request, messages.INFO, 'Invalid login')
            return redirect('/')