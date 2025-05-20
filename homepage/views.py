from django.shortcuts import render
from datetime import datetime, timedelta
import random

def home(request):
    featured_projects = []
    for i in range(4):
        featured_projects.append({
            'id': i+1,
            'title': f"Featured Project {i+1}",
            'short_description': f"Help us achieve our goal for project {i+1}",
            'current_amount': random.randint(10000, 100000),
            'total_target': random.randint(100000, 500000),
            'image_url': f"homepage/images/project{i+1}.jpg",
            'progress_percentage': random.randint(20, 80),
            'category': {"name": "test"}
        })
        
    categories = [
        {"name": "Technology"},
        {"name": "Health"},
        {"name": "Education"},
        {"name": "Environment"},
        {"name": "Art"},
        {"name": "Community"}
    ]
    
    return render(request, 'homepage/home.html', {
        'featured_projects': featured_projects
        , 'categories': categories
    })
    
    
