"""
pilot_stats.py - numbers for the pilot study (KEBAL group vs control group).

Main result = difference in score GAIN (post-test % minus pre-test %) between groups,
with Cohen's d and a permutation-test p-value (no extra libraries needed).
"""
import math

import numpy as np
import pandas as pd


def player_scores(df):
    """One row per player: pre/post/retention accuracy (0-100) + school code."""
    t = df[df["mode"].isin(["pre", "post", "retention"])]
    if t.empty:
        return pd.DataFrame(columns=["player_id", "school", "pre", "post", "retention"])
    s = (100 * t.groupby(["player_id", "school", "mode"])["correct"].mean()).unstack()
    for col in ("pre", "post", "retention"):
        if col not in s:
            s[col] = np.nan
    return s.reset_index()


def cohens_d(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    n1, n2 = len(a), len(b)
    if n1 < 2 or n2 < 2:
        return float("nan")
    pooled = math.sqrt(((n1 - 1) * a.var(ddof=1) + (n2 - 1) * b.var(ddof=1)) / (n1 + n2 - 2))
    return float((a.mean() - b.mean()) / pooled) if pooled > 0 else float("nan")


def permutation_p(a, b, n_perm=10000, seed=42):
    """Two-sided permutation test on the difference in means."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    if len(a) < 2 or len(b) < 2:
        return float("nan")
    rng = np.random.default_rng(seed)
    pooled = np.concatenate([a, b])
    observed = abs(a.mean() - b.mean())
    count = 0
    for _ in range(n_perm):
        rng.shuffle(pooled)
        if abs(pooled[:len(a)].mean() - pooled[len(a):].mean()) >= observed - 1e-12:
            count += 1
    return (count + 1) / (n_perm + 1)


def overconfidence(df, mode):
    """Share (%) of 'Certain' answers that were wrong in a test."""
    t = df[(df["mode"] == mode) & (df["confidence"] == 3)] if "confidence" in df else pd.DataFrame()
    return (100 * (1 - t["correct"].mean()), len(t)) if len(t) else (float("nan"), 0)


def summarise(attempts, settings, surveys):
    """attempts: all_attempts() DataFrame. settings: list of class_settings dicts. surveys: all_surveys() DataFrame."""
    groups = {s["code"]: s["grp"] for s in settings}
    if attempts.empty or not groups:
        return None
    df = attempts[attempts["school"].isin(groups)].copy()
    if df.empty:
        return None
    df["grp"] = df["school"].map(groups)
    sc = player_scores(df)
    sc["grp"] = sc["school"].map(groups)
    out = {}
    for g in ("kebal", "control"):
        s = sc[sc["grp"] == g]
        paired = s.dropna(subset=["pre", "post"])
        ret = s.dropna(subset=["pre", "retention"])
        gd = df[df["grp"] == g]
        oc_pre, n_pre = overconfidence(gd, "pre")
        oc_post, n_post = overconfidence(gd, "post")
        sus = surveys[surveys["school"].isin([c for c, v in groups.items() if v == g])] if not surveys.empty else pd.DataFrame()
        out[g] = {
            "n_players": int(s["player_id"].nunique()), "n_paired": len(paired),
            "pre": paired["pre"].mean(), "post": paired["post"].mean(),
            "gain": (paired["post"] - paired["pre"]).mean(), "gains": (paired["post"] - paired["pre"]).tolist(),
            "retention": ret["retention"].mean(), "n_retention": len(ret),
            "retention_gain": (ret["retention"] - ret["pre"]).mean(),
            "oc_pre": oc_pre, "oc_post": oc_post,
            "sus": sus["sus_score"].mean() if len(sus) else float("nan"), "n_sus": len(sus),
        }
    k, c = out["kebal"]["gains"], out["control"]["gains"]
    out["diff"] = (np.mean(k) - np.mean(c)) if len(k) and len(c) else float("nan")
    out["d"] = cohens_d(k, c)
    out["p"] = permutation_p(k, c)
    return out
