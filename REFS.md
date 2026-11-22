# REFERANS ARAÇLAR (kullanıcı ekledi, 21.11) — /home/user/Filmler/_refs/
Bootstrap her oturumda arka planda klonlar (GitHub'a senkron edilmez, 690 MB). Hepsi ücretsiz/açık kaynak. Python betiklerini `python3 <yol>` ile çalıştır (`-I` ile değil: modüller betik klasöründen yükleniyor).

## 1. ffmpeg-skill (kajisho5, MIT) — EN ÇOK KULLANILACAK
42 yerel FFmpeg aracı, sadece Python stdlib, bulut yok. Betikler: _refs/ffmpeg-skill/scripts/
- check.py <video> --platform youtube-shorts : TESLİM ÖNCESİ ZORUNLU KONTROL (9:16, 1080x1920, fps, -14 LUFS, true peak). Keeper videosunda denendi: hepsi PASS.
- scenes.py <video|mp3> --beats : vuruş ızgarası (hype edit kesmeleri için; FSM Acceleration'da güven 0.28 çıktı -> bu parçada kendi enerji analizimiz daha iyi). --highlights N --target 60 : uzun özetten en iyi anları seçer. --shots : sahne kesmeleri.
- cut.py --segments ... --snap beats : kesmeleri vuruşa oturtur.
- caption.py --srt / --transcribe --animate pop --karaoke : altyazı yakma (Whisper varsa).
- fit.py --aspect 9:16 : dikey çerçeve (bizde ZOOM YOK kuralı: --fit pad kullan, crop değil).
- speedramp.py, freeze.py : yavaş çekim / donma karesi. loudness.py : -14 LUFS.
- references/gotchas.md : yaygın hatalar.

## 2. rea-video (JuneYaooo, Apache-2.0) — REFERANS VİDEO ÇÖZÜMLEME
Bir videoyu sahne sahne çözer: çekim mi, yapay zekâ mı, kodla mı yapılmış, nasıl yeniden yapılır. Çıktı: report.html + VIDEO.md. Çevrimdışı mod ücretsiz (görüntü modeli API'si opsiyonel, KULLANMA - ücretli).
Kullanım: kullanıcı "şu tarz yap" diye TikTok/X referansı verince -> indir -> rea-video ile kesme süreleri, kurgu ritmi, yazı yerleşimi çıkar -> şablona uygula (ör. HYPE EDIT ŞABLONU). Kurulum: cd _refs/rea-video && pip install -e . (skills/rea-video/ talimatları).

## 3. lemo-opuscar (lemomo-ai) — 99 KOD FİLM STİLİ
Her stil = styles/<ad>/STYLE.md (kodla film tarifi). Kanal için uygun olanlar: news-package, caption-news, briefing-board, telestrator (taktik çizimi!), map-explainer, transit-map, text-flash-cuts, countdown (TOP 5 için), game-show (quiz için), halftone-dossier, newsreel (ON THIS DAY / CLASSIC için), dataviz, hardcore-info, spy-titles, kino-montage.
Kullanım: yeni seri/format tasarlarken ilgili STYLE.md'yi oku, kendi motorumuza (_engine) uyarla. Lisans: LICENSE dosyası parça parça; stil fikri serbest, demo varlıkları kopyalama.

## 4. OpenMontage (OpenMontageInc, AGPLv3) — AJAN VİDEO ÜRETİM HATTI
Araştırma -> senaryo -> varlık -> kurgu -> render (Remotion). pipeline_defs/: documentary-montage, clip-factory (uzun videodan çok kısa çıkarma), cinematic, animated-explainer, localization-dub (TR dublaj için fikir). Ücretsiz stok görüntü/arşivden gerçek hareketli klip korpusu kurabiliyor.
Kullanım: belgesel/uzun format ve "clip-factory" mantığı için referans; doğrudan kurmak ağır (Node + Remotion). AGPL: kodu değiştirip dağıtmıyoruz, sadece içeride kullanım -> sorun yok.

## 5. last30days-skill (mvanhorn, MIT) — SON 30 GÜNDE İNSANLAR NE KONUŞUYOR (kullanıcı ekledi 22.11)
Reddit, X, YouTube, TikTok, HN, Polymarket, web'deki son 30 günlük gönderileri etkileşime (upvote/beğeni) göre puanlayıp özet çıkarır. Kanal için: hangi futbolcu/olay şu an viral (video fikri), taraftar yorumlarından başlık/yorum sorusu, "tribün videosu" var mı araştırması.
Kurulum: bootstrap _refs/last30days-skill olarak klonlar ve ~/.claude/skills/last30days'e kopyalar -> /last30days <konu> ile çağrılır.
Kullanım (ajan içinde): engine önce bir sorgu planı ister (references/research-runbook.md Step 0.75, --plan - <<'PLAN_EOF' ... ) ya da --auto-resolve. HER ZAMAN --no-browser-cookies (kural: cookie yok).
SINIRLAR (22.11 test): bu ortamda Reddit/HN/DuckDuckGo/Startpage proxy'de KAPALI -> sonuç 0. Ortam izni eklenmek istendi ama servis reddetti; kullanıcı Ayarlar > ortam ağ izinlerinden www.reddit.com, old.reddit.com, hn.algolia.com, html.duckduckgo.com, www.startpage.com ekleyebilir. X/TikTok/Instagram ücretli anahtar (ScrapeCreators 10k ücretsiz kayıt, XAI) veya tarayıcı cookie istiyor -> cookie KULLANMA, ücretli servis yok. YouTube yt-dlp ile çalışır (bot korumasını aşma yok).

## 6. OpenCreator (krillinai, eski adı KrillinAI, Apache-2.0) — İÇERİK ÜRETİCİ ÇALIŞMA ALANI (kullanıcı ekledi 22.11)
Codex CLI tabanlı masaüstü/web uygulaması: video çevirisi (Whisper + LLM, iki dilli altyazı, dublaj, dikey/yatay render), indirici (yt-dlp), kapak/görsel/video üretimi, TTS, kısa video senaryosu, çöp adam animasyonu (packages/stickman-remotion), otomatik klip (geliştirmede).
Yol: _refs/opencreator. Ajan becerileri: skills/krillinai-{cli,subtitle,tts,render-vertical,render-horizontal,cover,pipeline}/SKILL.md.
SINIRLAR: çeviri/görsel/video üretimi/bulut TTS ÜCRETLİ anahtar ister (OpenAI, Aliyun, MiniMax, Kling, Veo...) -> KULLANMA. Ücretsiz kısımlar bizde zaten var (yt-dlp, Whisper/ffmpeg-skill, Kokoro/Supertonic, kendi motorumuz). Cookie gerektiren indirmeler YOK.
İşe yarayan fikirler: dikey videoda İKİ DİLLİ altyazı düzeni (render-vertical: üstte EN, altta TR), altyazı zamanlama/bölme mantığı (references/), stickman-remotion formatı (anlatımlı çizgi animasyon) fikir olarak.
