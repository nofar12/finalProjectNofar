# homepage/views.py
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def home1(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())

    #return HttpResponse("hello")
def home2(request):
    #template = loader.get_template('home.html')
    #return HttpResponse(template.render())

    return HttpResponse("hello")