import json
from datetime import datetime

# قراءة البيانات القديمة
try:
    with open("feed.json", "r", encoding="utf-8") as f:
        feed = json.load(f)
except:
    feed = []

# إضافة فيديو جديد
feed.append({
    "title": "AUTO TEST " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "channel": "Test Channel",
    "excerpt": "ملخص الفيديو التجريبي الجديد.",
    "date": datetime.now().strftime("%Y-%m-%d"),
    "link": "https://example.com/video"
})

# كتابة البيانات على feed.json
with open("feed.json", "w", encoding="utf-8") as f:
    json.dump(feed, f, ensure_ascii=False, indent=2)
