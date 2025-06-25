from instagrapi import Client
from dotenv import load_dotenv
import os
import time

load_dotenv()
SESSION_FILE = "session.json"
DOWNLOAD_DIR = "downloads"

def get_ig_client() -> Client:
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    print(f"user: {username} pass: {password}")

    if not username or not password:
        raise ValueError("Instagram credentials not set in .env")

    cl = Client()

    if os.path.exists(SESSION_FILE):
        try:
            cl.load_settings(SESSION_FILE)
            cl.get_timeline_feed()
            print("✅ Reused IG session")
            return cl
        except Exception as e:
            print(f"⚠️ Failed to reuse session: {e}, retrying fresh login")
            os.remove(SESSION_FILE)
    try:
        cl = Client()
        cl.login(username, password)
        cl.dump_settings(SESSION_FILE)
        print("🔐 Logged in and saved new session")
        return cl
    except Exception as login_err:
        print(f"❌ Login failed: {login_err}")
        raise

def download_video_media(cl: Client, url: str) -> str:
    attempt = 0

    while attempt < 4:
        print(f"starting download process attempt {attempt}")
        try:
            ensure_download_dir()
            media_pk = cl.media_pk_from_url(url)
            media_info = cl.media_info(media_pk)
            video_url = media_info.video_url
            path = cl.clip_download_by_url(video_url, folder=DOWNLOAD_DIR)
            return path
        except Exception as e:
            print(f"attempt {attempt} failed to download due to {e}")
            attempt += 1
            time.sleep(2)
    
    raise Exception("failed to download")

            

def upload_video(cl: Client, video_path: str, caption: str = "follow before i disappear forever (@suswindow)"):
    print("starting upload process")

    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    try:
        print ("uploading...")
        cl.clip_upload(video_path, caption=caption)
        print(f"✅ Uploaded: {video_path}")
        os.remove(video_path)
        return {"status": "uploaded", "path": video_path}
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        os.remove(video_path)
        raise Exception("Upload failed")

def ensure_download_dir():
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)