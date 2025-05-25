from django.urls import path
from . import views
from homepage import views as home_views
app_name = 'projects'

urlpatterns = [
    path('', home_views.project_list, name='projects_list'),
    path('new-project/',views.create_project,name='create_project'),
    path('<int:project_id>', views.project_details, name='project_details'),
    path('<int:project_id>/cancel', views.cancel_project, name='cancel_project'),
    path('<int:project_id>/donate', views.donate, name='donate'),
    path('project/<int:project_id>/add-rating/', views.add_rating, name='add_rating'),
    path('project/<int:project_id>/add-comment/', views.add_comment, name='add_comment'),
    path('<int:project_id>/get_ratings/', views.get_ratings, name='get_ratings'),
    path('<int:project_id>/get_comments/', views.get_comments, name='get_comments'),
    path('<int:project_id>/report', views.report_project, name='report_project'),
    path('tag-list/',views.tag_list,name='tagList'),
    path('my-projects/',views.my_projects,name='my_projects'),
    path('<int:project_id>/edit',views.edit_project,name='edit_project'),
    path('projects/image/<int:image_id>/delete/', views.delete_image, name='delete_image'),
    path('reported-projects/', views.reported_projects, name='reported_projects'),
    path('project-reports/<int:project_id>/', views.project_reports, name='project_reports'),
    path('reported-comments/', views.reported_comments, name='reported_comments'),
    path('delete-comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('report-comment/<int:comment_id>/', views.report_comment, name='report_comment'),
    path('<int:project_id>/delete/', views.delete_project, name='delete_project'),
]
