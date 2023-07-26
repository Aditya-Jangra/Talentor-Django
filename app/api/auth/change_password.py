from django.contrib.auth.hashers import check_password, make_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import *
from ..function.validation import *
from ..function.db import *
from ..function.jwt import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

class ChangePasswordView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        try:
            post_data = request.data
            user_id = request.user.id
            old_password = post_data.get('old_password').strip()
            new_password = post_data.get('new_password').strip()
            confirm_password = post_data.get('confirm_password').strip()
            is_validate = True
            status_code = HTTP_401_UNAUTHORIZED
            response = {}

            if new_password != confirm_password:
                message = 'Password does not match'
                is_validate = False

            if old_password == new_password:
                message = 'New password must be different from the old password'
                is_validate = False

            if is_validate:
                userObject = get_object_or_404(User, id=user_id)
                user_obj = fetchUserByEmail(userObject.email)
                if check_password(old_password, user_obj.password):
                    new_password_hashed = make_password(new_password)
                    user_obj.password = new_password_hashed
                    user_obj.save()
                    message = 'Password changed successfully'
                    status_code = HTTP_200_OK
                    jwt_token = getAccessToken(user_obj)
                    response['token'] = jwt_token
                else:
                    message = 'Password does not match'
                    status_code = HTTP_401_UNAUTHORIZED

            response['message'] = message
            response['status_code'] = status_code
            return Response(response, status=status_code)

        except Exception as e:
            return Response({'message': str(e), 'status_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)
