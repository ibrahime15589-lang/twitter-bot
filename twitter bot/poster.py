"""
poster.py
content_ideas.json içindeki fikirleri sırayla Twitter/X'te paylaşır.
Ücretsiz Twitter/X Developer hesabı yeterli (developer.twitter.com).

Kurulum:
    pip install tweepy --break-system-packages

Ücretsiz API anahtarlarını al:
    1. developer.twitter.com -> "Sign up for Free Account"
    2. Yeni bir App oluştur, "Read and Write" izni ver
    3. API Key, API Secret, Access Token, Access Token Secret'ı kopyala
    4. Aşağıya veya ortam değişkenlerine yapıştır
"""

import tweepy
import json
import os

# --- Buraya kendi ücretsiz API bilgilerini gir (ya da ortam değişkeni kullan) ---
API_KEY = os.environ.get("X_API_KEY", "BURAYA_YAZ")
API_SECRET = os.environ.get("X_API_SECRET", "BURAYA_YAZ")
ACCESS_TOKEN = os.environ.get("X_ACCESS_TOKEN", "BURAYA_YAZ")
ACCESS_TOKEN_SECRET = os.environ.get("X_ACCESS_TOKEN_SECRET", "BURAYA_YAZ")

IDEAS_FILE = "content_ideas.json"


def get_client():
    return tweepy.Client(
        consumer_key=API_KEY,
        consumer_secret=API_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET,
    )


def post_next_idea():
    """Sıradaki içerik fikrini paylaşır ve listeden siler."""
    if not os.path.exists(IDEAS_FILE):
        print("İçerik fikri bulunamadı. Önce trend_finder.py çalıştır.")
        return

    with open(IDEAS_FILE, "r", encoding="utf-8") as f:
        ideas = json.load(f)

    if not ideas:
        print("Paylaşılacak fikir kalmadı. Önce trend_finder.py çalıştır.")
        return

    next_idea = ideas.pop(0)
    client = get_client()

    try:
        client.create_tweet(text=next_idea["content_idea"][:280])
        print(f"Paylaşıldı: {next_idea['content_idea']}")
    except Exception as e:
        print(f"Paylaşım başarısız: {e}")
        ideas.insert(0, next_idea)  # başarısızsa geri koy
        return

    with open(IDEAS_FILE, "w", encoding="utf-8") as f:
        json.dump(ideas, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    post_next_idea()
