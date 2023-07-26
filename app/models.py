from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class RecruiterProject(models.Model):
    company_name = models.CharField(max_length=255)
    project_name = models.CharField(max_length=255)
    user         = models.ForeignKey(User, on_delete=models.CASCADE)
    is_primary   = models.IntegerField(default=0)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

class UserProfile(models.Model):
    license_key = models.CharField(max_length=255)
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

class LinkedinProfile(models.Model):
    profile_link = models.CharField(max_length=500)
    profile_slug = models.CharField(max_length=255)
    profile_data = models.JSONField()
    image_path   = models.TextField(null=True, default=None)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)


class RecruiterProjectLinkedinProfile(models.Model):
    recruiter_project = models.ForeignKey(RecruiterProject, on_delete=models.CASCADE)
    linkedin_profile  = models.ForeignKey(LinkedinProfile, on_delete=models.CASCADE)
    is_primary        = models.IntegerField(default=0)
    created_at        = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ['recruiter_project', 'linkedin_profile']


class Project(models.Model):
    title       = models.CharField(max_length=100)
    description = models.TextField()
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Person(models.Model):
    first_name = models.CharField(max_length=255)
    last_name  = models.CharField(max_length=255)
    email      = models.EmailField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    


# Not Used So Ignore
class RecruiterProfile(models.Model):
    company_name  = models.CharField(max_length=255)
    position_name = models.CharField(max_length=255)
    user          = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)