from django.urls import path
from . import api

# definition of endpoint urls and methods endpoints point to

urlpatterns = [
    path('get_patients/', api.get_patient_list, name='get_patients'),
]
