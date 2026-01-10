import json
import os
import requests

API_KEY = os.environ.get("YOUTUBE_API_KEY")

CHANNEL_IDS = [
    "UCcZAb104e_K7yJc8e_hPyDQ",  # DroosOnline4u
    "UCSFHcQ6-5uayv5v7yLQFUYA",  # thedocwaleed
    "UCQqN3qgYbkfd0EkdhJmN5tQ",  # ElzeroWebSchool
    "UCQqN3qgYbkfd0EkdhJmN5tQ",  # ElzeroTube
    "UCWg_cj4kueGU2jXJ7Klk5qg",  # Bahaa.Henish
    "UCscz2NaWRYuaDrwKBJkkVLQ",  # GhareebElshaikh
    "UCdNo5yauE8IU-vS8_dO3qew",  # abouzaid
    "UCUdtq-Fvlw7_NjzduNTZsbg",  # Abdullah_yw
    "UChbuH4HULlesX_rzlozkT6Q",  # AliMuhammadAli
    "UCaUZb4SGMAFVOJMqXQM3V1w",  # a5drcom
    "UCMZME066uGTeRUZcDQWaipA",  # WalidTaha
    "UC_nOoE4cIapZENcimY3I0uQ",  # KonoozTube
    "UC5RkBPuSzbyudZI0UA1B_Vw",  # TaherART
    "UC8eFjAmIUnLKLnfJZFPz6QQ",  # Ghanayem
    "UChmti2i_-Mn4_HE5liAfoXA",  # AhmedShahinOfficial
    "UCsQqxYEBQHILQS237kcoDKw",  # KareemEsmail
    "UC_o7uZRKgYgpv2SNhdCNmdg",  # EmadRashadOsman
    "UCVO0eI6y9QE0IHnpR2rxy5Q",  # EB85_
    "UC19LSQvi6ca8luKEWL0pdKw",  # W_wakeup
    "UCQPalfEYxVLs8nEB4LutApQ",  # thmanyahPodcasts
    "UCxHBGJc2HfCZbv2MgJ6F2Sw",  # BidonWaraq
    "UC89xhPO7T5uRpPK9Jl7NJrA",  # aramtv
    "UCfEjNgz1vYDYyury8q7PmYQ"   # MicsPodcas
]

FEED_FILE = "feed_1.json"
MAX_VIDEOS = 50  # أقصى عدد فيديوهات
feed = []

existing_links = set()

# قراءة بيانات سابقة لو موجودة
try:
    with open(FEED_FILE, "r", encoding="utf-8") as f:
        feed = json.load(f)
        existing_links = {item.get("link") for item in feed if "link" in item}
except:
    feed = []

for channel_id in CHANNEL_IDS:
    url = (
        f"https://www.googleapis.com/youtube/v3/search"
        f"?key={API_KEY}"
        f"&channelId={channel_id}"
        "&part=snippet"
        "&order=date"
        "&maxResults=5"
        "&type=video"
    )
    data = requests.get(url).json()
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

# تحديد أقصى عدد فيديوهات
feed = feed[:MAX_VIDEOS]

# حفظ الملف
with open(FEED_FILE, "w", encoding="utf-8") as f:
    json.dump(feed, f, ensure_ascii=False, indent=2)
