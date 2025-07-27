from rest_framework import serializers
from datetime import timedelta
from django.utils import timezone
from .models import Categories,Topic, Subjects, RevisionLog


class CreateCategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ['id','user','name', 'description', 'is_global']



class DetailedCategoriesSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField()

    class Meta:
        model = Categories
        fields = ['id','user', 'name', 'description', 'created_at', 'is_global']


class CreateSubjectsSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Subjects
        fields = ['id', 'categories','user', 'name', 'description']

    def validate_name(self, value):
        user = self.context['request'].user
        if Subjects.objects.filter(user=user, name=value).exists():
            raise serializers.ValidationError("Subject with this name already exists")
        return value
    
    def validate(self, data):
        subject_name = data.get('name')
        category = data.get('categories')
        if category.name.strip().lower() == subject_name.strip().lower():
            raise serializers.ValidationError("Subject name cannot be the same as its category name")
        return data

class CreateTopicSerializer(serializers.ModelSerializer):

    subject_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Topic
        fields = ['id', 'title', 'description', 'subject_id']

class DetailedSubjectsSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField(read_only=True)
    categories = DetailedCategoriesSerializer(read_only=True)
    topics = CreateTopicSerializer(many=True, read_only=True)

    class Meta:
        model = Subjects
        fields = ['id','categories', 'user', 'name', 'description', 'created_at', 'topics']



        


class DetailedTopicSerializer(serializers.ModelSerializer):

    

    class Meta:
        model = Topic
        fields = [
            'id', 'title', 'description', 
            'subject', 'total_revisions', 'last_revised',
            'deadline', 'created_at', 'is_completed',
            
            ]
        read_only_fields = ['id', 'created_at', 'total_revisions', 'last_revised']

class TopicUpdateSerializer(serializers.ModelSerializer):
    deadline_status = serializers.SerializerMethodField(read_only=True)
    subject_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Topic
        fields = [
            'id',
            'title',
            'description',
            'subject_id',
            'deadline',
            'is_completed',
            'deadline_status'
        ]

    def get_deadline_status(self, obj):
        if obj.deadline and obj.deadline < timezone.now().date():
            return "Overdue"
        elif obj.deadline and obj.deadline > timezone.now():
            return "Upcoming"
        else:
            return "No Deadline"



class CreateRevisionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = RevisionLog
        fields = ['id', 'topic', 'revised_at']

    def create(self, validated_data):
        revision = RevisionLog.objects.create(**validated_data)
        topic = revision.topic
        topic.total_revisions += 1
        topic.last_revised = revision.revised_at
        topic.save()
        return revision
        

class DetailedRevisionLogSerializer(serializers.ModelSerializer):
    topic = DetailedTopicSerializer(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)
    subject = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = RevisionLog
        fields = ['id', 'user', 'subject','notes', 'topic', 'revised_at']
        read_only_fields = ['id', 'user', 'subject', 'topic', 'revised_at']


    def get_user(self, obj):
        return str(obj.topic.subject.user.full_name)
    
    def get_subject(self, obj):
        return str(obj.topic.subject.name)