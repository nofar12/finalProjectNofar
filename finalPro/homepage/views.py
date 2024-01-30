# homepage/views.py
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def home1(request):
    return render(request, 'home.html')