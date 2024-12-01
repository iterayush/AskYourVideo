from django.urls import path
from .views import index, upload_video, get_transcript, answer_question

urlpatterns = [
    path('', index, name='index'),
    path('upload/', upload_video, name='upload_video'),
    path('transcript/<int:video_id>/', get_transcript, name='get_transcript'),
    path('answer/<int:video_id>/', answer_question, name='answer_question'),
]