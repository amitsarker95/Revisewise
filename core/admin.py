from django.contrib import admin
from .models import CustomUser



@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'is_active', 'is_staff']
    search_fields = ['full_name', 'email']

