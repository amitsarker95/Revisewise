from django.urls import path
from .views import CategoriesCreateView

urlpatterns = [
    path('categories/', CategoriesCreateView.as_view(), name='categories')
]
