from django.shortcuts import render
from django.http import HttpResponse
from .models import Project, ProjectCategory, Tag, ProjectTag, ProjectImage, Donation, Report, Rating, Comment
from datetime import date
# Create your views here.
def base(request):
    return render(request, 'projects/index.html')

def project_detail (request, project_id):
    # Logic to retrieve project details using project_id
    # For example, you might fetch the project from the database
    project = Project.objects.get(id=project_id)
    # You can also fetch related data like images, tags, etc.
    images = ProjectImage.objects.filter(project=project)
    tags = ProjectTag.objects.filter(project=project)
    donations = Donation.objects.filter(project=project)
    reports = Report.objects.filter(project=project)
    ratings = Rating.objects.filter(project=project)
    comments = Comment.objects.filter(project=project)
    
    

    # Render a template with the project details
    return render(request, 'projects/project_details.html', {
        'project': project,
        'images': images,
        'tags': tags,
        'donations': donations,
        'reports': reports,
        'ratings': ratings,
        'comments': comments
    })