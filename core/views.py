from django.shortcuts import render, redirect
#
from .forms import RegisterForm, UpdateProfileForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
from blogapp.models import Blog


# Create your views here.

def signup(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST) #get content of the form
        if form.is_valid(): #check if form is valid
            form.save()
            messages.success(request, "Account created successfully")
            return redirect("index")
        # else:
        #     messages.error(request, "Ooops Sorry! An error occured")
        #     return redirect("index")
        
    context = {"form":form}
    # context = {}
    return render(request, "core/signup.html", context)




def signin(request):
    if request.method == 'POST': #when post method
        email = request.POST["email"] #get value of email field
        password = request.POST["password"] #get value of password field
        
        user = authenticate(request, email=email, password=password) #check if user is in db
        if user is not None:
            login(request, user) #login user
            return redirect("index")
        
        else:
            messages.warning(request, "Invalid credentials")
            return redirect("signin")
        
    context = {}
    return render(request, "core/login.html", context)



def signout(request):
    logout(request)
    return redirect("index")


@login_required(login_url="signin")
def profile(request):
    user = request.user
    blogs = Blog.objects.filter(user=user)
    context={"user": user, "blogs": blogs}
    # context = {}
    return render(request, "core/profile.html", context)


@login_required(login_url="signin")
def update_profile(request):
    if request.user.is_authenticated:
        user = request.user
        form = UpdateProfileForm(instance=user)
        if request.method == 'POST':
            form = UpdateProfileForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile updated successfully")
                return redirect("profile")
        
        
    context = {"form": form}
    # context = {}
    return render(request, "core/update_profile.html", context)
