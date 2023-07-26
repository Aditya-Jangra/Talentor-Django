from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from app.models import RecruiterProfile, RecruiterProject, RecruiterProjectLinkedinProfile

class ManageRecruiterProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_user_id(self, request):
      
        user_id = request.user.id
        return user_id

    def post(self, request, format=None):
        try:
            user_id = self.get_user_id(request)

            post_data = request.data
            company_name = post_data['company_name']
            project_name = post_data['project_name']
            profile_id = post_data['profile_id']
            
            project = RecruiterProject.objects.filter(company_name=company_name, project_name=project_name, user_id=user_id).first()

            if project:         
                RecruiterProjectLinkedinProfile.objects.create(recruiter_project=project, linkedin_profile_id=profile_id)
            else:
                project = RecruiterProject.objects.create(company_name=company_name, project_name=project_name, user_id=user_id)
                RecruiterProjectLinkedinProfile.objects.create(recruiter_project=project, linkedin_profile_id=profile_id)

            return Response({'message': 'Recruitment project LinkedIn profile created/updated successfully.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)