from django.shortcuts import render
from datetime import datetime
from projects.models import ProjectCategory, Project, ProjectImage, Tag, Rating
from django.db.models import Avg
from django.db.models import Q
from django.http import JsonResponse

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
    search = request.GET.get('search')
    
    projects = []
    
    if search:
        projects = Project.objects.filter(Q(title__icontains=search) | Q(tags__name__icontains=search)).distinct()
    else:
        projects = Project.objects.filter(isCancelled=False).order_by('-startDate')
    
    return render(request, 'homepage/projects_list.html', {
        'search': search,
        'projects': projects
    })
    
    
def autocompelete(request):
    search = request.GET.get('search', '').strip()
    
    results = []
    
    if search:
        title_matches = Project.objects.filter(title__icontains=search).values_list('title', flat=True)
        tag_matches = Tag.objects.filter(name__icontains=search).values_list('name', flat=True)
        results = list(set(title_matches) | set(tag_matches))[:10]
        
    return JsonResponse({'suggestions': results})
    
