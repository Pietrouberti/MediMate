from django.forms import ValidationError
from django.http import JsonResponse
from .models import Patients
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import PatientSerializer

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_patient_list(request):
    try: 
        patients = Patients.objects.all();
        serialised_patients = PatientSerializer(patients, many=True)
        return JsonResponse({
            'patients' : serialised_patients.data,
            'success':  True, 
        })
    except Exception as e:
        return JsonResponse({'patients': None, 'success': False, 'error': str(e)})