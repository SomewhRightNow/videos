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
