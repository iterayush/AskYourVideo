import os
import subprocess
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Video
from pytube import YouTube
import whisper
from transformers import pipeline

def index(request):
    videos = Video.objects.all()  # Fetch all videos from the database
    return render(request, 'index.html', {'videos': videos})  # Pass the videos to the template

def upload_video(request):
    if request.method == 'POST':
        video_url = request.POST.get('video_url')
        
        try:
            yt = YouTube(video_url)
            video_title = yt.title
            video_stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
            video_file_path = video_stream.download(output_path='videos', filename=video_title + '.mp4')

            # Generate transcript
            transcript = generate_transcript(video_file_path)

            # Save to database
            video = Video(title=video_title, url=video_url, transcript=transcript)
            video.save()

            return redirect('index')
        except Exception as e:
            # Handle the exception and return an error message
            return render(request, 'index.html', {'error': str(e)})

def generate_transcript(video_path):
    model = whisper.load_model("base")
    result = model.transcribe(video_path)
    return result['text']

def get_transcript(request, video_id):
    video = Video.objects.get(id=video_id)
    return JsonResponse({'transcript': video.transcript})

# question answer
qa_pipeline = pipeline("question-answering")

def answer_question(request, video_id):
    if request.method == 'POST':
        question = request.POST.get('question')
        video = Video.objects.get(id=video_id)
        context = video.transcript

        # Get the answer
        answer = qa_pipeline(question=question, context=context)
        return JsonResponse({'answer': answer['answer']})