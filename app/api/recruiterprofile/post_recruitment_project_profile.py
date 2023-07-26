import os
import json
import requests
from django.conf import settings
from django.core.files.storage import default_storage
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from app.models import UserProfile, RecruiterProject, LinkedinProfile, RecruiterProjectLinkedinProfile
from django.utils import timezone

class RecruitmentProjectProfileView(APIView):
    def post(self, request, format=None):
        try:
            user_hash = request.POST.get('user_hash')
            company_name = request.POST.get('company_name')
            position_name = request.POST.get('position_name')
            profile_link = request.POST.get('profile_link')
            profile_slug = request.POST.get('profile_slug')
            profile_data = request.POST.get('profile_data')

            print("Not loaded 1")

            if not user_hash or not company_name or not position_name or not profile_link or not profile_slug or not profile_data:
                return Response({'status': 'error', 'message': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

            # Get or create the User
            user_profile = get_object_or_404(UserProfile, license_key=user_hash)
            user = user_profile.user

            # Get or create the RecruiterProject
            project, created = RecruiterProject.objects.get_or_create(user=user, company_name=company_name, project_name=position_name)

            new_added = True
            try:
                profile = get_object_or_404(LinkedinProfile, profile_slug=profile_slug)
                new_added = False
            except:
                new_added = True

            # Get or create the LinkedinProfile
            if new_added:
                profile = LinkedinProfile()
                profile.profile_slug = profile_slug

            profile.profile_link = profile_link
            profile.profile_data = json.loads(profile_data)
            profile.save()

            # Extract the profile image URL from profile_data JSON
            profile_decoded = json.loads(profile_data)
            profile_image = profile_decoded.get('imgURL')

            if profile_image:
                # Save the profile image
                file_path = self.save_profile_image(profile_image, profile.id)
                profile.image_path = file_path
            else:
                profile.image_path = "images/no_profile.png"

            profile.save()

            # Associate the RecruiterProject with the LinkedinProfile
            recruiter_profile, created = RecruiterProjectLinkedinProfile.objects.get_or_create(recruiter_project=project, linkedin_profile=profile)
            recruiter_profile.created_at = timezone.now()
            recruiter_profile.save()

            return Response({'status': 'success', 'message': 'Recruitment project profile updated'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def save_profile_image(self, profile_image_url, profile_slug):
        file_relative_path = "images/no_profile.png"
        try:
            print(profile_image_url)
            response = requests.get(profile_image_url)
            response.raise_for_status()

            content_type = response.headers.get('Content-Type')
            extension = ""
            if content_type == 'image/jpeg':
                extension = 'jpg'
            elif content_type == 'image/png':
                extension = 'png'

            file_name = f"{profile_slug}.{extension}"
            file_relative_path = f'images/{file_name}'
            file_path = os.path.join(settings.MEDIA_ROOT, file_relative_path)

            with open(file_path, 'wb') as file:
                file.write(response.content)
        except:
            print("Not loaded")
        return file_relative_path
