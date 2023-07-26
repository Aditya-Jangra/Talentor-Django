from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from app.models import RecruiterProject, UserProfile

class RecruitmentProjectsViews(APIView):
    def get(self, request, format=None):
        try:
            user_hash = request.query_params.get('user_hash')
            user_profile = get_object_or_404(UserProfile, license_key=user_hash)
            projects = RecruiterProject.objects.filter(user=user_profile.user).order_by('-id')

            serialized_projects = []
            for project in projects:
                serialized_project = {
                    'id': project.id,
                    'company_name': project.company_name,
                    'position_name': project.project_name,  # Updated field name
                    'is_primary': project.is_primary,
                    'created_at': project.created_at
                }
                serialized_projects.append(serialized_project)
            return Response(serialized_projects, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
