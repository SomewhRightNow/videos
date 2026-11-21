
# ---------------------------------------------------------------- timeline (backgrounds)
S = {i: L(i) - 0.05 for i in range(1, len(ROWS) + 1)}
CH = {9: ('01', 'THE BOY', 'ÇOCUK'), 12: ('02', 'THE HEIR', 'VELİAHT'), 20: ('03', 'THE PRICE', 'BEDEL'),
      29: ('04', 'THE FALL', 'DÜŞÜŞ'), 34: ('05', 'TODAY', 'BUGÜN')}
TITLE_T = E(8) + 0.25
cold = dict(sat=0.9, warm=-0.3); warm = dict(sat=1.0, warm=0.3); bwg = dict(sat=0.0, warm=0.4); nat = dict(sat=1.0, warm=0.0)
seg(0, lambda t: (gev('dive_metlife', t, 0.0), nat))
seg(S[2], lambda t: (cover('met_in', t, S[2], S[3], 1.0, 1.12, 0.5, 0.5), dict(sat=0.9, warm=-0.1)), 'flash')
seg(S[3], lambda t: (side('ney26a', t, S[3], S[4], 'right', 0.5, 0.22), warm), 'whip', 0.25)
seg(S[4], lambda t: (cover('ney26b', t, S[4], S[5], 1.0, 1.15, 0.5, 0.3), dict(sat=0.5, warm=-0.2)), 'fade', 0.4)
seg(S[5], lambda t: (side('ney26c', t, S[5], S[6], 'right', 0.5, 0.2, bw=True), bwg), 'fade', 0.5)
seg(S[6], lambda t: (cover('met_out', t, S[6], S[7], 1.0, 1.12, 0.5, 0.5), dict(sat=0.8, warm=0.3)), 'fade', 0.4)
seg(S[7], lambda t: (split2('santos11a', 'ney26a', t, S[7], S[8] + 1.0, (0.5, 0.35), (0.5, 0.22), bw=True), bwg), 'flash')
seg(TITLE_T, lambda t: (dark(t), {}), 'fade', 0.4)
# ch1 the boy
seg(S[9], lambda t: (gev('santos', t, S[9]), warm), 'fade', 0.4)
seg(S[10], lambda t: (cover('santos11a', t, S[10], S[11], 1.0, 1.15, 0.5, 0.35), warm), 'whip', 0.25)
seg(S[11], lambda t: (cover('santos11b', t, S[11], S[12], 1.05, 1.18, 0.5, 0.35), warm), 'flash')
# ch2 the heir
seg(S[12], lambda t: (gev('fly_bcn', t, S[12]), nat), 'fade', 0.4)
seg(S[13], lambda t: (cover('barca_team', t, S[13], S[14], 1.0, 1.12, 0.5, 0.4), warm), 'whip', 0.25)
seg(S[14], lambda t: (cover('barca_cl15', t, S[14], S[15], 1.0, 1.15, 0.5, 0.45), warm), 'flash')
seg(S[15], lambda t: (cover('campnou', t, S[15], S[16], 1.0, 1.2, 0.5, 0.5), dict(sat=0.7, warm=-0.4)), 'fade', 0.5)
seg(S[16], lambda t: (cover('remo1', t, S[16], S[17], 1.0, 1.12, 0.5, 0.45), dict(sat=0.6, warm=-0.3)), 'whip', 0.25)
seg(S[17], lambda t: (cover('remo2', t, S[17], S[18], 1.05, 1.25, 0.5, 0.45), dict(sat=0.9, warm=0.0)), 'flash')
seg(S[18], lambda t: (cover('remo3', t, S[18], S[19], 1.0, 1.12, 0.5, 0.45), dict(sat=1.1, warm=0.3)), 'flash')
seg(S[19], lambda t: (side('barca_ney', t, S[19], S[20], 'right', 0.5, 0.2), warm), 'fade', 0.4)
# ch3 the price
seg(S[20], lambda t: (cover('barca_team', t, S[20], S[21], 1.2, 1.35, 0.5, 0.35, bw=True), bwg), 'fade', 0.4)
seg(S[21], lambda t: (gev('fly_paris', t, S[21]), cold), 'whip', 0.25)
seg(Wt(21, 'Two') - 0.15, lambda t: (dark(t, (20, 26, 48)), {}), 'flash')
seg(S[22], lambda t: (side('psg_pres', t, S[22], S[23], 'right', 0.5, 0.2), dict(sat=1.0, warm=0.1)), 'flash')
seg(S[23], lambda t: (cover('psg_press', t, S[23], S[24], 1.0, 1.12, 0.5, 0.35), dict(sat=1.0, warm=0.1)), 'whip', 0.25)
seg(S[24], lambda t: (dark(t), {}), 'fade', 0.3)
seg(S[25], lambda t: (side('psg13', t, S[25], S[26], 'right', 0.5, 0.25, bw=True), bwg), 'flash')
seg(S[26], lambda t: (side('psg_mnm', t, S[26], S[27], 'left', 0.5, 0.25, bw=True), bwg), 'whip', 0.25)
seg(S[27], lambda t: (cover('parc', t, S[27], S[28], 1.0, 1.12, 0.5, 0.5), dict(sat=0.8, warm=-0.2)), 'fade', 0.4)
seg(S[28], lambda t: (cover('parc', t, S[28], S[29], 1.12, 1.3, 0.5, 0.45, bw=True), bwg), 'fade', 0.5)
# ch4 the fall
seg(S[29], lambda t: (gev('fly_riyadh', t, S[29]), dict(sat=1.0, warm=0.3)), 'fade', 0.4)
seg(S[30], lambda t: (side('hilal1', t, S[30], S[31], 'right', 0.5, 0.25), dict(sat=0.8, warm=0.0)), 'flash')
seg(S[31], lambda t: (side('hilal2', t, S[31], S[32], 'left', 0.5, 0.25, bw=True), bwg), 'whip', 0.25)
seg(S[32], lambda t: (gev('fly_home', t, S[32]), warm), 'fade', 0.4)
seg(S[33], lambda t: (side('ney26b', t, S[33], S[34], 'right', 0.5, 0.25), dict(sat=0.8, warm=0.1)), 'flash')
# ch5 today
seg(S[34], lambda t: (side('santos26', t, S[34], S[35], 'right', 0.5, 0.22), warm), 'fade', 0.4)
seg(S[35], lambda t: (cover('santos25', t, S[35], S[36], 1.0, 1.12, 0.5, 0.3), dict(sat=0.9, warm=0.1)), 'whip', 0.25)
seg(S[36], lambda t: (side('santos26b', t, S[36], S[37], 'left', 0.5, 0.25, bw=True), bwg), 'flash')
seg(S[37], lambda t: (cover('vila', t, S[37], S[38], 1.0, 1.12, 0.5, 0.5), dict(sat=0.9, warm=0.2)), 'fade', 0.4)
seg(S[38], lambda t: (side('wc14', t, S[38], S[39], 'right', 0.5, 0.3), warm), 'flash')
seg(S[39], lambda t: (cover('oly16', t, S[39], S[40], 1.0, 1.12, 0.5, 0.4), warm), 'whip', 0.25)
seg(S[40], lambda t: (split2('santos11a', 'ney26c', t, S[40], TOTAL, (0.5, 0.35), (0.5, 0.2), bw=True), bwg), 'fade', 0.5)
for i in CH: seg(S[i] - 0.4, lambda t: (dark(t), {}), 'fade', 0.4)
SEG.sort(key=lambda s: s[0])
G.HITS += [(S[3], 10), (TITLE_T, 14), (Wt(17, 'ninety-fifth') - 0.05, 14), (S[18], 16), (Wt(21, 'Two') - 0.05, 16), (S[24], 12),
           (Wt(30, 'torn') - 0.05, 14), (Wt(36, 'sent') - 0.05, 12)]
G.FLASHES += [(TITLE_T, 0.06, 0.4), (S[18], 0.06, 0.5), (Wt(21, 'Two') - 0.05, 0.05, 0.4)]
