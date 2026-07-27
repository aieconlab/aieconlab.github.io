#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""그림 1: 2026년 7월 신모델의 출력 단가 변화 — 인상 5, 동결 2, 인하 1.

모집단 규칙(원자료: data/july_price_direction_roster.txt):
2026년 7월 출시 모델 가운데 같은 회사의 **같은 등급**에 공식 단가가 공표된 직전 모델이
있는 것만 센다. 오픈웨이트로만 공개돼 개발사 API 단가가 없는 Hy3(7/6)·Inkling(7/15),
단가 미공표인 Muse Spark 1.1(7/9)은 제외. Claude Fable 5는 6월 9일 출시라 7월 집계 밖.

등급 대응 근거(각 사 공식 문서):
- OpenAI 모델 문서: Sol="frontier model", Terra="mini 등급에 대체로 대응",
  Luna="nano 등급에 대체로 대응" → Terra는 gpt-5.4-mini, Luna는 gpt-5.4-nano와 비교.
  (Terra를 gpt-5.4와 견주면 등급이 어긋난다 — 4차 개고까지의 오류)
- Anthropic 릴리스 노트 2026-07-24: Opus 5는 "the same pricing as Claude Opus 4.8"
- Google 릴리스 노트 2026-07-21: 3.6 Flash·3.5 Flash-Lite GA,
  3.6 Flash는 "lower price point than 3.5 Flash"

출력 단가(100만 토큰당 달러, 2026-07-28 각 사 공식 가격 문서 확인):
  인상 GPT-5.6 Luna  $1.25 → $6     (gpt-5.4-nano 대비 ×4.8)
  인상 Kimi K3       $4    → $15    (K2.6 대비 ×3.75)
  인상 GPT-5.6 Terra $4.50 → $15    (gpt-5.4-mini 대비 ×3.33)
  인상 Grok 4.5      $2.50 → $6     (Grok 4.3 대비 ×2.4)
  인상 3.5 Flash-Lite $1.50 → $2.50 (3.1 Flash-Lite 대비 ×1.67)
  동결 GPT-5.6 Sol   $30   → $30
  동결 Claude Opus 5 $25   → $25
  인하 3.6 Flash     $9    → $7.50  (-16.7%)

사용법: python3 fig01_output_price_moves.py [--out PNG] [--font FONT]
의존성: matplotlib
"""
import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
BLUE, NAVY, GRAY, NOTE, SPINE = "#2563eb", "#1b2a4a", "#8290a6", "#5a6472", "#c8cdd6"
RED = "#b4472e"   # 인상
GREEN = "#1f7a5a"  # 인하

# (7월 모델, 직전 동급 모델, 직전가, 현행가, 방향, 배수 라벨)
ROWS = [
    ("GPT-5.6 Luna", "gpt-5.4-nano", 1.25, 6.00, "up", "×4.8"),
    ("Kimi K3", "Kimi K2.6", 4.00, 15.00, "up", "×3.75"),
    ("GPT-5.6 Terra", "gpt-5.4-mini", 4.50, 15.00, "up", "×3.3"),
    ("Grok 4.5", "Grok 4.3", 2.50, 6.00, "up", "×2.4"),
    ("Gemini 3.5 Flash-Lite", "3.1 Flash-Lite", 1.50, 2.50, "up", "×1.67"),
    ("GPT-5.6 Sol", "gpt-5.5", 30.00, 30.00, "flat", "동결"),
    ("Claude Opus 5", "Claude Opus 4.8", 25.00, 25.00, "flat", "동결"),
    ("Gemini 3.6 Flash", "3.5 Flash", 9.00, 7.50, "down", "16.7% 인하"),
]

# ---- 수치 검증 ----
assert len(ROWS) == 8
_dirs = [r[4] for r in ROWS]
assert _dirs.count("up") == 5 and _dirs.count("flat") == 2 and _dirs.count("down") == 1, \
    ("방향 집계가 본문(동결 2·인상 5·인하 1)과 불일치", _dirs)
for name, prev, old, new, d, _ in ROWS:
    if d == "up":
        assert new > old, ("인상 행인데 값이 오르지 않음", name)
    elif d == "flat":
        assert new == old, ("동결 행인데 값이 다름", name)
    else:
        assert new < old, ("인하 행인데 값이 내리지 않음", name)
assert abs(6.00 / 1.25 - 4.8) < 1e-9        # Luna vs nano
assert abs(15.0 / 4.0 - 3.75) < 1e-9        # Kimi
assert abs(15.0 / 4.50 - 3.333) < 0.001     # Terra vs mini
assert abs(6.00 / 2.50 - 2.4) < 1e-9        # Grok
assert abs(2.50 / 1.50 - 1.667) < 0.001     # Flash-Lite
assert abs((1 - 7.5 / 9.0) - 0.1667) < 0.0005  # 3.6 Flash 인하
# 비교 15종 스펙트럼(본문 별도 서술)
assert abs(50.0 / 0.28 - 178.6) < 1.0


def dollar(v):
    return f"${v:g}" if v >= 1 else f"${v:.2f}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=HERE / "out" / "fig01_output_price_moves.png")
    ap.add_argument("--font", default="Apple SD Gothic Neo")
    a = ap.parse_args()

    plt.rcParams["font.family"] = a.font
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["text.parse_math"] = False
    fig, ax = plt.subplots(figsize=(10, 7.2), dpi=200)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    n = len(ROWS)
    ys = list(range(n, 0, -1))
    ax.set_xscale("log")
    ax.set_xlim(0.8, 130)
    ax.set_ylim(0.35, n + 0.75)

    COLOR = {"up": RED, "flat": NAVY, "down": GREEN}
    labels = []
    for (name, prev, old, new, d, mult), y in zip(ROWS, ys):
        c = COLOR[d]
        if d == "flat":
            ax.plot([old], [y], "o", ms=13, mfc="none", mec=GRAY, mew=1.6, zorder=3)
            ax.plot([new], [y], "o", ms=8, color=c, zorder=4)
        else:
            ax.annotate("", xy=(new, y), xytext=(old, y),
                        arrowprops=dict(arrowstyle="-|>", color=c, lw=2.2,
                                        shrinkA=5, shrinkB=5, mutation_scale=16), zorder=3)
            ax.plot([old], [y], "o", ms=7, mfc="white", mec=GRAY, mew=1.8, zorder=4)
            ax.plot([new], [y], "o", ms=8, color=c, zorder=5)

        # 데이터 영역 '밖'(축 여백)에 이름·배수를 둔다 — 마커·화살표와 겹치지 않게
        gut = ax.get_yaxis_transform()  # x는 axes 비율, y는 데이터 좌표
        labels.append(ax.text(-0.015, y, name, transform=gut, fontsize=11.5, color=NAVY,
                              ha="right", va="center", fontweight="bold"))
        labels.append(ax.text(1.015, y, mult, transform=gut, fontsize=11.5, ha="left",
                              va="center", color=c, fontweight="bold"))
        # 점 라벨: 직전(위) / 현행(아래)
        if d == "flat":
            labels.append(ax.text(old, y + 0.30, f"{prev} → {name.split()[-1]}  {dollar(new)}",
                                  fontsize=10, color=NAVY, ha="center", va="center"))
        else:
            labels.append(ax.text(old, y + 0.30, f"{prev} {dollar(old)}", fontsize=9.5,
                                  color=GRAY, ha="center", va="center"))
            labels.append(ax.text(new, y - 0.32, dollar(new), fontsize=11, color=c,
                                  ha="center", va="center", fontweight="bold"))

    # 방향 구분선(인상 5 / 동결 2 / 인하 1). 그룹 이름은 제목이 이미 밝히므로
    # 도형 안에는 선만 두어 라벨 충돌을 없앤다.
    for yline in (n - 4.5, n - 6.5):
        ax.axhline(yline, color=SPINE, lw=0.9, ls=":", zorder=1)

    ax.set_yticks([])
    ax.set_xticks([1, 3, 10, 30, 100])
    ax.set_xticklabels(["$1", "$3", "$10", "$30", "$100"], fontsize=12, color=NAVY)
    ax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(SPINE)
    ax.tick_params(colors=NAVY, labelsize=12)
    ax.grid(axis="x", color=SPINE, linewidth=0.6, alpha=0.45)
    ax.set_axisbelow(True)
    ax.set_xlabel("출력 100만 토큰당 공식 단가 (달러, 로그 눈금)", fontsize=12.5, color=NAVY,
                  labelpad=7)
    ax.set_title("2026년 7월 신모델의 값: 인상 다섯, 동결 둘, 인하 하나",
                 loc="left", fontsize=18.5, fontweight="bold", color=NAVY, pad=14)

    fig.subplots_adjust(left=0.215, right=0.885, top=0.925, bottom=0.30)

    NOTE_PARAS = [
        "주: 2026년 7월 출시 모델 가운데 같은 회사의 같은 등급에 공식 단가가 공표된 직전 모델이 있는 여덟 개. "
        "오픈웨이트로만 공개돼 개발사 API 단가가 없는 Hy3·Inkling과 단가 미공표인 Muse Spark 1.1은 제외했고, "
        "Claude Fable 5는 6월 9일 출시라 대상이 아니다. 등급 대응은 각 사 공식 문서를 따랐고, 오픈AI 모델 문서는 "
        "Terra를 'mini 등급', Luna를 'nano 등급'에 대응한다고 명시한다. 회색 원은 직전 동급 모델, 색 원은 현행.",
        "자료: OpenAI·Anthropic·Google·xAI·Moonshot AI 공식 가격 문서·모델 문서·릴리스 노트(2026-07-28 확인)  |  정리: AIEconLab",
    ]
    NOTE_X, NOTE_FS = 0.01, 11.3
    rend0 = fig.canvas.get_renderer()
    fig_w0 = fig.canvas.get_width_height()[0]
    limit = fig_w0 * (0.99 - NOTE_X)

    def measure(s):
        t = fig.text(0, -1, s, fontsize=NOTE_FS)
        w = t.get_window_extent(renderer=rend0).width
        t.remove()
        return w

    wrapped = []
    for pi, para in enumerate(NOTE_PARAS):
        cur = ""
        for word in para.split(" "):
            trial = (cur + " " + word).strip()
            if measure(trial) <= limit or not cur:
                cur = trial
            else:
                wrapped.append((pi, cur))
                cur = word
        wrapped.append((pi, cur))
    assert 2 <= len(wrapped) <= 6, ("주석 줄 수 이상", len(wrapped))
    ys_note = [0.170 - 0.034 * i for i in range(len(wrapped))]
    notes = [fig.text(NOTE_X, y, ln, fontsize=NOTE_FS, color=NOTE)
             for (pi, ln), y in zip(wrapped, ys_note)]
    for i, (pi, ln) in enumerate(wrapped[:-1]):
        if wrapped[i + 1][0] == pi:
            assert measure(ln) >= 0.86 * limit, ("주석 줄 채움 부족", ln[:20])

    # ---- 렌더링 후 검사 ----
    BAD_GLYPHS = "−–—"  # 한글 폰트에 글리프가 없어 두부 글자가 된다
    for t in labels + notes:
        assert not any(ch in t.get_text() for ch in BAD_GLYPHS), \
            ("한글 폰트에 없는 글리프 사용", t.get_text()[:24])
    fig.canvas.draw()
    rend = fig.canvas.get_renderer()
    bb = lambda t: t.get_window_extent(renderer=rend)
    fig_w, fig_h = fig.canvas.get_width_height()
    for t in labels + notes:
        assert bb(t).x1 <= fig_w - 3, ("우측 잘림", t.get_text()[:18])
        assert bb(t).x0 >= 0, ("좌측 잘림", t.get_text()[:18])
        assert bb(t).y1 <= fig_h - 2, ("상단 잘림", t.get_text()[:18])
    boxes = [bb(t) for t in labels]
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            assert not boxes[i].overlaps(boxes[j]), \
                ("라벨 겹침", labels[i].get_text()[:16], labels[j].get_text()[:16])
    # 여백에 둔 모델명·배수는 데이터 영역을 침범하면 안 된다(마커·화살표와 겹침 방지)
    ax_box = ax.get_window_extent(renderer=rend)
    for t in labels:
        if t.get_transform() is ax.get_yaxis_transform():
            b = bb(t)
            assert b.x1 <= ax_box.x0 + 1 or b.x0 >= ax_box.x1 - 1, \
                ("여백 라벨이 데이터 영역 침범", t.get_text()[:18])
    gaps = [bb(notes[k]).y0 - bb(notes[k + 1]).y1 for k in range(len(notes) - 1)]
    assert all(g >= 2 for g in gaps), ("주석 줄간 겹침", [round(g, 1) for g in gaps])
    xlab = ax.xaxis.get_label()
    assert bb(xlab).y0 - bb(notes[0]).y1 >= 4, "x축 라벨과 주석 겹침"
    print(f"layout checks passed: {len(boxes)} labels clear, note gaps "
          f"{'/'.join(f'{g:.1f}' for g in gaps)}px")

    a.out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(a.out, dpi=200, facecolor="white", metadata={"Date": None})
    print("wrote", a.out)


if __name__ == "__main__":
    main()
