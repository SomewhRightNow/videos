
def flag2(code, w, h):
    f = Image.new('RGBA', (w, h), (255, 255, 255, 255)); d = ImageDraw.Draw(f)
    if code == 'BRA':
        d.rectangle([0, 0, w, h], fill=BRA_G); d.polygon([(w * 0.08, h / 2), (w / 2, h * 0.1), (w * 0.92, h / 2), (w / 2, h * 0.9)], fill=BRA_Y)
        r = h * 0.24; d.ellipse([w / 2 - r, h / 2 - r, w / 2 + r, h / 2 + r], fill=(0, 39, 118))
    elif code == 'NOR':
        d.rectangle([0, 0, w, h], fill=(186, 12, 47)); d.rectangle([w * 0.27, 0, w * 0.27 + h * 0.25, h], fill=WH); d.rectangle([0, h * 0.375, w, h * 0.625], fill=WH)
        d.rectangle([w * 0.27 + h * 0.06, 0, w * 0.27 + h * 0.19, h], fill=(0, 32, 91)); d.rectangle([0, h * 0.44, w, h * 0.56], fill=(0, 32, 91))
    else: return flag(code, w, h)
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], 8, fill=255); f.putalpha(m); return f
_flag_orig = flag
def flag(code, w, h):
    return flag2(code, w, h) if code in ('BRA', 'NOR') else _flag_orig(code, w, h)
def bars(c, t, t_in, items, x, y, t_out=1e9, maxv=13):
    """horizontal stat bars: (label, value, colour)"""
    if not (t_in <= t < t_out): return
    a = 1 - prog(t, t_out - 0.3, t_out); d = ImageDraw.Draw(c)
    for k, (lab, v, col) in enumerate(items):
        p = ease_out(prog(t, t_in + k * 0.5, t_in + k * 0.5 + 0.9)); yy = y + k * 130
        txt(c, lab, F_H, 40, WH, x, yy, anchor='lm', alpha=a * p, stroke=3)
        d.rounded_rectangle([x, yy + 32, x + 760 * v / maxv * p, yy + 82], 10, fill=col + (int(240 * a),))
        txt(c, str(int(round(v * p))), F_MEGA, 54, WH, x + 760 * v / maxv * p + 24, yy + 58, anchor='lm', alpha=a * p, stroke=3)
def red_card(c, t, t_in, x, y, rot=-10, col=RED2, t_out=1e9):
    if not (t_in <= t < t_out): return
    p = ease_out(prog(t, t_in, t_in + 0.2)); card = Image.new('RGBA', (150, 210), (0, 0, 0, 0))
    ImageDraw.Draw(card).rounded_rectangle([0, 0, 149, 209], 14, fill=col + (255,))
    if t_out < 1e8: card = G._alpha(card, 1 - prog(t, t_out - 0.25, t_out))
    place(c, shadowed(card, 14), x, y, 2 - p, p, rot)
def overlays(c, t):
    # ---- cold open
    lower_third(c, t, 1.2, S[2], 'METLIFE STADIUM · NEW JERSEY', '05.07.2026 · WORLD CUP · ROUND OF 16', BRA_Y)
    if S[2] <= t < S[4]:
        sb = 0 if t < Wt(2, 'Haaland') - 0.1 else 1 if t < Wt(2, 'twice') - 0.1 else 2
        sa = 1 if t >= Wt(3, 'penalty') - 0.1 else 0
        scorebox(c, t, S[2] + 0.2, 'BRA', 'NOR', sa, sb, W * 0.27 if t >= S[3] else W / 2, 300, 'FT' if t >= S[4] - 0.4 else "HAALAND 79' · 90'" if sb == 2 else 'ROUND OF 16', t_out=S[4])
    if S[3] <= t < S[4]:
        stamp(c, t, Wt(3, 'penalty') - 0.1, "90+10' NEYMAR (PEN)", W * 0.27, 560, 56, BRA_G, -4, t_out=S[4])
        wipe(c, t, Wt(3, 'changes') - 0.1, 'IT CHANGES NOTHING', W * 0.27, 700, 56, WH, F_HI, bar=(0, 0, 0, 170), t_out=S[4])
    if S[4] <= t < S[5]: wipe(c, t, Wt(4, 'tears') - 0.2, 'BRAZIL ARE OUT', W / 2, 820, 80, WH, F_HI, bar=RED2 + (220,), t_out=S[5])
    if S[5] <= t < S[6]:
        a0 = S[5] + 0.1; a = fade_in(t, a0, 0.5) * (1 - prog(t, S[6] - 0.35, S[6]))
        shade(c, 'left', 0.9 * a); x = W * 0.31
        txt(c, '“', F_H, 200, GOLD2, x - 400, 300, alpha=a)
        txt(c, 'I tried, I tried.', F_TI, 58, WH, x, 380, alpha=a); txt(c, 'Now, it’s over.', F_TI, 58, WH, x, 456, alpha=fade_in(t, Wt(5, 'Now') - 0.1, 0.3) * a)
        txt(c, 'I started here.', F_TI, 58, GOLD2, x, 560, alpha=fade_in(t, Wt(5, 'started') - 0.1, 0.3) * a)
        txt(c, 'I finished here.', F_TI, 58, GOLD2, x, 636, alpha=fade_in(t, Wt(5, 'finished') - 0.1, 0.3) * a)
        txt(c, 'NEYMAR · TO GLOBO · 05.07.2026', F_MONO, 26, GRY, x, 740, alpha=a)
    if S[6] <= t < S[7]:
        wipe(c, t, Wt(6, 'Sixteen') - 0.1, 'AUG 2010', W / 2, 380, 150, WH, F_MEGA, t_out=S[7])
        wipe(c, t, Wt(6, 'first') - 0.1, 'FIRST GOAL FOR BRAZIL · SAME STADIUM', W / 2, 560, 50, (10, 10, 14), F_H, bar=BRA_Y + (255,), t_out=S[7])
    if S[7] <= t < TITLE_T:
        wipe(c, t, S[7] + 0.2, '2011', W * 0.25, 900, 90, WH, F_MEGA, t_out=TITLE_T)
        wipe(c, t, S[7] + 0.4, '2026', W * 0.75, 900, 90, WH, F_MEGA, t_out=TITLE_T)
        wipe(c, t, Wt(7, 'next') - 0.1, '"THE NEXT PELÉ"', W / 2, 160, 70, BRA_Y, F_HI, bar=(0, 0, 0, 190), t_out=TITLE_T)
    if TITLE_T <= t < S[9] - 0.4:
        a = fade_in(t, TITLE_T, 0.3) * (1 - prog(t, S[9] - 0.8, S[9] - 0.4)); p = ease_out(prog(t, TITLE_T, TITLE_T + 1.5))
        place(c, G._alpha(text_img('WHAT HAPPENED', F_MEGA, 110, WH), a), W / 2, 400, 1.12 - 0.12 * p, 1.0)
        place(c, G._alpha(text_img('TO NEYMAR?', F_MEGA, 150, BRA_Y), a), W / 2, 580, 1.12 - 0.12 * p, 1.0)
        txt(c, 'SANTOS · BARCELONA · PARIS · RIYADH · SANTOS', F_MONO, 24, GRY, W / 2, 760, alpha=a)
    chapter(c, t)
    # ---- ch1 the boy
    lower_third(c, t, S[9] + 0.3, S[10], 'VILA BELMIRO · SANTOS, BRAZIL', "PELÉ'S CLUB", WH)
    if S[9] <= t < S[10]: wipe(c, t, Wt(9, 'seventeen') - 0.1, '2009 · DEBUT AT 17', 1450, 480, 70, WH, F_HI, bar=(0, 0, 0, 170), t_out=S[10])
    if S[10] <= t < S[11]:
        wipe(c, t, Wt(10, 'nineteen') - 0.1, 'AGE 19', 1450, 380, 110, BRA_Y, F_MEGA, t_out=S[11])
        wipe(c, t, Wt(10, 'Copa') - 0.1, 'COPA LIBERTADORES 2011', 1450, 540, 64, WH, F_HI, bar=(0, 0, 0, 180), t_out=S[11])
        wipe(c, t, Wt(10, 'Copa') + 0.3, 'CHAMPIONS', 1450, 650, 54, (10, 10, 14), F_H, bar=(255, 255, 255, 255), t_out=S[11])
    if S[11] <= t < S[12]: wipe(c, t, Wt(11, 'biggest') - 0.1, 'EUROPE IS WATCHING', W / 2, 860, 80, WH, F_HI, bar=(0, 0, 0, 170), t_out=S[12] - 0.4)
    # ---- ch2 the heir
    if S[12] <= t < S[13]:
        wipe(c, t, Wt(12, 'twenty') - 0.1, '2013', W / 2, 360, 150, WH, F_MEGA, t_out=S[13])
        wipe(c, t, Wt(12, 'Barcelona') - 0.1, 'SANTOS → BARCELONA', W / 2, 530, 64, WH, F_HI, bar=BAR_R + (230,), t_out=S[13])
        wipe(c, t, Wt(12, 'Messi') - 0.1, 'NEXT TO LIONEL MESSI', W / 2, 640, 44, GOLD2, F_MONO, t_out=S[13])
    if S[13] <= t < S[14]:
        for k, (lt, nm) in enumerate([('M', 'MESSI'), ('S', 'SUÁREZ'), ('N', 'NEYMAR')]):
            tk = Wt(13, 'MSN') - 0.2 + k * 0.18
            if t >= tk:
                p = ease_out(prog(t, tk, tk + 0.3)); place(c, shadowed(text_img(lt, F_MEGA, 200, BRA_Y if lt == 'N' else WH), 16), W * (0.32 + 0.18 * k), 340, 1.4 - 0.4 * p, p)
                txt(c, nm, F_MONO, 28, GRY, W * (0.32 + 0.18 * k), 490, alpha=p)
        counter_txt(c, t, Wt(13, 'one', 1) - 0.1, 122, W / 2, 700, 170, GOLD2, dur=1.4, t_out=S[14])
        wipe(c, t, Wt(13, 'goals') - 0.1, 'GOALS IN ONE SEASON · 2014–15', W / 2, 840, 40, WH, F_MONO, t_out=S[14])
    if S[14] <= t < S[15]:
        lower_third(c, t, S[14] + 0.3, S[15], 'BERLIN · CHAMPIONS LEAGUE FINAL', '06.06.2015 · BARCELONA 3–1 JUVENTUS', BAR_R)
        stamp(c, t, Wt(14, 'scored') - 0.1, 'NEYMAR SCORES', 1450, 420, 70, BAR_R, -5, t_out=S[15])
        wipe(c, t, Wt(14, 'treble') - 0.1, 'THE TREBLE', 1450, 580, 100, GOLD2, F_MEGA, t_out=S[15])
    if S[15] <= t < S[16]: wipe(c, t, Wt(15, 'night') - 0.1, 'THE NIGHT', W / 2, 520, 160, WH, F_MEGA, t_out=S[16])
    if S[16] <= t < S[17]:
        lower_third(c, t, S[16] + 0.2, S[17], 'CAMP NOU · CHAMPIONS LEAGUE ROUND OF 16', '08.03.2017 · BARCELONA vs PSG', BAR_R)
        wipe(c, t, Wt(16, 'four-nil') - 0.1, 'FIRST LEG: PSG 4–0 BARÇA', W / 2, 380, 72, WH, F_HI, bar=PSG_B + (230,), t_out=S[17])
        wipe(c, t, Wt(16, 'miracle') - 0.1, 'NEEDED: A MIRACLE', W / 2, 520, 72, GOLD2, F_HI, bar=(0, 0, 0, 180), t_out=S[17])
    if S[17] <= t < S[18]:
        wipe(c, t, S[17] + 0.1, "88'", 330, 300, 150, WH, F_MEGA, t_out=S[18])
        wipe(c, t, Wt(17, 'three') - 0.1, 'NEEDED: 3 GOALS', 330, 450, 50, WH, F_HI, bar=RED2 + (230,), t_out=S[18])
        for k, (lab, wd) in enumerate([('⚽ NEYMAR', 'two'), ('⚽ NEYMAR', 'two'), ("95' ASSIST: NEYMAR", 'ninety-fifth')]):
            tk = Wt(17, wd) - 0.1 + (0.35 if k == 1 else 0)
            if t >= tk: wipe(c, t, tk, lab.replace('⚽ ', 'GOAL · '), 1500, 300 + k * 110, 52, WH, F_HI, bar=BAR_R + (230,), t_out=S[18])
    if S[18] <= t < S[19]:
        p = ease_out(prog(t, S[18], S[18] + 0.35)); place(c, shadowed(text_img('6–1', F_MEGA, 260, WH), 20), W / 2, 380, 1.4 - 0.4 * p, p)
        wipe(c, t, Wt(18, 'Remontada') - 0.1, 'LA REMONTADA', W / 2, 600, 100, GOLD2, F_HI, bar=(0, 0, 0, 180), t_out=S[19])
    if S[19] <= t < S[20] - 0.4:
        shade(c, 'left', 0.7)
        txt(c, "BALLON D'OR", F_MONO, 32, GRY, 520, 300, alpha=fade_in(t, S[19], 0.3))
        counter_txt(c, t, Wt(19, 'third') - 0.1, 3, 460, 470, 240, GOLD2, dur=0.5, t_out=S[20] - 0.4)
        wipe(c, t, Wt(19, 'third') + 0.2, 'RD · 2015', 640, 470, 60, WH, F_HI, t_out=S[20] - 0.4)
        wipe(c, t, Wt(19, 'next') - 0.1, 'NEXT: HIM?', 520, 680, 80, WH, F_HI, bar=(0, 0, 0, 170), t_out=S[20] - 0.4)
    # ---- ch3 the price
    if S[20] <= t < S[21]:
        wipe(c, t, Wt(20, 'second') - 0.1, 'No. 2', W / 2, 480, 220, WH, F_MEGA, t_out=S[21])
        wipe(c, t, Wt(20, 'Messi') - 0.1, 'BEHIND MESSI', W / 2, 680, 60, GOLD2, F_HI, bar=(0, 0, 0, 170), t_out=S[21])
    if S[21] <= t < S[22]:
        wipe(c, t, S[21] + 0.2, 'AUG 2017 · BARCELONA → PARIS', W / 2, 200, 50, WH, F_HI, bar=PSG_B + (230,), t_out=S[22])
        if t >= Wt(21, 'Two') - 0.1:
            counter_txt(c, t, Wt(21, 'Two') - 0.1, 222, W / 2 - 60, 520, 260, WH, dur=1.6, fmt='€{:d}', t_out=S[22])
            wipe(c, t, Wt(21, 'million') - 0.1, 'MILLION', W / 2, 720, 80, GOLD2, F_HI, t_out=S[22])
    if S[22] <= t < S[23]: stamp(c, t, Wt(22, 'most') - 0.1, 'WORLD RECORD', 560, 520, 100, (200, 150, 20), -6, t_out=S[23])
    if S[23] <= t < S[24]:
        wipe(c, t, Wt(23, 'main') - 0.1, 'THE MAIN MAN', W / 2, 760, 80, WH, F_HI, bar=PSG_B + (230,), t_out=S[24])
        wipe(c, t, Wt(23, 'Champions') - 0.1, 'THE PLAN: WIN THE CHAMPIONS LEAGUE', W / 2, 880, 44, GOLD2, F_MONO, t_out=S[24])
    if S[24] <= t < S[25]:
        p = ease_out(prog(t, S[24], S[24] + 0.4)); place(c, shadowed(text_img('IT NEVER HAPPENED.', F_MEGA, 110, WH), 16), W / 2, 520, 1.2 - 0.2 * p, p)
    if S[25] <= t < S[26]:
        shade(c, 'left', 0.75)
        wipe(c, t, S[25] + 0.1, 'FEB 2018', 520, 330, 110, WH, F_MEGA, t_out=S[26])
        stamp(c, t, Wt(25, 'broken') - 0.1, 'BROKEN FOOT', 520, 500, 80, RED2, -5, t_out=S[26])
        wipe(c, t, Wt(25, 'missed') - 0.1, 'MISSES REAL MADRID', 520, 650, 54, WH, F_HI, bar=(0, 0, 0, 180), t_out=S[26])
        wipe(c, t, Wt(25, 'PSG') - 0.1, 'PSG: OUT', 520, 760, 54, WH, F_HI, bar=RED2 + (230,), t_out=S[26])
    if S[26] <= t < S[27]:
        shade(c, 'right', 0.75)
        wipe(c, t, S[26] + 0.1, 'JAN 2019', 1400, 330, 110, WH, F_MEGA, t_out=S[27])
        stamp(c, t, Wt(26, 'same') - 0.1, 'SAME FOOT', 1400, 500, 80, RED2, 5, t_out=S[27])
        wipe(c, t, Wt(26, 'missed') - 0.1, 'MISSES MAN UNITED', 1400, 650, 54, WH, F_HI, bar=(0, 0, 0, 180), t_out=S[27])
        wipe(c, t, Wt(26, 'PSG') - 0.1, 'PSG: OUT AGAIN', 1400, 760, 54, WH, F_HI, bar=RED2 + (230,), t_out=S[27])
    if S[27] <= t < S[28]:
        lower_third(c, t, S[27] + 0.3, S[28], 'LISBON · CHAMPIONS LEAGUE FINAL', '23.08.2020', PSG_B)
        wipe(c, t, Wt(27, 'lost') - 0.1, 'PSG 0–1 BAYERN', W / 2, 460, 110, WH, F_MEGA, t_out=S[28])
    if S[28] <= t < S[29] - 0.4:
        wipe(c, t, Wt(28, 'won') - 0.1, '2025 · PSG WIN THE CHAMPIONS LEAGUE', W / 2, 420, 60, WH, F_HI, bar=PSG_B + (230,), t_out=S[29] - 0.4)
        wipe(c, t, Wt(28, 'gone') - 0.2, 'WITHOUT NEYMAR', W / 2, 580, 100, GOLD2, F_MEGA, t_out=S[29] - 0.4)
    # ---- ch4 the fall
    if S[29] <= t < S[30]:
        wipe(c, t, Wt(29, 'Saudi') - 0.1, 'PARIS → RIYADH · AL HILAL', W / 2, 200, 54, WH, F_HI, bar=HIL_B + (230,), t_out=S[30])
        if t >= Wt(29, 'ninety') - 0.15:
            counter_txt(c, t, Wt(29, 'ninety') - 0.15, 90, W / 2 - 40, 520, 240, WH, dur=1.0, fmt='€{:d}M', t_out=S[30])
    if S[30] <= t < S[31]:
        shade(c, 'left', 0.75)
        wipe(c, t, Wt(30, 'months') - 0.1, 'OCT 2023 · BRAZIL vs URUGUAY', 520, 360, 44, WH, F_MONO, t_out=S[31])
        stamp(c, t, Wt(30, 'torn') - 0.1, 'TORN ACL', 520, 520, 120, RED2, -6, t_out=S[31])
    if S[31] <= t < S[32]:
        shade(c, 'right', 0.75)
        counter_txt(c, t, Wt(31, 'seven') - 0.1, 7, 1400, 450, 300, GOLD2, dur=0.6, t_out=S[32])
        wipe(c, t, Wt(31, 'games') - 0.1, 'GAMES IN 18 MONTHS', 1400, 660, 60, WH, F_HI, bar=(0, 0, 0, 180), t_out=S[32])
    if S[32] <= t < S[33]:
        wipe(c, t, Wt(32, 'home') - 0.1, 'RIYADH → SANTOS', W / 2, 200, 54, WH, F_HI, bar=(0, 0, 0, 200), t_out=S[33])
        wipe(c, t, Wt(32, 'last') - 0.1, 'ONE LAST WORLD CUP', W / 2, 880, 80, BRA_Y, F_HI, bar=(0, 0, 0, 180), t_out=S[33])
    if S[33] <= t < S[34] - 0.4:
        shade(c, 'left', 0.75)
        stamp(c, t, Wt(33, 'calf') - 0.1, 'CALF INJURY', 520, 360, 80, RED2, -5, t_out=S[34] - 0.4)
        if t >= Wt(33, 'two') - 0.15:
            counter_txt(c, t, Wt(33, 'two') - 0.15, 2, 420, 600, 240, BRA_Y, dur=0.4, t_out=S[34] - 0.4)
            wipe(c, t, Wt(33, 'five') - 0.1, '/ 5 GAMES', 640, 600, 80, WH, F_HI, t_out=S[34] - 0.4)
    # ---- ch5 today
    if S[34] <= t < S[35]:
        shade(c, 'left', 0.7); counter_txt(c, t, Wt(34, 'thirty-four') - 0.15, 34, 520, 480, 300, WH, dur=0.7, t_out=S[35])
        wipe(c, t, Wt(34, 'thirty-four') + 0.3, 'YEARS OLD', 520, 680, 60, GOLD2, F_HI, t_out=S[35])
    if S[35] <= t < S[36]:
        if 'blk' not in _SH: _SH['blk'] = Image.new('RGBA', (W, H), (0, 0, 0, 255))
        c.alpha_composite(G._alpha(_SH['blk'], 0.5 * fade_in(t, S[35], 0.4)))
        txt(c, 'SANTOS · 2026 SEASON', F_MONO, 30, GRY, 560, 300, alpha=fade_in(t, S[35], 0.3))
        bars(c, t, Wt(35, 'cards') - 0.2, [('CARDS (12 YELLOW · 1 RED)', 13, (230, 190, 0)), ('GOALS', 10, BRA_G)], 560, 400, t_out=S[36])
    if S[36] <= t < S[37]:
        shade(c, 'right', 0.75)
        red_card(c, t, Wt(36, 'sent') - 0.1, 1400, 420, -10, t_out=S[37])
        wipe(c, t, Wt(36, 'Bahia') - 0.1, 'SANTOS vs BAHIA · 24.10.2026', 1400, 640, 44, WH, F_MONO, t_out=S[37])
        wipe(c, t, Wt(36, 'covering') - 0.1, '"VINÍCIUS JR. RULE"', 1400, 740, 60, GOLD2, F_HI, bar=(0, 0, 0, 180), t_out=S[37])
    if S[37] <= t < S[38]:
        lower_third(c, t, S[37] + 0.2, S[38], 'NEYMAR DA SILVA SANTOS SR.', 'SANTOS CEO · SINCE 06.11.2026', WH)
        wipe(c, t, Wt(37, 'contract') - 0.1, 'CONTRACT ENDS', W / 2, 420, 70, WH, F_HI, bar=(0, 0, 0, 180), t_out=S[38])
        wipe(c, t, Wt(37, 'thirty-first') - 0.1, '31.12.2026', W / 2, 560, 130, GOLD2, F_MEGA, t_out=S[38])
    if S[38] <= t < S[39]:
        shade(c, 'left', 0.75)
        wipe(c, t, Wt(38, 'all-time') - 0.1, "BRAZIL'S ALL-TIME TOP SCORER", 520, 300, 44, WH, F_HI, bar=BRA_G + (230,), t_out=S[39])
        counter_txt(c, t, Wt(38, 'Eighty') - 0.15, 80, 520, 500, 260, BRA_Y, dur=1.2, t_out=S[39])
        wipe(c, t, Wt(38, 'Pelé') - 0.1, 'PELÉ: 77', 520, 700, 70, WH, F_HI, t_out=S[39])
    if S[39] <= t < S[40]:
        for k, (yr, name, wd) in enumerate([('2015', 'CHAMPIONS LEAGUE', 'Champions'), ('2011', 'COPA LIBERTADORES', 'Copa'), ('2016', 'OLYMPIC GOLD', 'Olympic')]):
            wipe(c, t, Wt(39, wd) - 0.1, f'{yr}  ·  {name}', W / 2, 330 + k * 140, 70, GOLD2 if k == 2 else WH, F_HI, bar=(0, 0, 0, 170), t_out=S[40])
    if t >= S[40]:
        tq = Wt(40, 'happened') - 0.2
        if t < Wt(40, 'injuries') - 0.15:
            p = ease_out(prog(t, tq, tq + 0.4)); place(c, shadowed(text_img('WHAT HAPPENED?', F_MEGA, 120, WH), 18), W / 2, 300, 1.2 - 0.2 * p, p)
        else:
            if 'blk' not in _SH: _SH['blk'] = Image.new('RGBA', (W, H), (0, 0, 0, 255))
            c.alpha_composite(G._alpha(_SH['blk'], 0.55))
            for k, (lab, wd) in enumerate([('INJURIES?', 'injuries'), ('LEAVING MESSI?', 'Leaving'), ('TOO MUCH HYPE?', 'expect')]):
                wipe(c, t, Wt(40, wd) - 0.15, lab, W / 2, 230 + k * 130, 84, BRA_Y if k == 2 else WH, F_HI, bar=(0, 0, 0, 170))
            if t >= S[41]:
                wipe(c, t, Wt(41, 'one') - 0.2, 'ONE WORD IN THE COMMENTS', W / 2, 640, 50, (10, 10, 14), F_H, bar=(255, 255, 255, 255))
                ts_ = Wt(41, 'subscribe') - 0.1
                if t >= ts_:
                    p = ease_out(prog(t, ts_, ts_ + 0.25)); sb_ = text_img('SUBSCRIBE', F_H, 58, WH, bar=(220, 20, 30, 255), pad=(40, 12))
                    place(c, shadowed(sb_, 12), W / 2, 770, 1.3 - 0.3 * p, p)
                wipe(c, t, Wt(41, 'football') - 0.1, 'MORE FOOTBALL STORIES EVERY WEEK', W / 2, 860, 28, GRY, F_MONO)
            if t >= E(41) + 0.4: txt(c, 'SOMEWHERE RIGHT NOW', F_MONO, 26, GRY, W / 2, 70, alpha=fade_in(t, E(41) + 0.4, 0.5))
    gev_credit(c, t)
    photo_credit(c, t)
    if BURN_SUBS:
        if any(a <= t < b for a, b, *_ in SUBS): shade(c, 'bottom', 1.0)
        subtitles(c, t)
GEV_SEGS = [(0, S[2]), (S[9], S[10]), (S[12], S[13]), (S[21], Wt(21, 'Two') - 0.15), (S[29], S[30]), (S[32], S[33])]
def gev_credit(c, t):
    if any(a <= t < b for a, b in GEV_SEGS):
        txt(c, "GLOBE: GOD'S EYE VIEW · IMAGERY © ESRI, MAXAR, EARTHSTAR GEOGRAPHICS", F_MONO, 16, GRY, W - 40, H - 22, anchor='rm', alpha=0.9)
def photo_credit(c, t):
    if not any(a <= t < b for a, b in GEV_SEGS) and S[2] <= t < S[40]:
        txt(c, 'PHOTOS: WIKIMEDIA COMMONS (CC) · CREDITS IN DESCRIPTION', F_MONO, 14, GRY, W - 40, H - 20, anchor='rm', alpha=0.75)
BURN_SUBS = os.environ.get('BURN_SUBS') == '1'
G.OVERLAYS[0] = overlays

def write_srt():
    def ts(x): h = int(x // 3600); m = int(x % 3600 // 60); sec = x % 60; return f'{h:02d}:{m:02d}:{int(sec):02d},{int(sec % 1 * 1000):03d}'
    for lang, k in (('en', 2), ('tr', 3)):
        with open(f'What Happened to Neymar.{lang}.srt', 'w', encoding='utf-8') as f:
            for n, sub in enumerate(SUBS, 1): f.write(f'{n}\n{ts(sub[0])} --> {ts(sub[1])}\n{sub[k]}\n\n')

if __name__ == '__main__':
    if sys.argv[1] == 'srt': write_srt(); sys.exit()
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=19, maxrate='16M')
    else: G.main(sys.argv)
