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

