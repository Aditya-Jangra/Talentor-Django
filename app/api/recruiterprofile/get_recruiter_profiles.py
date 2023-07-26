from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from app.models import RecruiterProfile, RecruiterProject, RecruiterProjectLinkedinProfile
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class ManageRecruiterProfileView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            user_id = request.user.id
            post_data = request.data
            print(request.data)
            recruiterProjectLinkedObj = RecruiterProjectLinkedinProfile.objects.filter(linkedin_profile= post_data['profile_id']).values_list('recruiter_project_id',flat=True)
            recruiterProjectObj =RecruiterProject.objects.filter(user=user_id,id__in=recruiterProjectLinkedObj)
            print(recruiterProjectObj)

            serialized_profiles = []
            for profile in recruiterProjectObj:
             
                serialized_profile = {
                    'id': profile.id,
                    'company_name': profile.company_name,
                    'project_name': profile.project_name,
                    'user': profile.user_id,
                    'created_at': profile.created_at,
                    'updated_at': profile.updated_at
                }
                serialized_profiles.append(serialized_profile)

            return Response({'message': 'success', 'data': serialized_profiles}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        try:
            post_data = request.data
            company_name = post_data['company_name']
            project_name = post_data['project_name']
            user_id = request.user.id
            profile_id = post_data['profile_id']

            project = RecruiterProject.objects.filter(company_name=company_name, project_name=project_name, user_id=user_id).first()
            
            rplp_id = 0
            project_id = 0
            if project:   
                project_id = project.id          
                record = RecruiterProjectLinkedinProfile.objects.create(recruiter_project=project, linkedin_profile_id=profile_id)
                rplp_id = record.id
            else:           
                project = RecruiterProject.objects.create(company_name=company_name, project_name=project_name, user_id=user_id)
                record = RecruiterProjectLinkedinProfile.objects.create(recruiter_project=project, linkedin_profile_id=profile_id)
                rplp_id = record.id
                project_id = project.id

            return Response({'message': 'Recruitment project LinkedIn profile created/updated successfully.','id':rplp_id,'project_id':project_id}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)