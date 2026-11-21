# Somewhere Right Now (YouTube: @somewhrightnow) — kalıcı kurallar
Kullanıcı Türkçe yazar; Türkçe cevap ver. Kanal global İngilizce futbol Shorts kanalıdır.

## Senkron (iki hesap tek beyin)
Bu klasör (/home/user/Filmler) GitHub SomewhRightNow/videos `workspace` dalıyla iki yönlü ANLIK senkron (hook'lar otomatik): oturum başında `_sync/bootstrap.sh` (klasör+kurallar+beceriler+araç kurulumu), HER kullanıcı mesajından önce `_sync/live.sh` (diğer hesabın yeni işi/sohbeti gelir ve gösterilir), HER cevaptan sonra konuşma kaydı + `srn_sync.sh push`. Diğer hesabın sohbeti: konusmalar/<tarih>.md — yeni oturumda oku ve kaldığı yerden devam et. Bitmiş videolar: `up-<isim>` dallarında (HANDOFF.md'de raw URL). Yeni kural -> bu dosyaya ekle; yeni bilgi/klip/yükleme -> OPERASYON.md; durum -> HANDOFF.md. Sonra push. Medya senkron edilmez.

## TEK HAFIZA (kullanıcı, 21.11)
Tüm hesaplar tek hafızadan ilerler: kalıcı her bilgi SADECE bu klasöre yazılır (kural -> CLAUDE.md, bilgi/klip/yükleme -> OPERASYON.md, durum/açık iş -> HANDOFF.md, sohbet -> konusmalar/ otomatik). Hesaba özel hafıza/not yerine her zaman buraya yaz. Bir hesap bir şey öğrendiyse/değiştirdiyse diğeri sonraki mesajda görür (live.sh). Çelişki olursa en yeni kayıt geçerli.

## Başlarken (yeni oturum / yeni hesap)
1. /home/user/Filmler yoksa: `git clone -b workspace --single-branch https://github.com/SomewhRightNow/videos /home/user/Filmler`, sonra `bash /home/user/Filmler/setup.sh` (araçlar, fontlar, Kokoro ses modeli).
2. `HANDOFF.md` (son durum + açık işler) ve `OPERASYON.md` (kullanılan klipler, yüklemeler, strateji, stil) oku.
3. Yapay zekâ görsel araçları (yüz değiştirme, SD-Turbo, YOLO, SAM) ve beceriler (cinematic-film harita/pano motoru, cinecode) gerekiyorsa: `bash /home/user/Filmler/setup_ml.sh` (~3 GB, bir kez).
4. Çalışma klasörü: /home/user/Filmler/<proje>/ ; motor: /home/user/Filmler/_engine/engine.py

## Kurallar
- Bir görüntü/klip/fotoğraf yalnızca BİR KEZ kullanılır (aynı klibin başka saniyesi/kırpması da tekrar sayılır); eski videolarda kullanılanlar kullanılmaz (OPERASYON.md'deki listeye bak, kullandığını oraya yaz).
- Eksik yetenek -> GitHub'da açık kaynak araç; ücretli servis yok.
- Stil: profesyonel futbol haber kanalı (BREAKING/CONFIRMED/CLASSIC etiketleri, temiz lower-third, hatasız İngilizce VO + altyazı, merak + abone CTA). Çocukça/duygusal ekran yazısı yok ("tears", "AURA" vb.). Seri başına farklı Kokoro sesi (OPERASYON.md STRATEJİ).
- Bilgiyi 2 kaynakla doğrula; tek kaynaklıysa videoya koyma ya da belirt.
- Yükleme yalnızca kullanıcı "yükle" deyince. Aksi halde dosya + künye ver (künye düz kopyalanabilir metin, kod bloğu değil).
- Yayıncı logolarını silme. Content ID'den kaçmak için klip dönüştürme yapma. YouTube cookie kullanma, bot korumasını aşma.
- Kullanıcının e-postası gizli; dış servislere gönderme.
- Her teslimde tek satır telif riski notu. Yorum sorusu evet/hayır olmasın. Quiz videolarında 2D grafik yok. Kliplerde zoom yok, oyunlar tam gösterilir.
- Müzik: sadece Content ID'ye kayıtlı olmayan parçalar (free-stock-music.com FSM Team "not registered" ibareli; Kevin MacLeod). FMA "CC BY" phonk'lar Content ID yedi -> kullanma. Sentez müzik yapma (kullanıcı beğenmiyor).

## Yükleme akışı
Video -> bu depoya tek-commit dal (`up-<isim>`), raw URL https://raw.githubusercontent.com/SomewhRightNow/videos/up-<isim>/<dosya>.mp4 -> Zapier YouTube `youtube_upload_video` (title, description, video=raw URL, tags, privacy_status public, category_id 17, made_for_kids false, default_language en, localizations tr). Zapier "throttled" derse kota dolu: kullanıcıya elle yüklemeyi öner. Zapier bağlantısı hesaba bağlıdır; yeni hesapta kullanıcı kendi Zapier+YouTube bağlantısını kurmalı.

## EDIT STİLİ (kullanıcı, 21.11) — "edit" istendiğinde varsayılan bu
Referans: TikTok @00.09.66.00 "Spain vs France" hype edit (19 sn, 55.8K izlenme, 3.6K beğeni). Ayrıntı: OPERASYON.md "HYPE EDIT ŞABLONU".
- Yapı: 1) kanca/bağlam (ör. kura çekimi "SPAIN" - "FRANCE" kâğıdı açılıyor, 0-5 sn) 2) kupa/sahne görseli (1-2 sn) 3) beat'e senkron HIZLI KESMELER: yıldız oyuncuların yakın plan bakışları, gol sevinçleri, tünel/marş anları (her kesme 0.3-1.3 sn, drop'ta hızlanır) 4) son kare güçlü sevinç/poz.
- Yazı yok ya da minimum; seslendirme yok. Soru açıklamada/başlıkta: "Who will win?".
- Müzik: sert phonk/drop'lu parça, kesmeler vuruşa oturur. (Telif: sadece FSM Team "not registered" / Kevin MacLeod; ticari şarkı KULLANMA.)
- Konu: büyük maç öncesi iki takım/iki yıldız karşılaşması (X vs Y), derbi, final.
