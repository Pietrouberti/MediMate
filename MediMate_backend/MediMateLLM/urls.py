from django.urls import path
from . import api

urlpatterns = [
    path('get_summary/<uuid:id>', api.medi_mate_llm_chat_entry_point, name='summarise_records'),
]
