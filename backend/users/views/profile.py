from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from users.models import UserDetails
from users.serializers.user_details import UserDetailsSerializer

@api_view(['GET', 'PUT'])
@permission_classes([permissions.IsAuthenticated])
def user_profile_view(request):
    user = request.user
    user_details, _ = UserDetails.objects.get_or_create(user=user)

    if request.method == 'GET':
        serializer = UserDetailsSerializer(user_details)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserDetailsSerializer(user_details, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
