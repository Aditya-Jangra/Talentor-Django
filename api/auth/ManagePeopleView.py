from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from ..function.validation import validate_person_data
from ..function.db import get_people, create_person, update_person_data, delete_person


class ManagePeopleView(APIView):
    def get(self, request, format=None):
        try:            # Get all people from the database
            people = get_people()
            serialized_people = []
            for person in people:
                # Get the user associated with this person
                user = get_object_or_404(User, id=person['user_id'])
                # Serialize the person and user data
                serialized_person = {
                    'id': person['id'],
                    'name': person['name'],
                    'email': user.email,
                    'username': user.username
                }
                serialized_people.append(serialized_person)

            return Response({'message': 'success', 'people': serialized_people}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        try:
            # Validate the person data
            person_data = request.data
            validate_person_data(person_data)

            # Create the new person in the database
            person_id = create_person(person_data)

            return Response({'message': 'Person created successfully', 'id': person_id}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, format=None):
        try:
            
            # Validate the person data
            person_data = request.data
            validate_person_data(person_data)

            # Update the person in the database
            updated_person_id = update_person_data(person_data)

            return Response({'message': 'Person updated successfully', 'id': updated_person_id}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, format=None):
        try:
            # Get the person ID from the query parameters
            person_id = request.query_params.get('id')

            # Delete the person from the database
            delete_person(person_id)

            return Response({'message': 'Person deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)