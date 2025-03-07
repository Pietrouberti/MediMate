from patients.models import Patients
from rest_framework import serializers


# serializer to transform Patient objects into JSON format for frontend

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patients
        fields = ('id', 
                  'first_name',
                  'last_name',
                  'age',
                  'date_of_birth',
                  'gender',
                  'ethnicity',
                  'address'
                )
        