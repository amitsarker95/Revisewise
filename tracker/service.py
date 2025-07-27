from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound, PermissionDenied
from django.db.models import Q
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from datetime import datetime
from .models import Subjects, Categories, Topic, RevisionLog



class RevisionAppService:
    
    '''
    Category Services

    '''
    def get_all_categories(self):
        return Categories.objects.all()
    
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
            return f"Subject has been successfully deleted."
        except:
            raise Exception("Subject not found")
        

    '''
    Subject Services
    
    '''

    def get_all_topics(self, user):
        if user.is_authenticated:
            return Topic.objects.filter(subject__user=user)
        else:
            return Topic.objects.none()
        
    def get_topic_by_id_and_check_owner(self, id, user):
        try:
            topic = Topic.objects.get(id=id)
            if topic.subject.user != user:
                raise PermissionDenied("You are not allowed to access this topic")
            return topic
        except Topic.DoesNotExist:
            raise NotFound("Topic not found")
   
    def create_topic(self, **validated_data):
        try:
            topic = Topic.objects.create(**validated_data)
            return topic
        except IntegrityError:
            raise ValidationError({"title": ["Topic with this title already exists for this subject."]})
    
    def update_topic(self, topic_id, **validated_data):
        topic = Topic.objects.get(id=topic_id)
        is_completed = validated_data.pop('is_completed', False)
        for key, value in validated_data.items():
            setattr(topic, key, value)
        
        if is_completed:
            topic.is_completed = is_completed
            topic.total_revisions += 1
            topic.last_revised = datetime.now().date()
        else:
            topic.is_completed = is_completed
        topic.save()
        return topic
    
    def delete_topic(self, topic_id):
        try:
            topic = Topic.objects.get(id=topic_id)
            topic.delete()
            return f"Topic has been successfully deleted."
        except:
            raise Exception("Topic not found")
        
    def update_topic_status(self, topic_id, user, **validated_data):
        topic = self.get_topic_by_id_and_check_owner(topic_id, user)
        is_completed = validated_data.get('is_completed')
        if is_completed:
            topic.is_completed = is_completed
            topic.total_revisions += 1
            topic.last_revised = datetime.now().date()
            topic.save()
        return topic

    '''
    Revision Log Services
    
    '''

    def revision_log_create(self, topic, was_completed):
        if not was_completed and topic.is_completed:
            revision = RevisionLog.objects.create(
                topic=topic,
                notes="Topic marked as completed",
                revised_at= datetime.now().date()
            )
            topic.total_revisions


    def get_all_revision_log(self, user):
        if user.is_authenticated:
            return RevisionLog.objects.filter(topic__subject__user=user)
        else:
            return RevisionLog.objects.none()
        
    def get_revision_log_by_id(self, log_id, user):
        log = RevisionLog.objects.get(id=log_id)
        if log.topic.subject.user != user :
            raise PermissionDenied("You are not allowed to access this log")
        return RevisionLog.objects.get(id=log_id)

    def get_revision_log_by_topic(self, topic_id):
        return RevisionLog.objects.filter(topic=topic_id)
        

    def update_revision_log(self, log_id, **validated_data):
        log = RevisionLog.objects.get(id=log_id)
        for key, value in validated_data.items():
            setattr(log, key, value)
        log.save()
        return log
    
    def delete_revision_log(self, log_id, user):
        log = self.get_revision_log_by_id(log_id, user)
        log.delete()
        
