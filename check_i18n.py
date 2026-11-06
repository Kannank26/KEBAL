"""
check_i18n.py - find interface text that has no Bahasa Melayu translation yet.

    python check_i18n.py

Checks every T("...") call in app.py plus the dynamic lists (levels, badges, tactics,
channels, map places, help steps...). Also checks {placeholders} match.
"""
import ast
import re
import sys

import content
import coop_content
import engine
from i18n import MS

src = open("app.py", encoding="utf-8").read()
keys = set()
for node in ast.walk(ast.parse(src)):
    if isinstance(node, ast.Call) and getattr(node.func, "id", None) == "T" and node.args:
        a = node.args[0]
        if isinstance(a, ast.Constant) and isinstance(a.value, str):
            keys.add(a.value)
        elif isinstance(a, ast.IfExp):  # T("a" if x else "b")
            for part in (a.body, a.orelse):
                if isinstance(part, ast.Constant):
                    keys.add(part.value)
                elif isinstance(part, ast.IfExp):
                    keys.update(p.value for p in (part.body, part.orelse) if isinstance(p, ast.Constant))
# string lists that are passed through T() dynamically
for block in re.findall(r"(?:cards|items) = \[(.*?)\]\n", src, re.S):
    for pair in re.findall(r'\("((?:[^"\\]|\\.)+)", "((?:[^"\\]|\\.)+)"\)', block):
        keys.update(x.encode().decode("unicode_escape").encode("latin-1").decode("utf-8") for x in pair)
keys.update(re.findall(r'"(🎲 Mixed \(all levels\)|🟢 Easy|🟡 Medium|🟠 Hard|🔴 Expert[^"]*|🎯 Smart[^"]*)"', src))
dynamic = set()
dynamic.update(n for _, n, _ in engine.LEVELS)
dynamic.update(v for b in engine.BADGES.values() for v in b[1:])
dynamic.update(content.TACTICS)
dynamic.update(content.CHANNEL_ICONS)
dynamic.update(content.DIFFICULTIES)
dynamic.update(t for m_ in coop_content.COOP_MISSIONS for t in [m_["tactic"]])
dynamic.update(p["name"] for p in coop_content.POIS.values())
dynamic.update(d[5] for d in coop_content.DISTRICTS)
dynamic.update(coop_content.ROLE_LABEL.values())
dynamic.update(x for pair in content.HELP_STEPS for x in pair)
dynamic.update(["😬 Guessing", "🙂 Fairly sure", "😎 Certain", "🚩 Scam", "✅ Legit", "Scenario bank (offline)",
                "Live AI scenarios", "📱 Target phone", "🛡️ Guardian tools", "Story", "Co-op"])
dynamic.update(re.findall(r'^P_\w+(?:, P_\w+)* = (.*)$', src, re.M) and [])
for line in re.findall(r'^(P_[A-Z_, ]+) = (.+)$', src, re.M):
    dynamic.update(re.findall(r'"([^"]+)"', line[1]))
dynamic.update(["{n} red flag(s) spotted", "{n} false alarm(s)", "Correct verdict", "Perfect round bonus",
                "Calm Mind bonus", "{diff} difficulty bonus ×{mult}", "No points this round"])

for name in ("SUS_ITEMS", "HELPED"):
    m = re.search(name + r" = \[(.*?)\]\n", src, re.S)
    if m:
        dynamic.update(re.findall(r'"([^"]+)"', m.group(1)))
dynamic.update(["KEBAL group", "Control group", "large", "medium", "small", "negligible", "Retention Test",
                "That file is not a KEBAL database backup.", "That file is damaged or not a database.",
                "That database is missing KEBAL tables.", "Backup restored."])
missing = sorted(k for k in keys | dynamic if k not in MS)
bad_ph = [k for k in keys | dynamic if k in MS and set(re.findall(r"{(\w+)}", k)) != set(re.findall(r"{(\w+)}", MS[k]))]
print(f"{len(keys)} literal strings + {len(dynamic)} dynamic strings checked; {len(MS)} translations.")
for k in missing:
    print("MISSING:", repr(k))
for k in bad_ph:
    print("PLACEHOLDER MISMATCH:", repr(k))
sys.exit(1 if missing or bad_ph else 0)
