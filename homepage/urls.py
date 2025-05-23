from django.urls import path
from . import views

app_name='home'

urlpatterns = [
    path("", views.home, name="home"),
    path("category/<int:category_id>/", views.category, name="category"),
    path("autocomplete", views.autocompelete, name="autocomplete")
]
