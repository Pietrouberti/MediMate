from django.contrib import admin
from .models import Patients

@admin.register(Patients)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name')
    list_filter = ('first_name',)
    search_fields = ('first_name',)
# Register your models here.