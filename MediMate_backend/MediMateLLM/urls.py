from django.urls import path
from . import api

# definition of endpoint urls and methods endpoints point to

urlpatterns = [
    path('get_summary/encounters/<uuid:id>', api.get_encounter_records, name='summarise_encounter_records'),
    path('get_summary/medication/<uuid:id>', api.get_medication_records, name='summarise_medication_records'),
    path('get_summary/allergy/<uuid:id>', api.get_allergy_records, name="summaries_medication_records"),
    path('get_summary/conditions/<uuid:id>', api.get_condition_records, name="summaries_condition_records"),
    path('verify_diagnosis/', api.check_doctors_diagnosis, name='verify_diagnosis'),
    path('check_ddi/', api.check_medical_prescription, name= 'verify_medical_prescription')
]
