from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name='projects'
urlpatterns = [
    path('',views.base,name='index'),
    path('project_details/<int:project_id>/',views.project_detail,name='details'),
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
