import os
import subprocess
import textwrap
from pprint import pprint
# import shutil
# from flask import Flask, request, jsonify, send_file
from yt_dlp import YoutubeDL
# from flask_cors import CORS

DOWNLOAD_FOLDER = 'E:/Wideo'

def display_videos(url):
    ydl_opts = {
        'quiet': True,  # Wyłącza zbędne logi
        'extract_flat': True,  # Pobiera listę linków bez pobierania treści
        'skip_download': True
    }
    
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)  # Pobierz informacje bez pobierania

            if 'original_url' in info:
                print("playlista")
            else:
                print("wideo")
            # pprint.pprint(info)
    except Exception as e:
        print(f"Nie można pobrać informacji o filmie: {e}")
        
def download_video(url):
    output_path = os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s')
    options = {
        'format': 'bestvideo+bestaudio/best',  # Pobiera najlepsze wideo i audio, a następnie je łączy
        'merge_output_format': 'mkv',         # Format wyjściowy po połączeniu
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',  # Ścieżka i nazwa pliku
        'noplaylist': False,                   # Nie pobiera playlist, tylko pojedyncze wideo
        'quiet': False,                       # Pokazuje szczegóły pobierania
        'postprocessors': [{                  # Dodatkowe przetwarzanie po pobraniu
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mkv'          # Konwersja do formatu MP4
        }]
    }
    try:
        with YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=False)
            
            if 'entries' in info:
                for i in info['entries']:
                    print(f"{i['title']}:")
                    formats = i['formats']
                    for f in formats:
                        resolution = f.get('height', 'Audio')  # Wysokość wideo (lub Audio)
                        ext = f.get('ext', 'unknown')  # Format pliku
                        fps = f.get('fps', '-')  # Liczba klatek na sekundę
                        size = f.get('filesize', None)  # Rozmiar pliku
                        size_mb = f"{size / 1024 / 1024:.2f} MB" if size else "N/A"

                        print(f"- {f['format_id']:>4}: {resolution}p, {ext}, {fps} fps, {size_mb}")

                print("playlista")
            else:
                print("wideo")
            # ydl.download([url])
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
    
        if result.returncode == 0:
            if not os.path.exists(DOWNLOAD_FOLDER):
                os.makedirs(DOWNLOAD_FOLDER)
            url = input("Podaj URL filmu z YouTube: ")
            download_video(url)
        else:
            print('ffmpeg is not installed')
    except FileNotFoundError:
        print('ffmpeg is not installed')