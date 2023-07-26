from rest_framework_simplejwt.tokens import RefreshToken
from jwt import encode
'''
@ getAccessToken()  
@ Parameter { type,user_info,password  }
@ to user refresh and access token
@ return dictionary
'''
def getAccessToken(userObj):
    try:
        refresh = RefreshToken.for_user(userObj)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    except Exception as e:
        print(e)
        return  {
                'refresh': '',
                'access': ''
            }

