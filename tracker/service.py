from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound, PermissionDenied
from django.db.models import Q
from .models import Subjects, Categories, Topic, RevisionLog


class RevisionAppService:
    
    '''
    Category Services

    '''
    def get_all_categories(self, user):
        if user.is_authenticated:
            return Categories.objects.filter(Q(user=user) | Q(is_global=True))
        else:
            return Categories.objects.filter(is_global=True)
    
    def get_category_by_id(self, category_id):
        category = Categories.objects.get(id=category_id)
        return category
    
    def create_category(self, **validated_data):
        category = Categories.objects.create(**validated_data)
        return category
    
    def upadate_category(self, category_id, **validated_data):
        category = Categories.objects.get(id=category_id)
        for key, value in validated_data.items():
            setattr(category, key, value)
        category.save()
        return category

    
    def delete_category(self, category_id):
        try:
            category = Categories.objects.get(id=category_id)
            category.delete()
            return f"{category.name} has been successfully deleted."
        except:
            raise Exception("Category not found")
        
    '''
    Subject Services
    
    '''

    def get_all_subjects(self, user):
        if user.is_authenticated:
            return Subjects.objects.filter(user=user)
        else:
            return Subjects.objects.none()
        
    def get_subject_by_id_and_check_owner(self, id, user):
        try:
            subject = Subjects.objects.get(id=id)
        except Subjects.DoesNotExist:
            raise NotFound("Subject not found")

        if subject.user != user:
            raise PermissionDenied("You are not allowed to access this subject")

        return subject
    
    def create_subject(self, **validated_data):
        subject = Subjects.objects.create(**validated_data)
        return subject
    
    def upadate_subject(self, subject_id, **validated_data):
        subject = Subjects.objects.get(id=subject_id)
        for key, value in validated_data.items():
            setattr(subject, key, value)
        subject.save()
        return subject
    
    def delete_subject(self, subject_id):
        try:
            subject = Subjects.objects.get(id=subject_id)
            subject.delete()
            return f"{subject.name} has been successfully deleted."
        except:
            raise Exception("Subject not found")
        
   
