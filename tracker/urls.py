from django.urls import path
from .views import CategoriesCreateAPIView, CategoriesRetrieveUpdateDeleteAPIView, SubjectsCreateAPIView, \
                   SubjectsRetrieveUpdateDeleteAPIView, TopicsCreateAPIView

urlpatterns = [
    path('categories/', CategoriesCreateAPIView.as_view(), name='categories'),
    path('categories/<int:category_id>/', CategoriesRetrieveUpdateDeleteAPIView.as_view(), name='categories'),
    path('subjects/', SubjectsCreateAPIView.as_view(), name='subjects'),
    path('subjects/<int:subject_id>/', SubjectsRetrieveUpdateDeleteAPIView.as_view(), name='subjects'),
    path('topics/', TopicsCreateAPIView.as_view(), name='topics'),
]
