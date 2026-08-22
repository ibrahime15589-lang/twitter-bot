"""
trend_finder.py  (finans odaklı sürüm)
Google News RSS üzerinden güncel finans/ekonomi haberlerini çeker
ve bunlardan paylaşılabilir içerik fikirleri üretir.
Tamamen ücretsiz - API key GEREKMEZ, sadece Python standart kütüphaneleri kullanır.
"""

import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import random
import json
import os
import ssl

# Finans/ekonomi ile ilgili Google News RSS aramaları (Türkçe)
FINANCE_QUERIES = [
    "borsa",
    "dolar kuru",
    "altın fiyatları",
    "kripto para",
    "faiz kararı",
    "enflasyon",
    "ekonomi haberleri",
]

RSS_URL = "https://news.google.com/rss/search?q={query}&hl=tr&gl=TR&ceid=TR:tr"

# İçerik fikri şablonları - haber başlığını bu kalıplara oturtuyoruz
CONTENT_TEMPLATES = [
    "📊 Gündem: {headline}\nSizce bu piyasayı nasıl etkiler?",
    "💬 {headline}\nBu haberi nasıl yorumluyorsunuz?",
    "🔎 Bugünün önemli finans haberi:\n{headline}",
    "📈 {headline}\nDetaylar için kaynağa bakın, kısa yorumumu thread'de paylaşacağım 🧵",
    "⚡ Flaş: {headline}",
]

DISCLAIMER = "\n\n(Yatırım tavsiyesi değildir.)"


def _clean_headline(headline):
    """Google News RSS başlığının sonundaki kaynak adını (' - Milliyet' vb.) temizler."""
    if not headline:
        return ""
    if " - " in headline:
        headline = headline.rsplit(" - ", 1)[0].strip()
    return headline


def _fetch_rss(query):
    """Tek bir sorgu için Google News RSS başlıklarını çeker."""
    url = RSS_URL.format(query=urllib.parse.quote(query))
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
        data = resp.read()
    root = ET.fromstring(data)
    headlines = []
    for item in root.findall(".//item")[:5]:
        title = item.find("title")
        if title is not None and title.text:
            cleaned = _clean_headline(title.text)
            if cleaned:
                headlines.append(cleaned)
    return headlines


def get_finance_headlines(limit=10):
    """Birkaç finans sorgusundan toplam başlık listesi döner."""
    all_headlines = []
    for q in FINANCE_QUERIES:
        try:
            all_headlines.extend(_fetch_rss(q))
        except Exception as e:
            print(f"'{q}' için haber çekilemedi: {e}")
    unique = list(dict.fromkeys(all_headlines))
    random.shuffle(unique)
    return unique[:limit]


def generate_content_ideas(headlines):
    """Her haber başlığı için 1 içerik fikri üretir."""
    ideas = []
    for headline in headlines:
        template = random.choice(CONTENT_TEMPLATES)
        text = template.format(headline=headline)
        if any(k in headline.lower() for k in ["borsa", "dolar", "altın", "kripto", "faiz"]):
            text += DISCLAIMER
        ideas.append({"headline": headline, "content_idea": text})
    return ideas


def save_ideas(ideas, path="content_ideas.json"):
    """Üretilen fikirleri dosyaya kaydeder (bot bunları sırayla paylaşacak)."""
    existing = []
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                existing = json.load(f)
        except Exception:
            existing = []

    existing_headlines = {item.get("headline") for item in existing if isinstance(item, dict)}
    new_ideas = [i for i in ideas if i.get("headline") not in existing_headlines]

    existing.extend(new_ideas)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)
    print(f"{len(new_ideas)} yeni finans içerik fikri kaydedildi -> {path}")


if __name__ == "__main__":
    headlines = get_finance_headlines()
    print("Güncel finans haberleri:")
    for h in headlines:
        print(" -", h)
    ideas = generate_content_ideas(headlines)
    save_ideas(ideas)
