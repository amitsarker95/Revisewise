from django.shortcuts import render
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CreateCategoriesSerializer, DetailedCategoriesSerializer, \
                        CreateSubjectsSerializer, DetailedSubjectsSerializer, \
                        CreateTopicSerializer, DetailedTopicSerializer, \
                        TopicUpdateSerializer, CreateRevisionLogSerializer, \
                        DetailedRevisionLogSerializer

from .service import RevisionAppService


class CategoriesCreateAPIView(APIView):
    service = RevisionAppService()
    serializer_class = CreateCategoriesSerializer
    detail_serializer_class = DetailedCategoriesSerializer

    def get(self, request):
        categories = self.service.get_all_categories(request.user)
        serializer = self.detail_serializer_class(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        category = self.service.create_category(**serializer.validated_data)
        return Response(self.detail_serializer_class(category).data, status=status.HTTP_201_CREATED)

class CategoriesRetrieveUpdateDeleteAPIView(APIView):
    service = RevisionAppService()
    serializer_class = CreateCategoriesSerializer
    detail_serializer_class = DetailedCategoriesSerializer

    def get(self, request, category_id):
        try:
            category = self.service.get_category_by_id(category_id)
            serializer = self.detail_serializer_class(category)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            data =[
                {
                    "message": "Category not found"
                }
            ]
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        
    
    def put(self, request, category_id):
        try:
            category = self.service.get_category_by_id(category_id)
            serializer = self.serializer_class(category, data=request.data)
            serializer.is_valid(raise_exception=True)
            updated_category = self.service.upadate_category(category.id, **serializer.validated_data)
            return Response(self.detail_serializer_class(updated_category).data, status=status.HTTP_200_OK)
        except:
            data =[
                {
                    "message": "Category not found"
                }
            ]
            return Response(data, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, category_id):
        self.service.delete_category(category_id=category_id)
        return Response("Category deleted successfully",status=status.HTTP_204_NO_CONTENT)
    


class SubjectsCreateAPIView(APIView):
    service = RevisionAppService()
    serializer_class = CreateSubjectsSerializer
    detail_serializer_class = DetailedSubjectsSerializer

    def get(self, request):
        subjects = self.service.get_all_subjects(request.user)
        serializer = self.serializer_class(subjects, many=True)
        return Response(self.detail_serializer_class(subjects, many=True).data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        if request.user.is_authenticated:
            validated_data['user'] = request.user
        else:
            return Response("Authentication required", status=status.HTTP_401_UNAUTHORIZED)
        subject = self.service.create_subject(**validated_data)
        return Response(self.detail_serializer_class(subject).data, status=status.HTTP_201_CREATED)
    

class SubjectsRetrieveUpdateDeleteAPIView(APIView):
    service = RevisionAppService()
    serializer_class = CreateSubjectsSerializer
    detail_serializer_class = DetailedSubjectsSerializer


    def get(self, request, subject_id):
        try:
            if request.user.is_authenticated:
                subject = self.service.get_subject_by_id_and_check_owner(subject_id, request.user)
                serializer = self.detail_serializer_class(subject)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("Subject not found", status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request, subject_id):
        try:
            if request.user.is_authenticated:
                subject = self.service.get_subject_by_id_and_check_owner(subject_id, request.user)
                serializer = self.serializer_class(subject, data=request.data)
                serializer.is_valid(raise_exception=True)
                updated_subject = self.service.upadate_subject(subject.id, **serializer.validated_data)
                return Response(self.detail_serializer_class(updated_subject).data, status=status.HTTP_200_OK)
        except:
            return Response("Subject not found", status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, subject_id):
        try:
            if request.user.is_authenticated:
                subject = self.service.get_subject_by_id_and_check_owner(subject_id, request.user)
                self.service.delete_subject(subject.id)
                return Response("Subject deleted successfully",status=status.HTTP_204_NO_CONTENT)
        except:
            return Response("Subject not found", status=status.HTTP_404_NOT_FOUND)
        

class TopicsCreateAPIView(APIView):
    service = RevisionAppService()
    serializer_class = CreateTopicSerializer
    detail_serializer_class = DetailedTopicSerializer

    def get(self, request):
        # topics = self.service.get_all_topics(request.user)
        pass