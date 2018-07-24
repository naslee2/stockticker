from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request): #Index Page
    return render(request, "index.html")

def dashboard(request):
    return render(request, 'dashboard.html')

def login(request):

def register(request):

def logout(request):