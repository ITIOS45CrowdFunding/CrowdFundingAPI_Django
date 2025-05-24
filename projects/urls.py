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
    path('<int:project_id>/report', views.report_project, name='report_project'),
    # path('<int:project_id>/rate', views.rate_project, name='rate_project'),
    path('tag-list/',views.tag_list,name='tagList'),
    path('my-projects/',views.my_projects,name='my_projects'),
    path('<int:project_id>/edit',views.edit_project,name='edit_project'),
    path('projects/image/<int:image_id>/delete/', views.delete_image, name='delete_image')

]
