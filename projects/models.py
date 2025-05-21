from django.db import models
from django.conf import settings
from django.db.models import Avg, Sum, Count
class ProjectCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Project(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    details = models.TextField()
    target = models.IntegerField()
    startDate = models.DateField()
    endDate = models.DateField()
    category = models.ForeignKey(ProjectCategory, on_delete=models.SET_NULL, null=True)
    isFeatured = models.BooleanField(default=False)
    isCancelled = models.BooleanField(default=False)

    tags = models.ManyToManyField(Tag, through='ProjectTag')
    
    @property
    def days_remaining(self):
        from datetime import datetime
        return (self.endDate - datetime.now().date()).days
    
    @property
    def current_amount(self):
        from django.db.models import Sum
        return self.donation_set.aggregate(Sum('amount'))['amount__sum'] or 0
    
    @property
    def progress_percentage(self):
        if self.target > 0:
            return round((self.current_amount / self.target) * 100, 2)
        return 0


    @property
    def total_donations(self):
        return self.donation_set.aggregate(total=Sum('amount'))['total'] or 0

    @property
    def average_rating(self):
        return round(self.rating_set.aggregate(avg=Avg('value'))['avg'] or 0, 1)

    @property
    def comment_count(self):
        return self.comment_set.count()

    @property
    def report_count(self):
        return self.report_set.count()
    def __str__(self):
        return self.title

class ProjectTag(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('project', 'tag')  # optional but good practice

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='project_images/')

class Donation(models.Model):
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)

class Report(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    reason = models.TextField()

class Rating(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    value = models.IntegerField()

class Comment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
