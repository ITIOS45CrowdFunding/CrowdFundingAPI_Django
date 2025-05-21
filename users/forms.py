from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from django.forms.widgets import ClearableFileInput
from .models import Profile
from django.contrib.auth import get_user_model
User = get_user_model()

egyption_number=RegexValidator(
    regex=r'^01[0-2,5]{1}[0-9]{8}$',
    message="Please Enter a Valid Egyption Number"
)
class SignUpForm(UserCreationForm):
    #field i want to add it in user model
    first_name=forms.CharField(max_length=255,required=True,widget=forms.TextInput(attrs={
        'placeholder':'Enter Your First Name',
        'class':'w-full p-4 rounded-lg bg-white'
    }))
    last_name=forms.CharField(max_length=255,required=True,widget=forms.TextInput(attrs={
        'placeholder':'Enter Your Last Name',
        'class':'w-full p-4 rounded-lg bg-white'
    }))
    username=forms.CharField(max_length=255,required=True,widget=forms.TextInput(attrs={
        'placeholder':'Enter Your First Name',
        'class':'w-full p-4 rounded-lg bg-white'
    }))
    email=forms.CharField(max_length=100,required=True,widget=forms.EmailInput(attrs={
         'placeholder':'Enter Your Email',
        'class':'w-full p-4 rounded-lg bg-white'
    }))
    password1=forms.CharField(required=True,widget=forms.PasswordInput(attrs={
        'placeholder':'Enter Your Password',
        'class':'w-full p-4 rounded-lg bg-white',
        'type':'password'
    }))
    password2=forms.CharField(required=True,widget=forms.PasswordInput(attrs={
        'placeholder':'Confirm Your Password',
        'class':'w-full p-4 rounded-lg bg-white',
        'type':'password'
    }))
    mobile_phone=forms.CharField(max_length=14,required=True,validators=[egyption_number],widget=forms.TextInput(attrs={
        'placeholder':'Enter Your Phone Number',
        'class':'w-full p-4 rounded-lg bg-white'
    }))
    image = forms.ImageField(
        required=True,
        widget=ClearableFileInput(attrs={  
            'class': 'w-full p-4 rounded-lg bg-white'
        })
    )
     
    

    class Meta:
        model=User
        fields=['first_name','last_name','username','email','password1','password2','mobile_phone','image']
    
class LoginForm(forms.Form):
    email=forms.CharField(max_length=100,required=True,widget=forms.EmailInput(attrs={
         'placeholder':'Enter Your Email',
        'class':'w-full p-4 rounded-lg bg-white'
    }))
    password1=forms.CharField(required=True,widget=forms.PasswordInput(attrs={
        'placeholder':'Enter Your Password',
        'class':'w-full p-4 rounded-lg bg-white',
        'type':'password'
    }))
    class Meta:
        Model=User
        fields=['email','password1']