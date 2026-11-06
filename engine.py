"""
engine.py - game rules: missions, scoring, levels, badges and the optional
AI scenario generator.
"""
import copy
import json
import os
import random

from content import TRAINING_SCENARIOS, TACTICS, CHANNEL_ICONS, DIFFICULTIES

# ----------------------------------------------------------------- scoring
XP_VERDICT = 50
XP_PER_FLAG = 10
XP_FALSE_ALARM = -5
XP_PERFECT = 20
XP_CALM = 20
DIFFICULTY_MULTIPLIER = {"Easy": 1.0, "Medium": 1.0, "Hard": 1.2, "Expert": 1.5}
VOICE_CHANNELS = ("Phone call", "Video call")

LEVELS = [
    (0, "Rookie", "🐣"),
    (200, "Scam Spotter", "🔍"),
    (500, "Fraud Fighter", "🥊"),
    (900, "Cyber Guardian", "🛡️"),
    (1400, "Scam Grandmaster", "🏆"),
]

BADGES = {
    "first_catch": ("🎯", "First Catch", "Correctly caught your first scam"),
    "sharp_eye": ("🦅", "Sharp Eye", "Perfect round: right verdict, every red flag, no false alarms"),
    "calm_mind": ("🧘", "Calm Mind", "Correctly trusted a legit message without false alarms"),
    "hot_streak": ("🔥", "Hot Streak", "5 correct verdicts in a row"),
    "deepfake_buster": ("🤖", "Deepfake Buster", "Caught a voice or video deepfake scam"),
    "baseline": ("📏", "Baseline Set", "Completed the pre-test"),
    "growth": ("📈", "Proven Growth", "Post-test score beat your pre-test"),
    "sharp_ears": ("🎧", "Sharp Ears", "3 correct verdicts on voice / video call rounds"),
    "expert_eye": ("🧠", "Expert Eye", "5 correct verdicts on Expert rounds"),
    "story_survivor": ("📖", "Story Survivor", "Escaped 3 different Story Missions without losing money"),
    "untouchable": ("💎", "Untouchable", "Escaped all 5 Story Missions without losing money"),
}

MISSION_LENGTH = 5


def score_round(scenario, answered_scam, selected_idx):
    """Score one training round.

    scenario      : scenario dict (with cues)
    answered_scam : bool, player's verdict
    selected_idx  : set of cue indexes the player ticked as red flags
    """
    red = {i for i, c in enumerate(scenario["cues"]) if c["is_red_flag"]}
    selected = set(selected_idx)
    hits = len(selected & red)
    false_alarms = len(selected - red)
    missed = len(red - selected)
    verdict_ok = bool(answered_scam) == bool(scenario["is_scam"])

    xp = 0
    breakdown = []
    if verdict_ok:
        xp += XP_VERDICT
        breakdown.append(("Correct verdict", {}, XP_VERDICT))
    if hits:
        xp += hits * XP_PER_FLAG
        breakdown.append(("{n} red flag(s) spotted", {"n": hits}, hits * XP_PER_FLAG))
    if false_alarms:
        xp += false_alarms * XP_FALSE_ALARM
        breakdown.append(("{n} false alarm(s)", {"n": false_alarms}, false_alarms * XP_FALSE_ALARM))
    perfect = verdict_ok and missed == 0 and false_alarms == 0
    if perfect:
        xp += XP_PERFECT
        breakdown.append(("Perfect round bonus", {}, XP_PERFECT))
    calm = verdict_ok and not scenario["is_scam"] and false_alarms == 0
    if calm:
        xp += XP_CALM
        breakdown.append(("Calm Mind bonus", {}, XP_CALM))
    mult = DIFFICULTY_MULTIPLIER.get(scenario.get("difficulty"), 1.0)
    xp = max(0, xp)
    if mult != 1.0 and xp:
        bonus = int(round(xp * (mult - 1)))
        xp += bonus
        breakdown.append(("{diff} difficulty bonus ×{mult}", {"diff": scenario["difficulty"], "mult": mult}, bonus))
    return {
        "verdict_ok": verdict_ok, "hits": hits, "false_alarms": false_alarms, "missed": missed,
        "perfect": perfect, "calm": calm, "xp": xp, "breakdown": breakdown, "red": red, "selected": selected,
    }


def level_for(xp):
    """Return (name, icon, current_floor, next_floor or None)."""
    current = LEVELS[0]
    nxt = None
    for i, lvl in enumerate(LEVELS):
        if xp >= lvl[0]:
            current = lvl
            nxt = LEVELS[i + 1] if i + 1 < len(LEVELS) else None
    return current[1], current[2], current[0], (nxt[0] if nxt else None), (nxt[1] if nxt else None)


def earned_badges(df, pre=None, post=None):
    """df = player's attempts DataFrame. pre/post = (correct, total) or None."""
    got = set()
    if df is not None and not df.empty:
        tr = df[df["mode"] == "train"]
        if not tr.empty:
            if ((tr["is_scam"] == 1) & (tr["correct"] == 1)).any():
                got.add("first_catch")
            if ((tr["is_scam"] == 1) & (tr["correct"] == 1) & (tr["missed"] == 0) & (tr["false_alarms"] == 0)).any():
                got.add("sharp_eye")
            if ((tr["is_scam"] == 0) & (tr["correct"] == 1) & (tr["false_alarms"] == 0)).any():
                got.add("calm_mind")
            if ((tr["tactic"] == "Voice / video deepfake") & (tr["correct"] == 1)).any():
                got.add("deepfake_buster")
            streak = best = 0
            for c in tr["correct"].tolist():
                streak = streak + 1 if c else 0
                best = max(best, streak)
            if best >= 5:
                got.add("hot_streak")
            if ((tr["channel"].isin(VOICE_CHANNELS)) & (tr["correct"] == 1)).sum() >= 3:
                got.add("sharp_ears")
            if ((tr["difficulty"] == "Expert") & (tr["correct"] == 1)).sum() >= 5:
                got.add("expert_eye")
        st_ = df[df["mode"] == "story"]
        if not st_.empty:
            escaped = st_.loc[st_["correct"] == 1, "scenario_id"].nunique()
            if escaped >= 3:
                got.add("story_survivor")
            if escaped >= 5:
                got.add("untouchable")
    if pre:
        got.add("baseline")
    if pre and post and post[0] / post[1] > pre[0] / pre[1]:
        got.add("growth")
    return got


# ----------------------------------------------------------------- missions
def _shuffled(scenario, rng):
    s = copy.deepcopy(scenario)
    rng.shuffle(s["cues"])
    return s


def weak_tactics(df, min_tries=1):
    """Tactics ordered from weakest to strongest for this player (training rounds only)."""
    if df is None or df.empty:
        return []
    tr = df[df["mode"] == "train"]
    if tr.empty:
        return []
    g = tr.groupby("tactic")["correct"].agg(["mean", "count"])
    g = g[g["count"] >= min_tries].sort_values(["mean", "count"])
    return [t for t, row in g.iterrows() if row["mean"] < 1.0]


def build_mission(difficulty="Mixed", seen_ids=None, seed=None, weak=None):
    """Pick MISSION_LENGTH scenarios, preferring unseen ones, always with >=1 legit message.

    difficulty: Easy / Medium / Hard / Expert / Mixed / Smart
    Smart = scenarios from the player's weakest tactics first (adaptive), then Hard/Expert.
    """
    rng = random.Random(seed)
    seen_ids = set(seen_ids or [])
    if difficulty == "Smart":
        weak = weak or []
        rank = {t: i for i, t in enumerate(weak)}
        pool = list(TRAINING_SCENARIOS)
        rng.shuffle(pool)
        # sort key: weak tactic first, unseen first, harder first
        hard_rank = {"Expert": 0, "Hard": 1, "Medium": 2, "Easy": 3}
        pool.sort(key=lambda s: (rank.get(s["tactic"], 99), s["id"] in seen_ids, hard_rank[s["difficulty"]]))
        ordered = pool
    else:
        pool = [s for s in TRAINING_SCENARIOS if difficulty == "Mixed" or s["difficulty"] == difficulty]
        unseen = [s for s in pool if s["id"] not in seen_ids]
        seen = [s for s in pool if s["id"] in seen_ids]
        rng.shuffle(unseen)
        rng.shuffle(seen)
        ordered = unseen + seen
    pick = ordered[:MISSION_LENGTH]
    if pick and all(s["is_scam"] for s in pick):
        legit = [s for s in ordered if not s["is_scam"]]
        if legit:
            pick[-1] = legit[0]
    rng.shuffle(pick)
    return [_shuffled(s, rng) for s in pick]


# ----------------------------------------------------------- story missions
def story_path_summary(story, path):
    """path = list of (node_id, choice_index). Returns totals for the debrief."""
    score = loss = 0
    for node_id, ci in path:
        ch = story["nodes"][node_id]["choices"][ci]
        score += ch.get("score", 0)
        loss += ch.get("loss", 0)
        loss -= story["nodes"].get(ch["next"], {}).get("refund", 0)
    return {"score": score, "loss": max(0, loss)}


# ----------------------------------------------------------- AI generator
AI_SYSTEM_PROMPT = """You are the scenario designer for KEBAL, a scam-awareness training game used in Malaysian schools.
You write SAFE, SIMULATED training messages so learners can practise spotting scams.

Hard rules:
- Use ONLY fictional organisations: Bank Harmoni, Bank Seri Nusa, KilatPos (courier), PasarKu (marketplace),
  TeleSatu (telco), eWalletKu (e-wallet), or invent clearly fictional ones. NEVER use real company, bank,
  brand, government agency or celebrity names.
- Any link must be a made-up domain written as plain text (no http://).
- Never include real phone numbers; use formats like +60 1X-XXX XXXX with random digits.
- Keep the message under 70 words. Malaysian context and tone.
- Output ONLY one JSON object, no markdown, matching this schema exactly:
{"id": "AI", "channel": one of [SMS, WhatsApp, Email, Phone call, Social media, Telegram, Video call, QR code, Website],
 "sender": str, "context": str (one line, may be empty), "message": str, "is_scam": bool,
 "difficulty": "Easy"|"Medium"|"Hard"|"Expert", "tactic": one of TACTICS,
 "cues": [ {"text": str (max 12 words), "is_red_flag": bool, "why": str (max 25 words)} ] (4 or 5 cues),
 "lesson": str starting with "What to do:" for scams or "Legit!" for legit messages}
- For scams: 2-4 cues are true red flags and at least 1 cue is a decoy (normal or falsely reassuring detail).
- For legit messages: tactic is "Legit message" and ALL cues have is_red_flag false.
- For Hard/Expert: make it genuinely tricky. Use context that changes the answer, look-alike domains (rn vs m, I vs l),
  spoofed sender threads, real money already received, real events (floods, data leaks), and "falsely reassuring"
  decoy cues (padlock icon, known contact, real invoice number, familiar voice).
"""


def _validate(data):
    req = ["channel", "sender", "context", "message", "is_scam", "difficulty", "tactic", "cues", "lesson"]
    for k in req:
        if k not in data:
            raise ValueError(f"missing {k}")
    if data["channel"] not in CHANNEL_ICONS:
        data["channel"] = "SMS"
    if data["tactic"] not in TACTICS:
        data["tactic"] = "Legit message" if not data["is_scam"] else "Phishing link"
    if data["difficulty"] not in DIFFICULTIES:
        data["difficulty"] = "Medium"
    cues = data["cues"]
    if not isinstance(cues, list) or not 3 <= len(cues) <= 6:
        raise ValueError("bad cues")
    for c in cues:
        if not {"text", "is_red_flag", "why"} <= set(c):
            raise ValueError("bad cue")
        c["is_red_flag"] = bool(c["is_red_flag"])
    data["is_scam"] = bool(data["is_scam"])
    if not data["is_scam"]:
        for c in cues:
            c["is_red_flag"] = False
        data["tactic"] = "Legit message"
    elif not any(c["is_red_flag"] for c in cues):
        raise ValueError("scam without red flags")
    return data


def generate_ai_scenario(api_key, model=None, difficulty="Medium", language="English", tactic=None):
    """Ask Claude for a fresh scenario. Returns a validated dict, or raises on any problem."""
    import anthropic  # imported lazily so the app runs without the package/key

    model = model or os.environ.get("SCAMSHIELD_MODEL", "claude-sonnet-4-5")
    is_scam = random.random() < 0.7
    if not tactic:
        tactic = random.choice([t for t in TACTICS if t != "Legit message"]) if is_scam else "Legit message"
    tactic_list = ", ".join(TACTICS)
    user = (f"TACTICS = [{tactic_list}]. Create one {'SCAM' if is_scam else 'LEGITIMATE'} scenario. Difficulty: {difficulty}. "
            f"Tactic: {tactic}. Message language: {language}. Make it feel fresh and realistic for 2026 "
            f"(e-wallets, AI voice clones, eKYC, QR codes, task jobs, online marketplaces).")
    client = anthropic.Anthropic(api_key=api_key)
    resp = client.messages.create(model=model, max_tokens=1200, system=AI_SYSTEM_PROMPT,
                                  messages=[{"role": "user", "content": user}])
    text = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("no JSON in reply")
    data = _validate(json.loads(text[start:end + 1]))
    data["id"] = "AI-" + str(random.randint(10000, 99999))
    random.shuffle(data["cues"])
    return data
