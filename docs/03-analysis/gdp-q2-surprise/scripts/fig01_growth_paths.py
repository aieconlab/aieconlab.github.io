#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""그림 1: 2026년 연간 성장률의 등가 경로, 7월 15일 기준과 7월 23일 기준.

방법(기계적 환산, 전망 아님):
- 분기 실질 GDP 수준(계절조정)은 FRED NGDPRSAXDCKRQ(원자료 IMF IFS)를 사용.
  2026년 1분기까지 반영된 계열이며, 1분기 전기비는 약 1.83%로
  trend11 글(7/15)의 수치와 동일한 원천이다. 2025년 분기 경로(-0.2, 0.6,
  1.4, -0.1)와 2026Q1(1.8)은 한국은행 속보 PDF 표와 반올림 일치 확인.
- 2026년 2분기 수준은 1분기 수준에 전기비 0.62%(기자설명회에서 확인된
  비반올림치. 공표 반올림치는 0.6%. 이데일리·프라임경제 2026.7.23 보도)를
  곱해 잇는다. 이후 분기는 공통 전기비 g를 적용한다.
- 연간 성장률 = (2026년 4개 분기 평균 수준) / (2025년 4개 분기 평균 수준) - 1.
- '7월 15일 기준' 곡선은 1분기까지만 실적으로 두고 남은 3개 분기에 g를 적용
  (trend11 그림 1과 동일한 규칙), '7월 23일 기준' 곡선은 2분기 속보까지
  실적으로 두고 남은 2개 분기에 g를 적용한다.

검증(assert):
- 1분기 전기비 1.83% 내외(trend11 본문과 일치).
- 구곡선: g=0 → 2.6% 내외, 3.0%에 필요한 g는 0.26% 내외(trend11 본문과 일치).
- 신곡선: g=0 → 3.08%(반올림 3.1%), g=-0.1% → 3.00%(오차 0.02%p 이내).
  후자는 한국은행 설명회의 '하반기 평균 -0.1%여도 연 3%' 산술과의 교차 확인.
- 2025년 연간 성장률 1.1% 내외(한국은행 2025년 국민계정 잠정 1.1%와 정합).

사용법: python3 fig01_growth_paths.py [--out PNG] [--json JSON] [--font FONT]
                                       [--local CSV] [--offline] [--refresh]
                                       [--allow-updated-data]
의존성: matplotlib (다운로드는 표준 라이브러리 urllib 사용).

보호 장치:
- 원자료 SHA-256 고정 검사: 계열이 기록과 다르면 실행을 멈춘다. 데이터가
  개정된 경우 --allow-updated-data로 실행해 검산 assert 통과를 확인한 뒤
  EXPECTED_SHA256과 README 기록을 갱신한다.
- --refresh는 응답을 임시 파일에 받아 CSV 스키마·필수 분기 검증과 SHA 승인
  (기록 일치 또는 --allow-updated-data)까지 통과한 경우에만 캐시를 원자적으로
  교체한다(오류 응답도, 유효하지만 미승인인 개정 데이터도 기존 캐시를
  파괴하지 않음).
- JSON과 PNG는 수치 검산과 그림 레이아웃 검사(라벨 겹침)를 모두 통과한
  뒤에만 기록한다.
"""
import argparse
import csv
import hashlib
import io
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
BLUE, MID, LIGHT, NAVY, NOTE, SPINE = ("#2563eb", "#8290a6", "#7f8da3",
                                       "#1b2a4a", "#5a6472", "#c8cdd6")

FRED_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=NGDPRSAXDCKRQ"
# 2026Q2 전기비. 기자설명회에서 확인된 비반올림치(공표 반올림치는 0.6%).
Q2_QOQ = 0.0062
# 게시 시점의 원자료 스냅샷(2026-07-23 다운로드분). 개정 시 --allow-updated-data 참조.
EXPECTED_SHA256 = "02c1cf857933937b127c7d0819fe9cf77ca21acbd04e242ce5b09db48337d6d0"
# 계산에 반드시 필요한 분기(누락 시 원자료 불량으로 판정)
REQUIRED_QUARTERS = [f"{y}Q{q}" for y in (2024, 2025) for q in (1, 2, 3, 4)] + ["2026Q1"]


def parse_and_validate(raw: bytes):
    """CSV 스키마와 필수 분기를 검증해 levels를 반환. 실패 시 SystemExit."""
    try:
        reader = csv.DictReader(io.StringIO(raw.decode("utf-8")))
        cols = reader.fieldnames or []
        if "observation_date" not in cols or "NGDPRSAXDCKRQ" not in cols:
            raise ValueError(f"예상 밖 CSV 헤더: {cols[:5]}")
        levels = {}
        for row in reader:
            d = row["observation_date"]
            v = row.get("NGDPRSAXDCKRQ", "")
            if not v or v == ".":
                continue
            q = (int(d[5:7]) - 1) // 3 + 1
            levels[f"{d[:4]}Q{q}"] = float(v)
    except (UnicodeDecodeError, ValueError, KeyError, IndexError, TypeError) as e:
        raise SystemExit(f"원자료 파싱 실패(캐시 미변경): {e}")
    missing = [k for k in REQUIRED_QUARTERS if k not in levels]
    if missing:
        raise SystemExit(f"필수 분기 누락(캐시 미변경): {missing}")
    return levels


def load_series(local: Path | None, offline: bool, refresh: bool = False,
                allow_updated: bool = False):
    import os
    import tempfile
    from datetime import datetime as dt
    use_cache = bool(local) and local.exists() and not refresh
    if use_cache:
        raw = local.read_bytes()
        src_desc = "캐시 CSV"
        from_cache = True
    elif not offline:
        raw = urllib.request.urlopen(FRED_URL, timeout=60).read()
        src_desc = "다운로드 응답"
        from_cache = False
    else:
        raise SystemExit("offline인데 로컬 CSV가 없습니다")
    levels = parse_and_validate(raw)
    sha = hashlib.sha256(raw).hexdigest()
    # SHA 승인(기록 일치 또는 --allow-updated-data)은 캐시 교체보다 먼저 수행:
    # 유효하지만 미승인인 개정 데이터가 기존 캐시를 밀어내지 않게 한다.
    if sha != EXPECTED_SHA256 and not allow_updated:
        raise SystemExit(
            f"{src_desc}의 SHA-256이 기록({EXPECTED_SHA256[:12]}...)과 다릅니다: "
            f"{sha[:12]}... (캐시 미변경)\n"
            "데이터가 개정된 경우 --allow-updated-data로 실행해 검산 통과를 확인한 뒤 "
            "EXPECTED_SHA256과 README 표를 갱신하세요.")
    if not from_cache and local:
        local.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=str(local.parent), suffix=".tmp")
        with os.fdopen(fd, "wb") as f:
            f.write(raw)
        os.replace(tmp, local)  # 검증·SHA 승인을 통과한 응답만 원자적 교체
    # 캐시 파일의 수정 시각은 저장이 끝난 뒤 다시 읽는다(refresh 직후에도 유효)
    cache_mtime = (dt.fromtimestamp(os.stat(local).st_mtime, timezone.utc)
                   if local and local.exists() else None)
    return levels, sha, from_cache, cache_mtime


def annual_growth_2026(levels_2026, avg_2025):
    return sum(levels_2026) / 4.0 / avg_2025 - 1.0


def curve_as_of_0715(g, q1, avg_2025):
    lv = [q1, q1 * (1 + g), q1 * (1 + g) ** 2, q1 * (1 + g) ** 3]
    return annual_growth_2026(lv, avg_2025)


def curve_as_of_0723(g, q1, q2, avg_2025):
    lv = [q1, q2, q2 * (1 + g), q2 * (1 + g) ** 2]
    return annual_growth_2026(lv, avg_2025)


def solve(fn, target, lo=-0.03, hi=0.03):
    for _ in range(200):
        mid = (lo + hi) / 2.0
        if fn(mid) < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=HERE / "out" / "fig01_growth_paths.png")
    ap.add_argument("--json", type=Path, default=HERE.parent / "calc_results.json")
    ap.add_argument("--font", default="Apple SD Gothic Neo")
    ap.add_argument("--local", type=Path, default=HERE / "data" / "krgdp.csv")
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--refresh", action="store_true",
                    help="캐시를 무시하고 FRED에서 새로 내려받아 검증 후 캐시를 갱신")
    ap.add_argument("--allow-updated-data", action="store_true",
                    help="원자료 SHA가 기록과 달라도 진행(개정 데이터 반영 시)")
    a = ap.parse_args()

    levels, sha, from_cache, cache_mtime = load_series(
        a.local, a.offline, a.refresh, a.allow_updated_data)
    try:
        cache_rel = str(a.local.resolve().relative_to(HERE.parents[3]))
    except (ValueError, AttributeError):
        cache_rel = None  # 저장소 밖 경로는 기록하지 않음(경로 비식별)
    q2025 = [levels[f"2025Q{i}"] for i in range(1, 5)]
    q2024 = [levels[f"2024Q{i}"] for i in range(1, 5)]
    avg_2025 = sum(q2025) / 4.0
    q1 = levels["2026Q1"]
    q2 = q1 * (1 + Q2_QOQ)

    q1_qoq = q1 / levels["2025Q4"] - 1.0
    g2025 = avg_2025 / (sum(q2024) / 4.0) - 1.0
    yoy_q1 = q1 / levels["2025Q1"] - 1.0
    yoy_q2 = q2 / levels["2025Q2"] - 1.0

    old = lambda g: curve_as_of_0715(g, q1, avg_2025)
    new = lambda g: curve_as_of_0723(g, q1, q2, avg_2025)

    res = {
        "data_source": FRED_URL,
        "sha256": sha,
        "cache_path_repo_relative": cache_rel,
        "from_cache": from_cache,
        "cache_mtime_utc": cache_mtime.isoformat(timespec="seconds") if cache_mtime else None,
        "cache_mtime_note": "캐시 파일의 수정 시각. 다운로드 시각의 공식 기록은 README 표 참조.",
        "verified_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "q2_qoq_applied": Q2_QOQ,
        "q1_qoq_pct": round(q1_qoq * 100, 3),
        "q1_yoy_pct_fred": round(yoy_q1 * 100, 4),
        "q2_yoy_pct_implied": round(yoy_q2 * 100, 4),
        "growth_2025_pct": round(g2025 * 100, 2),
        "old_flat_pct": round(old(0.0) * 100, 3),
        "old_g_for_3.0_pct": round(solve(old, 0.03) * 100, 3),
        "new_flat_pct": round(new(0.0) * 100, 3),
        "new_minus0.1_pct": round(new(-0.001) * 100, 3),
        "new_g_for_3.0_pct": round(solve(new, 0.03) * 100, 3),
        "new_g_for_2.6_pct": round(solve(new, 0.026) * 100, 3),
        "new_q2pace_pct": round(new(Q2_QOQ) * 100, 3),
    }

    assert abs(q1_qoq - 0.0183) < 0.0005, q1_qoq
    assert 2.55 < res["old_flat_pct"] < 2.65
    assert abs(res["old_g_for_3.0_pct"] - 0.26) < 0.05
    assert round(res["new_flat_pct"], 1) == 3.1
    assert abs(res["new_minus0.1_pct"] - 3.0) < 0.02
    assert abs(g2025 * 100 - 1.1) < 0.1, g2025
    print("sanity checks passed:", json.dumps(res, ensure_ascii=False, indent=2))

    # ---- figure ----
    plt.rcParams["font.family"] = a.font
    plt.rcParams["axes.unicode_minus"] = False
    fig, ax = plt.subplots(figsize=(10, 7), dpi=200)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    gs = [x / 1000.0 for x in range(-12, 11)]  # -1.2% ~ +1.0%
    ax.plot([g * 100 for g in gs], [old(g) * 100 for g in gs],
            color=MID, linewidth=2.4, label="7월 15일 기준 (1분기까지 반영)",
            linestyle=(0, (6, 3)), zorder=3)
    ax.plot([g * 100 for g in gs], [new(g) * 100 for g in gs],
            color=BLUE, linewidth=3.4, label="7월 23일 기준 (2분기 속보 반영)",
            zorder=4)

    ax.axhline(3.0, color=SPINE, linewidth=1.2, linestyle=(0, (3, 3)), zorder=1)
    t_gov = ax.text(1.02, 3.025, "정부 전망 3.0%", fontsize=13.5, color=NOTE, ha="right")
    ax.axhline(2.6, color=SPINE, linewidth=1.2, linestyle=(0, (3, 3)), zorder=1)
    t_int = ax.text(1.02, 2.545, "IMF 7월·한국은행 5월 전망 2.6%", fontsize=13.5,
                    color=NOTE, ha="right", va="top")

    anns = []
    pts_new = [(0.0, new(0.0) * 100, "정체여도 약 3.1%", (0.52, 3.2)),
               (-0.1, new(-0.001) * 100, "한국은행 산술\n(-0.1%면 3.0%)", (-0.62, 3.18)),
               (res["new_g_for_2.6_pct"], 2.6, "2.6%가 되려면\n매 분기 -0.6%", (-0.5, 2.35))]
    for x, y, lab, (tx, ty) in pts_new:
        ax.plot([x], [y], "o", color=BLUE, markersize=9, zorder=5,
                markeredgecolor="white", markeredgewidth=1.5)
        anns.append(ax.annotate(lab, xy=(x, y), xytext=(tx, ty), fontsize=14.5,
                    fontweight="bold", color=NAVY, ha="center", va="center",
                    arrowprops=dict(arrowstyle="-", color=NAVY, lw=1.0), zorder=6))

    x_old = res["old_g_for_3.0_pct"]
    ax.plot([x_old], [3.0], "o", color=MID, markersize=8, zorder=5,
            markeredgecolor="white", markeredgewidth=1.5)
    anns.append(ax.annotate("7월 15일에는 +0.26% 필요", xy=(x_old, 3.0), xytext=(0.55, 2.8),
                fontsize=13.5, color=NOTE, ha="center", va="center",
                arrowprops=dict(arrowstyle="-", color=NOTE, lw=1.0), zorder=6))

    ax.set_xlim(-1.25, 1.05)
    ax.set_ylim(2.1, 3.75)
    ax.set_xlabel("남은 분기에 공통 적용한 전기비 성장률 (%)", fontsize=16.5, color=NAVY)
    ax.set_ylabel("2026년 연간 성장률 (%)", fontsize=16.5, color=NAVY)
    ax.tick_params(colors=NAVY, labelsize=15.5)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(SPINE)
    ax.grid(axis="y", color=SPINE, linewidth=0.6, alpha=0.5)
    ax.set_axisbelow(True)
    ax.set_title("같은 목표, 낮아진 문턱: 2026년 연간 성장률의 등가 경로",
                 loc="left", fontsize=21, fontweight="bold", color=NAVY, pad=18)
    leg = ax.legend(loc="upper left", frameon=False, fontsize=14.5)
    for t in leg.get_texts():
        t.set_color(NAVY)

    fig.subplots_adjust(left=0.09, right=0.97, top=0.90, bottom=0.21)
    note1 = fig.text(0.09, 0.082, "주: 남은 분기에 동일한 전기비가 지속된다는 기계적 환산으로, 전망이 아님. 2분기는 비반올림 전기비 0.62% 적용.",
                     fontsize=12.5, color=NOTE)
    note2 = fig.text(0.09, 0.036, "자료: FRED NGDPRSAXDCKRQ(원자료 IMF IFS) · 한국은행 2026년 2분기 속보  |  계산: AIEconLab",
                     fontsize=12.5, color=NOTE)

    # 렌더링 후 텍스트 충돌 검사: 겹치면 저장하지 않고 실패
    fig.canvas.draw()
    rend = fig.canvas.get_renderer()
    bb = lambda t: t.get_window_extent(renderer=rend)
    gap_xlab = bb(ax.xaxis.get_label()).y0 - bb(note1).y1
    gap_notes = bb(note1).y0 - bb(note2).y1
    assert gap_xlab >= 2, ("x축 제목과 주석 겹침", round(gap_xlab, 1))
    assert gap_notes >= 2, ("주석 줄간 겹침", round(gap_notes, 1))
    check_texts = [t_gov, t_int] + anns
    for i, t1 in enumerate(check_texts):
        for t2 in check_texts[i + 1:]:
            assert not bb(t1).overlaps(bb(t2)), \
                ("텍스트 겹침", t1.get_text()[:14], t2.get_text()[:14])
    print(f"layout checks passed: xlabel gap {gap_xlab:.1f}px, notes gap {gap_notes:.1f}px, "
          f"{len(check_texts)}개 라벨 상호 비겹침")

    # 수치·레이아웃 검사를 모두 통과한 뒤에만 산출물을 확정
    a.json.parent.mkdir(parents=True, exist_ok=True)
    a.json.write_text(json.dumps(res, ensure_ascii=False, indent=2))
    print("wrote", a.json)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(a.out, dpi=200, facecolor="white")
    print("wrote", a.out)


if __name__ == "__main__":
    main()
