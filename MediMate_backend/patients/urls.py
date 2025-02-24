from django.urls import path
from . import api

urlpatterns = [
    path('get_patients/', api.get_patient_list, name='get_patients'),
]
