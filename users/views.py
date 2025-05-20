from django.shortcuts import render,redirect
from .forms import SignUpForm
from .models import Profile
# Create your views here.

def signUp(request):
    form=SignUpForm()
    if request.method=='POST':
        form=SignUpForm(request.POST,request.FILES)
        if form.is_valid():
            user=form.save()
            profile=Profile.objects.create(
                user=user,
                phone=form.cleaned_data['mobile_phone'],
                image=form.cleaned_data['image']
            )
            profile.save()
            return redirect("users:login")
    return render(request,'users/signup.html',{'form':form})

def login(request):
    return render(request,'users/login.html')