from django.shortcuts import get_object_or_404
from .models import Subjects, Categories, Topic, RevisionLog
from django.db.models import Q


class RevisionAppService:

    def get_all_categories(self, user):
        if user.is_authenticated:
            return Categories.objects.filter(Q(user=user) | Q(is_global=True))
        else:
            return Categories.objects.filter(is_global=True)
    
    def get_category_by_id(self, category_id):
        category = Categories.objects.filter(id=category_id)
        return category
    
    def create_category(self, **validated_data):
        category = Categories.objects.create(**validated_data)
        return category
    
    def delete_category(self, category_id):
        try:
            category = Categories.objects.get(id=category_id)
            category.delete()
            return f"{category.name} has been successfully deleted."
        except:
            raise Exception("Category not found")
   
