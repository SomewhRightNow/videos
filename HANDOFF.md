# HANDOFF — son durum (21.11.2026, 04:00 UTC civarı)
Kanal: 139 abone, 127k izlenme, 69 video. HEDEF: hafta sonu (22.11) bitene kadar 200 abone.
Strateji ve seri/ses planı: OPERASYON.md -> "STRATEJİ" ve "STİL KURALI".

## Son yüklenen
- 21.11 Xavi & Iniesta Tore Arsenal Apart (CLASSIC) -> bzXPaU3tQO0

## Hazır ama yüklenmedi
- kane-news/"Kane Out For Months.mp4" (BREAKING, Kane syndesmosis + Olise). Kullanıcı "yükle" demedi.
- Moura own goal: kullanıcı "yükleme" dedi -> İPTAL. (Yükleme çağrısı yarıda kesildi; kanalda çıkarsa kullanıcıya sor.)
- Diğer hazır dosyalar: wk-fix (8 maç fikstür, Acceleration müzik), cr986 (Ronaldo 986), cr14 (14 more to the dream). Medya dosyaları bu depoda değil; gerekiyorsa yeniden üret.

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
