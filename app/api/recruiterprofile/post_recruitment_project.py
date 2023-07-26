from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from app.models import RecruiterProject, UserProfile
from django.contrib.auth.models import User
import datetime

class PostRecruitmentProjectView(APIView):
    def post(self, request, format=None):
        try:
            data = request.POST

            user_hash = data.get('user_hash')
            company_name = data.get('company_name')
            position_name = data.get('position_name')

            if not user_hash or not company_name or not position_name:
                return Response({'status': 'error', 'message': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)
            #user_hash is equivalent to License_key here.we have taken user hash from user_profile
            user_profile = get_object_or_404(UserProfile, license_key=user_hash)
            user = user_profile.user

            # Here there is an issue if that combination is not exist then what will be happens            
            update_status = False
            try:
                project = get_object_or_404(RecruiterProject, user=user, company_name=company_name, project_name=position_name)
                update_status = True
            except:
                update_status = False
            

            if update_status:
                project.updated_at = datetime.datetime.now()
                project.is_primary = True
            else:
                # Just change, project_name in place of position_name
                project = RecruiterProject(user=user, company_name=company_name, project_name=position_name)
                project.created_at = datetime.datetime.now()
                project.updated_at = datetime.datetime.now() # On Insertion always update updated at also
                project.is_primary = True

            project.save()

            # Update other projects to set is_primary to False, excluding the current project
            RecruiterProject.objects.exclude(id=project.id).update(is_primary=False)

            if update_status:
                return Response({'status': 'success'}, status=status.HTTP_200_OK)
            else:
                record = {
                    'id': project.id,
                    'company_name': project.company_name,
                    'position_name': project.project_name, # Also here in place of position name project name is used
                    'is_primary': project.is_primary,
                    'created_at': project.created_at,
                }
                return Response({'status': 'success', 'record': record}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
