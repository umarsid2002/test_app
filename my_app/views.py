from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate ,login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
# from django.conf import settings
import os
# import assemblyai as aai
# from google import genai
import yt_dlp
# from .models import BlogPost
# from django.contrib import messages

# Create your views here.
@login_required
def index(request):
    return render(request, 'index.html')

def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repeatPassword = request.POST['repeatPassword']

        if password == repeatPassword:
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
                login(request, user)
                return redirect('/')
            except:
                error_message = 'Problem Creating Account'
                return render(request, 'signup.html', {'error_message': error_message})
        else:
            error_message = 'passwords do not match'
            return render(request, 'signup.html', {'error_message': error_message})
    return render(request, 'signup.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message', error_message})
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('/')

@csrf_exempt
def generate_blog(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            yt_link = data['link']
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'invalid data sent'}, status= 400)

        # Get YT Title 
        title = yt_title(yt_link)
        return JsonResponse({'content': title})

def youtube_downloader(request, output_folder="C:/Users/umars/Downloads"):
    return render(request, 'video_downloader.html')

def blog_list(request):
    return render(request, 'all-blogs.html')

def yt_title(url):
    ydl_opts = {
        'quiet': True,  # Suppress output
        'no_warnings': True,  
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info.get('title', 'Title not found')