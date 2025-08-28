from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.models import UserDetails
from users.serializers import UserDetailsSerializer
from rest_framework import status


class OrgChartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Fetch all users with related managers
            all_details = UserDetails.objects.select_related('user', 'manager').all()
            serializer = UserDetailsSerializer(all_details, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
