from django.urls import path
from . import api

urlpatterns = [
    path('get_summary/encounters/<uuid:id>', api.get_encounter_records, name='summarise_encounter_records'),
    path('get_summary/medication/<uuid:id>', api.get_medication_records, name='summarise_medication_records'),
    path('get_summary/allergy/<uuid:id>', api.get_allergy_records, name="summaries_medication_records")
]
