"""
View of e_commerce_auth

View for login / Resgisterations forms
Authenticating users in login form
Creating new users and Customers in Registeration form

"""
#Libraries
from django.urls import reverse
from django.shortcuts import render_to_response, redirect, render
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,

    )
from .forms import UserLoginForm, UserRegisterForm,CustomerRegisterForm,editProfileForm

def login_view(request):
    """
    Authenticate users to get login
    :param request:
    :return: Return a login form
    """
    print(request.user.is_authenticated)
    next = request.GET.get('next')
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        #print(user.is_authenticated())
        if next:
            return redirect(next)
        return redirect("/")
    return render(request, "e_commerce_auth/login.html", {"form":form, "title": title})


def register_view(request):
    """
    Register a new User or Customer
    :param request:
    :return: Return a form containing Input Fields
    """
    if request.user.is_authenticated:
        return redirect(reverse('home'))
    print(request.user.is_authenticated)
    next = request.GET.get('next')
    title = "Register"
    userform = UserRegisterForm(request.POST or None)
    customerform = CustomerRegisterForm(request.POST or None,request.FILES)
    if userform.is_valid():
        user = userform.save(commit=False)
        password = userform.cleaned_data.get('password')
        user.set_password(password)
        user.first_name = userform.cleaned_data.get('first_name')
        user.last_name=userform.cleaned_data.get('last_name')
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        if customerform.is_valid():
            customer = customerform.save(commit=False)
            customer.user = user
            customer.city = customerform.cleaned_data.get('city')
            customer.country = customerform.cleaned_data.get('country')
            customer.address = customerform.cleaned_data.get('address')
            customer.phone_number = customerform.cleaned_data.get('phone_number')
            customer.date_of_birth = customerform.cleaned_data.get('date_of_birth')
            customer.user_image = customerform.cleaned_data.get('user_image')
            customer.save()
            if next:
                return redirect(next)
            return redirect("/")


    context = {
        "userform": userform,
        "customerform":customerform,
        "title": title
    }
    return render(request, "e_commerce_auth/signup.html", context)

def profile(request):
    title = "Update Profile"
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = editProfileForm(request.POST ,request.FILES,instance=request.user.customer_user)

            if form.is_valid():
                form.save()
                return redirect('')
        else:
            form = editProfileForm(instance=request.user.customer_user)
    print(form)
    return render(request,"e_commerce_auth/edit_profile.html", {"form":form, "title": title})



def logout_user(request):
    """Logout Function"""
    if request.user.is_authenticated:
        logout(request)
    return redirect(reverse('home'))


