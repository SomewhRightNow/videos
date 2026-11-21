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
- Moura own goal: kullanıcı "yükleme" dedi -> İPTAL. (Yükleme çağrısı yarıda kesildi; kanalda çıkarsa kullanıcıya sor.)
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
