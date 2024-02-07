from django.shortcuts import render

def findRecipe(request):
    return render(request, 'findRecipe.html')