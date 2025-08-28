from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class LogoutView(APIView):
    def post(self, request):
        # Your logout logic
        return Response({"message": "Logout endpoint"}, status=status.HTTP_200_OK)
