from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from app.models import LinkedinProfile, RecruiterProjectLinkedinProfile

class GetRecruitmentProjectsByProfile(APIView):
    def get(self, request, profile_slug, format=None):
        try:
            linkedin_profile = get_object_or_404(LinkedinProfile, profile_slug=profile_slug)
            recruiter_projects = RecruiterProjectLinkedinProfile.objects.filter(linkedin_profile=linkedin_profile).order_by('-id')
            
            serialized_projects = []
            for recruiter_project in recruiter_projects:
                project = recruiter_project.recruiter_project
                serialized_project = {
                    'project_id': project.id,
                    'company_name': project.company_name,
                    'position_name': project.project_name,
                    'created_at': project.created_at,
                    'updated_at': recruiter_project.created_at
                }
                serialized_projects.append(serialized_project)
            
            return Response(serialized_projects, status=status.HTTP_200_OK)
        
        except LinkedinProfile.DoesNotExist:
            return Response({'message': 'Linkedin profile not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
