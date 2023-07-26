from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from normal_app.models import RecruitmentProjectProfile

class GetRecruitmentProjectsByProfile(APIView):
    def get(self, request, profile_slug, format=None):
        try:
            projects = RecruitmentProjectProfile.objects.filter(profile_slug=profile_slug).order_by('-id')
            serialized_projects = []
            for project in projects:
                serialized_project = {
                    'project_id': project.project.id,
                    'company_name': project.project.company_name,
                    'position_name': project.project.position_name,
                    'created_at': project.created_at,
                    'updated_at': project.updated_at
                }
                serialized_projects.append(serialized_project)
            return Response(serialized_projects, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
