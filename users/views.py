from django.shortcuts import render, redirect, HttpResponse
from .forms import SignUpForm, LoginForm, ProfileForm, UserForm
from .models import Profile
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from .token import activation_token
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView
from projects.models import Project, Donation
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout

User = get_user_model()
# Create your views here.


def signUp(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            # i want to activate when you click to activation link
            user.is_active = False
            user.save()
            profile = Profile.objects.create(
                user=user,
                phone=form.cleaned_data["mobile_phone"],
                image=form.cleaned_data["image"],
            )
            profile.save()

            # sending activation link
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = activation_token.make_token(user)
            activation_link = request.build_absolute_uri(
                reverse("users:activate", kwargs={"uidb64": uid, "token": token})
            )

            subject = "Activation Your Account "
            message = f"{user.username} please click to activate Your Account :{activation_link}"
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
            request.session["newuser"] = user.username

            return redirect("users:activateMessage")
    return render(request, "users/signup.html", {"form": form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user and activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect("users:login")
    else:
        return render(request, "users/activation_error.html")


def login(request):
    form = LoginForm(request.POST or None)
    error = None
    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password1"]
        user = authenticate(request, email=email, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return redirect("home:home")
            else:
                error = "Account is not Activated Yet , Please Check Your mail"
        else:
            error = "Invalid email or Password"
    return render(request, "users/login.html", {"form": form, "error": error})


def activate_page(request):

    username = request.session.pop("newuser")
    return render(request, "users/activate_email.html", {"username": username})


@login_required
def view_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    # projects=Project.objects.filter(user=request.user)
    projects = [{"title": "new project", "details": "a new project added successfully"}]
    # donations=Donation.objects.filter(user=request.user)

    donations = [
        {"title": "new donation", "details": "a new donation added successfully"}
    ]
    return render(
        request,
        "users/profile.html",
        {"profile": profile, "projects": projects, "donations": donations},
    )


@login_required
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    form = ProfileForm()
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully")
            return redirect("users:profile")
    else:
        form = ProfileForm(instance=profile)
    return render(request, "users/edit_profile.html", {"form": form})


def edit_all_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    profile_form = ProfileForm()
    user_form=UserForm()
    user=request.user
    if request.method == "POST":
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        user_form = UserForm(request.POST, instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request, "Profile updated successfully")
            return redirect("users:profile")
    else:
        profile_form = ProfileForm(instance=profile)
        user_form = UserForm(instance=user)
    return render(
        request,
        "users/edit_all_profile.html",
        {"profile_form": profile_form, "user_form": user_form,'profile':profile},
    )


@login_required
def delete_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    user = request.user
    if request.method == "POST":
        if request.POST.get("confirm") == "yes":
            profile.delete()
            user.delete()
            logout(request)
            messages.success(request, "profile deleted successfully")
            return redirect("home:home")
    return render(request, "users/delete_profile.html")


class CustomPasswordResetView(PasswordResetView):
    template_name = "registration/password_reset.html"
    success_url = reverse_lazy("users:password_reset_done")
    email_template_name = "registration/password_reset_email.html"
    subject_template_name = "registration/password_reset_subject.txt"
    html_email_template_name = "registration/password_reset_email.html"

    def form_valid(self, form):
        # Save email to session
        self.request.session["reset_email"] = form.cleaned_data.get("email")
        return super().form_valid(form)


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "registration/password_reset_done.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["email"] = self.request.session.get("reset_email", "")
        return context
