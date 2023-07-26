from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import *
from ..function.db import fetchUserByEmail
from ..function.jwt import getAccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

class ProfileView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        try:
            user = request.user
            userObj = fetchUserByEmail(user.email)

            profile_data = {
                'email': userObj.email,
                'username': userObj.username,
            }

            return Response({'profile': profile_data, 'status_code': HTTP_200_OK}, status=HTTP_200_OK)

        except Exception as e:
            return Response({'message': str(e), 'status_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)
