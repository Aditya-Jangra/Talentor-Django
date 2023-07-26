from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework import status
from django.contrib.auth.models import User
import re


def removeSpaceAndUpToLowCase(post_data, key):
    return post_data[key].strip().lower()

def emailValidation(email):
    regex = r"^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$"
    return True if re.search(regex, email, re.IGNORECASE) else False

def checkEmpty(value):
    return True if value == '' else False

def checkRequestData(data):
    return True if data else False

def checkUserAccountByEmail(email):
    try:
        return User.objects.filter(email=email).exists()
    except Exception as e:
        return False

def checkUserByEmail(email):
    try:
        return User.objects.filter(email=email, is_active__in=[True]).exists()
    except Exception as e:
        return False


def validate_person_data(person_data):
    # Validate required fields
    name = removeSpaceAndUpToLowCase(person_data, 'name')
    age = person_data.get('age')

    if checkEmpty(name):
        return False, 'Name is required.'

    if age is None:
        return False, 'Age is required.'

    # Validate email field
    email = removeSpaceAndUpToLowCase(person_data, 'email')

    if not emailValidation(email):
        return False, 'Invalid email.'

    # Check if user with the given email already exists
    if checkUserAccountByEmail(email):
        return False, 'User with the given email already exists.'

    return True, None

class ManagePeopleView(APIView):
    def get(self, request, format=None):

        try:
            people = get_people()

            return Response({'message': 'success', 'people': people}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):

        try:
            person_data = request.data

            if not checkRequestData(person_data):
                return Response({'message': 'Invalid person data.'}, status=status.HTTP_400_BAD_REQUEST)

            errors = validate_person_data(person_data)

            if errors:
                return Response({'message': errors}, status=status.HTTP_400_BAD_REQUEST)


            return Response({'message': 'Person created successfully'}, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, format=None):

        try:
            person_data = request.data

            if not checkRequestData(person_data):
                return Response({'message': 'Invalid person data.'}, status=status.HTTP_400_BAD_REQUEST)

            person_id = request.query_params.get('id')

            if not person_id:
                return Response({'message': 'Person ID is required.'}, status=status.HTTP_400_BAD_REQUEST)



            return Response({'message': 'Person updated successfully', 'id': person_id}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, format=None):

        try:
            person_id = request.query_params.get('id')

            if not person_id:
                return Response({'message': 'Person ID is required.'}, status=status.HTTP_400_BAD_REQUEST)


            return Response({'message': 'Person deleted successfully'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
