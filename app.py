"""
app.py - ScamShield Arena (Streamlit UI)

Run:  streamlit run app.py
Every organisation and message in this app is fictional and for training only.
"""
import html
import os
import random
import re
import time

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

import content
import coop
import coop_content
import engine
import pilot_stats
import storage
from i18n import LANGS, T, TT

# Change the product name in ONE place (or set the APP_NAME environment variable).
APP_NAME = os.environ.get("APP_NAME", "KEBAL")
st.set_page_config(page_title=APP_NAME, page_icon="🛡️", layout="wide")
storage.init_db()
storage.init_pilot()
coop.init()

TEAL, TEAL_DARK, AMBER, RED, GREEN = "#0F766E", "#115E59", "#F59E0B", "#DC2626", "#16A34A"
def secret(name, default=""):
    """Environment variable first, then Streamlit secrets (used on Streamlit Community Cloud)."""
    if os.environ.get(name):
        return os.environ[name]
    try:
        return str(st.secrets.get(name, default))
    except Exception:  # noqa: BLE001 - no secrets file locally
        return default


TEACHER_PIN = secret("TEACHER_PIN", "1234")

P_HOME, P_PRE, P_ARENA, P_STORY = "🏠 Home", "📏 Pre-Test", "🎮 Training Arena", "🎭 Story Missions"
P_COOP = "🗺️ Co-op Simulation"
P_POST, P_PROGRESS, P_TEACHER, P_HELP = "🏁 Post-Test", "📊 My Progress", "👩‍🏫 Teacher Dashboard", "🆘 Safety & Help"
P_RETEST = "🔁 Retention Test"
PAGES = [P_HOME, P_PRE, P_ARENA, P_STORY, P_COOP, P_POST, P_RETEST, P_PROGRESS, P_TEACHER, P_HELP]
AUDIO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "audio")
CONFIDENCE = ["😬 Guessing", "🙂 Fairly sure", "😎 Certain"]

# ------------------------------------------------------------------ styles
st.markdown(f"""<style>
.block-container {{padding-top: 2rem; max-width: 1150px;}}
.hero {{background: linear-gradient(135deg, {TEAL} 0%, {TEAL_DARK} 100%); color: #fff; padding: 28px 30px;
        border-radius: 20px; margin-bottom: 18px;}}
.hero h1 {{color: #fff; margin: 0 0 6px 0; font-size: 2.2rem;}}
.hero p {{color: #ccfbf1; font-size: 1.08rem; margin: 0;}}
.hero .tag {{display:inline-block; background:{AMBER}; color:#1f2937; font-weight:700; font-size:.75rem;
            padding:3px 10px; border-radius:999px; margin-bottom:10px; letter-spacing:.04em;}}
.card {{border: 1px solid #e2e8f0; border-radius: 16px; padding: 16px 18px; background: #fff; height: 100%;}}
.card h4 {{margin: 0 0 6px 0; color: {TEAL_DARK};}}
.card p {{margin: 0; color: #475569; font-size: .95rem;}}
.ctx {{background:#FEF3C7; color:#78350F; border-radius:12px; padding:9px 13px; margin:0 auto 10px auto;
       max-width:400px; font-size:.92rem;}}
.phone {{max-width:400px; margin:0 auto; background:#0B1F1D; border-radius:30px; padding:14px 14px 16px 14px;
         box-shadow: 0 12px 30px rgba(15,118,110,.25); border: 6px solid #1E293B;}}
.phone-top {{display:flex; justify-content:space-between; gap:10px; color:#CCFBF1; font-size:.82rem;
             padding:2px 6px 10px 6px; border-bottom:1px solid rgba(255,255,255,.12);}}
.phone-top .from {{font-weight:700; color:#fff; text-align:right; overflow-wrap:anywhere;}}
.bubble {{background:#fff; color:#111827; border-radius:16px 16px 16px 4px; padding:13px 15px; margin-top:12px;
          font-size:1rem; line-height:1.5; white-space:pre-wrap; overflow-wrap:anywhere;}}
.sim {{text-align:center; color:#94A3B8; font-size:.66rem; margin-top:12px; letter-spacing:.1em;}}
.cue {{padding:10px 13px; border-radius:12px; margin-bottom:8px; border-left:6px solid; background:#F8FAFC;}}
.cue b {{display:block; margin-bottom:2px;}}
.cue span {{color:#475569; font-size:.9rem;}}
.cue.ok {{border-color:{GREEN}; background:#F0FDF4;}}
.cue.miss {{border-color:{AMBER}; background:#FFFBEB;}}
.cue.fa {{border-color:{RED}; background:#FEF2F2;}}
.cue.neutral {{border-color:#94A3B8;}}
.verdict {{border-radius:16px; padding:14px 18px; color:#fff; font-size:1.1rem; margin-bottom:12px;}}
.verdict.good {{background:{GREEN};}}
.verdict.bad {{background:{RED};}}
.lesson {{background:#ECFEFF; border:1px solid #A5F3FC; border-radius:14px; padding:12px 15px; color:#164E63;}}
.badge {{display:inline-block; text-align:center; width:150px; vertical-align:top; margin:0 10px 12px 0;
         border:1px solid #e2e8f0; border-radius:16px; padding:12px 8px; background:#fff;}}
.badge .ic {{font-size:2rem;}}
.badge .nm {{font-weight:700; color:{TEAL_DARK}; font-size:.9rem;}}
.badge .ds {{color:#64748B; font-size:.75rem;}}
.badge.locked {{opacity:.35; filter:grayscale(1);}}
.fourp {{display:flex; flex-wrap:wrap; gap:10px;}}
.fourp div {{flex:1 1 200px; border-radius:14px; padding:12px 14px; background:#F0FDFA; border:1px solid #99F6E4;}}
.fourp b {{color:{TEAL_DARK};}}
.callscr {{text-align:center; padding:18px 6px 6px 6px; color:#E2E8F0;}}
.callscr .av {{width:84px; height:84px; border-radius:50%; margin:6px auto 12px auto; display:flex; align-items:center;
               justify-content:center; font-size:2.4rem; background:linear-gradient(135deg,#334155,#0F766E);
               animation:pulse 1.6s infinite;}}
.callscr .lbl {{font-size:.8rem; letter-spacing:.12em; color:#94A3B8;}}
.callscr .who {{font-size:1.15rem; font-weight:700; color:#fff; margin:4px 0 10px 0; overflow-wrap:anywhere;}}
.callscr .hint {{font-size:.85rem; color:#5EEAD4;}}
@keyframes pulse {{0% {{box-shadow:0 0 0 0 rgba(94,234,212,.5);}} 70% {{box-shadow:0 0 0 16px rgba(94,234,212,0);}}
                  100% {{box-shadow:0 0 0 0 rgba(94,234,212,0);}}}}
.story-head {{border-radius:16px; padding:14px 18px; background:#0B1F1D; color:#E2E8F0; margin-bottom:12px;}}
.story-head b {{color:#5EEAD4;}}
.ending {{border-radius:18px; padding:18px 22px; color:#fff; margin-bottom:14px;}}
.ending h3 {{color:#fff; margin:0 0 6px 0;}}
.ending.safe {{background:{GREEN};}} .ending.close {{background:{AMBER}; color:#1F2937;}}
.ending.close h3 {{color:#1F2937;}} .ending.lost {{background:{RED};}}
.step {{border-radius:12px; padding:10px 13px; margin-bottom:8px; background:#F8FAFC; border-left:6px solid #94A3B8;}}
.step.good {{border-color:{GREEN};}} .step.meh {{border-color:{AMBER};}} .step.bad {{border-color:{RED};}}
.step small {{color:#64748B;}}
.roomcode {{font-size:2.6rem; font-weight:800; letter-spacing:.25em; color:{TEAL_DARK}; text-align:center;
           background:#F0FDFA; border:2px dashed {TEAL}; border-radius:16px; padding:8px 0;}}
.hud {{display:flex; flex-wrap:wrap; gap:10px; align-items:center; justify-content:space-between; border-radius:16px;
       padding:12px 16px; background:#0B1F1D; color:#E2E8F0; margin-bottom:12px;}}
.hud .t {{font-size:1.9rem; font-weight:800; color:#5EEAD4; font-variant-numeric:tabular-nums;}}
.hud .t.hot {{color:#FCA5A5; animation:blink 1s infinite;}}
.hud .rb {{background:{AMBER}; color:#1F2937; font-weight:800; border-radius:999px; padding:3px 12px; font-size:.85rem;}}
.doom {{background:#7F1D1D; color:#FEE2E2; border-radius:12px; padding:10px 14px; margin-bottom:10px; font-weight:700;
        animation:blink 1s infinite;}}
@keyframes blink {{50% {{opacity:.55;}}}}
.feed {{font-size:.92rem;}}
.feed div {{border-radius:10px; padding:7px 10px; margin-bottom:6px; background:#F8FAFC; border-left:5px solid #CBD5E1;}}
.feed .pressure {{background:#FEF2F2; border-color:{RED};}}
.feed .clue {{background:#F0FDF4; border-color:{GREEN};}}
.feed .chat {{background:#EFF6FF; border-color:#3B82F6;}}
.feed .reply {{background:#FFFBEB; border-color:{AMBER};}}
.feed .system {{background:#F0FDFA; border-color:{TEAL};}}
.feed small {{color:#64748B;}}
.pl {{display:inline-block; border-radius:999px; padding:4px 12px; margin:0 6px 6px 0; background:#F1F5F9; font-weight:600;}}
</style>""", unsafe_allow_html=True)


def esc(x):
    return html.escape(str(x or ""))


# ----------------------------------------------------------- session state
DEFAULTS = {"nav": P_HOME, "player": None, "mission": None, "round_result": None, "story": None, "room": None,
            "pre_answers": [], "post_answers": [], "retention_answers": [], "ai_key": "", "ai_lang": "English"}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v
ss = st.session_state
if "lang" not in ss:
    ss.lang = "ms" if st.query_params.get("lang") == "ms" else "en"


def go_to(page):
    """Request navigation; applied before the sidebar menu is drawn on the next run."""
    ss["_goto"] = page


if "_goto" in ss:
    ss.nav = ss.pop("_goto")


def player_xp(pid):
    df = storage.player_attempts(pid)
    return int(df["xp"].sum()) if not df.empty else 0


def api_key():
    return secret("ANTHROPIC_API_KEY") or ss.ai_key


def my_class():
    return storage.class_settings(ss.player.get("school", "")) if ss.player else storage.class_settings("")


def blocked_for_control():
    """Control-group students only take the tests until the study ends."""
    if ss.player and my_class()["grp"] == "control":
        st.info(T("Your group takes the tests only for now. You'll get full access to the game when the study ends. Thank you for helping!"))
        return True
    return False


# ----------------------------------------------------------- shared views
def phone_html(s):
    icon = content.CHANNEL_ICONS.get(s.get("channel"), "💬")
    ctx = f'<div class="ctx">📌 <b>{T("Situation:")}</b> {esc(s["context"])}</div>' if s.get("context") else ""
    return (f'{ctx}<div class="phone"><div class="phone-top"><span>{icon} {esc(T(s.get("channel") or ""))}</span>'
            f'<span class="from">{esc(s.get("sender"))}</span></div>'
            f'<div class="bubble">{esc(s.get("message"))}</div>'
            f'<div class="sim">{T("TRAINING SIMULATION · ALL NAMES FICTIONAL")}</div></div>')


def call_html(s):
    icon = "🎥" if s.get("channel") == "Video call" else "📞"
    ctx = f'<div class="ctx">📌 <b>{T("Situation:")}</b> {esc(s["context"])}</div>' if s.get("context") else ""
    return (f'{ctx}<div class="phone"><div class="callscr"><div class="lbl">{T("INCOMING")} {esc(T(s.get("channel", ""))).upper()}</div>'
            f'<div class="av">{icon}</div><div class="who">{esc(s.get("sender"))}</div>'
            f'<div class="hint">{T("🔊 Press play below and listen carefully")}</div></div>'
            f'<div class="sim">{T("TRAINING SIMULATION · SYNTHETIC VOICE · ALL NAMES FICTIONAL")}</div></div>')


def render_scenario(s):
    """Phone mock-up for text messages; call screen + audio player for voice scenarios."""
    audio = s.get("audio")
    if not audio:
        st.markdown(phone_html(s), unsafe_allow_html=True)
        return
    st.markdown(call_html(s), unsafe_allow_html=True)
    path = os.path.join(AUDIO_DIR, audio)
    if os.path.exists(path):
        st.audio(path, format="audio/mpeg")
    else:
        st.caption(T("⚠️ Audio file missing. Run generate_audio.py. Transcript below."))
    with st.expander(T("📝 Show transcript (for deaf / hard-of-hearing players)"), expanded=not os.path.exists(path)):
        st.markdown(f'<div class="bubble" style="margin-top:0">{esc(s["message"])}</div>', unsafe_allow_html=True)


def four_p():
    items = [("⏰ Pressure", "Urgency, fear, threats, deadlines, \"don't tell anyone\"."),
             ("💸 Payment", "Fees to claim prizes, deposits, transfers to personal accounts."),
             ("🔑 Private info", "Asks for OTP/TAC, passwords, banking login, IC photos."),
             ("🧭 Path", "Pulls you off official channels: odd links, APK files, new numbers, private groups.")]
    return '<div class="fourp">' + "".join(f"<div><b>{T(a)}</b><br>{esc(T(b))}</div>" for a, b in items) + "</div>"


def need_player():
    if not ss.player:
        st.info(T("Please sign in on the Home page first. It takes 10 seconds and only needs a nickname."))
        st.button(T("Go to Home"), on_click=go_to, args=(P_HOME,), type="primary")
        return False
    return True


# ------------------------------------------------------------------ sidebar
with st.sidebar:
    st.radio(T("🌐 Language"), list(LANGS), format_func=LANGS.get, key="lang", horizontal=True)
    st.markdown(f"## 🛡️ {esc(APP_NAME)}")
    st.caption(T("Practise on fake scams so you never fall for a real one."))
    st.radio("Navigate", PAGES, key="nav", label_visibility="collapsed", format_func=TT())
    st.divider()
    if ss.player:
        xp = player_xp(ss.player["id"])
        name, icon, floor, nxt, nxt_name = engine.level_for(xp)
        st.markdown(f"**{esc(ss.player['nickname'])}** · {icon} {T(name)}")
        st.progress(1.0 if nxt is None else (xp - floor) / (nxt - floor),
                    text=f"{xp} XP" + ("" if nxt is None else " · " + T("{n} to {lvl}", n=nxt - xp, lvl=T(nxt_name))))
        if st.button(T("Sign out")):
            for k, v in DEFAULTS.items():
                if k not in ("nav", "lang"):
                    ss[k] = v if not isinstance(v, list) else []
            go_to(P_HOME)
            st.rerun()
    with st.expander(T("⚙️ Live AI scenarios")):
        if os.environ.get("ANTHROPIC_API_KEY"):
            st.success(T("API key loaded from server."))
        else:
            ss.ai_key = st.text_input(T("Anthropic API key (optional)"), value=ss.ai_key, type="password",
                                      help=T("Without a key the app uses its built-in scenario bank."))
        ss.ai_lang = st.selectbox(T("AI message language"), ["English", "Bahasa Melayu", "Mixed (Manglish)"],
                                  index=["English", "Bahasa Melayu", "Mixed (Manglish)"].index(ss.ai_lang))


# =================================================================== HOME
def page_home():
    hero_txt = T("A flight simulator for scams. Practise on fake ones, including real-sounding voice calls, "
                 "spot the red flags, and prove you've levelled up.")
    st.markdown(f'<div class="hero"><span class="tag">{T("EDUTAINMENT · ANTI-SCAM")}</span>'
                f'<h1>🛡️ {esc(APP_NAME)}</h1>'
                f'<p>{esc(hero_txt)}</p></div>',
                unsafe_allow_html=True)
    cards = [("1 · 📏 Baseline test", "10 tricky messages, including a voice call. Scam or legit, and how sure are you? This measures where you start."),
             ("2 · 🎮 Train, 🎭 Survive, 🗺️ Team up", "Arena missions with voice calls, branching Story Missions, and live multiplayer Co-op Simulations on a town map."),
             ("3 · 🏁 Prove your growth", "A new 10-message test shows how much sharper you've become.")]
    for col, (h, b) in zip(st.columns(3), cards):
        col.markdown(f'<div class="card"><h4>{T(h)}</h4><p>{esc(T(b))}</p></div>', unsafe_allow_html=True)
    st.write("")

    if st.query_params.get("room") and not ss.player:
        st.success(T("🗺️ You've been invited to Co-op room **{code}**. Enter a nickname below to join.",
                     code=esc(st.query_params.get('room'))))
    if not ss.player:
        st.subheader(T("Start playing"))
        with st.form("signin"):
            a, b, c = st.columns(3)
            nick = a.text_input(T("Nickname"), max_chars=30, placeholder="CyberTiger")
            school = b.text_input(T("Class / school code (optional)"), max_chars=30, placeholder="SMKTI-4A")
            age = c.selectbox(T("Age group"), ["13–17", "18–24", "25–59", "60+"])
            st.caption(T("🔒 Privacy: don't use your real name. We only store your nickname, age group and code."))
            consent = st.checkbox(T("Research consent: I have read the information sheet, I am 18 or older, and I agree that my anonymous answers can be used for research. (Only needed if your class is part of a study.)"))
            if st.form_submit_button(T("Enter the Arena 🚀"), type="primary"):
                needs = storage.class_settings(school)["consent_required"]
                known = storage.find_player(nick, school)
                if not nick.strip():
                    st.warning(T("Please type a nickname."))
                elif needs and not consent and not (known and known.get("consent_at")):
                    st.warning(T("Your class is part of a research study. Please read the information sheet and tick the consent box to continue."))
                else:
                    player, new = storage.get_or_create_player(nick, school, age)
                    if consent:
                        storage.record_consent(player["id"])
                    ss.player = player
                    if st.query_params.get("room"):
                        go_to(P_COOP)
                    else:
                        go_to(P_PRE if new or not storage.test_score(player["id"], "pre") else P_ARENA)
                    st.rerun()
    else:
        pid = ss.player["id"]
        pre = storage.test_score(pid, "pre")
        st.subheader(T("Welcome, {name}! 👋", name=ss.player['nickname']))
        if not pre:
            st.write(T("First step: take the 2-minute **Pre-Test** so we can measure your progress."))
            st.button(T("Start Pre-Test →"), on_click=go_to, args=(P_PRE,), type="primary")
        else:
            st.write(T("Your baseline: **{a}/{b}**. Jump into the Arena to train.", a=pre[0], b=pre[1]))
            st.button(T("Enter Training Arena →"), on_click=go_to, args=(P_ARENA,), type="primary")

    st.write("")
    st.subheader(T("The 4P Scam Check"))
    st.markdown(four_p(), unsafe_allow_html=True)


# ============================================================= TESTS
def run_test(mode, items):
    label = T({"pre": "Pre-Test", "post": "Post-Test", "retention": "Retention Test"}[mode])
    pid = ss.player["id"]
    done = storage.test_score(pid, mode)
    answers_key = f"{mode}_answers"

    if done:
        pct = round(100 * done[0] / done[1])
        st.success(T("{label} complete: **{a}/{b}** ({pct}%)", label=label, a=done[0], b=done[1], pct=pct))
        if mode == "post":
            pre = storage.test_score(pid, "pre")
            if pre:
                pre_pct = round(100 * pre[0] / pre[1])
                d = pct - pre_pct
                a, b, c = st.columns(3)
                a.metric(T("Pre-Test"), f"{pre_pct}%")
                b.metric(T("Post-Test"), f"{pct}%", delta=T("{d} points", d=f"{d:+d}"))
                c.metric(T("Training rounds"), int((storage.player_attempts(pid)["mode"] == "train").sum()))
                if d > 0:
                    st.balloons()
                    st.markdown(T("### 📈 You improved by {d} points. That's real, measurable growth!", d=d))
                elif d == 0:
                    st.markdown(T("### Same score as before. Try a Hard mission and focus on your weakest tactic in My Progress."))
                else:
                    st.markdown(T("### Tricky set! Review the explanations below and play another mission."))
        if mode == "retention":
            pre, post = storage.test_score(pid, "pre"), storage.test_score(pid, "post")
            a, b, c = st.columns(3)
            if pre:
                a.metric(T("Pre-Test"), f"{round(100 * pre[0] / pre[1])}%")
            if post:
                b.metric(T("Post-Test"), f"{round(100 * post[0] / post[1])}%")
            c.metric(T("Retention Test"), f"{pct}%")
            st.markdown(T("### Thank you! This shows how much of your skill lasted over two weeks."))
        df = storage.player_attempts(pid)
        df = df[df["mode"] == mode]
        with st.expander(T("Review answers and explanations")):
            for it in items:
                row = df[df["scenario_id"] == it["id"]]
                if row.empty:
                    continue
                ok = bool(row.iloc[0]["correct"])
                truth = T("SCAM 🚩" if it["is_scam"] else "LEGIT ✅")
                st.markdown(f"{'✅' if ok else '❌'} **{esc(it['sender'])}** ({T(it['channel'])}): {T('it was')} **{truth}**. {esc(it['why'])}")
        if mode == "pre":
            st.button(T("Enter Training Arena →"), on_click=go_to, args=(P_ARENA,), type="primary")
        return

    answers = ss[answers_key]
    i = len(answers)
    if i == 0:
        st.write(T("{n} messages, including a voice call 🎧. For each one decide **Scam** or **Legit**, and say how sure you are. No hints during the test.", n=len(items)))
    st.progress(i / len(items), text=T("Question {i} of {n}", i=i + 1, n=len(items)))
    item = items[i]
    conf_key = f"{mode}_conf_{i}"

    def answer(is_scam):
        conf = CONFIDENCE.index(ss.get(conf_key, CONFIDENCE[1])) + 1
        ss[answers_key].append((is_scam, conf))
        if len(ss[answers_key]) == len(items):
            for it, (ans, cf) in zip(items, ss[answers_key]):
                storage.record_attempt(pid, mode, it, ans, ans == it["is_scam"], confidence=cf)
            ss[answers_key] = []

    left, right = st.columns([3, 2], vertical_alignment="center")
    with left:
        render_scenario(item)
    with right:
        st.markdown("#### " + T("Is this a scam?"))
        st.radio(T("How sure are you?"), CONFIDENCE, index=1, horizontal=True, key=conf_key, format_func=TT())
        st.button(T("🚩  Scam"), on_click=answer, args=(True,), type="primary", key=f"{mode}_s_{i}", width="stretch")
        st.button(T("✅  Legit"), on_click=answer, args=(False,), key=f"{mode}_l_{i}", width="stretch")


def page_pre():
    st.title(T(P_PRE))
    if need_player():
        run_test("pre", content.PRE_TEST)


def page_post():
    st.title(T(P_POST))
    if not need_player():
        return
    pid = ss.player["id"]
    df = storage.player_attempts(pid)
    trained = int((df["mode"] == "train").sum()) if not df.empty else 0
    if not storage.test_score(pid, "pre"):
        st.info(T("Take the Pre-Test first so we can measure your improvement."))
        st.button(T("Go to Pre-Test"), on_click=go_to, args=(P_PRE,), type="primary")
        return
    control = my_class()["grp"] == "control"
    if not control and trained < engine.MISSION_LENGTH and not storage.test_score(pid, "post"):
        st.info(T("Play at least one full mission ({n} rounds) first. You've played {t}.", n=engine.MISSION_LENGTH, t=trained))
        st.button(T("Go to Training Arena"), on_click=go_to, args=(P_ARENA,), type="primary")
        return
    run_test("post", content.POST_TEST)
    if storage.test_score(pid, "post") and not control and not storage.get_survey(pid):
        survey_form(pid)


SUS_ITEMS = [
    "I think that I would like to use KEBAL frequently.",
    "I found KEBAL unnecessarily complex.",
    "I thought KEBAL was easy to use.",
    "I think that I would need the support of a technical person to be able to use KEBAL.",
    "I found the various functions in KEBAL were well integrated.",
    "I thought there was too much inconsistency in KEBAL.",
    "I would imagine that most people would learn to use KEBAL very quickly.",
    "I found KEBAL very cumbersome to use.",
    "I felt very confident using KEBAL.",
    "I needed to learn a lot of things before I could get going with KEBAL.",
]
HELPED = ["Training Arena", "Story Missions", "Co-op Simulation", "Voice calls", "Red-flag explanations"]


def survey_form(pid):
    st.divider()
    st.subheader(T("📝 Quick survey (2 minutes)"))
    st.caption(T("1 = strongly disagree, 5 = strongly agree. Your honest opinion helps us improve KEBAL."))
    with st.form("sus"):
        answers = [st.radio(f"{i + 1}. {T(q)}", [1, 2, 3, 4, 5], index=None, horizontal=True, key=f"sus_{i}")
                   for i, q in enumerate(SUS_ITEMS)]
        helped = st.multiselect(T("Which parts helped you most?"), HELPED, format_func=TT())
        rec = st.slider(T("How likely are you to recommend KEBAL to your family? (0 = not at all, 10 = definitely)"), 0, 10, 7)
        comment = st.text_area(T("Anything else you want to tell us? (optional)"), max_chars=500)
        if st.form_submit_button(T("Submit survey"), type="primary"):
            if any(a is None for a in answers):
                st.warning(T("Please answer all 10 statements."))
            else:
                storage.save_survey(pid, answers, ", ".join(helped), rec, comment)
                st.success(T("Thank you! Survey saved."))
                st.rerun()


def page_retest():
    st.title(T(P_RETEST))
    if not need_player():
        return
    pid = ss.player["id"]
    if not storage.test_score(pid, "post"):
        st.info(T("Finish the Post-Test first. The retention test comes about two weeks later."))
        return
    if not my_class()["retention_open"] and not storage.test_score(pid, "retention"):
        st.info(T("The retention test isn't open yet. Your teacher will open it about two weeks after the post-test."))
        return
    run_test("retention", content.RETENTION_TEST)


# ============================================================= ARENA
def start_mission(difficulty, source):
    pid = ss.player["id"]
    df = storage.player_attempts(pid)
    seen = set(df.loc[df["mode"] == "train", "scenario_id"]) if not df.empty else set()
    weak = engine.weak_tactics(df)
    bank = engine.build_mission(difficulty, seen, seed=random.randint(0, 10**9), weak=weak)
    rounds = [None] * engine.MISSION_LENGTH if source == "ai" else bank
    ss.mission = {"difficulty": difficulty, "source": source, "rounds": rounds, "bank": bank,
                  "idx": 0, "results": [], "id": random.randint(0, 10**9)}
    ss.round_result = None


def next_round():
    ss.mission["idx"] += 1
    ss.round_result = None


def end_mission():
    ss.mission = None
    ss.round_result = None


def page_arena():
    st.title(T(P_ARENA))
    if not need_player() or blocked_for_control():
        return
    pid = ss.player["id"]
    m = ss.mission

    # ---------------- mission setup
    if m is None:
        if not storage.test_score(pid, "pre"):
            st.warning(T("Tip: take the Pre-Test first so you can prove your improvement later."))
        st.write(T("Each mission has **{n} messages**. Decide *Scam* or *Legit*, then tick the details that are real red flags. Careful: some details are **decoys**.", n=engine.MISSION_LENGTH))
        a, b = st.columns(2)
        labels = {"Mixed": "🎲 Mixed (all levels)", "Easy": "🟢 Easy", "Medium": "🟡 Medium", "Hard": "🟠 Hard",
                  "Expert": "🔴 Expert (complex + voice calls, ×1.5 XP)", "Smart": "🎯 Smart: target my weak spots"}
        diff = a.selectbox(T("Difficulty"), list(labels), format_func=TT(labels.get), index=4)
        has_key = bool(api_key())
        src = b.radio(T("Scenario source"), ["Scenario bank (offline)", "Live AI scenarios"], index=0,
                      horizontal=True, disabled=not has_key, format_func=TT(),
                      help=None if has_key else T("Add an API key in the sidebar to unlock live AI scenarios."))
        st.button(T("Start mission ▶"), type="primary",
                  on_click=start_mission, args=(diff, "ai" if src.startswith("Live") else "bank"))
        st.write("")
        st.markdown(T("**Scoring:** correct verdict +50 · each red flag spotted +10 · each false alarm −5 · perfect round +20 · *Calm Mind* (trusting a real message) +20 · Hard ×1.2 · Expert ×1.5"))
        st.caption(T("🎧 Expert includes real-sounding voice calls in Malay, English and Mandarin. Turn your sound on."))
        return

    # ---------------- mission complete
    if m["idx"] >= len(m["rounds"]):
        res = m["results"]
        total = sum(r["xp"] for r in res)
        correct = sum(r["verdict_ok"] for r in res)
        st.markdown(T("## 🏁 Mission complete! +{xp} XP", xp=total))
        a, b, c = st.columns(3)
        a.metric(T("Correct verdicts"), f"{correct}/{len(res)}")
        b.metric(T("Perfect rounds"), sum(r["perfect"] for r in res))
        c.metric(T("Total XP"), player_xp(pid))
        x, y, z = st.columns(3)
        x.button(T("Play another mission"), on_click=end_mission, type="primary")
        post_done = storage.test_score(pid, "post")
        if not post_done:
            y.button(T("Take the Post-Test →"), on_click=lambda: (end_mission(), go_to(P_POST)))
        z.button(T("See my progress →"), on_click=lambda: (end_mission(), go_to(P_PROGRESS)))
        return

    idx = m["idx"]
    # Lazily create AI rounds; fall back to the bank on any error.
    if m["rounds"][idx] is None:
        with st.spinner(T("🤖 Generating a fresh scenario...")):
            try:
                diff = m["difficulty"] if m["difficulty"] in content.DIFFICULTIES else random.choice(["Hard", "Expert"])
                m["rounds"][idx] = engine.generate_ai_scenario(api_key(), difficulty=diff, language=ss.ai_lang)
            except Exception as e:  # noqa: BLE001 - any failure falls back safely
                st.toast(T("AI unavailable ({err}). Using the scenario bank.", err=type(e).__name__))
                m["rounds"][idx] = m["bank"][idx]
    s = m["rounds"][idx]

    st.progress(idx / len(m["rounds"]), text=T("Round {i} of {n} · {diff}", i=idx + 1, n=len(m["rounds"]),
                                               diff=T(s.get("difficulty", "")))
                + (T(" · 🤖 AI-generated") if str(s["id"]).startswith("AI") else ""))
    left, right = st.columns([1, 1], gap="large")
    with left:
        render_scenario(s)

    with right:
        r = ss.round_result
        if r is None:
            with st.form(f"round_{m['id']}_{idx}"):
                verdict = st.radio(T("**1 · Your verdict**"), ["🚩 Scam", "✅ Legit"], index=None, horizontal=True,
                                   format_func=TT())
                st.markdown(T("**2 · Tick every detail that is a real red flag** (it's OK to tick none)"))
                ticks = [st.checkbox(c["text"], key=f"cue_{m['id']}_{idx}_{i}") for i, c in enumerate(s["cues"])]
                submitted = st.form_submit_button(T("Lock in answer 🔒"), type="primary")
            if submitted:
                if verdict is None:
                    st.warning(T("Choose Scam or Legit first."))
                else:
                    before = engine.level_for(player_xp(pid))[0]
                    answered_scam = verdict.startswith("🚩")
                    sel = {i for i, t in enumerate(ticks) if t}
                    res = engine.score_round(s, answered_scam, sel)
                    storage.record_attempt(pid, "train", s, answered_scam, res["verdict_ok"],
                                           res["hits"], res["false_alarms"], res["missed"], res["xp"])
                    res["level_up"] = engine.level_for(player_xp(pid))[0] if engine.level_for(player_xp(pid))[0] != before else None
                    m["results"].append(res)
                    ss.round_result = res
                    st.rerun()
        else:
            truth = T("a SCAM 🚩" if s["is_scam"] else "LEGIT ✅")
            cls = "good" if r["verdict_ok"] else "bad"
            head = T("Nice catch!" if r["verdict_ok"] and s["is_scam"] else ("Well judged!" if r["verdict_ok"] else "Not quite."))
            tactic = "" if not s["is_scam"] else " · " + T("Tactic:") + " " + esc(T(s["tactic"]))
            st.markdown(f'<div class="verdict {cls}"><b>{head}</b> {T("This message is {truth}", truth=truth)}'
                        f'{tactic}<br><b>+{r["xp"]} XP</b></div>', unsafe_allow_html=True)
            if r.get("level_up"):
                st.balloons()
                st.success(T("🎉 LEVEL UP! You are now a **{lvl}**!", lvl=T(r["level_up"])))
            for i, c in enumerate(s["cues"]):
                is_red, picked = i in r["red"], i in r["selected"]
                if is_red and picked:
                    cls, tag = "ok", T("✅ Red flag, you spotted it")
                elif is_red:
                    cls, tag = "miss", T("⚠️ Red flag you missed")
                elif picked:
                    cls, tag = "fa", T("❌ False alarm, not a red flag")
                else:
                    cls, tag = "neutral", T("👍 Not a red flag, correctly left unticked")
                st.markdown(f'<div class="cue {cls}"><b>{tag}: “{esc(c["text"])}”</b>'
                            f'<span>{esc(c["why"])}</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="lesson">💡 {esc(s["lesson"])}</div>', unsafe_allow_html=True)
            with st.expander(T("XP breakdown")):
                for lbl, params, pts in r["breakdown"] or [("No points this round", {}, 0)]:
                    if "diff" in params:
                        params = dict(params, diff=T(params["diff"]))
                    st.write(f"{T(lbl, **params)}: **{pts:+d}**")
            st.write("")
            last = idx + 1 >= len(m["rounds"])
            st.button(T("Finish mission 🏁" if last else "Next message →"), on_click=next_round, type="primary")
    st.write("")
    st.button(T("Quit mission"), on_click=end_mission)



# ============================================================= STORY MISSIONS
ENDING_STYLE = {"safe": ("safe", "Escaped"), "close": ("close", "Close call"), "lost": ("lost", "Scammed")}


def start_story(story_id):
    ss.story = {"id": story_id, "node": content.get_story(story_id)["start"], "path": [], "done": False}


def leave_story():
    ss.story = None


def choose(ci):
    st_ = ss.story
    story = content.get_story(st_["id"])
    node_id = st_["node"]
    choice = story["nodes"][node_id]["choices"][ci]
    st_["path"].append((node_id, ci))
    st_["node"] = choice["next"]
    nxt = story["nodes"][choice["next"]]
    if "ending" in nxt and not st_["done"]:
        summ = engine.story_path_summary(story, st_["path"])
        loss = summ["loss"] if nxt["ending"] == "lost" else min(summ["loss"], 500)
        st_["done"] = True
        st_["loss"] = loss
        storage.record_story(ss.player["id"], story, choice["next"], nxt["ending"], loss, summ["score"],
                             nxt["xp"], st_["path"])


def story_card(story, best):
    status = T({"safe": "🛡️ Escaped", "close": "😮‍💨 Close call", "lost": "💸 Scammed"}.get(best, "Not played yet"))
    return (f'<div class="card" style="margin-bottom:10px"><h4>{story["icon"]} {esc(story["title"])}</h4>'
            f'<p>{esc(story["subtitle"])}</p><p style="margin-top:8px"><b>{T("Tactic:")}</b> {esc(T(story["tactic"]))} · '
            f'<b>{T("Your best:")}</b> {status}</p></div>')


def page_story():
    st.title(T(P_STORY))
    if not need_player() or blocked_for_control():
        return
    pid = ss.player["id"]
    cur = ss.get("story")

    if not cur:
        st.write(T("Real scams aren't one message. They're **conversations that escalate**: hand-offs, threats, fake proof, small wins that build trust. In Story Missions every decision changes what happens next, and **there's no feedback until the end**, just like real life. Turn your sound on 🎧."))
        runs = storage.story_runs(pid)
        rank = {"safe": 3, "close": 2, "lost": 1}
        cols = st.columns(2)
        for i, story in enumerate(content.STORIES):
            mine = runs[runs["story_id"] == story["id"]] if not runs.empty else pd.DataFrame()
            best = None if mine.empty else max(mine["ending"], key=lambda e: rank[e])
            with cols[i % 2]:
                st.markdown(story_card(story, best), unsafe_allow_html=True)
                st.button(T("▶ Play: {title}", title=story["title"]), key=f"play_{story['id']}", on_click=start_story,
                          args=(story["id"],), type="primary" if best is None else "secondary")
        return

    story = content.get_story(cur["id"])
    node = story["nodes"][cur["node"]]

    # ---------------- ending + debrief
    if "ending" in node:
        cls, _ = ENDING_STYLE[node["ending"]]
        loss = cur.get("loss", 0)
        money = f"{T('Money lost:')} <b>RM{loss:,}</b>" if loss else f"{T('Money lost:')} <b>RM0</b> ✨"
        st.markdown(f'<div class="ending {cls}"><h3>{esc(node["title"])}</h3>{esc(node["text"])}'
                    f'<br><br>{money} · <b>+{node["xp"]} XP</b></div>', unsafe_allow_html=True)
        if node["ending"] == "safe":
            st.balloons()
        st.subheader(T("🔍 Debrief: your decisions"))
        for k, (nid, ci) in enumerate(cur["path"], 1):
            n = story["nodes"][nid]
            ch = n["choices"][ci]
            best_ch = max(n["choices"], key=lambda c: c.get("score", 0))
            cls = "good" if ch.get("score", 0) >= 2 else ("meh" if ch.get("score", 0) >= 0 else "bad")
            mark = {"good": "✅", "meh": "⚠️", "bad": "❌"}[cls]
            better = "" if best_ch is ch or ch.get("score", 0) >= best_ch.get("score", 0) else \
                f'<br><small>{T("💡 Best move here:")} “{esc(best_ch["text"])}”</small>'
            st.markdown(f'<div class="step {cls}"><b>{mark} {T("Step {k}", k=k)} · {esc(n.get("sender", ""))}</b><br>'
                        f'{T("You chose:")} “{esc(ch["text"])}”<br><small>{esc(ch.get("note", ""))}</small>{better}</div>',
                        unsafe_allow_html=True)
        debrief = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", esc(story["debrief"]))
        st.markdown(f'<div class="lesson">🧠 {debrief}</div>', unsafe_allow_html=True)
        st.write("")
        a, b = st.columns(2)
        a.button(T("🔁 Replay this mission"), on_click=start_story, args=(story["id"],), type="primary")
        b.button(T("← All Story Missions"), on_click=leave_story)
        return

    # ---------------- playing a node
    sent = engine.story_path_summary(story, cur["path"])["loss"]
    head = T("Step {k} · 💰 Your money at stake: RM{save} · Sent to strangers so far: <b>RM{sent}</b>",
             k=len(cur["path"]) + 1, save=f"{story['savings']:,}", sent=f"{sent:,}")
    st.markdown(f'<div class="story-head">{story["icon"]} <b>{esc(story["title"])}</b> · {head}</div>',
                unsafe_allow_html=True)
    if not cur["path"]:
        st.info(f"📖 {story['intro']}")
    left, right = st.columns([1, 1], gap="large")
    with left:
        render_scenario(node)
    with right:
        st.markdown(T("#### What do you do?"))
        for ci, ch in enumerate(node["choices"]):
            st.button(ch["text"], key=f"ch_{story['id']}_{cur['node']}_{len(cur['path'])}_{ci}",
                      on_click=choose, args=(ci,), width="stretch")
        st.caption(T("No hints. Decide like you would in real life."))
    st.write("")
    st.button(T("Leave mission"), on_click=leave_story)



# ============================================================= CO-OP SIMULATION
def coop_map(m, room, role, now):
    """Bandar Harmoni town map with players, investigations and danger zones."""
    C = coop_content
    st_ = room["state"]
    fig = go.Figure()
    for x0, y0, x1, y1, col, lab in C.DISTRICTS:
        fig.add_shape(type="rect", x0=x0, y0=y0, x1=x1, y1=y1, fillcolor=col, line_width=0, layer="below")
        fig.add_annotation(x=x0 + 1.5, y=y1 - 2.5, text=T(lab), showarrow=False, xanchor="left",
                           font=dict(size=10, color="#64748B"))
    for (x0, y0), (x1, y1) in C.ROADS:
        fig.add_shape(type="line", x0=x0, y0=y0, x1=x1, y1=y1, line=dict(color="#CBD5E1", width=9), layer="below")
        fig.add_shape(type="line", x0=x0, y0=y0, x1=x1, y1=y1, line=dict(color="#FFFFFF", width=5), layer="below")
    fig.add_trace(go.Scatter(x=[p[0] for p in C.RIVER], y=[p[1] for p in C.RIVER], mode="lines",
                             line=dict(color="#7DD3FC", width=7, shape="spline"), hoverinfo="skip"))
    # danger zones revealed by investigations
    for poi_id, at in st_.get("danger", []):
        if at <= now:
            p = C.POIS[poi_id]
            fig.add_shape(type="circle", x0=p["x"] - 10, y0=p["y"] - 10, x1=p["x"] + 10, y1=p["y"] + 10,
                          fillcolor="rgba(220,38,38,0.18)", line=dict(color=RED, width=2, dash="dot"))
    # investigation status rings
    for t in m["guardian_tools"]:
        if t.get("poi") and t["id"] in st_["ready"]:
            p = C.POIS[t["poi"]]
            done = st_["ready"][t["id"]] <= now
            fig.add_trace(go.Scatter(x=[p["x"]], y=[p["y"]], mode="markers", hoverinfo="skip",
                                     marker=dict(size=44, color="rgba(22,163,74,0.25)" if done else "rgba(245,158,11,0.35)",
                                                 line=dict(width=3, color=GREEN if done else AMBER))))
    # places: icon + small name tag under key places
    for pid, p in C.POIS.items():
        key = pid in m["pois"]
        fig.add_trace(go.Scatter(x=[p["x"]], y=[p["y"]], mode="text", text=[p["icon"]], cliponaxis=False,
                                 textfont=dict(size=24 if key else 15, color="#0F172A" if key else "rgba(15,23,42,0.4)"),
                                 hoverinfo="skip"))
        if key:
            anchor = "left" if p["x"] < 18 else ("right" if p["x"] > 85 else "center")
            fig.add_annotation(x=p["x"], y=p["y"] - 5.5, text=f"<b>{esc(T(p['name']))}</b>", showarrow=False,
                               xanchor=anchor, font=dict(size=10.5, color="#0F172A"),
                               bgcolor="rgba(255,255,255,0.85)", borderpad=2)
    # players
    pos = m["pos"]
    tp, gp = C.POIS[pos["target"]], C.POIS[pos["guardian"]]
    tx, ty = tp["x"], tp["y"]
    doom = st_.get("doom")
    if doom and doom.get("from"):
        f = min(1.0, max(0.0, (now - doom["start"]) / (doom["at"] - doom["start"])))
        a, b = C.POIS[doom["from"]], C.POIS[doom["to"]]
        tx, ty = a["x"] + (b["x"] - a["x"]) * f, a["y"] + (b["y"] - a["y"]) * f
    elif room["status"] == "ended" and st_.get("ending") == "danger":
        tx, ty = C.POIS["backlot"]["x"], C.POIS["backlot"]["y"]
    n = coop.names(room)
    fig.add_trace(go.Scatter(x=[tx - 6], y=[ty + 6], mode="text", text=[f"📱<b>{esc(n['T'])}</b>"], cliponaxis=False,
                             textfont=dict(size=13, color=RED), hoverinfo="skip"))
    if n["G"] != n["T"]:
        fig.add_trace(go.Scatter(x=[gp["x"] + 7], y=[gp["y"] + 6], mode="text", text=[f"🛡️<b>{esc(n['G'])}</b>"],
                                 cliponaxis=False, textfont=dict(size=13, color=TEAL_DARK), hoverinfo="skip"))
    fig.update_layout(xaxis=dict(range=[0, 100], visible=False), yaxis=dict(range=[0, 100], visible=False),
                      height=430, margin=dict(l=0, r=0, t=0, b=0), showlegend=False, plot_bgcolor="#F8FAFC",
                      paper_bgcolor="#F8FAFC")
    return fig


def feed_html(events, newest_first=True):
    evs = list(reversed(events)) if newest_first else events
    rows = []
    for e in evs[:40]:
        who = f"<b>{esc(e['actor'])}:</b> " if e["kind"] == "chat" and e.get("actor") else ""
        rows.append(f'<div class="{e["kind"]}">{who}{esc(e["text"])}</div>')
    return '<div class="feed">' + "".join(rows) + "</div>" if rows else f"<i>{T('Nothing yet...')}</i>"


def coop_do(aid):
    role = ss.get("coop_role")
    msg = coop.act(ss.room, ss.player, role, aid)
    if msg:
        ss.coop_msg = msg


def coop_radio(text):
    coop.chat(ss.room, ss.player["nickname"], text)


def coop_leave():
    if ss.room and ss.player:
        coop.leave_room(ss.room, ss.player["id"])
    ss.room = None
    if "room" in st.query_params:
        del st.query_params["room"]


def coop_create(mid):
    ss.room = coop.create_room(ss.player, mid)


def coop_join(code):
    ok_, res = coop.join_room(code, ss.player)
    if ok_:
        ss.room = res
    else:
        ss.coop_msg = res


def page_coop():
    st.title(T(P_COOP))
    if not need_player() or blocked_for_control():
        return
    if ss.room:
        st.query_params["room"] = ss.room
        coop_room()
        return
    st.write(T("Play **together** on the same room code. One player is the **📱 Target**, who gets the scam call, chat or visitor and feels the pressure. The others are **🛡️ Guardians** beside them, who investigate on the town map. You only win if the Target makes the safe move **and** a Guardian confirms or reports it before time runs out."))
    cards = [("1 · Create or join", "One player creates a room and shares the 5-letter code or link. Friends join from their own phones."),
             ("2 · Talk and investigate", "Only the Target hears the scammer, unless they switch to speaker. Only Guardians can investigate. You need each other."),
             ("3 · Beat the clock", "The scammer escalates every few seconds. Time out = the scammer wins.")]
    for col, (h, b_) in zip(st.columns(3), cards):
        col.markdown(f'<div class="card"><h4>{T(h)}</h4><p>{esc(T(b_))}</p></div>', unsafe_allow_html=True)
    st.write("")
    if ss.get("coop_msg"):
        st.warning(T(ss.pop("coop_msg")))
    left, right = st.columns(2)
    with left:
        st.subheader(T("Create a room"))
        ms = coop.missions()
        mid = st.selectbox(T("Mission"), [m["id"] for m in ms],
                           format_func=lambda i: f'{coop_content.get_mission(i)["icon"]} {coop_content.get_mission(i)["title"]}')
        m = coop_content.get_mission(mid)
        st.caption(f'{m["summary"]} · ⏱️ {m["duration"]}s · {T(m["tactic"])}')
        st.button(T("Create room ➕"), type="primary", on_click=coop_create, args=(mid,))
    with right:
        st.subheader(T("Join a room"))
        code = st.text_input(T("Room code"), value=st.query_params.get("room", ""), max_chars=5,
                             placeholder="K7Q2M").upper()
        st.button(T("Join ▶"), on_click=coop_join, args=(code,), disabled=len(code) != 5)
        st.caption(T("Playing alone? Create a room and start it. You'll play both roles (solo practice)."))
    st.write("")
    with st.expander(T("📶 How do my friends join from their phones?")):
        st.markdown(T("- **Same Wi-Fi:** open the app using the **Network URL** shown in the black window (e.g. `http://192.168.1.20:8501`), not `localhost`. Then share the room link.\n- **Anywhere:** deploy the app online (see README) and share the link.\n- Everyone must connect to the **same running app**."))


@st.fragment(run_every=1.5)
def coop_room():
    code, me_id = ss.room, ss.player["id"]
    room = coop.get_room(code)
    if not room:
        ss.room = None
        st.rerun()
    me = next((p for p in room["players"] if p["player_id"] == me_id), None)
    if me is None:
        if room["status"] != "playing":
            coop.join_room(code, ss.player)
            st.rerun(scope="fragment")
        st.error(T("This game started without you. Wait for the host to return to the lobby."))
        st.button(T("Leave room"), on_click=coop_leave)
        return
    coop.heartbeat(code, me_id)
    if ss.get("coop_msg"):
        st.toast(T(ss.pop("coop_msg")))
    if room["status"] == "playing":
        coop.tick(code)
        room = coop.get_room(code)
    if room["status"] == "lobby":
        coop_lobby(room, me)
    elif room["status"] == "playing":
        coop_game(room, me)
    else:
        coop_end(room, me)


def coop_lobby(room, me):
    m = coop_content.get_mission(room["mission_id"])
    is_host = room["host_id"] == me["player_id"]
    a, b = st.columns([1, 1.4])
    with a:
        st.markdown(f'<div class="roomcode">{room["code"]}</div>', unsafe_allow_html=True)
        try:
            base = (st.context.url or "").split("?")[0]
        except Exception:  # noqa: BLE001
            base = ""
        base = base or "http://<your-app-address>"
        st.caption(T("Share this link (or just the code):"))
        st.code(f"{base}?room={room['code']}", language=None)
        st.markdown(T("**Players in the room**"))
        st.markdown("".join(f'<span class="pl">{"🟢" if p["online"] else "⚪"} {esc(p["nickname"])}'
                            f'{" 👑" if p["player_id"] == room["host_id"] else ""}</span>' for p in room["players"]),
                    unsafe_allow_html=True)
    with b:
        st.markdown(f'<div class="card"><h4>{m["icon"]} {esc(m["title"])}</h4><p>{esc(m["summary"])}</p>'
                    f'<p style="margin-top:6px"><b>{T("Tactic:")}</b> {esc(T(m["tactic"]))} · <b>{T("Timer:")}</b> {m["duration"]}s</p></div>',
                    unsafe_allow_html=True)
        st.write("")
        if is_host:
            ids = [x["id"] for x in coop.missions()]
            st.selectbox(T("Change mission"), ids, index=ids.index(m["id"]), key="coop_mid",
                         format_func=lambda i: f'{coop_content.get_mission(i)["icon"]} {coop_content.get_mission(i)["title"]}',
                         on_change=lambda: coop.set_mission(room["code"], ss.coop_mid))
            players = room["players"]
            if len(players) > 1:
                pids = [p["player_id"] for p in players]
                cur = room["target_id"] if room["target_id"] in pids else pids[0]
                st.selectbox(T("📱 Who gets the scam (the Target)?"), pids, index=pids.index(cur), key="coop_tgt",
                             format_func=lambda i: next(p["nickname"] for p in players if p["player_id"] == i),
                             on_change=lambda: coop.set_target(room["code"], ss.coop_tgt))
                st.caption(T("Everyone else becomes a 🛡️ Guardian."))
                label = T("▶ Start mission")
            else:
                st.info(T("Waiting for friends... or start now to play **both roles** (solo practice)."))
                label = T("▶ Start solo practice")
            st.button(label, type="primary", on_click=coop.start_game, args=(room["code"],))
        else:
            st.info(T("⏳ Waiting for the host 👑 to start the mission..."))
    st.button(T("Leave room"), on_click=coop_leave)


def coop_game(room, me):
    m = coop_content.get_mission(room["mission_id"])
    role = me["role"] or "guardian"
    ss.coop_role = role
    now = time.time()
    st_ = room["state"]
    left_s = max(0, int(room["deadline"] - now))
    n = coop.names(room)
    stake = " · " + T("💰 At stake: RM{amt}", amt=f"{m['stake']:,}") if m["stake"] else ""
    st.markdown(f'<div class="hud"><div>{m["icon"]} <b>{esc(m["title"])}</b><br>'
                f'<small>{T("Room")} {room["code"]}{stake}</small></div>'
                f'<span class="rb">{T(coop_content.ROLE_LABEL[role])}</span>'
                f'<div class="t {"hot" if left_s <= 30 else ""}">⏱️ {left_s // 60}:{left_s % 60:02d}</div></div>',
                unsafe_allow_html=True)
    if st_.get("doom"):
        secs = max(0, int(st_["doom"]["at"] - now))
        doom_txt = T("🚨 {name} is walking to the {place} ALONE: arriving in {secs}s! Stop them!", name=n["T"],
                     place=T(coop_content.POIS[st_["doom"]["to"]]["name"]), secs=secs)
        st.markdown(f'<div class="doom">{esc(doom_txt)}</div>', unsafe_allow_html=True)
    if role == "both":
        view = st.radio("View", ["📱 Target phone", "🛡️ Guardian tools"], horizontal=True, key="solo_view",
                        label_visibility="collapsed", format_func=TT())
        show = "target" if view.startswith("📱") else "guardian"
    else:
        show = role
    events = coop.visible_events(room, role, now)
    incoming = dict(m["incoming"], message=coop.incoming_message(m))

    if show == "target":
        st.caption("📖 " + coop.fmt(m["brief"], room) + " " + coop.fmt(m["brief_target"], room))
        l, r = st.columns([1, 1.05], gap="large")
        with l:
            render_scenario(incoming)
        with r:
            st.markdown(T("**📨 Live feed**"))
            with st.container(height=260):
                st.markdown(feed_html(events), unsafe_allow_html=True)
            st.markdown(T("**Your moves**"))
            for a in m["target_actions"]:
                done = a["id"] in st_["done"]
                disabled = (done and a["kind"] != "cancel_doom") or (a["kind"] == "cancel_doom" and not st_.get("doom")) \
                    or (a["kind"] == "doom" and bool(st_.get("doom")))
                st.button(coop.fmt(a["label"], room) + (" ✓" if done and a["kind"] not in ("cancel_doom",) else ""),
                          key=f"act_{a['id']}", on_click=coop_do, args=(a["id"],), disabled=disabled, width="stretch")
    else:
        st.caption("📖 " + coop.fmt(m["brief"], room) + " " + coop.fmt(m["brief_guardian"], room))
        l, r = st.columns([1.15, 1], gap="large")
        with l:
            st.plotly_chart(coop_map(m, room, role, now), config={"displayModeBar": False, "staticPlot": True},
                            key="coop_map")
            if st_["speaker"] or role == "both":
                with st.expander(T("🔊 The call (on speaker)" if role != "both" else "🔊 The call"), expanded=False):
                    render_scenario(incoming)
            else:
                st.caption(T("🔇 You can't hear {name}'s call. Ask {name} to put it on speaker.", name=n["T"]))
        with r:
            st.markdown(T("**🔍 Investigate**"))
            pend = coop.pending_tools(room, now)
            for t in m["guardian_tools"]:
                poi = coop_content.POIS.get(t.get("poi"), None)
                label = coop.fmt(t["label"], room)
                if poi:
                    label = f'{poi["icon"]} {label} ({T(poi["name"])})'
                if t["id"] in pend:
                    label = f"⏳ {label} ... {int(pend[t['id']]) + 1}s"
                elif t["id"] in st_["done"]:
                    label += " ✓"
                st.button(label, key=f"act_{t['id']}", on_click=coop_do, args=(t["id"],),
                          disabled=t["id"] in st_["done"], width="stretch")
            st.markdown(T("**📓 Notebook & feed**"))
            with st.container(height=230):
                st.markdown(feed_html(events), unsafe_allow_html=True)
    if show == "target":
        with st.expander(T("🗺️ Map of Bandar Harmoni")):
            st.plotly_chart(coop_map(m, room, role, now), config={"displayModeBar": False, "staticPlot": True},
                            key="coop_map_t")
    # team radio
    st.markdown(T("**📻 Team radio**"))
    qs = [T(q) for q in ["🚨 HANG UP / STOP!", "⏳ Stall them!", "🔊 Put it on speaker!", "❓ What are they asking?",
                         "✅ Confirmed: it's a SCAM", "👍 OK"]]
    cols = st.columns(len(qs))
    for i, q in enumerate(qs):
        cols[i].button(q, key=f"radio_{i}", on_click=coop_radio, args=(q,), width="stretch")
    with st.form("radio_form", clear_on_submit=True, border=False):
        c1, c2 = st.columns([5, 1])
        txt = c1.text_input(T("Message"), label_visibility="collapsed", placeholder=T("Type a message to your team..."))
        if c2.form_submit_button(T("Send"), width="stretch") and txt:
            coop_radio(txt)


def coop_end(room, me):
    m = coop_content.get_mission(room["mission_id"])
    st_ = room["state"]
    got = coop.claim_reward(room["code"], me["player_id"])
    ending = m["endings"].get(st_["ending"], m["endings"].get("lost"))
    cls = {"win": "safe", "close": "close", "lost": "lost"}[st_["outcome"]]
    used = int(st_["ended_at"] - room["started_at"])
    stars = 3 if st_["score"] >= 200 else (2 if st_["score"] >= 140 else (1 if st_["outcome"] == "win" else 0))
    lost_amt = (m["stake"] if st_["outcome"] == "lost" else 0) + st_["loss"]
    loss = f" · {T('Money lost:')} RM{lost_amt:,}" if lost_amt else ""
    st.markdown(f'<div class="ending {cls}"><h3>{esc(coop.fmt(ending["title"], room))}</h3>{esc(coop.fmt(ending["text"], room))}'
                f'<br><br><b>{T("Team score:")} {st_["score"]}</b> {"⭐" * stars} · {T("Time used:")} {used}s{loss}</div>',
                unsafe_allow_html=True)
    shown = ss.pop("coop_reward", None)
    if shown:
        st.toast(T("+{xp} XP for you!", xp=shown[0]))
        if shown[1] == "win":
            st.balloons()
    a, b = st.columns([1.2, 1])
    with a:
        debrief = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", esc(m["debrief"]))
        st.markdown(f'<div class="lesson">🧠 {debrief}</div>', unsafe_allow_html=True)
        st.write("")
        win_txt = []
        for group in m["win"]:
            labels = [coop.fmt(x["label"], room) for x in m["target_actions"] + m["guardian_tools"] if x["id"] in group]
            win_txt.append(f" {T('OR')} ".join(f"“{l_}”" for l_ in labels))
        st.markdown(T("**🏆 Winning combination:**") + " " + f"  **{T('AND')}**  ".join(win_txt))
    with b:
        st.markdown(T("**🎞️ Full replay (everyone's view)**"))
        with st.container(height=320):
            st.markdown(feed_html(coop.visible_events(room, "both", st_["ended_at"] + 1), newest_first=False),
                        unsafe_allow_html=True)
    if room["host_id"] == me["player_id"]:
        st.button(T("🔁 Back to lobby (next mission)"), type="primary", on_click=coop.back_to_lobby, args=(room["code"],))
    else:
        st.caption(T("The host 👑 can take everyone back to the lobby."))
    st.button(T("Leave room"), on_click=coop_leave)
    if got:
        ss.coop_reward = got
        st.rerun(scope="app")


# ============================================================= PROGRESS
def page_progress():
    st.title(T(P_PROGRESS))
    if not need_player():
        return
    pid = ss.player["id"]
    df = storage.player_attempts(pid)
    pre, post = storage.test_score(pid, "pre"), storage.test_score(pid, "post")
    xp = int(df["xp"].sum()) if not df.empty else 0
    name, icon, floor, nxt, nxt_name = engine.level_for(xp)
    tr = df[df["mode"] == "train"] if not df.empty else pd.DataFrame()

    a, b, c, d = st.columns([1.7, 1, 1, 1])
    a.metric(T("Level"), f"{icon} {T(name)}")
    b.metric(T("Total XP"), xp)
    c.metric(T("Training rounds"), len(tr))
    d.metric(T("Arena accuracy"), f"{round(100 * tr['correct'].mean())}%" if len(tr) else "–")
    if nxt:
        st.progress((xp - floor) / (nxt - floor), text=T("{n} XP to {lvl}", n=nxt - xp, lvl=T(nxt_name)))

    st.subheader(T("Badges"))
    got = engine.earned_badges(df, pre, post)
    tiles = "".join(f'<div class="badge {"" if k in got else "locked"}"><div class="ic">{ic}</div>'
                    f'<div class="nm">{T(nm)}</div><div class="ds">{T(ds)}</div></div>'
                    for k, (ic, nm, ds) in engine.BADGES.items())
    st.markdown(tiles, unsafe_allow_html=True)

    left, right = st.columns(2)
    with left:
        st.subheader(T("Pre vs Post test"))
        if pre:
            vals = [100 * pre[0] / pre[1], 100 * post[0] / post[1] if post else None]
            fig = go.Figure(go.Bar(x=[T("Pre-Test"), T("Post-Test")], y=[v or 0 for v in vals],
                                   marker_color=["#94A3B8", TEAL],
                                   text=[f"{v:.0f}%" if v is not None else T("not yet") for v in vals],
                                   textposition="outside"))
            fig.update_layout(yaxis=dict(range=[0, 110], title=T("Score (%)")), height=320,
                              margin=dict(t=10, b=10, l=10, r=10), template="plotly_white")
            st.plotly_chart(fig)
        else:
            st.info(T("Take the Pre-Test to see this chart."))
    with right:
        st.subheader(T("Accuracy by scam tactic"))
        if len(tr):
            g = tr.groupby("tactic")["correct"].agg(["mean", "count"]).reset_index()
            g["Accuracy (%)"] = (100 * g["mean"]).round()
            g["Tactic"] = g["tactic"].map(T)
            g = g.sort_values("Accuracy (%)")
            fig = px.bar(g, x="Accuracy (%)", y="Tactic", orientation="h", text="Accuracy (%)",
                         color="Accuracy (%)", color_continuous_scale=[[0, RED], [0.5, AMBER], [1, GREEN]],
                         range_color=[0, 100], hover_data={"count": True})
            fig.update_layout(height=320, margin=dict(t=10, b=10, l=10, r=10), yaxis_title=None,
                              coloraxis_showscale=False, template="plotly_white", xaxis_range=[0, 110],
                              xaxis_title=T("Accuracy (%)"))
            st.plotly_chart(fig)
            weakest = g.iloc[0]
            if weakest["Accuracy (%)"] < 100:
                st.caption(T("🎯 Focus area: **{t}** ({p}% correct)", t=weakest["Tactic"], p=f"{weakest['Accuracy (%)']:.0f}"))
        else:
            st.info(T("Play a mission to see your strengths and weak spots."))

    left, right = st.columns(2)
    with left:
        st.subheader(T(P_STORY))
        runs = storage.story_runs(pid)
        rows = []
        for story in content.STORIES:
            mine = runs[runs["story_id"] == story["id"]] if not runs.empty else pd.DataFrame()
            if mine.empty:
                rows.append({T("Mission"): f'{story["icon"]} {story["title"]}', T("First try"): "–", T("Best"): "–",
                             T("Plays"): 0})
            else:
                lab = {k: T(v) for k, v in {"safe": "🛡️ Escaped", "close": "😮‍💨 Close call", "lost": "💸 Scammed"}.items()}
                best = max(mine["ending"], key=lambda e: {"safe": 3, "close": 2, "lost": 1}[e])
                rows.append({T("Mission"): f'{story["icon"]} {story["title"]}', T("First try"): lab[mine.iloc[0]["ending"]],
                             T("Best"): lab[best], T("Plays"): len(mine)})
        st.dataframe(pd.DataFrame(rows), hide_index=True)
        co = df[df["mode"] == "coop"] if not df.empty else pd.DataFrame()
        if len(co):
            st.caption(T("🗺️ Co-op Simulations: **{n}** played · **{w}** won · best team score **{b}**",
                         n=len(co), w=int(co['correct'].sum()), b=int(co['xp'].max())))
    with right:
        st.subheader(T("🎯 Confidence check"))
        t = df[df["mode"].isin(["pre", "post"]) & df["confidence"].notna()] if not df.empty and "confidence" in df else pd.DataFrame()
        if len(t):
            certain = t[t["confidence"] == 3]
            if len(certain):
                st.metric(T("When you were 😎 Certain, you were right"), f"{100 * certain['correct'].mean():.0f}%",
                          help=T("{n} 'Certain' answers", n=len(certain)))
                wrong_certain = int((certain["correct"] == 0).sum())
                if wrong_certain:
                    st.warning(T("⚠️ {n} answer(s) were wrong while you felt certain. Overconfidence is exactly what scammers exploit. Slow down on those tactics.", n=wrong_certain))
                else:
                    st.success(T("No overconfident mistakes. Your confidence matches your skill."))
            g = t.groupby("confidence")["correct"].agg(["mean", "count"]).reset_index()
            g["Confidence"] = g["confidence"].map(lambda c: T(CONFIDENCE[int(c) - 1]))
            st.dataframe(g.assign(**{"Accuracy": (100 * g["mean"]).round().astype(int).astype(str) + "%"})
                         [["Confidence", "Accuracy", "count"]].rename(
                             columns={"Confidence": T("Confidence"), "Accuracy": T("Accuracy"), "count": T("Answers")}),
                         hide_index=True)
        else:
            st.info(T("Take a test to see how well your confidence matches your accuracy."))


# ============================================================= TEACHER: PILOT
def pilot_panels():
    with st.expander(T("🧪 Pilot setup: groups, consent and retention test")):
        st.caption(T("Set each class code as the KEBAL group (plays the game) or the Control group (tests only)."))
        known = sorted({c["code"] for c in storage.all_class_settings()}
                       | set(storage.all_players()["school"].dropna().unique() if not storage.all_players().empty else []))
        known = [k for k in known if k]
        new = st.text_input(T("Add a class code"), placeholder="UMPSA-K").strip().upper()
        codes = known + ([new] if new and new not in known else [])
        if not codes:
            st.info(T("Type a class code above to configure it."))
        for code in codes:
            cs = storage.class_settings(code)
            a, b, c, d = st.columns([1.3, 1.4, 1.2, 1.2], vertical_alignment="bottom")
            a.markdown(f"**{esc(code)}**")
            grp = b.selectbox(T("Group"), ["kebal", "control"], index=0 if cs["grp"] == "kebal" else 1, key=f"grp_{code}",
                              format_func=TT({"kebal": "KEBAL group", "control": "Control group"}.get))
            cons = c.checkbox(T("Ask for research consent"), value=bool(cs["consent_required"]), key=f"cons_{code}")
            ret = d.checkbox(T("Retention test open"), value=bool(cs["retention_open"]), key=f"ret_{code}")
            if (grp, int(cons), int(ret)) != (cs["grp"], cs["consent_required"], cs["retention_open"]):
                storage.save_class_settings(code, grp, ret, cons)
                st.toast(T("Saved {code}", code=code))

    with st.expander(T("📈 Pilot results: KEBAL group vs control group"), expanded=True):
        res = pilot_stats.summarise(storage.all_attempts(), storage.all_class_settings(), storage.all_surveys())
        if not res or not res["kebal"]["n_paired"] and not res["control"]["n_paired"]:
            st.info(T("Results appear once students in configured classes finish both the pre-test and the post-test."))
        else:
            k, c = res["kebal"], res["control"]
            f = lambda v, suf="%": "–" if v != v else f"{v:.0f}{suf}"  # noqa: E731 - v != v is NaN
            rows = [
                (T("Students with pre + post"), str(k["n_paired"]), str(c["n_paired"])),
                (T("Pre-test mean"), f(k["pre"]), f(c["pre"])),
                (T("Post-test mean"), f(k["post"]), f(c["post"])),
                (T("Mean gain (points)"), f(k["gain"], ""), f(c["gain"], "")),
                (T("Retention test mean (n)"), f"{f(k['retention'])} ({k['n_retention']})", f"{f(c['retention'])} ({c['n_retention']})"),
                (T("Overconfident errors, pre → post"), f"{f(k['oc_pre'])} → {f(k['oc_post'])}", f"{f(c['oc_pre'])} → {f(c['oc_post'])}"),
                (T("SUS usability score (n)"), f"{f(k['sus'], '')} ({k['n_sus']})", "–"),
            ]
            st.dataframe(pd.DataFrame(rows, columns=["", T("KEBAL group"), T("Control group")]), hide_index=True)
            a, b, cc = st.columns(3)
            a.metric(T("Extra gain with KEBAL"), "–" if res["diff"] != res["diff"] else T("{g} pts", g=f"{res['diff']:+.0f}"))
            b.metric(T("Effect size (Cohen's d)"), "–" if res["d"] != res["d"] else f"{res['d']:.2f}")
            cc.metric(T("p-value (permutation test)"), "–" if res["p"] != res["p"] else f"{res['p']:.3f}")
            if res["d"] == res["d"]:
                size = "large" if abs(res["d"]) >= 0.8 else "medium" if abs(res["d"]) >= 0.5 else "small" if abs(res["d"]) >= 0.2 else "negligible"
                st.caption(T("Effect size is {size}. A p-value below 0.05 means the difference is unlikely to be chance.", size=T(size)))
            bars = []
            for g, lab in (("kebal", T("KEBAL group")), ("control", T("Control group"))):
                for m_, ml in (("pre", T("Pre")), ("post", T("Post")), ("retention", T("Retention Test"))):
                    v = res[g][m_]
                    if v == v:
                        bars.append({"group": lab, "test": ml, "score": round(v)})
            if bars:
                fig = px.bar(pd.DataFrame(bars), x="test", y="score", color="group", barmode="group", text="score",
                             color_discrete_sequence=[TEAL, "#94A3B8"], labels={"score": T("Score (%)"), "test": "", "group": ""})
                fig.update_layout(height=320, margin=dict(t=10, b=10, l=10, r=10), template="plotly_white", yaxis_range=[0, 110])
                st.plotly_chart(fig)

    with st.expander(T("💾 Backup & restore")):
        st.caption(T("Free hosting can wipe the app's data when it restarts. Download a backup after every session."))
        st.download_button(T("⬇️ Download full database backup (.db)"), storage.backup_bytes(),
                           file_name=f"kebal_backup_{time.strftime('%Y%m%d_%H%M')}.db", mime="application/octet-stream")
        sv = storage.all_surveys()
        st.download_button(T("⬇️ Download survey answers (CSV)"), sv.to_csv(index=False) if not sv.empty else "",
                           file_name="surveys.csv", mime="text/csv", disabled=sv.empty)
        up = st.file_uploader(T("Restore from a backup file"), type=["db"])
        if up is not None and st.button(T("⚠️ Replace ALL current data with this backup"), type="primary"):
            ok_, msg = storage.restore_from_bytes(up.getvalue())
            (st.success if ok_ else st.error)(T(msg))


# ============================================================= TEACHER
def page_teacher():
    st.title(T("👩‍🏫 Teacher / Pilot Dashboard"))
    pin = st.text_input(T("Teacher PIN"), type="password",
                        help=T("Set the TEACHER_PIN environment variable before a real pilot (default 1234)."))
    if pin != TEACHER_PIN:
        if pin:
            st.error(T("Wrong PIN."))
        return
    if TEACHER_PIN == "1234":
        st.warning(T("You are using the default PIN 1234. Set TEACHER_PIN before a real pilot."))
    pilot_panels()
    df = storage.all_attempts()
    if df.empty:
        st.info(T("No data yet. Ask students to sign in with the same class/school code and play."))
        return
    schools = sorted(df["school"].fillna("").unique().tolist())
    pick = st.selectbox(T("Class / school code"), ["All"] + schools,
                        format_func=TT(lambda x: x or "(no code)"))
    if pick != "All":
        df = df[df["school"] == pick]

    df["player"] = df["nickname"] + " · " + df["school"].fillna("")
    tests = df[df["mode"].isin(["pre", "post"])].groupby(["player", "mode"])["correct"].mean().unstack()
    for col in ("pre", "post"):
        if col not in tests:
            tests[col] = float("nan")
    paired = tests.dropna(subset=["pre", "post"])
    tr = df[df["mode"] == "train"]

    a, b, c, d, e = st.columns(5)
    a.metric(T("Players"), df["player"].nunique())
    b.metric(T("Training rounds"), len(tr))
    c.metric(T("Mean pre-test"), f"{100 * tests['pre'].mean():.0f}%" if tests["pre"].notna().any() else "–")
    d.metric(T("Mean post-test"), f"{100 * tests['post'].mean():.0f}%" if tests["post"].notna().any() else "–")
    if len(paired):
        gain = 100 * (paired["post"] - paired["pre"]).mean()
        e.metric(T("Mean gain (paired)"), T("{g} pts", g=f"{gain:+.0f}"), help=T("{n} players with both tests", n=len(paired)))
        st.caption(T("📈 {p}% of the {n} players who finished both tests improved.",
                     p=f"{100 * (paired['post'] > paired['pre']).mean():.0f}", n=len(paired)))
    else:
        e.metric(T("Mean gain (paired)"), "–")

    left, right = st.columns(2)
    with left:
        st.subheader(T("Pre vs post by player"))
        if len(paired):
            p = (100 * paired).reset_index()
            fig = go.Figure()
            for _, row in p.iterrows():
                fig.add_trace(go.Scatter(x=[row["pre"], row["post"]], y=[row["player"]] * 2, mode="lines",
                                         line=dict(color="#CBD5E1", width=3), showlegend=False))
            fig.add_trace(go.Scatter(x=p["pre"], y=p["player"], mode="markers", name=T("Pre"),
                                     marker=dict(color="#94A3B8", size=12)))
            fig.add_trace(go.Scatter(x=p["post"], y=p["player"], mode="markers", name=T("Post"),
                                     marker=dict(color=TEAL, size=12)))
            fig.update_layout(xaxis=dict(range=[-5, 105], title=T("Score (%)")), template="plotly_white",
                              height=max(260, 34 * len(p) + 80), margin=dict(t=10, b=10, l=10, r=10))
            st.plotly_chart(fig)
        else:
            st.info(T("Shows once players finish both tests."))
    with right:
        st.subheader(T("Cohort accuracy by tactic"))
        if len(tr):
            g = (100 * tr.groupby("tactic")["correct"].mean()).round().sort_values().reset_index()
            g["tactic"] = g["tactic"].map(T)
            fig = px.bar(g, x="correct", y="tactic", orientation="h", text="correct",
                         labels={"correct": T("Accuracy (%)"), "tactic": ""}, color_discrete_sequence=[TEAL])
            fig.update_layout(height=360, margin=dict(t=10, b=10, l=10, r=10), template="plotly_white",
                              xaxis_range=[0, 110])
            st.plotly_chart(fig)
            scams, legit = tr[tr["is_scam"] == 1], tr[tr["is_scam"] == 0]
            st.caption(T("Missed scams: **{a}%** of scam rounds · False alarms on legit messages: **{b}%** of legit rounds",
                         a=f"{100 * (1 - scams['correct'].mean()):.0f}", b=f"{100 * (1 - legit['correct'].mean()):.0f}")
                       if len(scams) and len(legit) else "")
        else:
            st.info(T("No training rounds yet."))

    # ---------- voice vs text, story outcomes, calibration
    st.subheader(T("Deeper insights"))
    x, y = st.columns(2)
    with x:
        st.markdown(T("**🎭 Story Missions: first attempt per player**"))
        runs = storage.story_runs()
        if not runs.empty:
            runs["player"] = runs["nickname"] + " · " + runs["school"].fillna("")
            if pick != "All":
                runs = runs[runs["school"] == pick]
        if not runs.empty:
            first = runs.sort_values("id").groupby(["player", "story_id"]).head(1)
            titles = {s_["id"]: f'{s_["icon"]} {s_["title"]}' for s_ in content.STORIES}
            g = first.groupby(["story_id", "ending"]).size().reset_index(name="players")
            g["Mission"] = g["story_id"].map(titles)
            fig = px.bar(g, x="players", y="Mission", color="ending", orientation="h",
                         labels={"players": T("players"), "Mission": "", "ending": T("ending")},
                         color_discrete_map={"safe": GREEN, "close": AMBER, "lost": RED},
                         category_orders={"ending": ["safe", "close", "lost"]})
            fig.update_layout(height=300, margin=dict(t=10, b=10, l=10, r=10), template="plotly_white",
                              legend_title=None, yaxis_title=None)
            st.plotly_chart(fig)
            esc_rate = 100 * (first["ending"] != "lost").mean()
            st.caption(T("First-try escape rate: **{p}%** · Simulated money lost on first tries: **RM{amt}**",
                         p=f"{esc_rate:.0f}", amt=f"{int(first['loss'].sum()):,}"))
        else:
            st.info(T("No Story Missions played yet."))
    with y:
        st.markdown(T("**🎯 Calibration: accuracy by confidence (tests)**"))
        t = df[df["mode"].isin(["pre", "post"]) & df["confidence"].notna()] if "confidence" in df else pd.DataFrame()
        if len(t):
            g = t.groupby(["mode", "confidence"])["correct"].mean().reset_index()
            g["Accuracy (%)"] = (100 * g["correct"]).round()
            g["Confidence"] = g["confidence"].map(lambda c: T(CONFIDENCE[int(c) - 1]))
            fig = px.bar(g, x="Confidence", y="Accuracy (%)", color="mode", barmode="group", text="Accuracy (%)",
                         color_discrete_map={"pre": "#94A3B8", "post": TEAL},
                         labels={"Confidence": T("Confidence"), "Accuracy (%)": T("Accuracy (%)")},
                         category_orders={"Confidence": [T(c) for c in CONFIDENCE], "mode": ["pre", "post"]})
            fig.update_layout(height=300, margin=dict(t=10, b=10, l=10, r=10), template="plotly_white",
                              yaxis_range=[0, 110], legend_title=None)
            st.plotly_chart(fig)
            oc = {m: t[(t["mode"] == m) & (t["confidence"] == 3)] for m in ("pre", "post")}
            parts = [f"{m}: **{100 * (1 - v['correct'].mean()):.0f}%**" for m, v in oc.items() if len(v)]
            st.caption(T("Overconfident misses (wrong while 'Certain'): ") + " · ".join(parts) if parts else "")
        else:
            st.info(T("Shows once players complete a test."))
    if len(tr):
        voice = tr[tr["channel"].isin(engine.VOICE_CHANNELS)]
        text = tr[~tr["channel"].isin(engine.VOICE_CHANNELS)]
        if len(voice) and len(text):
            st.caption(T("🎧 Voice/video rounds accuracy: **{a}%** vs text rounds: **{b}%**",
                         a=f"{100 * voice['correct'].mean():.0f}", b=f"{100 * text['correct'].mean():.0f}"))
    co = df[df["mode"] == "coop"]
    if len(co):
        g = co.groupby("scenario_id")["correct"].agg(["mean", "count"]).reset_index()
        g["Mission"] = g["scenario_id"].map(lambda i: f'{coop_content.get_mission(i)["icon"]} {coop_content.get_mission(i)["title"]}')
        st.markdown(T("**🗺️ Co-op Simulations: team win rate per mission** (one row per player per game)"))
        st.dataframe(g.assign(**{"Win rate": (100 * g["mean"]).round().astype(int).astype(str) + "%"})
                     [["Mission", "Win rate", "count"]].rename(
                         columns={"Mission": T("Mission"), "Win rate": T("Win rate"), "count": T("Player-games")}),
                     hide_index=True)

    st.subheader(T("Raw data"))
    st.dataframe(df.drop(columns=["player"]), height=260)
    c1, c2 = st.columns(2)
    c1.download_button(T("⬇️ Download all attempts (CSV)"), df.drop(columns=["player"]).to_csv(index=False),
                       file_name="attempts.csv", mime="text/csv")
    sr = storage.story_runs()
    c2.download_button(T("⬇️ Download story decisions (CSV)"), sr.to_csv(index=False) if not sr.empty else "",
                       file_name="story_runs.csv", mime="text/csv", disabled=sr.empty)


# ============================================================= HELP
def page_help():
    st.title(T(P_HELP))
    st.error(T("**Been scammed or just transferred money?** Act fast: call the National Scam Response Centre **(NSRC) at 997** right away, then call your bank."))
    cols = st.columns(3)
    for i, (title, body) in enumerate(content.HELP_STEPS):
        cols[i % 3].markdown(f'<div class="card" style="margin-bottom:12px"><h4>{i + 1}. {T(title)}</h4>'
                             f'<p>{T(body)}</p></div>', unsafe_allow_html=True)
    st.subheader(T("The 4P Scam Check"))
    st.markdown(four_p(), unsafe_allow_html=True)
    st.subheader(T("About this app"))
    st.write(T("{app} is an educational simulation. **Every organisation, person, phone number and website in the game is fictional.** The app never sends real messages and never asks for your real personal or banking information. We store only your nickname, age group and class code. All voices are synthetic (computer-generated); no real person's voice was cloned.", app=APP_NAME))
    if ss.lang == "ms":
        st.caption(T("🌐 Scenario messages stay in their original language (a realistic mix of Malay and English, like real scams)."))


ROUTES = dict(zip(PAGES, [page_home, page_pre, page_arena, page_story, page_coop, page_post, page_retest, page_progress,
                          page_teacher, page_help]))
ROUTES[ss.nav]()
