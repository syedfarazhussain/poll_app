from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponseRedirect

# Create your views here.
def signup(request):
  if request.method == 'POST':
    if request.POST['password'] == request.POST['confirmpassword']:
      try:
        user = User.objects.get(username = request.POST['username'])
        return render(request, 'signup.html', {'error' : 'Username has been already taken'})
      except User.DoesNotExist:
        user = User.objects.create_user(username =request.POST['username'], password=request.POST['password'])
        auth.login(request, user)
        return redirect('home')
    else:
      return render(request, 'signup.html', {'error' : 'Passwords must match'})

  else:
    return render (request, 'signup.html')

def login(request):
  next = request.GET.get('next', None)
  if request.method == 'POST':
    user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
    if user is not None:
      auth.login(request, user)
      if next:
        return redirect(next)
      return redirect('home')
    else:
      return render(request, 'login.html', {'error': 'username or password is incorrect.'})
  else:
    return render (request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('home')