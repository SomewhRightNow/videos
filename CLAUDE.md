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
4. Seslendirme (Chatterbox EN+TR) gerekiyorsa: `bash /home/user/Filmler/setup_tts.sh` (~5 dk, 6.3 GB model, bir kez; idempotent).
5. Çalışma klasörü: /home/user/Filmler/<proje>/ ; motor: /home/user/Filmler/_engine/engine.py

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
- MÜZİK/SES (kullanıcı 24.11, KESİN: 'şarkı yok yeter, güzel futbol edit olsun'): Videolara ŞARKI KOYMA (free-stock dahil hiçbir müzik). Ses = kaynağın ORİJİNAL sesi (stadyum/taraftar/spiker) parçalara göre kesilip birleştirilir, -14 LUFS. Edit kalitesi (hızlı kesme, geçiş flaşı, kendi grafiklerimiz) öne çıkar. Kullanıcı isterse yüklerken YouTube 'Ses ekle' kullanır. Not: orijinal yayın sesi Content ID eşleşmesini artırabilir -> yayın görüntüsü zaten 🔴 ise risk notunda belirt. GÜNCELLEME 24.11 akşam: kullanıcı 'müzik ekle ama farklı' -> Kevin MacLeod (incompetech.com, CC BY, Content ID'de değil; ağ izni eklendi) kullanılabilir. Eldeki: Hitman (karanlık hip-hop/trap, drop 52 sn) dpen'de kullanıldı; Volatile Reaction, Cyborg Ninja, Movement Proposition, Take a Chance sırada. Free-stock YASAK devam. Kredi: '<parça> Kevin MacLeod (incompetech.com) Licensed under CC BY 4.0'.
- YENİ VİDEO FORMATI (kullanıcı 23.11): oyuncunun üstünde isim etiketi (gkg1/track.py forma rengi takibi + film.py name_tag), büyük #sıra, temiz alt bant, sabit abone butonu, sert phonk. FMA "CC BY" phonk'lar Content ID yedi -> kullanma. Sentez müzik yapma (kullanıcı beğenmiyor).

- TOPLULUK KURALLARI (24.11): mci1 Celta kutlaması (oyuncu arkadaşının sırtına/arkasına binen, cinsel çağrışımlı poz + 'teamwork' esprisi) YouTube 'Çıplaklık ve cinsel içerik' UYARISI aldı (ilk ihlal, kaldırıldı, gelir yok). 90 gün içinde 2. ihlal = ihtar (strike). Cinsel çağrışımlı kutlama/hareket, imalı başlık/espri, açık giyim, kavga/şiddet ağırlıklı içerik KULLANMA. Teslimde telif riskinin yanında 'topluluk kuralı riski' de değerlendir.

- ŞABLON 'MATCHDAY POSTER' (ucl1/film2.py, kullanıcı 24.11 'şablonu değiştir'): takım renklerine bölünmüş arka plan, videonun üstünde/altında dev takım adı + arma (kayarak gelir), beat'te beyaz çerçeve flaşı, kendi VS çipi, sonda bölünmüş renkli 'WHO WINS' kartları. Eski koyu kart şablonundan farklı; sıradaki videolarda şablonları dönüşümlü kullan.

- ABONE BUTONU METNİ (kullanıcı 24.11 'alttaki kırmızı yere abone çekebilecek bir şey yazmalıyız'): sadece 'SUBSCRIBE · DAILY FOOTBALL' YETMEZ. Yeni tasarım (gal3/ov2.png): büyük kırmızı pill, zil ikonu + 'SUBSCRIBE' (büyük, beyaz) + 2. satır SARI vaat. Vaat içeriğe göre: gol/maç gecesi 'NEVER MISS A GOAL'; Ronaldo serisi 'DON'T MISS GOAL 988' (sıradaki sayı); seri/Part videoları 'PART 2 IS COMING'; klasik/on this day 'A NEW CLASSIC EVERY DAY'; sıralama 'MORE TOP LISTS DAILY'. Yalan vaat yok (Part 2 sadece gerçekten yapılacaksa).

- SIRALAMA ŞABLONU 'RANK LADDER' (kullanıcı 25.11: 'sol tablo tüm ekranı kaplıyor, sıralamalar için güzel kaliteli şablon'; tf2/film2.py): görüntü tam ekran ve dokunulmadan; üstte başlık plakası (İÇERİK BAŞLIĞI BÜYÜK, kaynaktaki gibi: ör. 'SMART [TACTICAL FOULS sarı] IN FOOTBALL' — kullanıcı 25.11 'içeriğin ne olduğu yazmalı' + sarı/kırmızı kare rozet içinde sıra no + büyük isim, alt sarı çizgi, gölge) kaynağın başlığını örter; bağlam sarı bayrak olarak altından kayar; sol merdiven: SADECE kaynakta yazı olan/bizim açılmış satırlar tam pill, boş satırlar küçük numara çipi; satırlar bitişik (aralıktan kaynak yazısı sızmasın), %100 opak; abone pill kaynak filigranını örter. Kaynağın listesi yoksa merdiveni küçük tut. Eski 'clean countdown' (tf2/film.py) KULLANMA. İPUCU: kaynak listesi zamanla açılıyorsa sırayı kaynağın açılma sırasına yakın kur (boş kapak satırı az olsun), pill genişliği = kaynak yazı genişliği (hd1/film.py srcw).

- CANLI MAÇ GOL KLİPLERİ (kullanıcı 25.11: 'bu gol videolarında canlı olan Deniz Gül'e yaptığımız gibi isim yazıp geçmen lazım'): o akşam oynanan maçın gol klibi gelirse DÜZ KLİP yap (gal3/tk1 plain.py): klip tamamı + orijinal ses, -14 LUFS; üst plaka SADECE isim + dakika + skor (ör. 'LUIS SUÁREZ 80'' / 'SPORTING 2-2 MAN UNITED'), kaynak yazısını örter; imza + abone pill. VO, tekrar, isim etiketi takibi, kapanış kartı YOK; hızlı teslim (ffmpeg overlay, birkaç dakika). Hikâye/VO'lu BREAKING edit sadece kullanıcı isterse. ŞABLON (kullanıcı 25.11 'artık deniz gül videosundaki şablonu kullan'): gal1 düzeni = koyu zemin, ortada video, üstte ortalı BEYAZ 'İSİM · DK'' + beyaz skor satırı (kullanıcı 25.11: SARI YOK, çizgi yok, sadece isim/dk/skor), videonun sağ altında küçük imza, altta kırmızı abone pill (beyaz yazı) (pm1/deniz.py; dikey kaynakta video tam ekran). Kullanıcı 'arkadaki sesi değiş' derse orijinal ses yerine Kevin MacLeod parçası (rotasyon; açıklamaya CC BY kredisi).

- TRİBÜN ÇEKİMİNİ BEN BULURUM (kullanıcı 26.11 'senin araman lazım'): X'e giriş yok (şifre/çerez/ücretli API YOK, nitter vb. bot korumasını aşma YOK). Akış: WebSearch (allowed_domains x.com, twitter.com; sorgular '<oyuncu> gol tribün', '<oyuncu> from the stands', '<takım> desde la grada', '<oyuncu> fan view') -> bulunan tweet linkleri `python3 _engine/tools/x_find.py <outdir> <linkler>` (syndication ile indirir, her video için 6 karelik şerit) -> şeritlere bak, tribün çekimini seç (telefon, önde taraftar kafaları, titreme, yayın skor grafiği yok) -> düz klip (pm1/deniz.py / tk1/plain.py). Ek kaynak: Dailymotion API (_engine/tools/dm_find.py). Eski tweet videoları telif nedeniyle 403 olabiliyor -> hızlı indir. Yayın görüntüsünü tribün gibi göstermek YASAK (Content ID atlatma).

- TRİBÜN AVCISI (yerel oturum, kullanıcının bilgisayarı, 26.11): Windows'ta C:\Filmler klasöründe açılan yerel Claude Code oturumunun TEK görevi: Claude in Chrome ile kullanıcının giriş yapılmış X'inde gol sonrası 'Son'/'Latest' + video filtresiyle tribün çekimi aramak (sorgular: '<oyuncu> goal', '<takım> fans', 'tribün', 'from the stands', stadyum adı; birkaç dil). Tribün = telefonla, önde taraftar kafaları, yayın skor grafiği YOK. Bulunca _live/stands.txt'e satır ekle: `<UTC saat> | <oyuncu> <dk>' | <maç> | <tweet linki>` ve git add/commit/push (workspace dalı). Video işleme YAPMA (bulut oturumu yapar). Gol listesi: ESPN (uefa.europa, uefa.europa.conf, eng.1 vb.). X'te paylaşım/beğeni/yorum YAPMA, sadece oku.

- KANAL İMZASI (kullanıcı 25.11: 'videonun bir yerine imzamızı koy', 'çok büyük olmasın', 'tam ortada olmasın, ideal yerde, güzel dursun'): HER videoda baştan sona başlık plakasının SAĞ ALT köşesinden sarkan küçük sekme: koyu zemin, üst kenarı sarı çizgiyle birleşik, minik kırmızı play ikonu + '@somewhrightnow' (Outfit 26px @1440). Oyun alanına girmez. Kod: hd1/film.py 'channel signature'. Başlık plakası olmayan şablonlarda üst bandın sağ altına aynı sekme.

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

- TR DUBLAJ TESLİMİ (kullanıcı 25.11): uzun videolarda Türkçe dublaj AYRI .m4a ses dosyası olarak iletilir (video süresiyle birebir, efekt+müzik dahil, -14 LUFS) -> YouTube'da ek ses parçası olarak yüklenir. Ayrı TR video dosyası gerekmez.
- SES (kullanıcı 25.11 'ses çok yapay zeka belli oluyor'): anlatım için Kokoro YERİNE Chatterbox (Resemble AI, MIT, /home/user/.ttsvenv, logs/gen_takes_cb.py; TR: mtl_tts language_id='tr', logs/tr_dub_cb.py). Whisper ile satır kontrolü; isimleri fonetik yaz (Jürgen -> Yurgen).
- UZUN VİDEO SENARYO (25.11): PRESSWIND 'Why Football Legends Still Can't Explain X' (1M+) yapısı: açılışta efsanelerin zıt yorumları -> 'Which one is it?' -> kronolojik hikâye, kısa konuşma cümleleri, kancalar ('Remember that.', 'But here's the thing.') -> kapanışta açılış sorusuna dönüş.

- ANLIK GOLLER BİRİNCİ ÖNCELİK (kullanıcı 26.11 'anlık goller ilk sırada olmalı, en çok onlar izleniyor'; UEFA ihtarı sonrası): yayın görüntüsü YOK (ihtar 24.02.2027'de düşene kadar kesin). Sıra: (1) tribün çekimi -> düz klip (cmb1/plain.py, Deniz Gül şablonu) 5-10 dk; (2) resmi kulüp klibi; GOAL kartı YAPMA (kullanıcı 26.11 'gol kartı boş'): görüntü yoksa video yok. Verim: X 'Tribün' listesi (tribün videosu atan taraftar/ultras/groundhopper hesapları, her bulunan hesap eklenir) + TRİBÜN AVCISI. Hız kritik: golden sonra ilk 30-60 dk. Tribün araması: TRİBÜN AVCISI (yerel) + WebSearch/x_find.py. Kalan zamanda görüntüsüz içerik (haber/istatistik/maç önü/quiz/on this day) + haftada 1 belgesel.

- CANLI SİSTEM (kullanıcı 27.11): maç akşamı oturum açılınca HEMEN `_live/tribun_alarm.py`'yi Monitor ile başlat (30 dk'da bir yeniden kur), her olayda PushNotification (tür + oyuncu/dk + skor + TikTok/X linkleri). Kullanıcı tribün linki atınca `_live/hizli.py <link> <ad> "İSİM · DK'" "SKOR" --push` (VAR/kırmızı vb. olaylarda üst satır olay). Yayın görüntüsünü tribün gibi gösterme YOK.
