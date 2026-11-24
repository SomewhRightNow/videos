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
- Wikimedia 429/hız sınırında BEKLEME (kullanıcı 22.11, tekrar tekrar söyledi): hemen başka kaynağa geç (kulüp/federasyon basın fotoğrafları, Flickr CC, Unsplash/Pexels, haber siteleri HD) ya da eldekiyle bitir.
- Kaynak klipteki üçüncü taraf yazı/liste/filigran: büyük blur YAPMA (kullanıcı 22.11 'kocaman blur'); OpenCV inpainting denendi ama oyuncu geçişlerinde bozulma yaptı (kullanıcı beğenmedi) -> TERCİH: kaynağın yazısını tam örten KENDİ tasarım grafiğimiz (ör. ogm2 panel(): kendi geri sayım listemiz aynı yerde, kendi fontumuz). Sağ üst yayıncı logosu küçük blur kuralı aynen geçerli.
- Sıralama/derleme videoları (kullanıcı 22.11): her zaman GERİ SAYIM (#10 -> #1), en büyük isim/an #1 en sonda, büyük #rakam ekranda; merak için.
- Abone CTA'sı (kullanıcı 23.11): sadece sonda değil, videonun ALTINDA sabit kırmızı 'SUBSCRIBE' butonu baştan sona; videolar sıkmadan hızlı (boşluk az, VO ~1.15 hız).
- BAŞLIKLAR (kullanıcı 23.11 'başlıklar daha ilgi çekici olmalı'): ekran başlığı ve YouTube title merak/şok kancası olsun (ör. 'KEEPER, WHAT WAS THAT?!', 'WATCH THE KEEPER', 'He Did WHAT?'), düz bilgi değil; ama yanlış/clickbait iddia yok.
- BİLDİRİM (kullanıcı 22.11): her iş/video bitince (teslim dosyası gönderilince) PushNotification ile kısa bildirim at (ne bitti + telif riski).
- Eksik yetenek -> GitHub'da açık kaynak araç; ücretli servis yok.
- Stil: profesyonel futbol haber kanalı (BREAKING/CONFIRMED/CLASSIC etiketleri, temiz lower-third, hatasız İngilizce VO + altyazı, merak + abone CTA). Çocukça/duygusal ekran yazısı yok ("tears", "AURA" vb.). Seri başına farklı Kokoro sesi (OPERASYON.md STRATEJİ).
- Bilgiyi 2 kaynakla doğrula; tek kaynaklıysa videoya koyma ya da belirt.
- Yükleme yalnızca kullanıcı "yükle" deyince. Aksi halde dosya + künye ver (künye düz kopyalanabilir metin, kod bloğu değil).
- Yayıncı logosu: kullanıcı 21.11 "sağ üste bundan sonra hep blur" -> HER edit'te kaynak klibin SAĞ ÜST köşesini (yayıncı logosu) bulanıklaştır (Gaussian, kutu ~ kaynak genişliğinin %8'i x yüksekliğin %11'i, kenardan). Diğer logolara dokunma. Content ID'den kaçmak için klip dönüştürme yapma. YouTube cookie kullanma, bot korumasını aşma.
- Kullanıcının e-postası gizli; dış servislere gönderme.
- Her teslimde tek satır telif riski notu. Yorum sorusu evet/hayır olmasın. Quiz videolarında 2D grafik yok. Kliplerde zoom yok, oyunlar tam gösterilir.
- Müzik (24.11 düzeltme): free-stock-music.com'da 'not registered in YouTube Content ID' rozeti SADECE FSM Team (+Ron Gelinas, Surf House, parkour-introvert) parçalarında DOĞRULANDI. Alex-Productions/Electronic Senses/Glitch vb. sayfalarında rozet YOK -> Content ID durumu belirsiz, KULLANMA (Metaphonk/Go Hard gkg1'de kullanıldı = risk). Kevin MacLeod güvenli. Kullanıcı 24.11 'şarkıları değiştir, etkileyici şarkılar': FSM Team'den kullanılmamışları dene (Banger [drum&bass, drop 22 sn], Ride That Train [drop 12 sn], ESCP Abyss [drop 31 sn]); asıl trend/popüler şarkı için YouTube uygulamasında yüklerken Shorts ses kütüphanesinden 'Ses ekle' (lisanslı, engellenmez) öner. Ticari şarkıyı videoya gömme YASAK. Sentez müzik yapma.
- YENİ VİDEO FORMATI (kullanıcı 23.11): oyuncunun üstünde isim etiketi (gkg1/track.py forma rengi takibi + film.py name_tag), büyük #sıra, temiz alt bant, sabit abone butonu, sert phonk. FMA "CC BY" phonk'lar Content ID yedi -> kullanma. Sentez müzik yapma (kullanıcı beğenmiyor).

- TOPLULUK KURALLARI (24.11): mci1 Celta kutlaması (oyuncu arkadaşının sırtına/arkasına binen, cinsel çağrışımlı poz + 'teamwork' esprisi) YouTube 'Çıplaklık ve cinsel içerik' UYARISI aldı (ilk ihlal, kaldırıldı, gelir yok). 90 gün içinde 2. ihlal = ihtar (strike). Cinsel çağrışımlı kutlama/hareket, imalı başlık/espri, açık giyim, kavga/şiddet ağırlıklı içerik KULLANMA. Teslimde telif riskinin yanında 'topluluk kuralı riski' de değerlendir.

- ŞABLON 'MATCHDAY POSTER' (ucl1/film2.py, kullanıcı 24.11 'şablonu değiştir'): takım renklerine bölünmüş arka plan, videonun üstünde/altında dev takım adı + arma (kayarak gelir), beat'te beyaz çerçeve flaşı, kendi VS çipi, sonda bölünmüş renkli 'WHO WINS' kartları. Eski koyu kart şablonundan farklı; sıradaki videolarda şablonları dönüşümlü kullan.

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
- YÜKSEK (engellenir): Premier League yayın görüntüsü (ESKİ PL maçları da: 2025 Liverpool-MU derlemede engellendi) (TNT/Sky/NBC/beIN vb., özellikle MAÇ GÜNÜ/aynı hafta), La Liga, Bundesliga, Serie A, Ligue 1, UCL/UEL güncel yayın görüntüsü; FIFA Dünya Kupası/World Cup yayınları. Aynı gün yüklenen lig maçı yayın klibi = neredeyse kesin engel.
- 22.11: Resmi UEFA ŞL özeti (Dortmund 8-4 Legia 2016, X @ofsayt) UEFA Content ID yedi -> UEFA/ŞL özetleri ESKİ olsa da YÜKSEK.
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
