from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from app.models import RecruiterProject,RecruiterProjectLinkedinProfile
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class DeleteRecruiterProfileView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, format=None):
        try:
            user_id = request.user.id
            post_data = request.data
            profile_id = post_data['profile_id']
            project_id = post_data['project_id']

           
            project = get_object_or_404(RecruiterProject, id=project_id, user_id=user_id)

            RecruiterProjectLinkedinProfile.objects.filter(recruiter_project_id=project_id, linkedin_profile_id=profile_id).delete()

            return Response({'message': 'Profile deleted successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)