import os
import json
from datetime import datetime, timedelta, UTC
from googleapiclient.discovery import build
from dotenv import load_dotenv

# Загрузка ключей
load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")
youtube = build("youtube", "v3", developerKey=API_KEY)

# Список официальных каналы судов (без рекламы и ведущих)
COURT_CHANNELS = [
    {"name": "9th Judicial Circuit Court (Florida)", "id": "UCAScD_Wc7dqvkVrcgrxcf_g"},
    {"name": "Wisconsin Court System", "id": "UCU_152eO5y21D0pS9pM9pXg"},
    {"name": "Judge Mary Kiernan (Clean Trials)", "id": "UCqX6pX5vjXv8b_O1yGvA_2A"},
    {"name": "Law&Crime Trials (ONLY Live Stream Channel)", "id": "UCz8K1occVvDTYDfFo7N5EZw"}
]

def get_high_value_videos(channel_id, days_back=60): # Увеличили окно до 2 месяцев
    """
    Расширенный поиск для обхода 'нулевого' результата.
    """
    time_limit = (datetime.now(UTC) - timedelta(days=days_back)).isoformat().replace("+00:00", "Z")
    
    # Упрощаем запрос, чтобы найти хоть какой-то контент
    search_query = "Trial | Court | Sentence" 
    
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        order="date",
        q=search_query,
        type="video",
        # Смена на medium позволяет находить видео от 4 минут
        videoDuration="medium", 
        maxResults=5,
        publishedAfter=time_limit
    )
    
    try:
        response = request.execute()
        print(f"DEBUG: Channel {channel_id} returned {len(response.get('items', []))} items.")
    except Exception as e:
        print(f"API Error: {e}")
        return []
    
    videos = []
    for item in response.get("items", []):
        videos.append({
            "video_id": item["id"]["videoId"],
            "title": item["snippet"]["title"],
            "channel_name": item["snippet"]["channelTitle"],
            "published_at": item["snippet"]["publishedAt"]
        })
    return videos

def run_scout():
    print(f"--- STARTING CLEAN SCOUT (Date: {datetime.now().strftime('%Y-%m-%d')}) ---")
    all_videos = []
    
    for court in COURT_CHANNELS:
        print(f"Searching official records in: {court['name']}...")
        found = get_high_value_videos(court["id"])
        all_videos.extend(found)
        print(f"Found {len(found)} candidate(s).")
    
    # Сохраняем результаты
    with open("scout_output.json", "w", encoding="utf-8") as f:
        json.dump(all_videos, f, indent=4, ensure_ascii=False)
    
    print("-" * 30)
    print(f"DONE. Total videos for AI analysis: {len(all_videos)}")
    print("Next step: Run python analyst_pro.py")

if __name__ == "__main__":
    run_scout()
