#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""그림 1: 미국 신규 대졸자 실업률 vs 전체 근로자 (뉴욕 연은 College Labor Market 재계산).

기본 동작: 뉴욕 연은 CSV를 내려받고(--data로 로컬 파일 지정 가능) 역전 에피소드
(신규 대졸자 − 전체 근로자 > 0, 12개월 이상 연속)를 데이터에서 직접 계산해 그린다.
음영·주석·끝값은 모두 데이터에서 동적으로 산출한다(하드코딩 없음).

사용법:
    python3 fig01_us_recent_grads.py [--data CSV] [--out PNG] [--facts JSON]
                                     [--access-date YYYY-MM-DD] [--allow-updated-data]

의존성: pandas, matplotlib. 한글 폰트 기본값은 macOS 'Apple SD Gothic Neo'(--font로 변경).
2026-05-05 갱신분 CSV SHA-256:
    bc1014335fe1dade67994c15f0182526c468160b3df40c76610a903e3c40e39e
해시가 이 값과 다르면(=뉴욕 연은이 데이터를 갱신했으면) 기본값으로 중단한다.
갱신 데이터로 계속하려면 --allow-updated-data를 지정한다.
"""
import argparse
import datetime as dt
import hashlib
import urllib.request
from pathlib import Path

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
URL = ("https://www.newyorkfed.org/medialibrary/research/interactives/"
       "data/college-labor-market/college-labor-unemployment-data.csv")
KNOWN_SHA256 = "bc1014335fe1dade67994c15f0182526c468160b3df40c76610a903e3c40e39e"

BLUE, MID, LIGHT, NAVY, NOTE, SPINE = ("#2563eb", "#8290a6", "#7f8da3",
                                       "#1b2a4a", "#5a6472", "#c8cdd6")


def fetch(data_path, allow_updated_data=False):
    if data_path:
        raw = Path(data_path).read_bytes()
        src = str(data_path)
    else:
        req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
        raw = urllib.request.urlopen(req, timeout=60).read()
        cache = HERE / "data"
        cache.mkdir(exist_ok=True)
        (cache / "college-labor-unemployment-data.csv").write_bytes(raw)
        src = URL
    sha = hashlib.sha256(raw).hexdigest()
    print(f"source: {src}\nsha256: {sha}")
    if sha != KNOWN_SHA256:
        msg = ("해시가 2026-05-05 갱신분과 다름 — 뉴욕 연은이 데이터를 갱신했을 수 있음. "
               "게시글 수치와 달라질 수 있으므로 기본값은 중단. 계속하려면 --allow-updated-data.")
        if not allow_updated_data:
            raise SystemExit("중단: " + msg)
        print("주의(계속 진행): " + msg)
    from io import BytesIO
    return pd.read_csv(BytesIO(raw), parse_dates=["Date"]).sort_values("Date").reset_index(drop=True)


def episodes(df, min_len=12):
    """gap > 0 연속 구간 중 min_len 이상만 반환."""
    pos = (df["gap"] > 0).astype(int)
    grp = (pos.diff() != 0).cumsum()
    out = []
    for _, sub in df.groupby(grp):
        if pos.loc[sub.index[0]] == 1 and len(sub) >= min_len:
            out.append({"start": sub.Date.iloc[0], "end": sub.Date.iloc[-1],
                        "n": int(len(sub)), "ongoing": bool(sub.index[-1] == df.index[-1])})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", help="로컬 CSV 경로(생략 시 뉴욕 연은에서 다운로드)")
    ap.add_argument("--out", type=Path, default=HERE / "out" / "fig01_us_recent_grads.png")
    ap.add_argument("--facts", type=Path, default=HERE / "out" / "nyfed_facts_regen.json")
    ap.add_argument("--font", default="Apple SD Gothic Neo")
    ap.add_argument("--access-date", default=None,
                    help="푸터 조회일(YYYY-MM-DD). 커밋본 재현 시 2026-07-22. 기본: 오늘")
    ap.add_argument("--allow-updated-data", action="store_true",
                    help="원자료 해시가 기록과 달라도 계속 진행")
    a = ap.parse_args()

    df = fetch(a.data, a.allow_updated_data)
    df["gap"] = df["Recent graduates"] - df["All workers"]
    eps = episodes(df)
    cur = next((e for e in eps if e["ongoing"]), None)
    last = df.iloc[-1]
    print(f"latest {last.Date:%Y-%m}: RG {last['Recent graduates']:.1f} / All {last['All workers']:.1f} "
          f"/ Young {last['Young workers']:.1f} / CG {last['College graduates']:.1f}")
    if cur:
        print(f"current episode: {cur['start']:%Y-%m} ~ ongoing, {cur['n']} months")

    plt.rcParams["font.family"] = a.font
    plt.rcParams["axes.unicode_minus"] = False
    fig, ax = plt.subplots(figsize=(10, 7), dpi=200)
    fig.patch.set_facecolor("white")

    series = [("Young workers", MID, 2.2, "청년 비대졸(22-27세)"),
              ("Recent graduates", BLUE, 3.4, "신규 대졸자(22-27세)"),
              ("All workers", NAVY, 2.2, "전체 근로자(16-65세)"),
              ("College graduates", LIGHT, 2.2, "대졸 전체(22-65세)")]
    styles = {"All workers": "--", "College graduates": ":"}
    for col, c, lw, _ in series:
        ax.plot(df.Date, df[col], color=c, linewidth=lw,
                linestyle=styles.get(col, "-"), zorder=3)
    if cur:
        ax.axvspan(cur["start"], cur["end"], color=BLUE, alpha=0.08, zorder=1)
        ax.annotate(f"{cur['start'].year}년 {cur['start'].month}월 이후\n{cur['n']}개월 연속 역전",
                    xy=(cur["start"] + (cur["end"] - cur["start"]) / 2, ax.get_ylim()[1]),
                    xytext=(0, -14), textcoords="offset points",
                    ha="center", va="top", fontsize=16, fontweight="bold", color=BLUE)
    # 끝값 레이블
    x_end = df.Date.iloc[-1] + pd.DateOffset(months=6)
    offsets = {"Young workers": 0.55, "Recent graduates": 0.0,
               "All workers": -0.45, "College graduates": -1.35}
    for col, c, _, label in series:
        ax.annotate(f"{label} {last[col]:.1f}%", xy=(x_end, last[col] + offsets[col]),
                    fontsize=16, fontweight="bold" if col == "Recent graduates" else "normal",
                    color=NAVY if col == "All workers" else c, va="center", annotation_clip=False)

    ax.set_xlim(df.Date.iloc[0], df.Date.iloc[-1] + pd.DateOffset(months=3))
    ax.set_ylim(0, None)
    ax.set_ylabel("실업률 (%)", fontsize=16.5, color=NAVY)
    ax.tick_params(colors=NAVY, labelsize=15.5)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(SPINE)
    ax.grid(axis="y", color=SPINE, linewidth=0.6, alpha=0.5)
    ax.set_axisbelow(True)
    ax.set_title("미국 신규 대졸자의 실업률이 전체 근로자를 웃돌고 있다",
                 loc="left", fontsize=23, fontweight="bold", color=NAVY, pad=18)

    fig.subplots_adjust(left=0.075, right=0.72, top=0.90, bottom=0.15)
    access = a.access_date or dt.date.today().isoformat()
    fig.text(0.075, 0.062, "주: 계절조정·3개월 이동평균(월별), 재학생 제외. 음영은 12개월 이상 연속 역전 구간. 계열 정의는 본문 참조.",
             fontsize=12.5, color=NOTE)
    fig.text(0.075, 0.028, f"자료: 뉴욕 연방준비은행 College Labor Market ({access} 조회)  |  계산: AIEconLab",
             fontsize=12.5, color=NOTE)

    a.out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(a.out, dpi=200, facecolor="white")
    print("wrote", a.out)

    import json
    a.facts.parent.mkdir(parents=True, exist_ok=True)
    a.facts.write_text(json.dumps({
        "latest": {c: float(last[c]) for c, *_ in series} | {"month": f"{last.Date:%Y-%m}"},
        "episodes_ge_12m": [{"start": f"{e['start']:%Y-%m}", "end": f"{e['end']:%Y-%m}",
                             "months": e["n"], "ongoing": e["ongoing"]} for e in eps],
    }, ensure_ascii=False, indent=2))
    print("wrote", a.facts)


if __name__ == "__main__":
    main()
