import json
import os
import requests
from datetime import datetime

API_KEY = os.environ.get("YOUTUBE_API_KEY")

# حط هنا Channel IDs اللي انت عايزها
CHANNEL_IDS = [
    "UC_x5XG1OV2P6uZZ5FSM9Ttw"  # مثال (Google Developers)
]

FEED_FILE = "feed_1.json"
MAX_VIDEOS = 50

# قراءة البيانات القديمة
try:
    with open(FEED_FILE, "r", encoding="utf-8") as f:
        feed = json.load(f)
except:
    feed = []

existing_links = {item.get("link") for item in feed if "link" in item}

for channel_id in CHANNEL_IDS:
    url = (
        "https://www.googleapis.com/youtube/v3/search"
        f"?key={API_KEY}"
        f"&channelId={channel_id}"
        "&part=snippet"
        "&order=date"
        "&maxResults=5"
        "&type=video"
    )

    response = requests.get(url)
    data = response.json()

    for item in data.get("items", []):
        video_id = item["id"]["videoId"]
        link = f"https://www.youtube.com/watch?v={video_id}"

        if link in existing_links:
            continue

        feed.append({
            "title": item["snippet"]["title"],
            "channel": item["snippet"]["channelTitle"],
            "excerpt": item["snippet"]["description"][:150],
            "date": item["snippet"]["publishedAt"],
            "link": link,
            "thumbnail": item["snippet"]["thumbnails"]["medium"]["url"],
            "platform": "YouTube"
        })

# ترتيب الأحدث أولًا
feed = sorted(feed, key=lambda x: x["date"], reverse=True)

# تحديد عدد أقصى للفيديوهات
feed = feed[:MAX_VIDEOS]

# حفظ الملف
with open(FEED_FILE, "w", encoding="utf-8") as f:
    json.dump(feed, f, ensure_ascii=False, indent=2)
