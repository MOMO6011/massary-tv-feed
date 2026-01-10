import json
import os
import requests
import isodate

API_KEY = os.environ.get("YOUTUBE_API_KEY")

CHANNEL_IDS = [
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
    "UC4DXKosClX-lZirpQsIOjnQ"   # MicsPodcas
]

FEED_FILE = "feed_1.json"
MAX_VIDEOS = 50
feed = []
existing_links = set()

# قراءة البيانات السابقة
try:
    with open(FEED_FILE, "r", encoding="utf-8") as f:
        feed = json.load(f)
        existing_links = {item.get("link") for item in feed if "link" in item}
except:
    feed = []

for channel_id in CHANNEL_IDS:
    # الحصول على uploads playlist لكل قناة
    channel_data = requests.get(
        f"https://www.googleapis.com/youtube/v3/channels?part=contentDetails&id={channel_id}&key={API_KEY}"
    ).json()

    items = channel_data.get("items") if not items:     print(f"⚠️ القناة {channel_id} لم ترجع أي بيانات، سيتم تخطيها.")     continue  uploads_playlist_id = items[0]["contentDetails"]["relatedPlaylists"]["uploads"]

    # جلب الفيديوهات مع contentDetails لتفادي request إضافي
    playlist_url = (
        f"https://www.googleapis.com/youtube/v3/playlistItems"
        f"?playlistId={uploads_playlist_id}"
        f"&part=snippet,contentDetails"
        f"&maxResults=50"
        f"&key={API_KEY}"
    )
    playlist_data = requests.get(playlist_url).json()

    for item in playlist_data.get("items", []):
        video_id = item["contentDetails"]["videoId"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        if video_url in existing_links:
            continue

        # ✅ حماية ضد KeyError و تجاهل Shorts
        content = item.get('contentDetails', {})
        duration = content.get('duration')
        if not duration:
            continue  # تجاهل الفيديوهات بدون مدة

        video_seconds = isodate.parse_duration(duration).total_seconds()
        if video_seconds < 60:
            continue  # تجاهل Shorts

        # إضافة الفيديو للـ feed
        feed.append({
            "title": item["snippet"]["title"],
            "channel": item["snippet"]["channelTitle"],
            "excerpt": item["snippet"]["description"][:150],
            "date": item["snippet"]["publishedAt"],
            "link": video_url,
            "thumbnail": item["snippet"]["thumbnails"]["medium"]["url"],
            "platform": "YouTube"
        })

# ترتيب الأحدث فوق + أقصى عدد فيديوهات
feed = sorted(feed, key=lambda x: x["date"], reverse=True)
feed = feed[:MAX_VIDEOS]

# حفظ JSON
with open(FEED_FILE, "w", encoding="utf-8") as f:
    json.dump(feed, f, ensure_ascii=False, indent=2)

print(f"تم تحديث feed_1.json بنجاح! إجمالي الفيديوهات: {len(feed)}")
