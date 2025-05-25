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
from django.contrib.admin.views.decorators import staff_member_required
 

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
    similar_projects = Project.objects.filter(tags__in=project.tags.all()).exclude(id=project_id).distinct()
    

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
        'similar_projects': similar_projects
    })

@login_required
def donate(request,project_id):
    project = get_object_or_404(Project,id=project_id)
    if request.method == 'POST':
        amount = request.POST.get('amount')
        try:
            amount = float(amount)
            if amount <= 0 or amount > project.target:
                raise ValueError
        except (ValueError, TypeError):
            return render(request, 'projects/donate.html', {'project': project, 'error': 'Please enter a valid amount'})
        
        donation = Donation(amount=amount, project=project, user=request.user) 
        donation.save()
        print(request)
        messages.success(request, 'God bless U, thanks for ur donation!')
        return redirect('projects:project_details', project_id=project_id)
    return render(request, 'projects/donate.html', {'project': project})

@login_required
def report_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        reason = request.POST.get('reason')
        already_reported = Report.objects.filter(project=project, user=request.user).exists()
        if already_reported:
            messages.warning(request, 'You have already reported this project.')
            return redirect('projects:project_details', project_id=project_id)
        if reason:
            report = Report(project=project, user=request.user, reason=reason) 
            report.save()
            messages.success(request, 'Your report has been submitted.')
        return redirect('projects:project_details', project_id=project_id)

    return render(request, 'projects/report_project.html', {'project': project})

@staff_member_required
def reported_projects(request):
    reported_projects = Project.objects.filter(report__isnull=False).distinct()
    return render(request, 'projects/reported_projects.html', {'reported_projects': reported_projects})

@staff_member_required
def project_reports(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    reports = Report.objects.filter(project=project)
    return render(request, 'projects/project_reports.html', {'project': project, 'reports': reports})
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



@csrf_exempt 
@require_POST
@login_required
def add_comment(request, project_id):
    """
    Add a new comment to a project via AJAX
    """
    try:
        # Get the project
        project = get_object_or_404(Project, id=project_id)
        
        # Parse JSON data
        data = json.loads(request.body)
        comment_text = data.get('text', '').strip()
        
        # Validate comment text
        if not comment_text:
            return JsonResponse({
                'success': False,
                'error': 'Comment text cannot be empty'
            }, status=400)
        
        if len(comment_text) > 1000:  # Adjust max length as needed
            return JsonResponse({
                'success': False,
                'error': 'Comment is too long (maximum 1000 characters)'
            }, status=400)
        
       
        # Create the comment
        comment = Comment.objects.create(
            project=project,
            user=request.user,
            text=comment_text
        )
        
        # Return success response with comment data
        return JsonResponse({
            'success': True,
            'message': 'Comment added successfully',
            'comment': {
                'id': comment.id,
                'text': comment.text,
                'user': comment.user.username,
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        }, status=400)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'An error occurred: {str(e)}'
        }, status=500)


@login_required
def add_rating(request, project_id):
    """
    Add or update a rating for a project via AJAX
    """
    try:
        # Get the project
        project = get_object_or_404(Project, id=project_id)
        
        # Parse JSON data
        data = json.loads(request.body)
        rating_value = data.get('rating')
        
        # Validate rating value
        try:
            rating_value = int(rating_value)
        except (ValueError, TypeError):
            return JsonResponse({
                'success': False,
                'error': 'Invalid rating value'
            }, status=400)
        
        if rating_value < 1 or rating_value > 5:
            return JsonResponse({
                'success': False,
                'error': 'Rating must be between 1 and 5'
            }, status=400)
        
        # Check if user is trying to rate their own project
        if project.user == request.user:
            return JsonResponse({
                'success': False,
                'error': 'You cannot rate your own project'
            }, status=400)
        
        # Create or update the rating
        rating, created = Rating.objects.update_or_create(
            project=project,
            user=request.user,
            defaults={'value': rating_value}
        )
        
        action = 'added' if created else 'updated'
        
        return JsonResponse({
            'success': True,
            'message': f'Rating {action} successfully',
            'rating': {
                'id': rating.id,
                'value': rating.value,
                'user': rating.user.username,
                'is_current_user': True
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        }, status=400)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'An error occurred: {str(e)}'
        }, status=500)


def get_ratings(request, project_id):
    """
    Get all ratings for a project via AJAX
    """
    try:
        # Get the project
        project = get_object_or_404(Project, id=project_id)
        
        # Get all ratings for this project
        ratings = Rating.objects.filter(project=project).select_related('user')
        
        # Calculate average rating
        avg_rating = ratings.aggregate(avg=Avg('value'))['avg']
        
        # Prepare ratings data
        ratings_data = []
        for rating in ratings:
            ratings_data.append({
                'id': rating.id,
                'username': rating.user.username,
                'value': rating.value,
            })
        
        # Calculate rating distribution (optional)
        rating_distribution = {}
        for i in range(1, 6):
            rating_distribution[i] = ratings.filter(value=i).count()
        
        return JsonResponse({
            'success': True,
            'average_rating': round(avg_rating, 1) if avg_rating else None,
            'total_ratings': ratings.count(),
            'ratings': ratings_data,
            'rating_distribution': rating_distribution
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'An error occurred: {str(e)}'
        }, status=500)


def get_comments(request, project_id):
    """
    Get all comments for a project via AJAX (optional - for loading comments dynamically)
    """
    try:
        # Get the project
        project = get_object_or_404(Project, id=project_id)
        
        # Get all comments for this project
        comments = Comment.objects.filter(project=project).select_related('user')
        
        # Prepare comments data
        comments_data = []
        for comment in comments:
            comments_data.append({
                'id': comment.id,
                'text': comment.text,
                'user': comment.user.username,
            })
        
        return JsonResponse({
            'success': True,
            'total_comments': comments.count(),
            'comments': comments_data
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'An error occurred: {str(e)}'
        }, status=500)
    
    
def similar_projects(request, project_id):
    """Fetch similar projects based on tags"""
    project = get_object_or_404(Project, id=project_id)
    similar_projects = Project.objects.filter(tags__in=project.tags.all()).exclude(id=project_id).distinct()
    
    return render(request, 'projects/similar_projects.html', {
        'project': project,
        'similar_projects': similar_projects
    })


