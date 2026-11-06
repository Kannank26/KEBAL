"""
storage.py - SQLite storage for players and attempts.

Privacy-first: we store only a nickname, an age group and an optional
school/organisation code. No real names, emails, IC or phone numbers.
"""
import os
import sqlite3
from datetime import datetime, timezone

import pandas as pd

DB_PATH = os.environ.get("SCAMSHIELD_DB", os.path.join(os.path.dirname(os.path.abspath(__file__)), "scamshield.db"))


def _conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with _conn() as c:
        c.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nickname TEXT NOT NULL,
                school TEXT NOT NULL DEFAULT '',
                age_group TEXT NOT NULL,
                created_at TEXT NOT NULL,
                UNIQUE(nickname, school)
            )""")
        c.execute("""
            CREATE TABLE IF NOT EXISTS attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER NOT NULL,
                mode TEXT NOT NULL,            -- 'pre', 'post' or 'train'
                scenario_id TEXT NOT NULL,
                channel TEXT,
                tactic TEXT,
                difficulty TEXT,
                is_scam INTEGER NOT NULL,
                answered_scam INTEGER NOT NULL,
                correct INTEGER NOT NULL,
                hits INTEGER DEFAULT 0,
                false_alarms INTEGER DEFAULT 0,
                missed INTEGER DEFAULT 0,
                xp INTEGER DEFAULT 0,
                created_at TEXT NOT NULL,
                FOREIGN KEY(player_id) REFERENCES players(id)
            )""")
        cols = {r[1] for r in c.execute("PRAGMA table_info(attempts)").fetchall()}
        if "confidence" not in cols:  # migration for databases from version 1
            c.execute("ALTER TABLE attempts ADD COLUMN confidence INTEGER")
        c.execute("""
            CREATE TABLE IF NOT EXISTS story_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER NOT NULL,
                story_id TEXT NOT NULL,
                ending TEXT NOT NULL,          -- 'safe', 'close' or 'lost'
                ending_node TEXT NOT NULL,
                loss INTEGER DEFAULT 0,
                score INTEGER DEFAULT 0,
                xp INTEGER DEFAULT 0,
                path TEXT,                     -- JSON list of [node, choice]
                created_at TEXT NOT NULL
            )""")


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def get_or_create_player(nickname, school, age_group):
    nickname = nickname.strip()[:30]
    school = school.strip().upper()[:30]
    with _conn() as c:
        row = c.execute("SELECT * FROM players WHERE nickname=? AND school=?", (nickname, school)).fetchone()
        if row:
            return dict(row), False
        c.execute("INSERT INTO players (nickname, school, age_group, created_at) VALUES (?,?,?,?)",
                  (nickname, school, age_group, _now()))
        row = c.execute("SELECT * FROM players WHERE nickname=? AND school=?", (nickname, school)).fetchone()
        return dict(row), True


def record_attempt(player_id, mode, scenario, answered_scam, correct, hits=0, false_alarms=0, missed=0, xp=0,
                   confidence=None):
    with _conn() as c:
        c.execute("""INSERT INTO attempts (player_id, mode, scenario_id, channel, tactic, difficulty, is_scam,
                     answered_scam, correct, hits, false_alarms, missed, xp, created_at, confidence)
                     VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                  (player_id, mode, scenario["id"], scenario.get("channel"), scenario.get("tactic"),
                   scenario.get("difficulty", "Test"), int(bool(scenario["is_scam"])), int(bool(answered_scam)),
                   int(bool(correct)), hits, false_alarms, missed, xp, _now(), confidence))


def record_story(player_id, story, ending_node, ending, loss, score, xp, path):
    """Save a finished Story Mission (detail table + an attempts row so XP and badges count it)."""
    import json
    with _conn() as c:
        c.execute("""INSERT INTO story_runs (player_id, story_id, ending, ending_node, loss, score, xp, path, created_at)
                     VALUES (?,?,?,?,?,?,?,?,?)""",
                  (player_id, story["id"], ending, ending_node, loss, score, xp, json.dumps(path), _now()))
    record_attempt(player_id, "story", {"id": story["id"], "channel": "Story", "tactic": story["tactic"],
                                        "difficulty": "Expert", "is_scam": True},
                   answered_scam=ending != "lost", correct=ending != "lost", xp=xp)


def story_runs(player_id=None):
    q = """SELECT r.*, p.nickname, p.school, p.age_group FROM story_runs r JOIN players p ON p.id = r.player_id"""
    args = ()
    if player_id is not None:
        q += " WHERE r.player_id=?"
        args = (player_id,)
    with _conn() as c:
        rows = c.execute(q + " ORDER BY r.id", args).fetchall()
    return pd.DataFrame([dict(r) for r in rows])


def player_attempts(player_id):
    with _conn() as c:
        rows = c.execute("SELECT * FROM attempts WHERE player_id=? ORDER BY id", (player_id,)).fetchall()
    return pd.DataFrame([dict(r) for r in rows])


def all_attempts():
    with _conn() as c:
        rows = c.execute("""SELECT a.*, p.nickname, p.school, p.age_group FROM attempts a
                            JOIN players p ON p.id = a.player_id ORDER BY a.id""").fetchall()
    return pd.DataFrame([dict(r) for r in rows])


def all_players():
    with _conn() as c:
        rows = c.execute("SELECT * FROM players ORDER BY id").fetchall()
    return pd.DataFrame([dict(r) for r in rows])


def test_score(player_id, mode):
    """Return (correct, total) for a player's pre or post test, or None if not done."""
    with _conn() as c:
        row = c.execute("SELECT SUM(correct) AS s, COUNT(*) AS n FROM attempts WHERE player_id=? AND mode=?",
                        (player_id, mode)).fetchone()
    if not row or not row["n"]:
        return None
    return int(row["s"]), int(row["n"])


def reset_test(player_id, mode):
    with _conn() as c:
        c.execute("DELETE FROM attempts WHERE player_id=? AND mode=?", (player_id, mode))


# ======================================================================
# Pilot / research support (version 5)
# ======================================================================
def init_pilot():
    with _conn() as c:
        c.execute("""CREATE TABLE IF NOT EXISTS class_settings (
            code TEXT PRIMARY KEY,
            grp TEXT NOT NULL DEFAULT 'kebal',          -- 'kebal' or 'control'
            retention_open INTEGER NOT NULL DEFAULT 0,
            consent_required INTEGER NOT NULL DEFAULT 0)""")
        c.execute("""CREATE TABLE IF NOT EXISTS surveys (
            player_id INTEGER PRIMARY KEY,
            sus_score REAL NOT NULL,
            answers TEXT NOT NULL,                     -- JSON list of the 10 SUS answers (1-5)
            helped TEXT, recommend INTEGER, comment TEXT,
            created_at TEXT NOT NULL)""")
        cols = {r[1] for r in c.execute("PRAGMA table_info(players)").fetchall()}
        if "consent_at" not in cols:
            c.execute("ALTER TABLE players ADD COLUMN consent_at TEXT")


def class_settings(code):
    code = (code or "").strip().upper()
    with _conn() as c:
        row = c.execute("SELECT * FROM class_settings WHERE code=?", (code,)).fetchone()
    return dict(row) if row else {"code": code, "grp": "kebal", "retention_open": 0, "consent_required": 0}


def save_class_settings(code, grp, retention_open, consent_required):
    code = code.strip().upper()
    with _conn() as c:
        c.execute("""INSERT INTO class_settings (code, grp, retention_open, consent_required) VALUES (?,?,?,?)
                     ON CONFLICT(code) DO UPDATE SET grp=excluded.grp, retention_open=excluded.retention_open,
                     consent_required=excluded.consent_required""",
                  (code, grp, int(bool(retention_open)), int(bool(consent_required))))


def all_class_settings():
    with _conn() as c:
        rows = c.execute("SELECT * FROM class_settings ORDER BY code").fetchall()
    return [dict(r) for r in rows]


def record_consent(player_id):
    with _conn() as c:
        c.execute("UPDATE players SET consent_at=COALESCE(consent_at, ?) WHERE id=?", (_now(), player_id))


def sus_score(answers):
    """System Usability Scale: odd items (1st, 3rd...) score-1, even items 5-score, sum x 2.5."""
    total = sum((a - 1) if i % 2 == 0 else (5 - a) for i, a in enumerate(answers))
    return total * 2.5


def save_survey(player_id, answers, helped, recommend, comment):
    import json
    with _conn() as c:
        c.execute("""INSERT OR REPLACE INTO surveys (player_id, sus_score, answers, helped, recommend, comment, created_at)
                     VALUES (?,?,?,?,?,?,?)""",
                  (player_id, sus_score(answers), json.dumps(answers), helped, recommend, (comment or "")[:500], _now()))


def get_survey(player_id):
    with _conn() as c:
        row = c.execute("SELECT * FROM surveys WHERE player_id=?", (player_id,)).fetchone()
    return dict(row) if row else None


def all_surveys():
    with _conn() as c:
        rows = c.execute("""SELECT s.*, p.nickname, p.school FROM surveys s JOIN players p ON p.id=s.player_id
                            ORDER BY s.created_at""").fetchall()
    return pd.DataFrame([dict(r) for r in rows])


def backup_bytes():
    """A consistent copy of the whole database, safe to take while the app is running."""
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "backup.db")
        src = sqlite3.connect(DB_PATH)
        dst = sqlite3.connect(path)
        with dst:
            src.backup(dst)
        src.close()
        dst.close()
        with open(path, "rb") as f:
            return f.read()


def restore_from_bytes(data):
    """Replace the database with an uploaded backup. Returns (ok, message)."""
    import tempfile
    if not data.startswith(b"SQLite format 3"):
        return False, "That file is not a KEBAL database backup."
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "upload.db")
        with open(path, "wb") as f:
            f.write(data)
        try:
            test = sqlite3.connect(path)
            tables = {r[0] for r in test.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            test.close()
        except sqlite3.DatabaseError:
            return False, "That file is damaged or not a database."
        if not {"players", "attempts"} <= tables:
            return False, "That database is missing KEBAL tables."
        src = sqlite3.connect(path)
        dst = sqlite3.connect(DB_PATH)
        with dst:
            src.backup(dst)
        src.close()
        dst.close()
    init_db()
    init_pilot()
    return True, "Backup restored."


def find_player(nickname, school):
    with _conn() as c:
        row = c.execute("SELECT * FROM players WHERE nickname=? AND school=?",
                        (nickname.strip()[:30], school.strip().upper()[:30])).fetchone()
    return dict(row) if row else None
