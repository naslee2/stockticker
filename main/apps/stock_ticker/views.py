from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request): #Index Page
  return render(request, "index.html")

def dashboard(request):
  if 'id' not in request.session:
    return redirect('/index')
  else:
    return render(request, 'dashboard.html')

def register(request):
  if request.method == "POST":
    errors = User.objects.validator(request.POST)
    if 'valid_user' in errors:
      request.session['register_email'] = errors['valid_user'].email
      request.session['name'] = errors['valid_user'].username
      request.session['id'] = errors['valid_user'].id
      return redirect('/dashboard')
    else:
      for tag, error in errors.iteritems():
        messages.error(request, error, extra_tags=tag)
      return redirect('/index')
  else:
    return redirect('/index')

def login(request):
  if request.method == "POST":
    errors2 = User.objects.validator2(request.POST)
    if 'success' in errors2:
      request.session['username'] = errors2['success'].username
      request.session['email'] = errors2['success'].email
      request.session['id'] = errors2['success'].id
      return redirect('/dashboard')
    else:
      for tag, error in errors2.iteritems():
        messages.error(request, error, extra_tags=tag)
      return redirect('/index')
  else: 
    return redirect('/index')


def logout(request):
  request.session.clear()
  return redirect('/index')