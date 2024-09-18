from re import split
from django.shortcuts import render
import os
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.conf import settings
from .forms import Audio
from pydub import AudioSegment

# Create your views here.
def home(request):
    media_folder = os.path.join(settings.STATICFILES_DIRS[0],'media')
    audio_list = [file for file in os.listdir(media_folder) if file.endswith(('.mp3', '.wav', '.ogg'))]
    return render(request,"index.html",{"audio_list": sorted(audio_list)})



def upload(request):
    if request.method == 'GET':
        music = Audio()
        return render(request, 'upload.html',{"music": music})
    elif request.method == "POST":
        music = Audio(request.POST, request.FILES)
        if music.is_valid():
            audio_file = request.FILES['music']
            name = audio_file.name
            name = "_".join(name.split(" "))
            audio = AudioSegment.from_file(audio_file, format="mp3")
            processed_audio = audio + 10
            media_folder = os.path.join(settings.STATICFILES_DIRS[0],'media')
            os.makedirs(media_folder, exist_ok=True)
            processed_audio_path = os.path.join(media_folder, name)
            processed_audio.export(processed_audio_path, format="mp3")
        return HttpResponseRedirect(reverse(home))