"""Who Delivers When It Matters?  RR SupeRR Selector Season 2, Round 1.
Run:  cd RR/app && streamlit run app.py
"""
from pathlib import Path
import numpy as np, pandas as pd
import plotly.graph_objects as go
import streamlit as st

HERE = Path(__file__).resolve().parent; DATA = HERE / 'data'
PINK, BLUE, TXT, MUTED, GRID, CARD = '#E8368F', '#5B8CFF', '#E8ECF8', '#97A1C0', 'rgba(150,165,210,.18)', '#161C2E'
SHORT = {'Chennai Super Kings': 'CSK', 'Mumbai Indians': 'MI', 'Royal Challengers Bengaluru': 'RCB', 'Royal Challengers Bangalore': 'RCB', 'Kolkata Knight Riders': 'KKR', 'Sunrisers Hyderabad': 'SRH',
         'Delhi Capitals': 'DC', 'Punjab Kings': 'PBKS', 'Rajasthan Royals': 'RR', 'Gujarat Titans': 'GT', 'Lucknow Super Giants': 'LSG'}
sh = lambda t: SHORT.get(t, t)
LAB = ['Low', 'Medium', 'High']
BAND_NAME = {'Low': 'Low<br>0.5 to 0.85', 'Medium': 'Medium<br>0.85 to 1.4', 'High': 'High (pressure)<br>1.4 and above'}
SCOPE_LABEL = {'Both': 'IPL + T20I', 'IPL': 'IPL only', 'T20I': 'T20I only'}
W_IMPACT, W_CLUTCH = 0.8, 0.2

st.set_page_config(page_title='Who Delivers When It Matters?', page_icon='🏏', layout='wide', initial_sidebar_state='collapsed')
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@500;600;700;800&display=swap');
[data-testid="stSidebar"], [data-testid="collapsedControl"], header[data-testid="stHeader"] {{ display: none; }}
.stApp {{ background: radial-gradient(900px 420px at 0% -8%, rgba(232,54,143,.13), transparent 60%), radial-gradient(900px 480px at 100% 0%, rgba(91,140,255,.12), transparent 55%), #0C111D; }}
.block-container {{ max-width: 1440px; padding: 1.4rem 3rem 3rem 3rem; }}
html, body, [class*="css"], .stMarkdown, button, input {{ font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif; }}
h1, h2, h3, h4, .title, .card .v, .pod .rk, .pod .nm, .pod .big {{ font-family: 'Poppins', 'Inter', sans-serif; }}
h1, h2, h3, h4 {{ color: {TXT}; letter-spacing: -.01em; }} h4 {{ margin-top: 1.6rem; font-weight: 600; }}
.brand {{ font-family:'Poppins',sans-serif; font-weight:600; letter-spacing:.1em; font-size:.8rem; color:{MUTED}; text-transform:uppercase; }} .brand b {{ color:{PINK}; }}
.title {{ font-size: 2.7rem; font-weight: 700; color:{TXT}; margin: 22px 0 6px 0; letter-spacing:-.02em; }} .sub {{ color:{MUTED}; font-size:1.08rem; margin-bottom: 22px; max-width: 880px; line-height:1.55; }}
.card {{ background: linear-gradient(160deg, #181F33, #121828); border:1px solid rgba(150,165,210,.16); border-radius: 14px; padding: 18px 22px; height: 100%; min-height: 128px; box-shadow: 0 8px 24px rgba(0,0,0,.25); }}
.card .l {{ font-size:.72rem; color:{MUTED}; text-transform:uppercase; letter-spacing:.09em; font-weight:600; }} .card .v {{ font-size: 2.1rem; font-weight: 700; color:{TXT}; line-height:1.2; margin: 2px 0; }}
.card .s {{ color:#AEB8D6; font-size:.88rem; line-height:1.45; }} .card.hi {{ border-top: 3px solid {PINK}; }}
.pod {{ background: linear-gradient(160deg, #181F33, #121828); border:1px solid rgba(150,165,210,.16); border-radius: 14px; padding: 18px 22px; border-top: 4px solid {PINK}; box-shadow: 0 8px 24px rgba(0,0,0,.25); }}
.pod .rk {{ font-size: 2.2rem; font-weight: 800; line-height: 1; }} .pod .nm {{ font-size: 1.3rem; font-weight: 600; color:{TXT}; margin-top: 6px; }} .pod .tm {{ color:{MUTED}; font-size:.88rem; }}
.pod .row {{ display:flex; gap: 26px; margin-top: 14px; }} .pod .row div {{ font-size:.7rem; color:{MUTED}; text-transform:uppercase; letter-spacing:.08em; font-weight:600; }} .pod .row b {{ display:block; font-family:'Poppins',sans-serif; font-size:1.3rem; color:{TXT}; text-transform:none; letter-spacing:0; margin-top:2px; }}
.pod.g1 {{ border-top-color:#F2C14E; }} .pod.g1 .rk {{ color:#F2C14E; }} .pod.g2 {{ border-top-color:#C9D2E8; }} .pod.g2 .rk {{ color:#C9D2E8; }} .pod.g3 {{ border-top-color:#D58A4B; }} .pod.g3 .rk {{ color:#D58A4B; }}
.note {{ background: rgba(232,54,143,.06); border: 1px solid rgba(232,54,143,.22); border-left: 4px solid {PINK}; padding: 12px 16px; color:#D3DAF2; border-radius: 10px; font-size:.95rem; line-height:1.55; }}
.tblwrap {{ overflow: auto; border-radius: 12px; }} .tblwrap::-webkit-scrollbar {{ width: 8px; }} .tblwrap::-webkit-scrollbar-thumb {{ background: rgba(150,165,210,.25); border-radius: 8px; }}
table.t {{ width:100%; border-collapse: separate; border-spacing: 0 5px; font-size: .92rem; }}
table.t th {{ border: 0 !important; position: sticky; top: 0; z-index: 2; background: #0C111D; color:{MUTED}; font-size:.68rem; font-weight:600; text-transform:uppercase; letter-spacing:.09em; text-align:left; padding: 6px 10px; }}
table.t td {{ background: rgba(255,255,255,.035); padding: 9px 10px; color:#DCE2F5; border: 0 !important; white-space: nowrap; }}
table.t td:first-child {{ border-radius: 10px 0 0 10px; }} table.t td:last-child {{ border-radius: 0 10px 10px 0; }}
table.t tr:hover td {{ background: rgba(232,54,143,.08); }}
table.t .num, table.t th.num {{ text-align:right; }} table.t td b {{ color:#fff; font-weight:600; }}
.rkb {{ display:inline-block; min-width: 26px; height: 26px; line-height: 26px; text-align:center; border-radius: 50%; background: rgba(150,165,210,.14); color:{TXT}; font-weight:600; font-size:.8rem; }}
.rkb.r1 {{ background:#F2C14E; color:#1b1500; }} .rkb.r2 {{ background:#C9D2E8; color:#10151f; }} .rkb.r3 {{ background:#D58A4B; color:#1d1004; }}
.pill {{ display:inline-block; padding: 2px 10px; border-radius: 999px; background: rgba(91,140,255,.16); color:#AFC4FF; font-size:.78rem; font-weight:600; letter-spacing:.03em; }}
.barwrap {{ display:inline-block; vertical-align:middle; width: 64px; height: 7px; border-radius: 6px; background: rgba(255,255,255,.08); margin-right: 8px; overflow:hidden; }} .barwrap i {{ display:block; height:100%; border-radius:6px; background: linear-gradient(90deg, {BLUE}, {PINK}); }}
.pos {{ color:#5FE0A3; font-weight:600; }} .neg {{ color:#FF7A8A; font-weight:600; }} .zero {{ color:{MUTED}; }}
.lab {{ display:inline-block; padding: 2px 10px; border-radius: 6px; font-size:.78rem; font-weight:600; }}
.lab.up {{ background: rgba(95,224,163,.14); color:#5FE0A3; }} .lab.mid {{ background: rgba(150,165,210,.14); color:#C3CBE6; }} .lab.down {{ background: rgba(255,122,138,.14); color:#FF7A8A; }}
tr.tot td {{ background: rgba(232,54,143,.09); }}
</style>""", unsafe_allow_html=True)


SEASONS = ['All', 2022, 2023, 2024, 2025, 2026]


@st.cache_data
def load():
    r = {}
    for k in ('bat', 'bowl'):
        for sc in SCOPE_LABEL:
            for yr in SEASONS:
                fp = DATA / f'ratings_{k}_{sc}_{yr}.parquet'
                if not fp.exists(): continue
                t = pd.read_parquet(fp).dropna(subset=['clutch']).copy()
                if len(t) < 15: continue
                zr = (t.rating_per100 - t.rating_per100.mean()) / t.rating_per100.std(); zc = (t.clutch - t.clutch.mean()) / t.clutch.std()      # combined score: 80% Pressure Impact + 20% clutch, each put on the same scale first
                combo = W_IMPACT * zr + W_CLUTCH * zc; t['combined'] = (50 + 15 * (combo - combo.mean()) / combo.std()).clip(0, 100); r[(k, sc, yr)] = t
    m = {k: pd.read_parquet(DATA / f'matches_{k}.parquet').assign(year=lambda x: pd.to_datetime(x.date).dt.year) for k in ('bat', 'bowl')}
    b = {k: pd.read_parquet(DATA / f'bands_{k}.parquet') for k in ('bat', 'bowl')}
    bs = {k: pd.read_parquet(DATA / f'bandstats_{k}.parquet') for k in ('bat', 'bowl')}
    return r, m, b, pd.read_parquet(DATA / 'leverage_by_over.parquet'), bs
R, M, BD, LBO, BS = load()
f1 = lambda x, d=1: '-' if pd.isna(x) else f'{x:+.{d}f}'
CLUTCH_SCALE = [('Excellent', 2.0), ('Great', 1.0), ('Above Average', 0.5), ('Average', 0.0), ('Below Average', -0.5), ('Poor', -1.0), ('Awful', -2.0)]
def clutch_rating(x):
    if pd.isna(x): return '-'
    return min(CLUTCH_SCALE, key=lambda t: abs(t[1] - x))[0]
def runs_word(k, cap=False):
    w = 'extra runs' if k == 'bat' else 'runs saved'
    return w.capitalize() if cap else w
team_of = lambda x: sh(x) if isinstance(x, str) else '-'


def plain(fig, h=380):
    fig.update_layout(height=h, margin=dict(l=6, r=10, t=46, b=6), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color=TXT, family='Inter, sans-serif', size=12), title_font=dict(size=15, family='Poppins, Inter, sans-serif'), showlegend=False,
                      hoverlabel=dict(bgcolor='#181F33', bordercolor='rgba(150,165,210,.3)', font=dict(color=TXT, family='Inter, sans-serif')))
    fig.update_xaxes(gridcolor='rgba(150,165,210,.09)', zerolinecolor='rgba(150,165,210,.45)', zerolinewidth=1.2, linecolor='rgba(150,165,210,.2)', tickfont=dict(color=MUTED), title_font=dict(color=MUTED, size=12))
    fig.update_yaxes(gridcolor='rgba(150,165,210,.09)', zerolinecolor='rgba(150,165,210,.45)', zerolinewidth=1.2, linecolor='rgba(150,165,210,.2)', tickfont=dict(color=MUTED), title_font=dict(color=MUTED, size=12))
    return fig


def lollipop(names, vals, title, fmt='{:+.1f}', h=460, hover='', cs=((0, '#5B8CFF'), (1, '#E8368F'))):
    """Horizontal lollipop chart: a thin stem, a coloured dot and the value written beside it."""
    names, vals = list(names), [float(v) for v in vals]; lo, hi = min(vals + [0]), max(vals + [0]); pad = (hi - lo) * 0.14 or 1
    sx, sy = [], []
    for n_, v_ in zip(names, vals): sx += [0, v_, None]; sy += [n_, n_, None]
    fig = go.Figure(go.Scatter(x=sx, y=sy, mode='lines', line=dict(color='rgba(150,165,210,.35)', width=3), hoverinfo='skip'))
    fig.add_trace(go.Scatter(x=vals, y=names, mode='markers+text', text=[fmt.format(v) for v in vals], textposition=['middle right' if v >= 0 else 'middle left' for v in vals], textfont=dict(color=TXT, size=12),
                             marker=dict(size=17, color=vals, colorscale=[list(c) for c in cs], line=dict(color='#0C111D', width=2)), hovertemplate='<b>%{y}</b><br>%{x:+.2f}' + hover + '<extra></extra>', cliponaxis=False))
    fig.update_layout(title=title, xaxis_range=[lo - pad * (1.4 if lo < 0 else 0), hi + pad], yaxis=dict(categoryorder='array', categoryarray=names[::-1], showgrid=False)); return plain(fig, h)


def html_table(df, kinds=None, fmts=None, height=None, last_total=False):
    """A styled HTML table. kinds: column -> rank | player | team | bar | signed | label | num | text."""
    kinds, fmts = kinds or {}, fmts or {}
    def isnan(v):
        try: return pd.isna(v)
        except Exception: return False
    th = ''.join(f'<th class="{"num" if kinds.get(c) in ("num", "signed", "bar") else ""}">{c}</th>' for c in df.columns); rows = []
    for ri, (_, r) in enumerate(df.iterrows()):
        tds = []
        for c in df.columns:
            v = r[c]; kd = kinds.get(c, 'text'); txt = '-' if isnan(v) else (fmts[c](v) if c in fmts else v)
            if kd == 'rank': rk = int(v); cell = f'<span class="rkb {"r" + str(rk) if rk <= 3 else ""}">{rk}</span>'
            elif kd == 'player': cell = f'<b>{txt}</b>'
            elif kd == 'team': cell = f'<span class="pill">{txt}</span>' if txt != '-' else '<span class="zero">-</span>'
            elif kd == 'bar': w = 0 if isnan(v) else max(0, min(100, (float(v) - 40) / 60 * 100)); cell = f'<span class="barwrap"><i style="width:{w:.0f}%"></i></span>{txt}'
            elif kd == 'signed': cls = 'zero' if isnan(v) or float(v) == 0 else ('pos' if float(v) > 0 else 'neg'); cell = f'<span class="{cls}">{txt}</span>'
            elif kd == 'label': cell = f'<span class="lab {"up" if txt in ("Excellent", "Great", "Above Average") else "down" if txt in ("Below Average", "Poor", "Awful") else "mid"}">{txt}</span>'
            else: cell = str(txt)
            tds.append(f'<td class="{"num" if kd in ("num", "signed", "bar") else ""}">{cell}</td>')
        rows.append(f'<tr class="{"tot" if last_total and ri == len(df) - 1 else ""}">{"".join(tds)}</tr>')
    style = f' style="max-height:{height}px"' if height else ''
    st.markdown(f'<div class="tblwrap"{style}><table class="t"><thead><tr>{th}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>', unsafe_allow_html=True)


def sf(v, d=1):
    v = 0.0 if abs(v) < 0.5 * 10 ** -d else v          # avoid showing -0.00
    return f'{v:+.{d}f}' if v != 0 else f'{0:.{d}f}'


def card(label, value, sub, hi=False): return f'<div class="card {"hi" if hi else ""}"><div class="l">{label}</div><div class="v">{value}</div><div class="s">{sub}</div></div>'


hc = st.columns([1.2, 4.0, 2.9, 1.6])
hc[0].markdown('<div class="brand">RR <b>SupeRR</b> Selector</div>', unsafe_allow_html=True)
page = hc[1].segmented_control('Page', ['Home', 'Pressure Impact', 'Clutch', 'Players', 'How it works'], default='Home', key='page', label_visibility='collapsed') or 'Home'
scope = hc[2].segmented_control('Data', list(SCOPE_LABEL), default='Both', key='scope', format_func=lambda s: SCOPE_LABEL[s], label_visibility='collapsed') or 'Both'
season = hc[3].selectbox('Season', SEASONS, format_func=lambda y: 'All seasons' if y == 'All' else str(y), key='season', label_visibility='collapsed')
role_label = {'Batters': 'bat', 'Bowlers': 'bowl'}


def cur(k):
    t = R.get((k, scope, season))
    if t is None: st.info('Not enough data for this combination of competition and season. Try All seasons or IPL + T20I.')
    return t


def role_pick(key): return role_label[st.segmented_control('Role', list(role_label), default='Batters', key=key, label_visibility='collapsed') or 'Batters']


def page_home():
    st.markdown(f'<div class="title">Who delivers when it matters?</div><div class="sub">The IPL and T20I players who add the most when the match is on the line, ranked by one combined score: 80% Pressure Impact and 20% clutch. Showing {SCOPE_LABEL[scope]}.</div>', unsafe_allow_html=True)
    c = st.columns(3, gap='large')
    c[0].markdown(card('Combined score', 'one number', '50 is the average rated player. Every 15 points is a big step up.', True), unsafe_allow_html=True)
    c[1].markdown(card('Pressure Impact (80%)', 'vs an average player', 'Runs a player adds (batters, extra runs) or saves (bowlers) in the big moments, compared with an average player.'), unsafe_allow_html=True)
    c[2].markdown(card('Clutch (20%)', 'vs his own level', 'Does he do better in the big moments than he usually does?'), unsafe_allow_html=True)
    st.write(''); k = role_pick('home_role'); d = cur(k)
    if d is None: return
    d = d.sort_values('combined', ascending=False).reset_index(drop=True); top = d.head(10)
    pc = st.columns(3, gap='large')
    for i in range(3):
        r = top.iloc[i]; pc[i].markdown(f'<div class="pod g{i + 1}"><div class="rk">{i + 1}</div><div class="nm">{r.player}</div><div class="tm">{r.ipl_2026_team if isinstance(r.ipl_2026_team, str) else "not in a 2026 squad"}</div>'
                                        f'<div class="row"><div>Score<b>{r.combined:.0f}</b></div><div>Pressure Impact<b>{f1(r.rating_per100)}</b></div><div>Clutch<b>{f1(r.clutch, 2)}</b></div></div></div>', unsafe_allow_html=True)
    st.write('')
    left, right = st.columns([6, 6], gap='large')
    with left:
        st.markdown('#### Top 10')
        tb = pd.DataFrame({'#': np.arange(1, 11), 'Player': top.player.values, 'Team': top.ipl_2026_team.map(team_of).values, 'Score': top.combined.values, 'Impact': top.rating_per100.values, 'Clutch': top.clutch.values})
        html_table(tb, kinds={'#': 'rank', 'Player': 'player', 'Team': 'team', 'Score': 'bar', 'Impact': 'signed', 'Clutch': 'signed'}, fmts={'Score': lambda v: f'<b>{v:.0f}</b>', 'Impact': lambda v: sf(v, 1), 'Clutch': lambda v: sf(v, 2)}, height=640)
        st.caption('Score = combined score. Impact = Pressure Impact (extra runs per 100 pressure balls for batters, runs saved for bowlers). Players with nearly the same score are effectively tied.')
    with right:
        st.markdown('#### Who is who')
        t = d.copy(); t['top'] = t.index < 10; f = go.Figure(); ymid = 0.0 if k == 'bowl' else t.rating_per100.median()       # bowlers are split at an average player (zero); batters at the middle rated player
        xr = max(t.clutch.abs().max() * 1.08, 0.5); y0, y1 = min(t.rating_per100.min(), ymid) - 2, t.rating_per100.max() + 3
        for (xa, xb, ya, yb, col) in ((0, xr, ymid, y1, 'rgba(232,54,143,.07)'), (-xr, 0, ymid, y1, 'rgba(91,140,255,.07)'), (0, xr, y0, ymid, 'rgba(95,224,163,.04)'), (-xr, 0, y0, ymid, 'rgba(255,122,138,.05)')):
            f.add_shape(type='rect', x0=xa, x1=xb, y0=ya, y1=yb, fillcolor=col, line=dict(width=0), layer='below')
        pos = ['top center', 'bottom center', 'middle right', 'middle left']
        s_ = t[~t.top]; f.add_trace(go.Scatter(x=s_.clutch, y=s_.rating_per100, mode='markers', marker=dict(size=9, color='rgba(140,160,215,.55)', line=dict(color='rgba(12,17,29,.9)', width=1)), customdata=s_.player, hovertemplate='<b>%{customdata}</b><br>Pressure Impact %{y:+.1f}<br>Clutch %{x:+.2f}<extra></extra>'))
        s_ = t[t.top]; f.add_trace(go.Scatter(x=s_.clutch, y=s_.rating_per100, mode='markers+text', text=s_.player.str.split().str[-1], textposition=[pos[i % 4] for i in range(len(s_))], textfont=dict(color=TXT, size=12, family='Poppins, Inter, sans-serif'),
                                              marker=dict(size=15, color=PINK, line=dict(color='white', width=1.8)), customdata=s_.player, hovertemplate='<b>%{customdata}</b><br>Pressure Impact %{y:+.1f}<br>Clutch %{x:+.2f}<extra></extra>'))
        f.add_vline(x=0, line_color='rgba(150,165,210,.5)', line_width=1.2); f.add_hline(y=ymid, line_color='rgba(150,165,210,.5)', line_width=1.2)
        for tx, ty, txt, anc, va in ((xr, y1, 'RISE AND DELIVER', 'right', 'top'), (-xr, y1, 'GOOD', 'left', 'top'), (xr, y0, 'RISE, BUT BELOW AVERAGE', 'right', 'bottom'), (-xr, y0, 'STRUGGLE WHEN IT COUNTS', 'left', 'bottom')):
            f.add_annotation(x=tx, y=ty, text=f'<b>{txt}</b>', showarrow=False, font=dict(color='rgba(190,200,230,.75)', size=11, family='Poppins, Inter, sans-serif'), xanchor=anc, yanchor=va)
        f.update_layout(title='', xaxis_title='Clutch: does he lift above his own level? →', yaxis_title='Pressure Impact: vs an average player →', xaxis_range=[-xr, xr], yaxis_range=[y0, y1]); st.plotly_chart(plain(f, 560), use_container_width=True)
        st.caption(('Up means better than an average player (the horizontal line is zero). ' if k == 'bowl' else 'Up means a higher Pressure Impact than the typical rated player in this view (the horizontal line is the middle player). ') + 'Right means he does better when it matters than his own usual level. Labelled dots are the combined top 10.')


def page_impact():
    st.markdown('<div class="title">Pressure Impact</div><div class="sub">For batters, Pressure Impact is the <b>extra runs</b> a player adds per 100 pressure balls. For bowlers it is the <b>runs saved</b>. Both are compared with an average player in the same situation. Pressure balls are the ones that can swing the match most (about 1 in 7). Players need at least 75 pressure balls to be rated.</div>', unsafe_allow_html=True)
    k = role_pick('imp_role'); d = cur(k)
    if d is None: return
    d = d.sort_values('rating_per100', ascending=False).reset_index(drop=True); t = d.head(10)
    left, right = st.columns(2, gap='large')
    with left: st.plotly_chart(lollipop(t.player, t.rating_per100, 'Top 10: ' + runs_word(k) + ' per 100 pressure balls', hover=' ' + runs_word(k) + ' per 100 pressure balls'), use_container_width=True)
    with right:
        st.markdown('#### All rated players')
        tb = pd.DataFrame({'#': np.arange(1, len(d) + 1), 'Player': d.player, 'Team': d.ipl_2026_team.map(team_of), 'Pressure Impact': d.rating_per100.values, 'Pressure balls': d.p_n.astype(int).values})
        html_table(tb, kinds={'#': 'rank', 'Player': 'player', 'Team': 'team', 'Pressure Impact': 'signed', 'Pressure balls': 'num'}, fmts={'Pressure Impact': lambda v: sf(v, 1)}, height=500)


def page_clutch():
    st.markdown('<div class="title">Clutch</div><div class="sub">Clutch compares a player with <b>his own</b> normal level. A high score means he did more than usual when the stakes were high.</div>', unsafe_allow_html=True)
    b = R[('bowl', 'Both', 'All')]; bb = b[b.player == 'Jasprit Bumrah']
    if len(bb) and season == 'All':
        r = bb.iloc[0]; imp_rank = int((b.rating_per100 > r.rating_per100).sum() + 1); cl_rank = int((b.clutch > r.clutch).sum() + 1)
        o = lambda n: f'{n}{"th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")}'
        st.markdown(f'<div class="note"><b>Why is a top player low on clutch?</b> Take Bumrah: {o(imp_rank)} among bowlers on Pressure Impact but {o(cl_rank)} of {len(b)} on clutch ({f1(r.clutch, 2)}). Clutch only rewards a player who is better in big moments than in ordinary ones. '
                    'Bumrah is elite in both, so there is no gap to reward and his score ends up near zero. Clutch measures rising, not being good, which is why it makes up only 20% of the combined score.</div>', unsafe_allow_html=True)
    st.write(''); k = role_pick('cl_role'); d = cur(k)
    if d is None: return
    d = d.sort_values('clutch', ascending=False).reset_index(drop=True); t = d.head(10)
    left, right = st.columns(2, gap='large')
    with left: st.plotly_chart(lollipop(t.player, t.clutch, 'Top 10 by clutch score', fmt='{:+.2f}', hover=' clutch', cs=((0, '#3F5FB8'), (1, '#7FD6FF'))), use_container_width=True)
    with right:
        st.markdown('#### All rated players')
        tb = pd.DataFrame({'#': np.arange(1, len(d) + 1), 'Player': d.player, 'Team': d.ipl_2026_team.map(team_of), 'Clutch': d.clutch.values, 'Rating': d.clutch.map(clutch_rating), 'Pressure Impact': d.rating_per100.values})
        html_table(tb, kinds={'#': 'rank', 'Player': 'player', 'Team': 'team', 'Clutch': 'signed', 'Rating': 'label', 'Pressure Impact': 'signed'}, fmts={'Clutch': lambda v: sf(v, 2), 'Pressure Impact': lambda v: sf(v, 1)}, height=500)
    st.markdown('#### How to read a clutch score')
    sc_, tx_ = st.columns([4, 6], gap='large')
    with sc_: html_table(pd.DataFrame({'Rating': [a for a, b_ in CLUTCH_SCALE], 'Clutch score': [b_ for a, b_ in CLUTCH_SCALE]}), kinds={'Rating': 'label', 'Clutch score': 'signed'}, fmts={'Clutch score': lambda v: sf(v, 1)})
    tx_.markdown('Most players land between **1 and -1**, with zero neutral. Positive scores are "clutch" and negative scores are "choke". Only a few players are lucky (or unlucky) enough to have extreme scores. A player\'s rating is the label closest to his score.')
    st.caption('Clutch is noisy: it changes a lot between halves of a player\'s career, so it is a hint and not a verdict.')


def band_table(k, pid, fam, inn, wpa_rows, season='All'):
    bs = BS[k][BS[k].pid == pid]; bs = bs if fam is None else bs[bs.family == fam]; bs = bs if season == 'All' else bs[bs.year == season]
    if inn != 'Both': bs = bs[bs.inn == (1 if inn == 'First innings' else 2)]
    g = bs.groupby('fg').sum(numeric_only=True).reindex(LAB).fillna(0); g.loc['All'] = g.sum(); g = g[g.balls > 0]
    w = wpa_rows.groupby('fg').wpa.sum().reindex(LAB).fillna(0); w.loc['All'] = w.sum(); g['wpa'] = w.reindex(g.index)
    nm = {'Low': 'Low (0.5 to 0.85)', 'Medium': 'Medium (0.85 to 1.4)', 'High': 'High (1.4 and above)', 'All': 'All balls'}
    if k == 'bat':
        out = pd.DataFrame({'Pressure level': [nm[i] for i in g.index], 'Balls faced': g.balls.astype(int), 'Runs': g.runs.astype(int), 'Strike rate': (100 * g.runs / g.balls).round(1), 'Outs': g.outs.astype(int),
                            'Average': (g.runs / g.outs.replace(0, np.nan)).round(1), 'Fours': g.fours.astype(int), 'Sixes': g.sixes.astype(int), 'Dot ball %': (100 * g.dots / g.balls).round(0), 'Win prob. added': g.wpa.round(2)})
    else:
        out = pd.DataFrame({'Pressure level': [nm[i] for i in g.index], 'Balls bowled': g.balls.astype(int), 'Runs conceded': g.runs.astype(int), 'Wickets': g.wickets.astype(int), 'Economy': (6 * g.runs / g.balls).round(2),
                            'Average': (g.runs / g.wickets.replace(0, np.nan)).round(1), 'Strike rate': (g.balls / g.wickets.replace(0, np.nan)).round(1), 'Dot ball %': (100 * g.dots / g.balls).round(0), 'Win prob. added': g.wpa.round(2)})
    return out.reset_index(drop=True)


def page_players():
    c1, c2 = st.columns([1, 3], gap='large')
    with c1: k = role_pick('pl_role')
    rr = cur(k)
    if rr is None: return
    rr = rr.sort_values('combined', ascending=False); p = c2.selectbox('Player', rr.player.tolist(), key=f'pl_{k}_{scope}_{season}', label_visibility='collapsed')
    r = rr[rr.player == p].iloc[0]; fam = None if scope == 'Both' else scope
    m = M[k][M[k].pid == r.pid].copy(); m = m if fam is None else m[m.family == fam]; m = m if season == 'All' else m[m.year == season]
    st.markdown(f'<div class="title" style="margin-top:6px">{p}</div><div class="sub">{r.ipl_2026_team if isinstance(r.ipl_2026_team, str) else "not in a 2026 squad"} · {SCOPE_LABEL[scope]} · {int(r.p_n)} pressure balls (evidence: {r.reliability})</div>', unsafe_allow_html=True)
    c = st.columns(4, gap='large')
    c[0].markdown(card('Combined score', f'{r.combined:.0f}', '50 is the average rated player', True), unsafe_allow_html=True)
    c[1].markdown(card('Pressure Impact', f1(r.rating_per100), runs_word(k) + ' per 100 pressure balls vs an average player'), unsafe_allow_html=True)
    c[2].markdown(card('Clutch', f1(r.clutch, 2), f'{clutch_rating(r.clutch)} · vs his own normal level'), unsafe_allow_html=True)
    c[3].markdown(card('Win probability added', f1(r.career_wpa, 2), 'matches\' worth of win chance he added'), unsafe_allow_html=True)
    bsall = BS[k][BS[k].pid == r.pid]; bsall = bsall if fam is None else bsall[bsall.family == fam]; bsall = bsall if season == 'All' else bsall[bsall.year == season]; gg = bsall.groupby('fg').sum(numeric_only=True)
    if r.clutch < 0 and r.rating_per100 > rr.rating_per100.quantile(.85) and 'High' in gg.index and len(gg) > 1:
        hi, lo = gg.loc['High'], gg.drop('High').sum()
        a_, b_ = (100 * hi.runs / hi.balls, 100 * lo.runs / lo.balls) if k == 'bat' else (6 * hi.runs / hi.balls, 6 * lo.runs / lo.balls)
        pair = f'strike rate {a_:.0f} under pressure against {b_:.0f} otherwise' if k == 'bat' else f'economy {a_:.2f} under pressure against {b_:.2f} otherwise'
        if abs(a_ / b_ - 1) < 0.06:
            msg = f'{p} performs about the same when it matters as at other times ({pair}). Pressure Impact rewards that, because few players match it. Clutch only rewards a step up, and he is already elite everywhere.'
        else:
            msg = f'{p} does play differently under pressure ({pair}), but clutch also weighs how much was at stake, and it is noisy: his score is close to zero and well within the margin of error. Pressure Impact is the better guide to how good he is when it matters.'
        st.markdown(f'<br><div class="note"><b>Why is clutch low?</b> {msg}</div>', unsafe_allow_html=True)
    st.write(''); t1, t2, t3 = st.tabs(['By pressure level', 'Against each team', 'Big games'])
    with t1:
        inn = st.segmented_control('Innings', ['Both', 'First innings', 'Chase'], default='Both', key='bandinn', label_visibility='collapsed') or 'Both'
        bd = BD[k][BD[k].pid == r.pid]; bd = bd if fam is None else bd[bd.family == fam]; bd = bd if season == 'All' else bd[bd.year == season]
        if inn != 'Both': bd = bd[bd.inn == (1 if inn == 'First innings' else 2)]
        bt = band_table(k, r.pid, fam, inn, bd, season)
        fm = {c_: (lambda v: f'{v:.0f}') for c_ in bt.columns if c_ in ('Dot ball %',)}; fm.update({'Strike rate': (lambda v: f'{v:.1f}') if k == 'bat' else (lambda v: f'{v:.1f}'), 'Average': lambda v: f'{v:.1f}', 'Win prob. added': lambda v: sf(v, 2)})
        if k == 'bowl': fm['Economy'] = lambda v: f'{v:.2f}'
        html_table(bt, kinds={**{c_: 'num' for c_ in bt.columns[1:]}, 'Pressure level': 'player', 'Win prob. added': 'signed'}, fmts=fm, last_total=True)
        st.caption('Pressure level is how much a ball can swing the match. High is the pressure zone and has fewer balls, so its numbers move around more. Balls below 0.5 are nearly decided and are left out of this table and of clutch.')
        bb = bd.groupby('fg').agg(balls=('balls', 'sum'), value=('value', 'sum'), wpa=('wpa', 'sum')).reindex(LAB).fillna(0).reset_index(); n = bb.balls.replace(0, np.nan)
        bb['per100'] = 100 * bb.value / n; bb['wpa100'] = 100 * bb.wpa / n; bb['x'] = bb.fg.map(BAND_NAME); cA, cB = st.columns(2, gap='large'); bcol = ['#4A5C93', BLUE, PINK]
        f = go.Figure(go.Bar(x=bb.x, y=bb.per100, width=0.45, marker=dict(color=bcol, line=dict(width=0)), text=[('' if pd.isna(v) else sf(v, 1)) for v in bb.per100], textposition='outside', textfont=dict(color=TXT), customdata=bb.balls, hovertemplate='%{x}<br>%{y:+.1f} per 100 balls<br>%{customdata} balls<extra></extra>', cliponaxis=False)); f.add_hline(y=0, line_color='rgba(150,165,210,.5)')
        f.update_layout(title=runs_word(k, True) + ' per 100 balls'); cA.plotly_chart(plain(f, 340), use_container_width=True)
        g = go.Figure(go.Bar(x=bb.x, y=bb.wpa100, width=0.45, marker=dict(color=bcol, line=dict(width=0)), text=[('' if pd.isna(v) else sf(v, 2)) for v in bb.wpa100], textposition='outside', textfont=dict(color=TXT), customdata=bb.balls, hovertemplate='%{x}<br>%{y:+.2f} wins per 100 balls<br>%{customdata} balls<extra></extra>', cliponaxis=False)); g.add_hline(y=0, line_color='rgba(150,165,210,.5)')
        g.update_layout(title='Win probability added per 100 balls'); cB.plotly_chart(plain(g, 340), use_container_width=True)
    with t2:
        g = m.groupby('opponent').agg(p_balls=('p_balls', 'sum'), p_value=('p_value', 'sum')).reset_index(); g = g[g.p_balls >= 12]
        if g.empty: st.info('Not enough pressure balls against any single team in this view.')
        else:
            g['per100'] = 100 * g.p_value / g.p_balls; g['team'] = g.opponent.map(sh); g = g.sort_values('per100', ascending=False)
            st.plotly_chart(lollipop(g.team, g.per100, runs_word(k, True) + ' per 100 pressure balls, by opponent', h=max(300, 40 * len(g) + 110), hover=' per 100 pressure balls'), use_container_width=True)
    with t3:
        st.caption('Big games are finals, qualifiers, eliminators and semi-finals.')
        ko = m[m.ko]
        if ko.empty: st.info('No big games in this view.')
        else:
            kk = ko.groupby(['date', 'stage', 'opponent']).agg(balls=('balls', 'sum'), value=('value', 'sum'), wpa=('wpa', 'sum')).reset_index().sort_values('date')
            kk['date'] = pd.to_datetime(kk.date).dt.strftime('%d %b %Y'); kk['opponent'] = kk.opponent.map(sh)
            kk = kk.rename(columns={'date': 'Date', 'stage': 'Stage', 'opponent': 'Vs', 'balls': 'Balls', 'value': runs_word(k, True), 'wpa': 'Win prob. added'})
            html_table(kk, kinds={'Date': 'text', 'Stage': 'label', 'Vs': 'team', 'Balls': 'num', runs_word(k, True): 'signed', 'Win prob. added': 'signed'}, fmts={runs_word(k, True): lambda v: sf(v, 1), 'Win prob. added': lambda v: sf(v, 2)})


def page_how():
    st.markdown('<div class="title">How it works</div>', unsafe_allow_html=True)
    left, right = st.columns([4, 6], gap='large')
    with left:
        st.markdown("""
**1. Win chance.** For every ball we estimate how likely the batting side is to win.

**2. Pressure.** Some balls can swing a match more than others. A **pressure ball** is one in the top band of that swing (about 1 ball in 7), mostly in the middle and end of a chase.

**3. Pressure Impact.** We score every ball in runs and compare it with an average player in the same spot. For a batter, the score is the **extra runs** he adds; for a bowler it is the **runs saved**. A player's average over his pressure balls, with luck stripped out, is his Pressure Impact.

**4. Clutch.** Compares a player with his own normal level. A player who is excellent everywhere has no gap to show, so he can score near zero. Balls in nearly decided moments (pressure level below 0.5) are not used.

**5. Combined score.** 80% Pressure Impact and 20% clutch, turned into one score where 50 is the average rated player. Clutch gets the smaller share because it is much noisier.
""")
    with right:
        row = LBO[LBO.scope == scope].sort_values('over'); f = go.Figure()
        f.add_trace(go.Scatter(x=row.over, y=row['first'], name='First innings', mode='lines', line=dict(color=BLUE, width=3.5, shape='spline'), fill='tozeroy', fillcolor='rgba(91,140,255,.12)'))
        f.add_trace(go.Scatter(x=row.over, y=row.chase, name='Chase', mode='lines', line=dict(color=PINK, width=3.5, shape='spline'), fill='tozeroy', fillcolor='rgba(232,54,143,.12)'))
        f.add_hline(y=1, line_color='rgba(190,200,230,.5)', line_dash='dot'); f.update_layout(title='Does the model make sense? Average pressure level, over by over', xaxis_title='over', yaxis_title='average pressure level (1 = an average ball)', xaxis_range=[1, 20], yaxis_range=[0, 2.5])
        st.plotly_chart(plain(f, 420).update_layout(showlegend=True, legend=dict(orientation='h', y=1.0, x=1, xanchor='right', yanchor='bottom', font=dict(color=TXT))), use_container_width=True)
        st.markdown('<div class="note">In the first innings there is no target, so no ball matters much more than another. In a chase, the closer the finish, the more every ball matters, so the line climbs towards the last overs. A sensible pressure measure should look like this.</div>', unsafe_allow_html=True)
    st.write(''); st.markdown('**Can you trust it?** It predicts matches it has not seen better than guessing, but it mostly reflects how good a player is overall, and clutch barely repeats from one half of a career to the other. Treat players with close scores as tied.')


{'Home': page_home, 'Pressure Impact': page_impact, 'Clutch': page_clutch, 'Players': page_players, 'How it works': page_how}[page]()
