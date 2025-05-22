# Create this file at projects/management/commands/seed_data.py

from django.core.management.base import BaseCommand
from projects.models import ProjectCategory, Project, Tag, ProjectTag, ProjectImage, Donation, Report, Rating, Comment
from users.models import Profile,CustomUser as User
from django.utils import timezone
import random
import os
from django.conf import settings
from datetime import timedelta

class Command(BaseCommand):
    help = 'Seeds the database with initial data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')
        
        # Clear existing data
        self.clear_data()
        
        # Create users
        users = self.create_users()
        
        # Create categories
        categories = self.create_categories()
        
        # Create tags
        tags = self.create_tags()
        
        # Create projects
        projects = self.create_projects(users, categories)
        
        # Assign tags to projects
        self.assign_tags_to_projects(projects, tags)
        
        # Create project images
        self.create_project_images(projects)
        
        # Create donations
        self.create_donations(projects, users)
        
        # Create ratings
        self.create_ratings(projects, users)
        
        # Create comments
        self.create_comments(projects, users)
        
        # Create reports
        self.create_reports(projects, users)
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded database!'))
    
    def clear_data(self):
        self.stdout.write('Clearing existing data...')
        
        # Delete all records from our custom models
        Comment.objects.all().delete()
        Rating.objects.all().delete()
        Report.objects.all().delete()
        Donation.objects.all().delete()
        ProjectImage.objects.all().delete()
        ProjectTag.objects.all().delete()
        Project.objects.all().delete()
        Tag.objects.all().delete()
        ProjectCategory.objects.all().delete()
        
        # Delete all non-superuser users
        User.objects.filter(is_superuser=False).delete()
        
        self.stdout.write(self.style.SUCCESS('Data cleared!'))
    
    def create_users(self):
        self.stdout.write('Creating users...')
        
        # Create some regular users
        user_data = [
            {'username': 'john_smith', 'email': 'john@example.com', 'password': 'securepass123', 'first_name': 'John', 'last_name': 'Smith'},
            {'username': 'sarah_johnson', 'email': 'sarah@example.com', 'password': 'securepass123', 'first_name': 'Sarah', 'last_name': 'Johnson'},
            {'username': 'ahmed_ali', 'email': 'ahmed@example.com', 'password': 'securepass123', 'first_name': 'Ahmed', 'last_name': 'Ali'},
            {'username': 'fatma_hassan', 'email': 'fatma@example.com', 'password': 'securepass123', 'first_name': 'Fatma', 'last_name': 'Hassan'},
            {'username': 'michael_brown', 'email': 'michael@example.com', 'password': 'securepass123', 'first_name': 'Michael', 'last_name': 'Brown'},
        ]
        
        users = []
        for data in user_data:
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password'],
                first_name=data['first_name'],
                last_name=data['last_name']
            )
            # Create a profile for the user if your Profile model has a one-to-one relationship with User
            try:
                Profile.objects.create(user=user)
            except:
                # If Profile is created automatically via signals, this might fail
                pass
            users.append(user)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(users)} users'))
        return users
    
    def create_categories(self):
        self.stdout.write('Creating project categories...')
        
        categories = [
            'Health',
            'Education',
            'Environment',
            'Technology',
            'Arts',
            'Community',
            'Business',
            'Sports',
            'Disaster Relief',
            'Animals'
        ]
        
        created_categories = []
        for category_name in categories:
            category = ProjectCategory.objects.create(name=category_name)
            created_categories.append(category)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(created_categories)} categories'))
        return created_categories
    
    def create_tags(self):
        self.stdout.write('Creating tags...')
        
        tags = [
            'Urgent', 'Water', 'Innovation', 'Children', 'Medical', 'Green',
            'Sustainable', 'School', 'Food', 'Shelter', 'Music', 'Art',
            'Local', 'Global', 'Research', 'Wildlife', 'Climate', 'Tech',
            'Rural', 'Urban', 'Women', 'Elderly', 'Infrastructure', 'Training'
        ]
        
        created_tags = []
        for tag_name in tags:
            tag = Tag.objects.create(name=tag_name)
            created_tags.append(tag)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(created_tags)} tags'))
        return created_tags
    
    def create_projects(self, users, categories):
        self.stdout.write('Creating projects...')
        
        projects_data = [
            {
                'title': 'Clean Water for Rural Communities',
                'details': 'This project aims to provide clean drinking water to five rural communities by installing water purification systems.',
                'target': 50000,
                'start_date': timezone.now() - timedelta(days=30),
                'end_date': timezone.now() + timedelta(days=60),
                'category': 'Health',
                'is_featured': True,
                'creator': 'ahmed_ali'
            },
            {
                'title': 'Renewable Energy School Program',
                'details': 'Help us bring solar panels to local schools to teach students about renewable energy while reducing energy costs.',
                'target': 75000,
                'start_date': timezone.now() - timedelta(days=45),
                'end_date': timezone.now() + timedelta(days=45),
                'category': 'Education',
                'is_featured': True,
                'creator': 'sarah_johnson'
            },
            {
                'title': 'Community Garden Initiative',
                'details': 'We\'re creating a community garden to provide fresh produce to local residents and educate about sustainable farming.',
                'target': 15000,
                'start_date': timezone.now() - timedelta(days=15),
                'end_date': timezone.now() + timedelta(days=75),
                'category': 'Environment',
                'is_featured': False,
                'creator': 'fatma_hassan'
            },
            {
                'title': 'Tech Skills for Youth',
                'details': 'A program to teach coding and digital skills to underprivileged youth to enhance their career opportunities.',
                'target': 40000,
                'start_date': timezone.now() - timedelta(days=60),
                'end_date': timezone.now() + timedelta(days=30),
                'category': 'Technology',
                'is_featured': True,
                'creator': 'michael_brown'
            },
            {
                'title': 'Local Art Exhibition',
                'details': 'Support local artists by funding an exhibition to showcase their work and promote cultural appreciation.',
                'target': 12000,
                'start_date': timezone.now() - timedelta(days=10),
                'end_date': timezone.now() + timedelta(days=80),
                'category': 'Arts',
                'is_featured': False,
                'creator': 'john_smith'
            },
        ]
        
        created_projects = []
        for data in projects_data:
            # Find the creator user
            creator = User.objects.get(username=data['creator'])
            
            # Find the category
            category = next((c for c in categories if c.name == data['category']), None)
            if not category:
                continue
            
            # Create the project with the correct field names
            project = Project.objects.create(
                title=data['title'],
                details=data['details'],
                target=data['target'],
                startDate=data['start_date'],  # Changed from start_date to startDate
                endDate=data['end_date'],      # Changed from end_date to endDate
                category=category,
                isFeatured=data['is_featured'], # Changed from is_featured to isFeatured
                user=creator                   # Changed from creator to user
            )
            created_projects.append(project)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(created_projects)} projects'))
        return created_projects
    
    def assign_tags_to_projects(self, projects, tags):
        self.stdout.write('Assigning tags to projects...')
        
        count = 0
        for project in projects:
            # Assign 2-4 random tags to each project
            num_tags = random.randint(2, 4)
            selected_tags = random.sample(tags, num_tags)
            
            for tag in selected_tags:
                ProjectTag.objects.create(project=project, tag=tag)
                count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Assigned {count} tags to projects'))
    
    def create_project_images(self, projects):
        self.stdout.write('Creating project images...')
        
        # Path to the project_images directory
        images_dir = os.path.join(settings.MEDIA_ROOT, 'project_images')
        
        # Get list of image files in media/project_images/
        try:
            image_files = [
                f for f in os.listdir(images_dir)
                if os.path.isfile(os.path.join(images_dir, f))
                and f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))
            ]
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('Directory media/project_images/ not found. Please create it and add images.'))
            return
        
        if not image_files:
            self.stdout.write(self.style.ERROR('No images found in media/project_images/.'))
            return
        
        count = 0
        for project in projects:
            # Assign 2-4 random images per project
            num_images = random.randint(2, 4)
            # Shuffle images to ensure randomness
            selected_images = random.sample(image_files, min(num_images, len(image_files)))
            
            for image_name in selected_images:
                # Construct the path for the ImageField (relative to MEDIA_ROOT)
                image_path = os.path.join('project_images', image_name)
                
                ProjectImage.objects.create(
                    project=project,
                    image=image_path
                )
                count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {count} project images'))
    
    def create_donations(self, projects, users):
        self.stdout.write('Creating donations...')
        
        count = 0
        for project in projects:
            # Create 3-8 donations per project
            num_donations = random.randint(3, 8)
            for _ in range(num_donations):
                # Choose a random user as donor
                donor = random.choice(users)
                
                # Create donation with amount between 50 and 5000
                amount = random.randint(50, 5000)
                
                Donation.objects.create(
                    project=project,
                    user=donor,
                    amount=amount
                    # Removed the 'date' field as it's not in your Donation model
                )
                count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {count} donations'))
        
    def create_ratings(self, projects, users):
        self.stdout.write('Creating ratings...')
        
        count = 0
        for project in projects:
            # Create 4-10 ratings per project
            num_ratings = random.randint(4, 10)
            for _ in range(num_ratings):
                # Choose a random user as rater
                rater = random.choice(users)
                
                # Create rating with value between 1 and 5
                value = random.randint(1, 5)
                
                # Check if this user already rated this project
                if not Rating.objects.filter(project=project, user=rater).exists():
                    Rating.objects.create(
                        project=project,
                        user=rater,
                        value=value
                    )
                    count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {count} ratings'))
    
    def create_comments(self, projects, users):
        self.stdout.write('Creating comments...')
        
        comments_text = [
            "Great project! Looking forward to seeing the results.",
            "I just donated. Hope this helps your cause!",
            "How can I get involved as a volunteer?",
            "This project addresses a critical need in our community.",
            "Will you be providing updates on the progress?",
            "Impressive initiative! I've shared it with my network.",
            "Can you provide more details about the implementation?",
            "Is there a minimum donation amount?",
            "I love the idea. Best of luck!",
            "This is exactly what our community needs right now.",
            "Do you need any help with specific skills for this project?",
            "Keep up the amazing work!",
            "I've seen similar projects succeed elsewhere. Excited to see this happen here too.",
            "Will there be any public events related to this project?",
            "Is there a way to follow your progress on social media?"
        ]
        
        count = 0
        for project in projects:
            # Create 3-8 comments per project
            num_comments = random.randint(3, 8)
            for _ in range(num_comments):
                # Choose a random user as commenter
                commenter = random.choice(users)
                
                # Choose a random comment text
                text = random.choice(comments_text)
                
                Comment.objects.create(
                    project=project,
                    user=commenter,
                    text=text
                    # Removed the 'created_at' field as it's not in your Comment model
                )
                count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {count} comments'))
    
    def create_reports(self, projects, users):
        self.stdout.write('Creating reports...')
        
        report_reasons = [
            "Suspicious activity",
            "Misleading information",
            "Potential scam",
            "Inappropriate content",
            "Duplicate project",
            "The project goals are unclear",
            "Unable to verify the creator's identity"
        ]
        
        count = 0
        for project in projects:
            # Only create reports for some projects (20% chance)
            if random.random() < 0.2:
                # Create 1-3 reports
                num_reports = random.randint(1, 3)
                for _ in range(num_reports):
                    # Choose a random user as reporter
                    reporter = random.choice(users)
                    
                    # Choose a random reason
                    reason = random.choice(report_reasons)
                    
                    # Check if this user already reported this project
                    if not Report.objects.filter(project=project, user=reporter).exists():
                        Report.objects.create(
                            project=project,
                            user=reporter,
                            reason=reason
                        )
                        count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {count} reports'))