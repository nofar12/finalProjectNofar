from django.shortcuts import render
from .forms import UserRegistrationForm

def signUp_user(request): #if user sumbit the sign up form
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')  # Redirect to success page
    else:
        form = UserRegistrationForm()
    return render(request, 'signUp.html', {'form': form})
