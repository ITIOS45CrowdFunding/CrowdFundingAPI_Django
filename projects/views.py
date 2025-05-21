import json
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ProjectForm
from .models import Tag, ProjectImage, Project
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from .models import Project, ProjectCategory, Tag, ProjectTag, ProjectImage, Donation, Report, Rating, Comment
from datetime import date
from django.db import models

def create_project(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = User.objects.get(pk=1)
            project.save()

            try:
                tags_json = json.loads(request.POST.get('tags', '[]'))
                tag_names = [tag['value'].strip() for tag in tags_json if 'value' in tag and tag['value'].strip()]
                if len(tag_names) < 2:
                    form.add_error('tags', 'Please enter at least 2 tags.')
                    return render(request, 'projects/create.html', {'form': form})

                for name in tag_names:
                    tag, _ = Tag.objects.get_or_create(name=name)
                    project.tags.add(tag)
            except json.JSONDecodeError:
                form.add_error('tags', 'Tags format is invalid.')
                return render(request, 'projects/create.html', {'form': form})
            # Save images
            for file in request.FILES.getlist('images'):
                ProjectImage.objects.create(project=project, image=file)

        else:
            return render(request, 'projects/create.html', {'form': form})
        return redirect('some_success_url')
    
    return render(request, 'projects/create.html', {'form': form})





def tag_list(request):
    tags = Tag.objects.values_list('name', flat=True)
    return JsonResponse(list(tags), safe=False)

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


# Create your views here.
def index(request):
    pass

def details(request,project_id):
    pass

def update_project(request,project_id):
    pass
def donate(request,project_id):
    pass

def add_comment(request,project_id):
    pass

def report_project(request,project_id):
    pass

def rate_project(request,project_id):
    pass

def my_projects(request):
    user = User.objects.get(id=1)
    projects = Project.objects.filter(user=user)
    return render(request, 'projects/my_projects.html', {'projects': projects})

def cancel_project(request,project_id):
    user = User.objects.get(id=1)
    project = Project.objects.get(id=project_id)
    if project.user != user:
        return render(request, 'projects/my_projects.html')
    else:
        project.isCancelled = True
        project.save()
        return redirect('projects:my_projects')
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            #handle tags
            try:
                tags_json = json.loads(request.POST.get('tags', '[]'))
                tag_names = [tag['value'].strip() for tag in tags_json if 'value' in tag and tag['value'].strip()]
                if len(tag_names) < 2:
                    form.add_error('tags', 'Please enter at least 2 tags.')
                    return render(request, 'projects/create.html', {'form': form})

                for name in tag_names:
                    tag, _ = Tag.objects.get_or_create(name=name)
                    project.tags.add(tag)
            except json.JSONDecodeError:
                form.add_error('tags', 'Tags format is invalid.')
                return render(request, 'projects/edit.html', {'form': form, 'project': project, 'images': project.projectimage_set.all()})
            # Handle multiple images
            for image in request.FILES.getlist('images'):
                ProjectImage.objects.create(project=project, image=image)
            return redirect('projects:my_projects')
    else:
        form = ProjectForm(instance=project)
        images = project.projectimage_set.all()
        tags_csv = ",".join(project.tags.values_list('name', flat=True))  
        return render(request, 'projects/edit.html', {
            'form': form,
            'project': project,
            'images': images,
            'tags_csv': tags_csv
    })

# from django.contrib.auth.decorators import login_required
# @login_required
def delete_image(request, image_id):
    image = get_object_or_404(ProjectImage, id=image_id, project__user=request.user)
    project_id = image.project.id
    image.delete()
    return redirect('projects:edit_project', project_id=project_id)