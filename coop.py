"""
coop.py - multiplayer rooms for the Co-op Simulation.

All players connected to the SAME running app share one SQLite database, so a room
code works across phones/laptops (same Wi-Fi via the Network URL, or a hosted link).
Time is the server's clock, so every player sees the same countdown.

Room lifecycle:  lobby -> playing -> ended (outcome: win | close | lost)
"""
import json
import random
import sqlite3
import string
import time

import storage
from coop_content import COOP_MISSIONS, get_mission, TRANSLATIONS
from content_expert import AUDIO_CLIPS

CODE_CHARS = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"  # no 0/O, 1/I
ONLINE_SECS = 8


def _conn():
    conn = sqlite3.connect(storage.DB_PATH, timeout=10, isolation_level=None)
    conn.row_factory = sqlite3.Row
    return conn


def init():
    with _conn() as c:
        c.execute("""CREATE TABLE IF NOT EXISTS rooms (
            code TEXT PRIMARY KEY, mission_id TEXT NOT NULL, status TEXT NOT NULL, host_id INTEGER NOT NULL,
            target_id INTEGER, started_at REAL, deadline REAL, state TEXT NOT NULL, created_at REAL NOT NULL)""")
        c.execute("""CREATE TABLE IF NOT EXISTS room_players (
            code TEXT NOT NULL, player_id INTEGER NOT NULL, nickname TEXT NOT NULL, role TEXT,
            joined_at REAL NOT NULL, last_seen REAL NOT NULL, PRIMARY KEY (code, player_id))""")
        c.execute("""CREATE TABLE IF NOT EXISTS room_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT, code TEXT NOT NULL, visible_at REAL NOT NULL,
            actor TEXT, kind TEXT NOT NULL, audience TEXT NOT NULL, text TEXT NOT NULL)""")


def _fresh_state():
    return {"done": [], "ready": {}, "speaker": False, "doom": None, "stalls": 0, "penalties": 0, "bonus": 0,
            "loss": 0, "outcome": None, "ending": None, "ended_at": None, "score": 0, "rewarded": [], "danger": []}


# ------------------------------------------------------------------ rooms
def create_room(player, mission_id="C1"):
    for _ in range(50):
        code = "".join(random.choice(CODE_CHARS) for _ in range(5))
        try:
            with _conn() as c:
                c.execute("INSERT INTO rooms (code, mission_id, status, host_id, state, created_at) VALUES (?,?,?,?,?,?)",
                          (code, mission_id, "lobby", player["id"], json.dumps(_fresh_state()), time.time()))
            join_room(code, player)
            return code
        except sqlite3.IntegrityError:
            continue
    raise RuntimeError("could not create room")


def join_room(code, player):
    code = code.strip().upper()
    with _conn() as c:
        room = c.execute("SELECT * FROM rooms WHERE code=?", (code,)).fetchone()
        if not room:
            return False, "No room with that code."
        now = time.time()
        exists = c.execute("SELECT 1 FROM room_players WHERE code=? AND player_id=?", (code, player["id"])).fetchone()
        if exists:
            c.execute("UPDATE room_players SET last_seen=? WHERE code=? AND player_id=?", (now, code, player["id"]))
        else:
            if room["status"] == "playing":
                return False, "That game has already started. Ask the host to return to the lobby."
            c.execute("INSERT INTO room_players (code, player_id, nickname, role, joined_at, last_seen) VALUES (?,?,?,?,?,?)",
                      (code, player["id"], player["nickname"], None, now, now))
    return True, code


def leave_room(code, player_id):
    with _conn() as c:
        c.execute("DELETE FROM room_players WHERE code=? AND player_id=?", (code, player_id))
        left = c.execute("SELECT player_id FROM room_players WHERE code=? ORDER BY joined_at", (code,)).fetchall()
        room = c.execute("SELECT host_id FROM rooms WHERE code=?", (code,)).fetchone()
        if room and room["host_id"] == player_id and left:
            c.execute("UPDATE rooms SET host_id=? WHERE code=?", (left[0]["player_id"], code))


def heartbeat(code, player_id):
    with _conn() as c:
        c.execute("UPDATE room_players SET last_seen=? WHERE code=? AND player_id=?", (time.time(), code, player_id))


def get_room(code):
    with _conn() as c:
        room = c.execute("SELECT * FROM rooms WHERE code=?", (code,)).fetchone()
        if not room:
            return None
        players = c.execute("SELECT * FROM room_players WHERE code=? ORDER BY joined_at", (code,)).fetchall()
    r = dict(room)
    r["state"] = json.loads(r["state"])
    r["players"] = [dict(p) for p in players]
    now = time.time()
    for p in r["players"]:
        p["online"] = now - p["last_seen"] < ONLINE_SECS
    return r


def set_mission(code, mission_id):
    with _conn() as c:
        c.execute("UPDATE rooms SET mission_id=? WHERE code=? AND status='lobby'", (mission_id, code))


def set_target(code, player_id):
    with _conn() as c:
        c.execute("UPDATE rooms SET target_id=? WHERE code=?", (player_id, code))


def names(room):
    """{T} and {G} display names."""
    players = room["players"]
    t = next((p["nickname"] for p in players if p["role"] in ("target", "both")), "Target")
    gs = [p["nickname"] for p in players if p["role"] == "guardian"]
    g = " & ".join(gs) if gs else (t if any(p["role"] == "both" for p in players) else "Guardian")
    return {"T": t, "G": g}


def fmt(text, room):
    n = names(room)
    return text.replace("{T}", n["T"]).replace("{G}", n["G"])


def start_game(code):
    now = time.time()
    with _conn() as c:
        c.execute("BEGIN IMMEDIATE")
        room = c.execute("SELECT * FROM rooms WHERE code=?", (code,)).fetchone()
        players = c.execute("SELECT * FROM room_players WHERE code=? ORDER BY joined_at", (code,)).fetchall()
        m = get_mission(room["mission_id"])
        if len(players) == 1:
            c.execute("UPDATE room_players SET role='both' WHERE code=?", (code,))
        else:
            target = room["target_id"] if room["target_id"] in [p["player_id"] for p in players] else players[0]["player_id"]
            c.execute("UPDATE room_players SET role='guardian' WHERE code=?", (code,))
            c.execute("UPDATE room_players SET role='target' WHERE code=? AND player_id=?", (code, target))
            c.execute("UPDATE rooms SET target_id=? WHERE code=?", (target, code))
        c.execute("DELETE FROM room_events WHERE code=?", (code,))
        c.execute("UPDATE rooms SET status='playing', started_at=?, deadline=?, state=? WHERE code=?",
                  (now, now + m["duration"], json.dumps(_fresh_state()), code))
        c.execute("COMMIT")
    room = get_room(code)
    _event(code, now, None, "system", "all", fmt("🎬 " + m["brief"], room))


def back_to_lobby(code):
    with _conn() as c:
        c.execute("UPDATE rooms SET status='lobby', started_at=NULL, deadline=NULL, state=? WHERE code=?",
                  (json.dumps(_fresh_state()), code))
        c.execute("DELETE FROM room_events WHERE code=?", (code,))
        c.execute("UPDATE room_players SET role=NULL WHERE code=?", (code,))


def _event(code, visible_at, actor, kind, audience, text, conn=None):
    q = "INSERT INTO room_events (code, visible_at, actor, kind, audience, text) VALUES (?,?,?,?,?,?)"
    if conn is not None:
        conn.execute(q, (code, visible_at, actor, kind, audience, text))
    else:
        with _conn() as c:
            c.execute(q, (code, visible_at, actor, kind, audience, text))


def chat(code, nickname, text):
    text = text.strip()[:200]
    if text:
        _event(code, time.time(), nickname, "chat", "all", text)


def incoming_message(m):
    clip = m["incoming"].get("audio")
    text = AUDIO_CLIPS[clip]["text"] if clip in AUDIO_CLIPS else ""
    if clip in TRANSLATIONS:
        text += "\n\n" + TRANSLATIONS[clip]
    return text


# ------------------------------------------------------------------ events for a viewer
def visible_events(room, role, now=None):
    """Stored events + scripted pressure lines, filtered for this role, oldest first."""
    now = now or time.time()
    m = get_mission(room["mission_id"])
    st = room["state"]
    with _conn() as c:
        rows = [dict(r) for r in c.execute("SELECT * FROM room_events WHERE code=? AND visible_at<=? ORDER BY visible_at, id",
                                             (room["code"], now)).fetchall()]
    if room["started_at"]:
        stop = st["ended_at"] or now
        for t, text in m["pressure"]:
            at = room["started_at"] + t
            if at <= stop:
                rows.append({"visible_at": at, "actor": None, "kind": "pressure", "audience": "call", "text": fmt(text, room)})
    rows.sort(key=lambda e: e["visible_at"])

    def can_see(e):
        a = e["audience"]
        if role == "both" or a == "all":
            return True
        if a == "call":
            return role == "target" or st["speaker"]
        return a == role
    return [e for e in rows if can_see(e)]


def pending_tools(room, now=None):
    now = now or time.time()
    return {tid: at - now for tid, at in room["state"]["ready"].items() if at > now}


# ------------------------------------------------------------------ actions
def _load(c, code):
    room = c.execute("SELECT * FROM rooms WHERE code=?", (code,)).fetchone()
    return dict(room), json.loads(room["state"])


def _save(c, code, state, **cols):
    sets = ", ".join(f"{k}=?" for k in cols)
    vals = list(cols.values())
    c.execute(f"UPDATE rooms SET state=?{', ' + sets if sets else ''} WHERE code=?", [json.dumps(state)] + vals + [code])


def _end(c, code, room_row, state, outcome, ending, now):
    m = get_mission(room_row["mission_id"])
    state["outcome"], state["ending"], state["ended_at"] = outcome, ending, now
    time_left = max(0, room_row["deadline"] - now)
    clues = sum(1 for tid, at in state["ready"].items() if at <= now and _tool(m, tid).get("kind") == "clue")
    if outcome == "win":
        score = 100 + int(time_left) + 10 * clues + 15 * state["bonus"] - 15 * state["penalties"]
        score = max(60, score)
    elif outcome == "close":
        score = 40 + 5 * clues
    else:
        score = 10 + 5 * clues
    state["score"] = int(min(score, 300))
    _save(c, code, state, status="ended")


def _tool(m, tid):
    for a in m["target_actions"] + m["guardian_tools"]:
        if a["id"] == tid:
            return a
    return {}


def act(code, player, role, action_id):
    """Apply one action. Returns a short message for the actor (or None)."""
    now = time.time()
    with _conn() as c:
        c.execute("BEGIN IMMEDIATE")
        room_row, st = _load(c, code)
        if room_row["status"] != "playing":
            c.execute("ROLLBACK")
            return "The game is not running."
        m = get_mission(room_row["mission_id"])
        room_view = get_room(code)
        a = _tool(m, action_id)
        if not a:
            c.execute("ROLLBACK")
            return None
        is_target_action = a in m["target_actions"]
        if is_target_action and role not in ("target", "both"):
            c.execute("ROLLBACK")
            return "Only the Target can do that."
        if not is_target_action and role not in ("guardian", "both"):
            c.execute("ROLLBACK")
            return "Only the Guardian can do that."
        if action_id in st["done"] and a["kind"] not in ("cancel_doom",):
            c.execute("ROLLBACK")
            return "Already done."
        who = player["nickname"]
        kind = a["kind"]
        msg = None

        if not is_target_action:  # ---------------- guardian investigation
            if a.get("requires") == "speaker" and not st["speaker"]:
                _event(code, now, who, "result", "guardian", "⚠️ " + fmt(a["missing"], room_view), c)
                c.execute("COMMIT")
                return fmt(a["missing"], room_view)
            st["done"].append(action_id)
            st["ready"][action_id] = now + a.get("delay", 5)
            label = fmt(a["label"], room_view)
            _event(code, now, who, "action", "all", f"🛡️ {who} → {label} (⏳ ~{a.get('delay', 5)}s)", c)
            icon = "❌" if kind == "bad" else "🔍"
            _event(code, now + a.get("delay", 5), who, "clue", "guardian" if kind != "bad" else "all",
                   f"{icon} {fmt(a['clue'], room_view)}", c)
            if kind == "bad":
                st["penalties"] += 1
            if a.get("reveal_danger"):
                st["danger"].append([a["reveal_danger"], now + a.get("delay", 5)])
        else:  # ---------------------------------------- target move
            label = fmt(a["label"], room_view)
            if kind == "cancel_doom":
                if st["doom"]:
                    st["doom"] = None
                    _event(code, now, who, "action", "all", "✋ " + fmt(a["text"], room_view), c)
                else:
                    c.execute("ROLLBACK")
                    return "You're not going anywhere right now."
            else:
                st["done"].append(action_id)
            if kind == "fatal":
                _event(code, now, who, "action", "all", f"📱 {who} → {label}", c)
                _end(c, code, room_row, st, "lost", a["ending"], now)
                c.execute("COMMIT")
                return None
            if kind == "share":
                st["speaker"] = True
                st["bonus"] += 1
            if kind == "bad":
                st["penalties"] += 1
                st["loss"] += a.get("loss", 0)
                if a.get("speaker_off"):
                    st["speaker"] = False
            if kind == "bonus":
                st["bonus"] += 1
            if kind == "stall":
                st["stalls"] += 1
                room_row["deadline"] += a.get("seconds", 15)
            if kind == "doom":
                st["doom"] = {"start": now, "at": now + a["seconds"], "ending": a["ending"],
                              "from": a.get("doom_from"), "to": a.get("doom_to")}
            if kind == "info":
                _event(code, now, who, "action", "call", f"📱 {who} → {label}", c)
                _event(code, now + 2, None, "reply", "call", "💬 " + fmt(a["reply"], room_view), c)
            elif kind != "cancel_doom":
                _event(code, now, who, "action", "all", "📱 " + fmt(a.get("text", f"{who} → {label}"), room_view), c)
        _save(c, code, st, deadline=room_row["deadline"])
        c.execute("COMMIT")
    tick(code)
    return msg


def tick(code):
    """Advance time-based rules: guardian results arriving, win check, doom arrival, timeout."""
    now = time.time()
    with _conn() as c:
        c.execute("BEGIN IMMEDIATE")
        room_row, st = _load(c, code)
        if room_row["status"] != "playing":
            c.execute("ROLLBACK")
            return
        m = get_mission(room_row["mission_id"])
        completed = {tid for tid in st["done"]
                     if tid not in st["ready"] or st["ready"][tid] <= now}
        if st["doom"] and now >= st["doom"]["at"]:
            _end(c, code, room_row, st, "lost", st["doom"]["ending"], st["doom"]["at"])
        elif all(any(a in completed for a in group) for group in m["win"]) and not st["doom"]:
            _end(c, code, room_row, st, "win", "win", now)
        elif now >= room_row["deadline"]:
            outcome = m["timeout"]
            _end(c, code, room_row, st, "lost" if outcome == "lost" else "close", outcome, room_row["deadline"])
        c.execute("COMMIT")


def claim_reward(code, player_id):
    """Give XP once per player per game. Returns (xp, outcome) if newly awarded, else None."""
    with _conn() as c:
        c.execute("BEGIN IMMEDIATE")
        room_row, st = _load(c, code)
        if room_row["status"] != "ended" or player_id in st["rewarded"]:
            c.execute("ROLLBACK")
            return None
        st["rewarded"].append(player_id)
        _save(c, code, st)
        c.execute("COMMIT")
    m = get_mission(room_row["mission_id"])
    storage.record_attempt(player_id, "coop", {"id": m["id"], "channel": "Co-op", "tactic": m["tactic"],
                                               "difficulty": "Co-op", "is_scam": True},
                           answered_scam=st["outcome"] == "win", correct=st["outcome"] == "win", xp=st["score"])
    return st["score"], st["outcome"]


def team_history(player_id):
    import pandas as pd
    df = storage.player_attempts(player_id)
    return df[df["mode"] == "coop"] if not df.empty else pd.DataFrame()


def missions():
    return COOP_MISSIONS
