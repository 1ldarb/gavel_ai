import os
import json
import pickle
import datetime
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Сфера доступа для загрузки видео
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_authenticated_service():
    """
    Авторизация через OAuth 2.0.
    Использует client_secrets.json и сохраняет token.pickle для работы на сервере.
    """
    creds = None
    # Файл token.pickle хранит токены доступа пользователя
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
            
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("client_secrets.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build("youtube", "v3", credentials=creds)

def upload_to_youtube(youtube, file_path, metadata):
    """
    Загрузка видео с AEO-оптимизированным описанием.
    """
    # Формируем теги для юридической ниши (высокий RPM)
    tags = ["law", "trial", "court", "verdict", "legal", "epstein files"]
    
    body = {
        "snippet": {
            "title": metadata["hook"][:100], # YouTube лимит 100 символов
            "description": f"{metadata['aeo_desc']}\n\n#law #trial #court",
            "tags": tags,
            "categoryId": "27" # Education (привлекает дорогую рекламу)
        },
        "status": {
            "privacyStatus": "private", # Сначала грузим как приватное для финальной проверки
            "selfDeclaredMadeForKids": False
        }
    }

    print(f"--- Starting upload: {file_path} ---")
    
    insert_request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=MediaFileUpload(file_path, chunksize=-1, resumable=True)
    )

    response = None
    while response is None:
        status, response = insert_request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%")

    print(f"Success! Video ID: {response['id']}")
    return response['id']

def run_publisher():
    # Авторизация
    youtube = get_authenticated_service()
    
    # Загрузка данных из аналитика
    if not os.path.exists("analyst_output.json"):
        print("Error: analyst_output.json not found.")
        return

    with open("analyst_output.json", "r", encoding="utf-8") as f:
        videos_data = json.load(f)

    for video in videos_data:
        v_id = video['video_id']
        
        # Проходим по всем нарезанным клипам
        for i, highlight in enumerate(video.get('analysis', [])):
            file_name = f"output/{v_id}_clip_{i}.mp4"
            
            if os.path.exists(file_name):
                try:
                    upload_to_youtube(youtube, file_name, highlight)
                    # Опционально: переместить файл в архив после загрузки
                    # os.rename(file_name, f"output/uploaded_{v_id}_{i}.mp4")
                except Exception as e:
                    print(f"Upload failed for {file_name}: {e}")
            else:
                print(f"File not found: {file_name}")

if __name__ == "__main__":
    run_publisher()
