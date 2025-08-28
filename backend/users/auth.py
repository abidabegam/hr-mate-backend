import jwt
from django.conf import settings
from datetime import datetime, timedelta

class JwtTools:
    @staticmethod
    def generate_token(user):
        """
        Generates a JWT token for the given user
        """
        expiration_time = datetime.utcnow() + timedelta(hours=1)  # Token expires in 1 hour
        token = jwt.encode(
            {'user_id': user.id, 'exp': expiration_time},
            settings.SECRET_KEY,  # Secret key from Django settings
            algorithm='HS256'
        )
        return token

    @staticmethod
    def set_cookie(response, token):
        """
        Set JWT token as a cookie in the response
        """
        response.set_cookie(
            key='token',
            value=token,
            max_age=3600,  # 1 hour expiration
            httponly=True,  # Prevent JavaScript access to the cookie
            secure=True  # Only set the cookie over HTTPS
        )

    @staticmethod
    def get_user_from_token(token):
        """
        Decodes a JWT token and returns the user object
        """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            return User.objects.get(id=payload['user_id'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')
