from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CreateCategoriesSerializer, DetailedCategoriesSerializer, \
                        CreateSubjectsSerializer, DetailedSubjectsSerializer, \
                        CreateTopicSerializer, DetailedTopicSerializer, \
                        TopicUpdateSerializer, CreateRevisionLogSerializer, \
                        DetailedRevisionLogSerializer

from .service import RevisionAppService


class CategoriesCreateView(APIView):
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

class CategoriesRetrieveUpdateDeleteView(APIView):
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

        