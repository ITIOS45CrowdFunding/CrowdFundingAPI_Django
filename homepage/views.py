from django.shortcuts import render
from datetime import datetime, timedelta
import random
from projects.models import ProjectCategory, Project, ProjectImage, Tag, Rating
from django.db.models import Avg
from django.db.models import Q

def home(request):
    current_date = datetime.now().date()
    highest_rated_projects = Project.objects.filter(isCancelled=False, endDate__gte=current_date).annotate(avg_rating=Avg("rating__value")).order_by('-avg_rating')[:5]
    latest_projects = Project.objects.filter(isCancelled=False).order_by('-startDate')[:5]
    featured_projects = Project.objects.filter(isFeatured=True, isCancelled=False).order_by('-startDate')[:5]
    categories = ProjectCategory.objects.all()
        
    return render(request, 'homepage/home.html', {
        'highest_rated_projects': highest_rated_projects, 
        'latest_projects': latest_projects,
        'featured_projects': featured_projects, 
        'categories': categories
    })
    
    
def category(request, category_id):
    category = ProjectCategory.objects.get(id=category_id)
    projects = Project.objects.filter(category=category, isCancelled=False).order_by('-startDate')
    
    return render(request, 'homepage/category.html', {
        'projects': projects,
        'category': category
    })
    
    
def project_list(request):
    projects = Project.objects.filter(isCancelled=False).order_by('-startDate')
    
    return render(request, 'homepage/projects_list.html', {
        'projects': projects
    })
