import json
import os
import requests

API_KEY = os.environ.get("YOUTUBE_API_KEY")

CHANNEL_IDS = [
    "UC_x5XG1OV2P6uZZ5FSM9Ttw"  # مثال - هنغيره بعدين
]

FEED_FILE = "feed_1.json"


try:
    with open(FEED_FILE, "r", encoding="utf-8") as f:
        feed = json.load(f)
except:
    feed = []

existing_links = {item.get("link") for item in feed}

for channel_id in CHANNEL_IDS:
    url = (
        "https://www.googleapis.com/youtube/v3/search"
        f"?key={API_KEY}"
        f"&channelId={channel_id}"
        "&part=snippet"
        "&order=date"
        "&maxResults=3"
    )

    data = requests.get(url).json()

    for item in data.get("items", []):
        if item["id"]["kind"] != "youtube#video":
            continue

        video_id = item["id"]["videoId"]
        link = f"https://www.youtube.com/watch?v={video_id}"

        if link in existing_links:
            continue

        feed.append({
            "title": item["snippet"]["title"],
            "channel": item["snippet"]["channelTitle"],
            "excerpt": item["snippet"]["description"][:150],
            "date": item["snippet"]["publishedAt"][:10],
            "link": link,
            "platform": "YouTube"
        })

with open(FEED_FILE, "w", encoding="utf-8") as f:
    json.dump(feed, f, ensure_ascii=False, indent=2)
