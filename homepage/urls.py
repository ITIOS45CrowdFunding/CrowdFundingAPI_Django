from django.urls import path
from . import views

app_name='home'

urlpatterns = [
    path("", views.home),
    path("category/<int:category_id>/", views.category, name="category"),
    # path("search/", views.search, name="search"),
    # path("project_list/", views.project_list, name="project_list"),
]
