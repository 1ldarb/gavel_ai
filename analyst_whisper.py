import os
import json
import yt_dlp
import whisper
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Загружаем модель Whisper (base достаточно для скорости, medium — для точности)
model = whisper.load_model("base")

def download_audio(video_id):
    """Скачивает аудиодорожку видео через yt-dlp."""
    url = f"https://www.youtube.com/watch?v={video_id}"
    options = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])
    return f"downloads/{video_id}.mp3"

def get_transcript_local(audio_path):
    """Локальная транскрибация через Whisper."""
    print(f"Транскрибирую аудио: {audio_path}...")
    result = model.transcribe(audio_path)
    return result['text']

def run_analyst():
    if not os.path.exists("scout_output.json"): return
    with open("scout_output.json", "r") as f: videos = json.load(f)

    if not os.path.exists("downloads"): os.makedirs("downloads")

    results = []
    for video in videos[:2]: # Тестируем на 2 видео
        print(f"--- Processing: {video['title']} ---")
        try:
            audio_file = download_audio(video['video_id'])
            full_text = get_transcript_local(audio_file)
            
            # Далее — анализ через LLM (как в прошлом коде)
            # analysis = find_viral_moments(full_text)
            # video["analysis"] = analysis["highlights"]
            
            results.append(video)
            print(f"Success! Текст получен локально.")
            
            # Удаляем временный файл для экономии места на Hetzner
            os.remove(audio_file)
        except Exception as e:
            print(f"Ошибка: {e}")

    with open("analyst_output.json", "w") as f:
        json.dump(results, f, indent=4)

if __name__ == "__main__":
    run_analyst()
