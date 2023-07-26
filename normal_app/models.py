from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User


class RecruitmentProject(models.Model):           
    user_hash = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    position_name = models.CharField(max_length=255)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name

#name changed from recruiter to recruitmentproject

class RecruitmentProjectProfile(models.Model):
    project_id = models.IntegerField()
    profile_link = models.CharField(max_length=255)
    profile_slug = models.CharField(max_length=255)
    profile_data = models.JSONField()
    image_path = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.profile_slug
