from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from normal_app.models import RecruitmentProject

class RecruitmentProjectSelectionView(APIView):
    def post(self, request, format=None):
        try:
            project_id = request.data.get('id')  # Retrieve the value of 'id' from request data
            project = get_object_or_404(RecruitmentProject, id=project_id)

            RecruitmentProject.objects.exclude(id=project_id).update(is_primary=False)
            project.is_primary = True
            project.save()

            return Response({'message': 'Recruitment project selection updated successfully.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
