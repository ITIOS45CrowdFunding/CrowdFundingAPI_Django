from django.urls import path
from . import views

app_name='home'

urlpatterns = [
    path("", views.home, name="home"),
    path("category/<int:category_id>/", views.category, name="category"),
    # path("search/", views.search, name="search"),
    path("projects_list/", views.project_list, name="projects_list"),
]
