# HANDOFF — son durum (21.11.2026, 04:00 UTC civarı)
Kanal: 139 abone, 127k izlenme, 69 video. HEDEF: hafta sonu (22.11) bitene kadar 200 abone.
Strateji ve seri/ses planı: OPERASYON.md -> "STRATEJİ" ve "STİL KURALI".

## Son yüklenen
- 21.11 On This Day 2012 Mexès overhead kick (Anderlecht 1-3 Milan) -> to7oHtH8LaE
- 21.11 Messi LAST UCL Goal for Barcelona -> be7R-NhxZtA
- 21.11 On This Day 2007 England 2-3 Croatia -> WR941GM4zTY
- 21.11 Xavi & Iniesta Tore Arsenal Apart (CLASSIC) -> bzXPaU3tQO0

## Hazır ama yüklenmedi
- kane-news/"Kane Out For Months.mp4" (BREAKING, Kane syndesmosis + Olise). Kullanıcı "yükle" demedi.
- Moura own goal: kullanıcı "yükleme" demişti AMA kanalda yayında (VGn6YYz2QsQ "Porto Scores Own Goal vs a 3rd-Tier Team") -> kullanıcıya soruldu.
- Diğer hazır dosyalar: wk-fix (8 maç fikstür, Acceleration müzik), cr986 (Ronaldo 986), cr14 (14 more to the dream). Medya dosyaları bu depoda değil; gerekiyorsa yeniden üret.


## 21.11 öğlen durum (hesap değişimi öncesi)
- Bekleyen yüklemeler (YouTube kotası doldu, Zapier throttled): 
  1) Top 5 Free Kicks -> raw https://raw.githubusercontent.com/SomewhRightNow/videos/up-top5fk/top5-free-kicks.mp4 (künye konuşma 2026-11-21.md'de)
  2) Nakamura ON THIS DAY -> raw https://raw.githubusercontent.com/SomewhRightNow/videos/up-nakamura/otd-nakamura-2006.mp4
  3) Open Goal Missed -> raw https://raw.githubusercontent.com/SomewhRightNow/videos/up-opengoal/open-goal-missed.mp4
  Künyeler: konusmalar/2026-11-21.md (son hâlleri). Kullanıcı "yükle" derse Zapier ile bu raw URL'leri yükle.
- Devam eden: kits1 "IN ANOTHER UNIVERSE" (oyuncu başka formada). Yüz değişimi denendi (Messi->Valverde RM karesi); kullanıcı "alakası yok" dedi -> sonraki adım: oyuncunun KENDİ fotoğrafında forma değişimi (433 tarzı). Videoda "In another universe" çerçevesi + YouTube altered content beyanı.
- Kullanıcı tercihleri: derleme verirse Top5 yapma, tamamını kullan + yazı + müzik; "edit" = HYPE EDIT şablonu (CLAUDE.md).
- Canlı: Man City 0-1 Fulham (Muniz 15', Haaland golü VAR iptal) -> Fulham kazanırsa BREAKING önerildi.

## Hafta sonu takvimi (TSİ)
- Cmt 20:30 Newcastle–Arsenal, 23:00 Real Madrid–Celta, gece Sudamericana finali Boca–Atlético Mineiro.
- Paz 15:00 Barcelona–Villarreal, 19:30 Liverpool–Man Utd (Pochettino'nun ilk maçı), 22:45 Atalanta–Inter.
- Canlı takip: python3 /home/user/Filmler/_live/watch.py <lig> <espn_event_id> (ESPN scoreboard API ile id bul; ör. eng.1, esp.1, ita.1, ger.1, conmebol.sudamericana).
- Planlanan ilk video: Pochettino'nun ilk maçı önizlemesi (BREAKING/PREVIEW, ses am_michael).

## Araçlar
- Klip bulma: python3 /home/user/Filmler/_engine/tools/dm_find.py YYYY-MM-DD "sorgu"... (Dailymotion; Diario Libero / La República 8-11 sn gol klipleri, beIN AU özetleri).
- X videoları: cdn.syndication.twimg.com/tweet-result?id=<id>&token=a + yt-dlp. TikTok: yt-dlp.
- Commons fotoğraf: projects/nl-faceoff/logs/{cs,thumbs,get2}.py
- Haber şablonu (VO+altyazı+lower-third): projects/kane-news/{film.py,mix.py}; CLASSIC şablonu: projects/ft1/.
- TTS: ~/.cinecode/kokoro/venv/bin/python <proje>/logs/kokoro_tts.py <ses> 1.08 out.wav "metin"

## 21.11 14:10 UTC — ikinci hesap (Pro) oturumu
- Bu hesabın bulut ortamı "videos" adlı kişisel ortama alındı (Default ortam X/twimg'i engelliyordu). İzinli: x.com, api.x.com, twitter.com, *twimg (cdn.syndication, video, pbs, abs), free-stock-music.com, dailymotion (www/api/geo), tiktok (www/vt), commons/upload.wikimedia.org. Dailymotion CDN (dmcdn.net) listede yok; engellenirse eklenmeli.
- tfb1 "Keeper Sent Off For This" HAZIR (raw up-tfb1/keeper-sent-off.mp4). Kullanıcı "yükle" demedi.
- llf1 "Anderson Equaliser" HAZIR (raw up-anderson/anderson-equaliser.mp4). Maç sonucu 88. dk itibarıyla 1-1, final teyit edilmedi. Kullanıcı "yükle" demedi.
- 21.11 14:45: Oynatma listesi planı PLAYLISTS.md (9 format + 2 yıldız listesi, 76 video dağıtıldı). Listeleri oluşturma: Zapier bağlanınca dene, yoksa kullanıcı Studio'dan.
- UZUN VİDEO konu adayı (kullanıcı "kenarda kalsın", 21.11): "Same parents, different countries" — Williams (Nico İspanya / Iñaki Gana) + Doué (Désiré Fransa / Guéla Fildişi) kardeşler, 2026 DK. Kadrolar henüz doğrulanmadı. Reddedilenler: Ronaldo/Messi/Haaland/Norveç (çok çekildi), City 115, 2030 DK 3 kıta, İspanya marşı, kupa replikası, soccer kelimesi, ağız kapatma, çorap deliği, Merlin ördek.
- brothers (UZUN VİDEO, kullanıcı onayladı 21.11): Williams + Doué kardeşler. Senaryo taslağı brothers/script.md (37 satır, ~3:20). Durum: kullanıcı onayı bekleniyor; sonra Commons foto + harita + VO + 2560x1440 render.
- tgz1 "Coventry 1-1 Palace" HAZIR (yerel). brothers belgeseli SIRADA (2K): VO hazır (bm_lewis 3:00, audio/narration.m4a), harita hazır, Commons arama logs/cs.json (rate-limit), müzik seçilecek.
- brothers v3: HAZIR + QA geçti (up-brothers LFS). Kullanıcı "kontrol et, sorun yoksa yükle" dedi; bu hesapta Zapier yok -> diğer hesap yükleyebilir (raw: media.githubusercontent.com/media/SomewhRightNow/videos/up-brothers/same-parents-different-countries.mp4).
- brothers v2: kullanıcı QA istedi; bulunan sorunlar (altyazı bandı çakışması, Doué bölümünde İñaki fotoğrafı görünmesi, boş kareler, Liberya kadraj dışı) scene.py'de düzeltildi, v2 render + burn arka planda (logs/render2.log, burn2.log). YouTube yüklemesi bu hesapta yok (Zapier bağlı değil).
- 22.11 Nico belgeseli kapağı: brothers/thumb/make.py (rembg kesimler P01/P03, İspanya kırmızı/Gana altın çapraz, WHY? rozeti) -> thumbnail_2560.jpg + 1280
- 24.11: TikTok CDN hostları (v16/v19-webapp-prime.us.tiktok.com, sf16.tiktokcdn-us.com, p19-common-sign) ortam ağına EKLENDİ -> TikTok linkleri yt-dlp ile iniyor. ZSsLJsPX7 (çalım derlemesi) indirildi, edit sırada.

## 25.11 UZUN VİDEO: Haaland belgeseli (DEVAM EDİYOR)
- Konu (kullanıcı onayladı): "Why Football Legends Still Can't Explain Haaland" (~3 dk), sonra seri: Mbappé.
- Proje: /home/user/Filmler/haaland (cinematic-film becerisi). script.json (36 satır, EN + 'tr' alanı Türkçe dublaj), beats.md, fact_notes (2 kaynak).
- Türkçe dublaj: Piper TTS tr_TR-dfki-medium (haaland/tts/). EN: Kokoro (bm_george / am_onyx örnekleri).
- Durum: senaryo + ses örnekleri kullanıcı onayında (Gate 1).

## 25.11 sabah
- tt5 "Keeper, HOW Did You Save That?!" (Impossible GK Saves) teslim edildi, yüklenmedi.
- Haaland uzun belgesel (haaland/): 2K render bitti; EN + TR dublaj mp4 paketleniyor (out/), SRT en/tr, thumbnail, credits hazır.
- 25.11 öğlen: Haaland v2 (PRESSWIND yapısı + Chatterbox ses) bitti: EN önizleme + TR dublaj .m4a + SRT teslim. Yükleme kopyası: haaland/out/'Haaland v2 EN 1440p (yukleme).mp4' (1440p crf16, ~1 GB -> yüklerken LFS/up-haaland dalı). Kullanıcı 'yükle' demedi.
- 25.11 16:45 Haaland v2 GitHub'da: up-haaland dalı (LFS). Video: https://media.githubusercontent.com/media/SomewhRightNow/videos/up-haaland/why-legends-cant-explain-haaland.mp4 (2560x1440, 3:12.8, 1.1 GB, check.py PASS) + thumbnail.jpg + haaland_tr_dub.m4a + haaland_en.srt/haaland_tr.srt. Künye: konusmalar/2026-11-25.md. Bu hesapta Zapier YOK -> kullanıcı elle ya da Zapier'li hesap yükler. TR dublaj Studio > Diller > ses parçası.
