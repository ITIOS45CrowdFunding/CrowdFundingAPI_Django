from django.urls import path
from . import views

app_name='users'
urlpatterns = [
    path('signup/',views.signUp,name='signup'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('activate_email/',views.activate_page,name="activateMessage"),
    path('login/',views.login,name='login')
    
]