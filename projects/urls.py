from django.urls import path
from . import views

app_name='projects'
urlpatterns = [
    # path('project/',views.project,name='project'),
    path('new-project/',views.create_project,name='createProject'),
    path('tag-list/',views.tag_list,name='tagList')
]