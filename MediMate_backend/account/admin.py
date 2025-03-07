from django.contrib import admin
from .models import User


# registers the Admin model into the CMS

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)

