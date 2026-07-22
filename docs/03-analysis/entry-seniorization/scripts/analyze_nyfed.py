#!/usr/bin/env python3
"""Analyze NY Fed College Labor Market unemployment data.

Computes gap = recent grads - all workers, persistent-inversion episodes
(gap > 0 for >= 12 consecutive months), and Q1 2026 quarterly averages.
"""
import json
import pandas as pd

DATA = "/private/tmp/claude-501/-Users-hayun-Documents-Github-AIEconLab--claude-worktrees-ai-trends-july-17-1ce616/ae37edf6-cc22-4044-ad92-2e5d4cc51c0e/scratchpad/entry_seniorization/data/college-labor-unemployment-data.csv"
OUT = "/private/tmp/claude-501/-Users-hayun-Documents-Github-AIEconLab--claude-worktrees-ai-trends-july-17-1ce616/ae37edf6-cc22-4044-ad92-2e5d4cc51c0e/scratchpad/entry_seniorization/out/nyfed_facts.json"

df = pd.read_csv(DATA, parse_dates=["Date"])
df = df.sort_values("Date").reset_index(drop=True)
print("rows:", len(df), "| range:", df.Date.min().date(), "->", df.Date.max().date())
print("columns:", list(df.columns))
assert df.Date.diff().dropna().dt.days.between(28, 31).all(), "not monthly-continuous"

df["gap"] = df["Recent graduates"] - df["All workers"]

# episodes of gap > 0 lasting >= 12 consecutive months
pos = (df["gap"] > 0).astype(int)
grp = (pos.diff() != 0).cumsum()
episodes = []
for g, sub in df.groupby(grp):
    if pos.loc[sub.index[0]] == 1 and len(sub) >= 12:
        ongoing = sub.index[-1] == df.index[-1]
        episodes.append({
            "start": sub.Date.iloc[0].strftime("%Y-%m"),
            "end": None if ongoing else sub.Date.iloc[-1].strftime("%Y-%m"),
            "length_months": int(len(sub)),
            "ongoing": bool(ongoing),
            "max_gap_pp": round(float(sub.gap.max()), 3),
            "mean_gap_pp": round(float(sub.gap.mean()), 3),
        })
# also list ALL positive runs (any length) for context
all_runs = []
for g, sub in df.groupby(grp):
    if pos.loc[sub.index[0]] == 1:
        all_runs.append({
            "start": sub.Date.iloc[0].strftime("%Y-%m"),
            "end": sub.Date.iloc[-1].strftime("%Y-%m"),
            "length_months": int(len(sub)),
        })

latest = df.iloc[-1]
q1 = df[(df.Date.dt.year == 2026) & (df.Date.dt.quarter == 1)]
q1_avg = {c: round(float(q1[c].mean()), 3) for c in
          ["Recent graduates", "All workers", "Young workers", "College graduates"]}

facts = {
    "source_page": "https://www.newyorkfed.org/research/college-labor-market",
    "data_url": "https://www.newyorkfed.org/medialibrary/research/interactives/data/college-labor-market/college-labor-unemployment-data.csv",
    "meta_url": "https://www.newyorkfed.org/medialibrary/research/interactives/data/college-labor-market/college-labor-chart-meta.json",
    "download_timestamp_utc": "2026-07-21T23:58:44Z",
    "sha256_csv": "bc1014335fe1dade67994c15f0182526c468160b3df40c76610a903e3c40e39e",
    "sha256_meta_json": "af1074fa206e066bd70a7bf40d5ca7f81194342b09027707784a42ce78f14290",
    "release_date_info": "May 5, 2026, with 2026:Q1 data",
    "frequency_smoothing": "Monthly; rates are seasonally adjusted and smoothed with a three-month moving average (per NY Fed notes). October 2025 results are estimated due to missing data.",
    "series_definitions_verbatim": (
        "All workers are those aged 16 to 65; college graduates are those aged 22 to 65 "
        "with a bachelor's degree or higher; recent college graduates are those aged 22 to 27 "
        "with a bachelor's degree or higher; young workers are those aged 22 to 27 without a "
        "bachelor's degree. All figures exclude those currently enrolled in school."
    ),
    "notes_verbatim": (
        "Notes: Rates are seasonally adjusted and smoothed with a three-month moving average. "
        "All workers are those aged 16 to 65; college graduates are those aged 22 to 65 with a "
        "bachelor's degree or higher; recent college graduates are those aged 22 to 27 with a "
        "bachelor's degree or higher; young workers are those aged 22 to 27 without a bachelor's "
        "degree. All figures exclude those currently enrolled in school. Shaded areas indicate "
        "periods designated recessions by the National Bureau of Economic Research. Click on the "
        "labels in the chart legend to show and hide trend lines in the display. October 2025 "
        "results are estimated due to missing data."
    ),
    "source_verbatim": "Source: U.S. Census Bureau and U.S. Bureau of Labor Statistics, Current Population Survey (IPUMS).",
    "data_range": {"first_month": df.Date.min().strftime("%Y-%m"), "last_month": df.Date.max().strftime("%Y-%m")},
    "latest_month": latest.Date.strftime("%Y-%m"),
    "latest_values_pct": {
        "recent_graduates": round(float(latest["Recent graduates"]), 3),
        "all_workers": round(float(latest["All workers"]), 3),
        "young_workers": round(float(latest["Young workers"]), 3),
        "college_graduates": round(float(latest["College graduates"]), 3),
    },
    "current_gap_pp": round(float(latest["gap"]), 3),
    "episodes_gap_positive_ge12m": episodes,
    "all_positive_gap_runs_any_length": all_runs,
    "q1_2026_quarterly_averages_pct": q1_avg,
    "q1_2026_crosscheck": {
        "press_claim": "5.7% recent grads vs 4.3% all workers",
        "computed_recent_grads": q1_avg["Recent graduates"],
        "computed_all_workers": q1_avg["All workers"],
        "recent_grads_match_5.7": bool(round(q1_avg["Recent graduates"], 1) == 5.7),
        "all_workers_match_4.3": bool(round(q1_avg["All workers"], 1) == 4.3),
    },
}

with open(OUT, "w") as f:
    json.dump(facts, f, indent=2, ensure_ascii=False)

print(json.dumps(facts, indent=2, ensure_ascii=False))
