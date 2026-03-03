import os
import json
import yt_dlp
import whisper
from openai import OpenAI
from dotenv import load_dotenv

# Конфигурация окружения
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Загрузка модели Whisper (модель 'base' — баланс скорости и точности)
print("--- Loading Whisper model... ---")
whisper_model = whisper.load_model("base")

def download_audio(video_id):
    """Скачивает аудио высокого качества для точной транскрибации."""
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
    
    output_path = f"downloads/{video_id}.mp3"
    url = f"https://www.youtube.com/watch?v={video_id}"
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'no_warnings': True
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return output_path

def analyze_highlights_with_filter(text):
    """
    Анализ текста через GPT-4o. 
    Генерирует англоязычные метаданные и фильтрует рекламу.
    """
    prompt = f"""
    You are a professional legal news editor for a high-RPM YouTube channel.
    Analyze the provided transcript and extract 3 viral segments (30-90 seconds each).

    YOUR GOAL:
    Maximize Satisfied Watch Time (SWT) by finding heated arguments, shocking testimonies, or final verdicts.

    CRITICAL RESTRICTIONS (STRICT AD-FILTERING):
    - EXCLUDE any segments containing native advertisements or sponsorships.
    - IGNORE mentions of: "One Skin", "Carry Proof", "VPN", "Sponsor", "Promocode", or "Sidebar".
    - If the host starts talking about a product, that segment is TRASH. Do not use it.

    LANGUAGE & SEO (AEO OPTIMIZATION):
    - All output values ('hook' and 'aeo_desc') MUST be in ENGLISH.
    - Use powerful legal keywords to attract US-based high-paying advertisers.

    Transcript:
    {text[:25000]}

    Return ONLY a JSON object in this format:
    {{
      "highlights": [
        {{
          "start": 150.0,
          "end": 210.5,
          "hook": "TRUMP vs JUDGE: Heated Courtroom Argument Uncut",
          "aeo_desc": "Watch the intense legal battle as the defense challenges the judge's ruling in this landmark case. Full trial analysis and legal breakdown."
        }}
      ]
    }}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o", # Используем 4o для лучшего понимания контекста рекламы
            messages=[
                {"role": "system", "content": "You are a strict legal content curator. You only speak JSON and English for output metadata."},
                {"role": "user", "content": prompt}
            ],
            response_format={ "type": "json_object" },
            temperature=0.1 # Низкая температура для точности таймкодов
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"AI Error: {e}")
        return {"highlights": []}

def run_pro_analyst():
    print(f"--- STARTING PRO ANALYSIS (AEO & Ads Filtering) ---")
    
    if not os.path.exists("scout_output.json"):
        print("Error: scout_output.json not found. Run scout.py first.")
        return

    with open("scout_output.json", "r", encoding="utf-8") as f:
        videos = json.load(f)

    final_results = []
    
    for video in videos:
        v_id = video['video_id']
        print(f"\nProcessing Video ID: {v_id}")
        
        try:
            # 1. Загрузка звука
            audio_file = download_audio(v_id)
            
            # 2. Превращение звука в текст (Whisper)
            print(f"Transcribing {v_id}...")
            transcription = whisper_model.transcribe(audio_file)
            full_text = transcription['text']
            
            # 3. Анализ и фильтрация рекламы через GPT-4o
            print(f"Analyzing and filtering ads for {v_id}...")
            analysis_data = analyze_highlights_with_filter(full_text)
            
            if analysis_data.get("highlights"):
                video["analysis"] = analysis_data["highlights"]
                final_results.append(video)
                print(f"Success: Found {len(analysis_data['highlights'])} clean English segments.")
            
            # Удаление временного аудио
            if os.path.exists(audio_file):
                os.remove(audio_file)
                
        except Exception as e:
            print(f"Error processing {v_id}: {e}")

    # Сохранение финального результата для Editor и Publisher
    with open("analyst_output.json", "w", encoding="utf-8") as f:
        json.dump(final_results, f, indent=4, ensure_ascii=False)
    
    print("\n" + "="*40)
    print("DONE: analyst_output.json is ready with English metadata.")

if __name__ == "__main__":
    run_pro_analyst()
