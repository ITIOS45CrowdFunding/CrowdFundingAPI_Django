from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.ProjectCategory)
admin.site.register(models.ProjectImage)
admin.site.register(models.Project)
admin.site.register(models.Tag)
admin.site.register(models.ProjectTag)
admin.site.register(models.Donation)
admin.site.register(models.Report)
admin.site.register(models.Rating)
admin.site.register(models.Comment)
