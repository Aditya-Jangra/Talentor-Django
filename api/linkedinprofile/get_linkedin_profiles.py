from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from ..function.validation import validate_person_data
from ..function.db import get_linked_in_profiles
from app.models import LinkedinProfile
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class ManageLinkedInProfileView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:            # Get all people from the database
            people = get_linked_in_profiles()
            serialized_people=[]
            for person in people:
                # Serialize the person and user data
                serialized_person = {
                    'id':person['id'],
                    'profile_slug':person['profile_slug'],
                    'name':person['profile_data']['name'],
                    'profile_image': person['profile_data']['imgURL'],
                    'position':person['profile_data']['experience'][0]['position']
                }
                serialized_people.append(serialized_person)

            return Response({'message': 'success', 'people': serialized_people}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self, request, format=None):
        try:
            # Validate the person data
            post_data = request.data
            slug      = post_data['profile_slug']
            
            data=LinkedinProfile.objects.get(profile_slug=slug)

            return Response({'message': '', 'profile_data': data.profile_data, 'id' : data.id}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)