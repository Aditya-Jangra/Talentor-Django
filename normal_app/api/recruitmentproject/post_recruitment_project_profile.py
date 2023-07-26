import json
from django.core.files.storage import default_storage
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from normal_app.models import RecruitmentProject, RecruitmentProjectProfile
import datetime

class RecruitmentProjectProfileView(APIView):
    def post(self, request, format=None):
        try:
            user_hash = request.POST.get('user_hash')
            company_name = request.POST.get('company_name')
            position_name = request.POST.get('position_name')
            profile_link = request.POST.get('profile_link')
            profile_slug = request.POST.get('profile_slug')
            profile_data = request.POST.get('profile_data')

            if not user_hash or not company_name or not position_name or not profile_link or not profile_slug or not profile_data:
                return Response({'status': 'error', 'message': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)
            
            # returning into a tuple, instead of a single variable
            project, created = RecruitmentProject.objects.get_or_create(user_hash=user_hash, company_name=company_name, position_name=position_name)
           
        
            profile, ProjectProfile= RecruitmentProjectProfile.objects.get_or_create(project_id=project.id,profile_data=profile_data, profile_slug=profile_slug,profile_link=profile_link)

            profile.profile_link = profile_link
            profile.profile_data = profile_data
            profile_decoded = json.loads(profile_data)
            profile_image = profile_decoded.get('imgURL')
            if profile_image:
                image_path = self.save_profile_image(profile_image, profile_slug)
                profile.image_path = image_path
            else:
                profile.image_path = None

            profile.save()

            if created:
                return Response({'status': 'success', 'message': 'New profile created'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'status': 'success', 'message': 'Profile updated'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def save_profile_image(self, profile_image, profile_slug):
        file_name = f"{profile_slug}.jpg"
        file_path = f"profile_images/{file_name}"
        with default_storage.open(file_path, 'wb+') as destination:
            destination.write(profile_image)
        return file_path
