from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('user','name', 'description', 'created_at', 'is_global')
    list_filter = ('is_global', 'user')
    list_display_links = ('name',)
    list_editable = ('is_global',)
    search_fields = ('full_name', 'user__email')
    read_only_fields = ('created_at',)


    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
    
    def save_model(self, request, object, form, change):
        if not object.user:
            object.user = request.user
        super().save_model(request, object, form, change)

@admin.register(Subjects)
class SubjecsAdmin(admin.ModelAdmin):
    list_display = ('user', 'categories', 'name', 'description', 'created_at')
    list_filter = ('categories', 'user')
    list_display_links = ('name', )
    search_fields = ('name', 'user__full_name', 'user__email')
    readonly_fields = ('created_at',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
    
    def save_model(self, request, object, form, change):
        if not object.user:
            object.user = request.user
        super().save_model(request, object, form, change)



admin.site.register(Topic)
admin.site.register(RevisionLog)
