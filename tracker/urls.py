from django.urls import path
from .views import CategoriesCreateAPIView, CategoriesRetrieveUpdateDeleteAPIView, SubjectsCreateAPIView, \
                   SubjectsRetrieveUpdateDeleteAPIView, TopicsCreateAPIView, TopicsRetrieveUpdateDeleteAPIView, \
                   RevisionLogRetriveUpdateDeleteAPIView, RevisionLogAPIView

urlpatterns = [
    path('categories/', CategoriesCreateAPIView.as_view(), name='categories'),
    path('categories/<int:category_id>/', CategoriesRetrieveUpdateDeleteAPIView.as_view(), name='categories'),
    path('subjects/', SubjectsCreateAPIView.as_view(), name='subjects'),
    path('subjects/<int:subject_id>/', SubjectsRetrieveUpdateDeleteAPIView.as_view(), name='subjects'),
    path('topics/', TopicsCreateAPIView.as_view(), name='topics'),
    path('topics/<int:topic_id>/', TopicsRetrieveUpdateDeleteAPIView.as_view(), name='topic-update-delete'),
    path('revision-log/', RevisionLogAPIView.as_view(), name='revision-log'),
    path('revision-log/<int:log_id>/', RevisionLogRetriveUpdateDeleteAPIView.as_view(), name='revision-log-update-delete'),
]
