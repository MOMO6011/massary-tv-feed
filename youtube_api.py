import json
import os
import requests
import isodate
import time

API_KEY = os.environ.get("YOUTUBE_API_KEY")

CHANNEL_IDS = [
    "UCxmEEGYXJkgJJO12nJhXl5g",  # Omar Abdelrahim
    "UCEHvaZ336u7TIsUQ2c6SAeQ",  # DroosOnline
    "UCcZAb104e_K7yJc8e_hPyDQ",  # DroosOnline4u
    "UCSFHcQ6-5uayv5v7yLQFUYA",  # thedocwaleed
    "UCSNkfKl4cU-55Nm-ovsvOHQ",  # ElzeroWebSchool
    "UCQqN3qgYbkfd0EkdhJmN5tQ",  # ElzeroTube
    "UCWg_cj4kueGU2jXJ7Klk5qg",  # Bahaa.Henish
    "UCnGblT_CyMwswTIH9QmJ3YQ",  # GhareebElshaikh
    "UCdNo5yauE8IU-vS8_dO3qew",  # abouzaid
    "UCUdtq-Fvlw7_NjzduNTZsbg",  # Abdullah_yw
    "UChbuH4HULlesX_rzlozkT6Q",  # AliMuhammadAli
    "UCaUZb4SGMAFVOJMqXQM3V1w",  # a5drcom
    "UCIL3YfRG2k7V9EDC3jzy-kg",  # WalidTaha
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
    "UC4DXKosClX-lZirpQsIOjnQ"   # MicsPodcast
]

FEED_FILE = "feed_1.json"
MAX_VIDEOS = 50
feed = []
existing_links = set()

# تحميل الفيد القديم
try:
    with open(FEED_FILE, "r", encoding="utf-8") as f:
        feed = json.load(f)
        existing_links = {item["link"] for item in feed if "link" in item}
except:
    feed = []

for channel_id in CHANNEL_IDS:
    print(f"🔍 معالجة القناة: {channel_id}")

    channel_data = requests.get(
        "https://www.googleapis.com/youtube/v3/channels",
        params={
            "part": "contentDetails",
            "id": channel_id,
            "key": API_KEY
        }
    ).json()

    items = channel_data.get("items")

    if not items:
        print(f"⚠️ القناة {channel_id} لم ترجع بيانات – تم التخطي")
        continue

    uploads_playlist_id = items[0]["contentDetails"]["relatedPlaylists"]["uploads"]

    playlist_data = requests.get(
        "https://www.googleapis.com/youtube/v3/playlistItems",
        params={
            "part": "snippet,contentDetails",
            "playlistId": uploads_playlist_id,
            "maxResults": 50,
            "key": API_KEY
        }
    ).json()

    video_ids = [
        item["contentDetails"]["videoId"]
        for item in playlist_data.get("items", [])
    ]

    if not video_ids:
        continue

    videos_data = requests.get(
        "https://www.googleapis.com/youtube/v3/videos",
        params={
            "part": "contentDetails",
            "id": ",".join(video_ids),
            "key": API_KEY
        }
    ).json()

    durations = {
        v["id"]: isodate.parse_duration(
            v["contentDetails"]["duration"]
        ).total_seconds()
        for v in videos_data.get("items", [])
    }

    for item in playlist_data.get("items", []):
        video_id = item["contentDetails"]["videoId"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        if video_url in existing_links:
            continue

        if durations.get(video_id, 0) < 90:
            continue  # تجاهل Shorts

        feed.append({
            "title": item["snippet"]["title"],
            "channel": item["snippet"]["channelTitle"],
            "excerpt": item["snippet"]["description"][:150],
            "date": item["snippet"]["publishedAt"],
            "link": video_url,
            "thumbnail": item["snippet"]["thumbnails"]["medium"]["url"],
            "platform": "YouTube"
        })

    time.sleep(0.2)

feed = sorted(feed, key=lambda x: x["date"], reverse=True)[:MAX_VIDEOS]

with open(FEED_FILE, "w", encoding="utf-8") as f:
    json.dump(feed, f, ensure_ascii=False, indent=2)

print(f"✅ تم تحديث feed_1.json | إجمالي الفيديوهات: {len(feed)}")
