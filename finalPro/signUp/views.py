from django.shortcuts import render
from .forms import UserRegistrationForm
from .models import UserProfile


def signUp_user(request): #adding the data to the database of users
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            #return redirect('success')  # Redirect to success page
    else:
        form = UserRegistrationForm()


    return render(request, 'signUp.html', {'form': form})


