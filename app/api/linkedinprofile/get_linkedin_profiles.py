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
from django.db.models import Q
import ast

class ManageLinkedInProfileView(APIView):
    def get(self, request, format=None):
        try:
            offset = int(request.query_params.get("offset", 0))
            search_text = request.query_params.get("search_text", "")
            is_company = request.query_params.get("is_company", True)

            query = Q()
            if search_text != "":
                if is_company == "true":
                    query |= Q(profile_data__name__icontains=search_text)
                 
                else:
                    query |= Q(profile_data__experience__0__position__icontains=search_text)
                 
            # Filter the records based on the query
            filtered_records = LinkedinProfile.objects.filter(query)
            total_count = filtered_records.count()
            limit = 10
            linkedin_data = filtered_records[offset:offset+limit].values()
          
            serialized_people = []
            for person in linkedin_data:
                profile_data = person['profile_data']
                experience = profile_data.get('experience', [{}])
                position = experience[0].get('position', '') if experience else ''
                serialized_person = {
                    'id': person['id'],
                    'profile_slug': person['profile_slug'],
                    'name': profile_data.get('name', ''),
                    'profile_image': person['image_path'],
                    'position': position
                }
                serialized_people.append(serialized_person)

            return Response({'message': 'success', 'people': serialized_people, 'total_count': total_count}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
    def post(self, request, format=None):
        try:
            # Validate the person data
            post_data = request.data
            slug      = post_data['profile_slug']
            # id        = post_data['id']
        
            data=LinkedinProfile.objects.filter(profile_slug=slug).first()

            return Response({'message': '', 'profile_data': data.profile_data,'image_path':data.image_path, 'id' : data.id}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)