import json
from django.shortcuts import render, redirect
from .forms import ProjectForm
from .models import Tag, ProjectImage
from django.contrib.auth.models import User


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
                print(form.errors)
                return render(request, 'projects/create.html', {'form': form})
            # Save images
            for file in request.FILES.getlist('images'):
                ProjectImage.objects.create(project=project, image=file)

        else:
            return render(request, 'projects/create.html', {'form': form})
        return redirect('some_success_url')
    
    return render(request, 'projects/create.html', {'form': form})



from django.http import JsonResponse

def tag_list(request):
    tags = Tag.objects.values_list('name', flat=True)
    return JsonResponse(list(tags), safe=False)
from django.shortcuts import render
from django.db import models

# Create your views here.
def index(request):
    pass

def details(request,project_id):
    pass

def update_project(request,project_id):
    pass

def cancel_project(request,project_id):
    pass

def donate(request,project_id):
    pass

def add_comment(request,project_id):
    pass

def report_project(request,project_id):
    pass

def rate_project(request,project_id):
    pass
