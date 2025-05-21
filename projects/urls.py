from django.urls import path
from . import views
app_name = 'projects'

urlpatterns = [
    path('', views.index, name='index'),
    path('new-project/',views.create_project,name='create_Project'),
    path('<int:project_id>', views.details, name='details'),
    path('<int:project_id>/update', views.update_project, name='update_project'),
    path('<int:project_id>/cancel', views.cancel_project, name='cancel_project'),
    path('<int:project_id>/donate', views.donate, name='donate'),
    path('<int:project_id>/comment', views.add_comment, name='add_comment'),
    path('<int:project_id>/report', views.report_project, name='report_project'),
    path('<int:project_id>/rate', views.rate_project, name='rate_project'),
    path('tag-list/',views.tag_list,name='tagList')

]
