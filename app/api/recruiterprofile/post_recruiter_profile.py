from rest_framework import status
from django.shortcuts import get_object_or_404
from app.models import RecruiterProject, RecruiterProjectLinkedinProfile
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response

class ManageRecruiterProfileView2(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
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