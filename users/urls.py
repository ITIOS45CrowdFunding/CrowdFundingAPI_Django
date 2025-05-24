from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .views import CustomPasswordResetView, CustomPasswordResetDoneView
from django.contrib.auth.views import LogoutView


app_name='users'
urlpatterns = [
    path('signup/',views.signUp,name='signup'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('activate_email/',views.activate_page,name="activateMessage"),
    path('login/',views.login,name='login'),
      path('password-reset/',
         CustomPasswordResetView.as_view(),
         name='password_reset'),
    
    path('password-reset/done/',
         CustomPasswordResetDoneView.as_view(),
         name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html',
             success_url=reverse_lazy('users:password_reset_complete')
         ), 
         name='password_reset_confirm'),
    
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ), 
         name='password_reset_complete'),
    path('logout/', LogoutView.as_view(next_page='users:login'), name='logout'),
    path('profile/',views.view_profile,name="profile"),
    path('profile/edit',views.edit_profile,name='edit_profile'),
    path('profile/delete',views.delete_profile,name='delete_profile')
         
]