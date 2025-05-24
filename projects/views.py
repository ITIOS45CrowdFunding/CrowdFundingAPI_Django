import json
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ProjectForm
from users.models import CustomUser as User
from django.http import JsonResponse
from django.shortcuts import render
from .models import Project, Tag, ProjectTag, ProjectImage, Donation, Report, Rating, Comment
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Project, Comment, Rating
from django.db.models import Avg

@login_required
def create_project(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = User.objects.get(pk=request.user.id)
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
                return render(request, 'projects/create.html', {'form': form,"tag_error":"Tags format is invalid."})
            # Save images
            for file in request.FILES.getlist('images'):
                ProjectImage.objects.create(project=project, image=file)

        else:
            return render(request, 'projects/create.html', {'form': form})
        return redirect('projects:my_projects')
    
    return render(request, 'projects/create.html', {'form': form})





def tag_list(request):
    tags = Tag.objects.values_list('name', flat=True)
    return JsonResponse(list(tags), safe=False)

# Create your views here.
def base(request):
    return render(request, 'projects/index.html')

def project_details (request, project_id):
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
    avg_rating = ratings.aggregate(Avg('value'))['value__avg'] or 0
    

    # Render a template with the project details
    return render(request, 'projects/project_details.html', {
        'project': project,
        'images': images,
        'tags': tags,
        'donations': donations,
        'reports': reports,
        'ratings': ratings,
        'comments': comments,
        'avg_rating': avg_rating,
    })

def donate(request,project_id):
    project = get_object_or_404(Project,id=project_id)
    if request.method == 'POST':
        amount = request.POST.get('amount')
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return render(request, 'projects/donate.html', {'project': project, 'error': 'Please enter a valid amount'})
        
        donation = Donation(amount=amount, project=project, user=User.objects.get(pk=1)) #remeber to adjust this(user)
        donation.save()
        messages.success(request, 'God bless U, thanks for ur donation!')
        return redirect('projects:project_details', project_id=project_id)
    return render(request, 'projects/donate.html', {'project': project})

def add_comment(request,project_id):
    pass

def report_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        reason = request.POST.get('reason')
        if reason:
            report = Report(project=project, user=User.objects.get(pk=1), reason=reason) #remeber to adjust this(user)
            report.save()
            messages.success(request, 'Your report has been submitted.')
        return redirect('projects:project_details', project_id=project_id)

    return render(request, 'projects/report_project.html', {'project': project})


def rate_project(request,project_id):
    pass
@login_required
def my_projects(request):
    user = User.objects.get(id=request.user.id)
    projects = Project.objects.filter(user=user)
    return render(request, 'projects/my_projects.html', {'projects': projects})

@login_required
def cancel_project(request,project_id):
    user = User.objects.get(id=request.user.id)
    project = Project.objects.get(id=project_id)
    if project.user != user:
        return render(request, 'projects/my_projects.html',{"error":"You don't have permission to cancel this project."})
    else:
        project.isCancelled = True
        project.save()
        return redirect('projects:my_projects')
@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id,user=request.user)

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

@login_required
def delete_image(request, image_id):
    image = get_object_or_404(ProjectImage, id=image_id, project__user=request.user)
    project_id = image.project.id
    image.delete()
    return redirect('projects:edit_project', project_id=project_id)



@csrf_exempt  # since we're using fetch() manually; optionally use @csrf_protect + ensure CSRF token is passed
@require_POST
@login_required
def add_comment(request, project_id):
    try:
        project = get_object_or_404(Project, id=project_id)
        data = json.loads(request.body)

        # Extract comment text and rating
        text = data.get('text', '').strip()
        rating_value = int(data.get('rating', 0))

        if not text:
            return JsonResponse({'error': 'Comment text is required.'}, status=400)

        # Save comment
        Comment.objects.create(
            project=project,
            user=request.user,
            text=text
        )

        # Save or update rating (1 rating per user per project)
        Rating.objects.update_or_create(
            project=project,
            user=request.user,
            defaults={'value': rating_value}
        )

        return JsonResponse({'success': True, 'message': 'Comment and rating submitted.'})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)