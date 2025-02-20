from django.forms import ValidationError
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import  UserSerializer


'''Endpoint to get the details of the currently logged in user'''
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_user(request):
    try:
        user = UserSerializer(request.user)
        return JsonResponse({
            'user': user.data,
            'success': True
        })
    except Exception as e:
        return JsonResponse({ 'error': str(e), 'success': False }, status=500) 


