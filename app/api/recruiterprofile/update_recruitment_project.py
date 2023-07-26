from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from app.models import RecruiterProject

class RecruitmentProjectSelectionView(APIView):
    def post(self, request, format=None):
        try:
            project_id = request.POST.get('id')  # Retrieve the value of 'id' from request data
            project = get_object_or_404(RecruiterProject, id=project_id)

            # Update is_primary to 1 for the given project id
            project.is_primary = True
            project.save()

            # Retrieve the user_hash
            user_hash = project.user

            # Update is_primary to 0 for other projects with the same user_hash
            RecruiterProject.objects.filter(user=user_hash).exclude(id=project_id).update(is_primary=False)

            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'failure', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
