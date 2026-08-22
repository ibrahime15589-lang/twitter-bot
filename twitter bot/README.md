# Finans Growth Bot — Sıfır Bütçeli Kitle Büyütme Botu

Bu bot iki şey yapar:
1. Google News RSS'ten güncel **finans/ekonomi haberlerini** (borsa, dolar, altın, kripto, faiz, enflasyon) çekip **içerik fikri üretir** — hiçbir API key gerekmez, tamamen ücretsiz. Piyasa/yatırım içeren başlıklara otomatik "yatırım tavsiyesi değildir" uyarısı ekler.
2. Ürettiği fikirleri **otomatik olarak Twitter/X'te paylaşır** (ücretsiz API ile)
3. GitHub Actions sayesinde **günde 3 kez kendi kendine çalışır** — bilgisayarını açık tutmana gerek yok, tamamen ücretsiz.

> İçerik konularını `trend_finder.py` içindeki `FINANCE_QUERIES` listesinden değiştirebilir/genişletebilirsin (örn. "hisse önerisi", "emtia fiyatları" vb. ekleyebilirsin).

## Kurulum (15-20 dakika, tamamen ücretsiz)

### 1. GitHub'a yükle
- Bu klasörü yeni bir GitHub reposuna (public veya private, farketmez) yükle.

### 2. Twitter/X ücretsiz Developer hesabı al
1. https://developer.twitter.com adresine git, ücretsiz hesap oluştur.
2. Bir "Project" ve "App" oluştur.
3. App ayarlarında **"Read and Write"** iznini aç (önemli, aksi halde paylaşım yapamaz).
4. API Key, API Key Secret, Access Token, Access Token Secret bilgilerini al.

### 3. Anahtarları GitHub'a güvenli şekilde ekle
Reponda: **Settings → Secrets and variables → Actions → New repository secret**
Şu 4 secret'ı ekle:
- `X_API_KEY`
- `X_API_SECRET`
- `X_ACCESS_TOKEN`
- `X_ACCESS_TOKEN_SECRET`

### 4. Bitti
GitHub Actions otomatik olarak günde 3 kez çalışacak: sabah finans haberlerinden fikir üretir, her çalıştırmada sıradaki fikri paylaşır.
İstersen "Actions" sekmesinden **"Run workflow"** butonuyla manuel de tetikleyebilirsin.

## Instagram / TikTok'a genişletmek istersen
İkisi de resmi API için **iş hesabı + geliştirici onayı** istiyor (hâlâ ücretsiz, sadece kurulumu birkaç gün sürebilir):
- Instagram: Meta for Developers → Instagram Graph API (Business hesabına bağlanman gerekiyor)
- TikTok: TikTok for Developers → Content Posting API (onay süreci var)

Bu ikisini kurmak istersen söyle, aynı yapıya modül olarak ekleyebiliriz.

## Gerçekçi beklenti
Bu bot sana **tutarlılığı** ve **trend yakalamayı** otomatikleştiriyor — asıl büyümeyi sağlayan şey düzenli, ilgi çekici içerik. Bot bunu kolaylaştırır ama sihirli değnek değil; ürettiği fikirleri ara sıra gözden geçirip kendi sesine göre düzenlemen büyümeyi hızlandırır.
