import os
import json
import subprocess

def edit_video():
    if not os.path.exists("analyst_output.json"):
        print("Ошибка: Файл analyst_output.json не найден.")
        return

    with open("analyst_output.json", "r") as f:
        videos = json.load(f)

    if not os.path.exists("output"):
        os.makedirs("output")

    for video in videos:
        v_id = video['video_id']
        url = f"https://www.youtube.com/watch?v={v_id}"
        
        for i, highlight in enumerate(video.get('analysis', [])):
            start = highlight['start']
            end = highlight['end']
            duration = end - start
            output_file = f"output/{v_id}_clip_{i}.mp4"

            print(f"--- Cutting clip {i} for {v_id} ({start}s to {end}s) ---")
            
            # Команда для yt-dlp + ffmpeg: скачивание и нарезка без загрузки всего файла
            cmd = [
                "yt-dlp",
                "-g", url,
                "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
            ]
            
            # Получаем прямые ссылки на видео и аудио
            links = subprocess.check_output(cmd).decode().split('\n')
            video_link = links[0]
            audio_link = links[1]

            # Нарезаем через FFmpeg
            ffmpeg_cmd = [
                "ffmpeg", "-ss", str(start), "-t", str(duration),
                "-i", video_link, "-ss", str(start), "-t", str(duration),
                "-i", audio_link, "-c:v", "libx264", "-c:a", "aac",
                "-strict", "experimental", output_file, "-y"
            ]
            
            subprocess.run(ffmpeg_cmd)
            print(f"Clip saved: {output_file}")

if __name__ == "__main__":
    edit_video()
