from django.urls import path
from .views import CategoriesCreateView, CategoriesRetrieveUpdateDeleteView

urlpatterns = [
    path('categories/', CategoriesCreateView.as_view(), name='categories'),
    path('categories/<int:category_id>/', CategoriesRetrieveUpdateDeleteView.as_view(), name='categories'),
]
