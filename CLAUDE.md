# Somewhere Right Now — çalışma alanı girişi
Bu depoda: `main` = yüklenen videolar; `workspace` dalı = ortak beyin (kurallar, notlar, motor, araçlar, projeler).
Oturum açılınca SessionStart hook workspace dalını /home/user/Filmler içine klonlar/günceller; oturum sonunda Stop hook değişiklikleri geri gönderir. Farklı Claude hesaplarındaki çalışmalar tek yerde birleşir.

Asıl kurallar ve son durum:
@/home/user/Filmler/CLAUDE.md
@/home/user/Filmler/HANDOFF.md

Hook çalışmadıysa elle: git clone -b workspace --single-branch https://github.com/SomewhRightNow/videos /home/user/Filmler && bash /home/user/Filmler/setup.sh
