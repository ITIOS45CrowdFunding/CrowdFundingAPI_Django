from django.shortcuts import render,redirect,HttpResponse
from .forms import SignUpForm,LoginForm
from .models import Profile
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from .token import activation_token
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate,login as auth_login
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView

from django.urls import reverse_lazy

User = get_user_model()
# Create your views here.

def signUp(request):
    form=SignUpForm()
    if request.method=='POST':
        form=SignUpForm(request.POST,request.FILES)
        if form.is_valid():
            user=form.save(commit=False)
            # i want to activate when you click to activation link
            user.is_active=False
            user.save()
            profile=Profile.objects.create(
                user=user,
                phone=form.cleaned_data['mobile_phone'],
                image=form.cleaned_data['image']
            )
            profile.save()


            # sending activation link
            uid = urlsafe_base64_encode(force_bytes(user.pk)) 
            token=activation_token.make_token(user)
            activation_link=request.build_absolute_uri(
                reverse('users:activate', kwargs={'uidb64': uid, 'token': token})
            )
            subject="Activation Your Account "
            message=f"{user.username} please click to activate Your Account :{activation_link}"
            send_mail(subject,message,settings.DEFAULT_FROM_EMAIL,[user.email])
            # request.session['newuser']=user.username
            return redirect("users:activateMessage")
    return render(request,'users/signup.html',{'form':form})

def activate(request,uidb64,token):
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        user=User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user and activation_token.check_token(user,token):
        user.is_active=True
        user.save()
        return redirect("users:login")
    else:
        return render(request, 'users/activation_error.html')

def login(request):
    form=LoginForm(request.POST or None)
    error=None
    if request.method=='POST' and form.is_valid():
        email=form.cleaned_data['email']
        password=form.cleaned_data['password1']
        user=authenticate(request,email=email,password=password)
        if user is not None:
            if user.is_active:
                auth_login(request,user)
                return redirect("home:home")
            else:
                error="Account is not Activated Yet , Please Check Your mail"
        else:
            error="Invalid email or Password"
    return render(request,'users/login.html',{'form':form,'error':error})

def activate_page(request):
    username=request.session.pop('newuser')
    return render(request,'users/activate_email.html',{'username':username})

class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset.html'
    success_url = reverse_lazy('users:password_reset_done')
    email_template_name = 'registration/password_reset_email.txt'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    html_email_template_name = 'registration/password_reset_email.html' 

    def form_valid(self, form):
        # Save email to session
        self.request.session['reset_email'] = form.cleaned_data.get('email')
        return super().form_valid(form)


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['email'] = self.request.session.get('reset_email', '')
        return context