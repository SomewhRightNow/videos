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
- Yayıncı logolarını silme (istisna: kullanıcı açıkça isterse bulanıklaştır — 21.11 Sakamoto). Content ID'den kaçmak için klip dönüştürme yapma. YouTube cookie kullanma, bot korumasını aşma.
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

## OYNATMA LİSTESİ KURALI (kullanıcı, 21.11)
Her videonun üst etiketi = oynatma listesi adı (BREAKING, LAST NIGHT, GOAL OF THE DAY, ON THIS DAY, CLASSIC, TOP 5, PLAY ALONG, BIG GAMES, FANS). Künyeye "Playlist: <ad>" satırı ekle; yükleyince listeye ekle. Lig/yıldız listesi ancak 6+ video olunca açılır. Dağılım ve video ID'leri: PLAYLISTS.md (yeni yüklemeyi oraya da yaz).
Topluluk gönderileri (Posts): esasen abonelere gider -> abone kazanımı için kullanma; en fazla haftada 1 maç önü anketi. Anlık haber = BREAKING Short.

## TELİF RİSK UYARISI (kullanıcı, 21.11 — Anderson videosu PL Content ID ile DÜNYA GENELİNDE ENGELLENDİ)
Teslimden ÖNCE riski sınıfla. YÜKSEK riskte cevabın EN BAŞINA "🔴 **YÜKSEK TELİF RİSKİ — ENGELLENEBİLİR**" satırını koy ve nedenini yaz (terminal kırmızı yazı desteklemiyor; kırmızı = 🔴).
- YÜKSEK (engellenir): Premier League yayın görüntüsü (TNT/Sky/NBC/beIN vb., özellikle MAÇ GÜNÜ/aynı hafta), La Liga, Bundesliga, Serie A, Ligue 1, UCL/UEL güncel yayın görüntüsü; FIFA Dünya Kupası/World Cup yayınları. Aynı gün yüklenen lig maçı yayın klibi = neredeyse kesin engel.
- ORTA: eski maç yayın görüntüsü (yıllar önce, ikinci lig, telefonla TV çekimi), fan hesaplarındaki derlemeler.
- DÜŞÜK: tribünden çekilmiş taraftar videosu, resmi kulüp/federasyon/UEFA sosyal klipleri (Wirtz, Nusa geçti), Commons fotoğraf + VO formatı.
YÜKSEK riskte alternatif öner: sadece tribün çekimi, ya da Commons foto + skor kartı + VO (Almanya 5-0 formatı).

## REFERANS ARAÇLAR (kullanıcı, 21.11)
_refs/ altında: ffmpeg-skill, rea-video, lemo-opuscar, OpenMontage. Ne işe yaradıkları ve komutlar: REFS.md. Her teslimden önce: `python3 /home/user/Filmler/_refs/ffmpeg-skill/scripts/check.py <video> --platform youtube-shorts` (FAIL varsa düzelt). Kullanıcı referans video verirse önce rea-video ile çözümle.

## YÜKLEME KALİTESİ (kullanıcı, 21.11: "YouTube'a yüklenince görüntü bozuluyor")
Nedenler: (1) 1080p yükleme -> YouTube düşük bitrate AVC verir; (2) GitHub 100MB sınırı için crf19/9M ile yeniden sıkıştırıyorduk; (3) düşük çözünürlüklü kaynak klipler (576p) büyütülüyordu; (4) bulanık degrade arka planlar YouTube sıkıştırmasında bantlaşır.
Kural: yükleme kopyası HER ZAMAN 1440p (Shorts 1440x2560, uzun 2560x1440), crf 16, maxrate 45M, bt709 etiketli (engine.deliver varsayılanı bu). 100MB üstü -> Git LFS (yeniden sıkıştırma YOK). Kaynak en az 720p olmalı; daha düşükse uyar. Teslim öncesi ffmpeg-skill check.py.
- Gol edit'lerinde yavaş çekim tekrarı KOYMA (kullanıcı 21.11: "slow motion koyma"); klip gerçek hızda, kullanıcı fotoğraf verirse sona ekle.
- Müzik rotasyonu (kullanıcı 21.11): art arda videolarda aynı parçayı KULLANMA; her yeni videoda farklı FSM Team / Kevin MacLeod parçası seç, son kullanılanı OPERASYON.md kayıtlarından kontrol et. (21.11 tfb1/llf1/tgz1/lwb1/tgz2 hepsi Acceleration idi -> sıradakiler başka parça.)
