from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import *
from ..function.validation import *
from ..function.db import *
from ..function.jwt import *
  
class LoginView(APIView):
    def post(self, request, format = None):
        try:
            post_data   = request.data
            email       = post_data.get('email')
            password    = post_data.get('password')
            is_validate = True
            status_code = HTTP_401_UNAUTHORIZED 
            response = {}
            message  = ''
            jwtToken = ''
            if not checkRequestData(post_data) or checkEmpty(email) or checkEmpty(password) or not emailValidation(email)        :
                message = 'Invalid credentials'
                is_validate = False

            elif not checkUserAccountByEmail(email):
                message = 'Invalid credentials'
                is_validate = False

            elif not checkUserByEmail(email):
                message = 'Your account is deactivated.Contact an administrator.'
                is_validate = False

            if is_validate :
                userObj = fetchUserByEmail(email)

                if check_password(password,userObj.password):
                    message = 'success'
                    status_code = HTTP_200_OK 
                    jwtToken = getAccessToken(userObj)              
                else:
                    message = 'Invalid credentials'
                    status_code = HTTP_401_UNAUTHORIZED 

            response['message']     =  message
            response['status_code'] =  status_code
            response['token']       = jwtToken
            return Response(response,status=status_code)

        except Exception as e:
            return Response({'message':str(e),'status_code':HTTP_400_BAD_REQUEST,},status=HTTP_400_BAD_REQUEST)