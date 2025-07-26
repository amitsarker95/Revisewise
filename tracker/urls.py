from django.urls import path
from .views import CategoriesCreateAPIView, CategoriesRetrieveUpdateDeleteAPIView, SubjectsCreateAPIView

urlpatterns = [
    path('categories/', CategoriesCreateAPIView.as_view(), name='categories'),
    path('categories/<int:category_id>/', CategoriesRetrieveUpdateDeleteAPIView.as_view(), name='categories'),
    path('subjects/', SubjectsCreateAPIView.as_view(), name='subjects'),
]
