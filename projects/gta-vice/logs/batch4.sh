#!/bin/bash
cd /home/user/Filmler/gta-vice
run(){ logs/make.sh scene/$2.png "$3" gen/v_$1.png; echo "$1 done"; }
run messi s_messi_104 assets/orig/p_messi.jpg,research/cand/mes1.jpg,research/cand/mes2.jpg,research/cand/mes3.jpg
run ronaldo s_ronaldo_105 assets/orig/p_ronaldo.jpg,research/cand/ron1.jpg,research/cand/ron2.jpg
run haaland t_haaland_301 assets/orig/p_haaland.jpg,research/cand/haa1.jpg,research/cand/haa2.jpg,research/cand/haa3.jpg
run kane t_kane_304 assets/orig/p_kane.jpg,research/cand/kan1.jpg,research/cand/kan2.jpg,research/cand/kan3.jpg
run mbappe t_mbappe_308 assets/orig/p_mbappe.jpg,research/cand/mba1.jpg,research/cand/mba2.jpg,research/cand/mba3.jpg
run vini t_vini_304 assets/orig/p_vini.jpg,research/cand/vin1.jpg,research/cand/vin2.jpg,research/cand/vin3.jpg
run yamal s_yamal_108 assets/orig/p_yamal.jpg,research/cand/yam1.jpg,research/cand/yam2.jpg,research/cand/yam3.jpg
run arda s_arda_108 assets/orig/p_arda.jpg,../arda-safe/assets/orig/arda.jpg,../guess-player-d4/assets/orig/arda_fb.jpg,../guess-player-d4/assets/orig/arda_tr.jpg
echo ALLDONE
