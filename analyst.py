import os
import json
import youtube_transcript_api
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_transcript_universal(video_id):
    """
    Пробуем все доступные методы: list_transcripts, get_transcript или просто list.
    """
    api = youtube_transcript_api.YouTubeTranscriptApi
    
    # Попытка 1: Стандартный list_transcripts
    if hasattr(api, 'list_transcripts'):
        try:
            ts_list = api.list_transcripts(video_id)
            return ts_list.find_transcript(['en']).fetch()
        except: pass

    # Попытка 2: Метод list (который мы увидели в твоем dir)
    if hasattr(api, 'list'):
        try:
            # В некоторых версиях 2026 года .list() возвращает объект для fetch
            ts_list = api.list(video_id)
            return ts_list.find_transcript(['en']).fetch()
        except: pass

    # Попытка 3: Прямой get_transcript (если он скрыт)
    try:
        return api.get_transcript(video_id)
    except: pass

    print(f"Не удалось получить текст для {video_id} ни одним способом.")
    return None

def find_viral_moments(text):
    """
    Анализируем через LLM для поиска моментов, которые 'взорвут' алгоритм SWT.
    """
    prompt = f"""
    Найди 3 виральных сегмента (30-90 сек) в судебном заседании.
    Ищи пики удержания (AVD) и эмоциональные споры.
    Текст: {text[:15000]}
    Ответ строго в JSON: {{"highlights": [{{"start": 0, "end": 0, "hook": ""}}]}}
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={ "type": "json_object" }
    )
    return json.loads(response.choices[0].message.content)

def run_analyst():
    if not os.path.exists("scout_output.json"): return
    with open("scout_output.json", "r") as f: 
        videos = json.load(f)

    results = []
    # Обрабатываем видео для захвата премиального CPM Израиля ($4.41-$14.08)
    for video in videos[:3]:
        print(f"--- Analyzing: {video['title']} ---")
        data = get_transcript_universal(video['video_id'])
        if data:
            full_text = " ".join([t['text'] for t in data])
            analysis = find_viral_moments(full_text)
            video["analysis"] = analysis["highlights"]
            results.append(video)
            print(f"Success! Clips found: {len(analysis['highlights'])}")

    with open("analyst_output.json", "w") as f:
        json.dump(results, f, indent=4)
    print("Analyst node finished.")

if __name__ == "__main__":
    run_analyst()
