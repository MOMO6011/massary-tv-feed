import json
from datetime import datetime

# البيانات التجريبية
feed = [
    {
        "title": "تجربة فيديو " + datetime.now().strftime("%H:%M:%S"),
        "channel": "Test Channel",
        "excerpt": "ملخص الفيديو التجريبي الجديد.",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "link": "https://example.com/video"
    }
]

# كتابة البيانات على feed.json
with open("feed.json", "w", encoding="utf-8") as f:
    json.dump(feed, f, ensure_ascii=False, indent=2)
