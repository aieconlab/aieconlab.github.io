#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""그림·본문의 하드코딩 수치를 data/ 원자료 사본과 기계 대조한다.

그림 스크립트(fig01/fig02/make_cover)는 상수를 내장하므로, 이 스크립트가 그 상수들이
원자료(각 사 공식 가격 문서 사본, AA 렌더 스냅숏, 알파벳 트랜스크립트, arXiv PDF)에
실제로 존재하는지 확인한다. 하나라도 실패하면 비영(non-zero)으로 종료한다.

사용법: python3 verify_sources.py   (scripts/ 어디서 실행해도 data/는 상대 경로로 찾음)
의존성: pypdf
"""
import re
import sys
import html as H
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"


def text_of(name, strip=True):
    s = (DATA / name).read_text(errors="ignore")
    if strip:
        s = re.sub(r"<script[^>]*>.*?</script>", " ", s, flags=re.S | re.I)
        s = re.sub(r"<style[^>]*>.*?</style>", " ", s, flags=re.S | re.I)
        s = re.sub(r"<[^>]+>", " ", s)
        s = H.unescape(re.sub(r"\s+", " ", s))
    return s


def pdf_text(name):
    from pypdf import PdfReader
    t = " ".join((p.extract_text() or "") for p in PdfReader(DATA / name).pages)
    return re.sub(r"\s+", " ", t)


CHECKS = [
    # (파일, [필수 문자열 또는 (라벨, 정규식)]) — 그림·본문 상수의 근거
    ("openai_pricing.html", ["gpt-5.6-sol", "gpt-5.5", "$30.00", "$15.00", "$6.00",
                             "gpt-5.5-pro", "$180.00",
                             # 표본 밖에는 더 높은 값도 있다(본문 '숫자의 기준'에 명기)
                             # HTML 엔티티(&quot;)로 인코딩돼 있어 따옴표를 느슨하게 매칭
                             ("o1-pro 입력150/출력600",
                              r'o1-pro(?:&quot;|")\],\[0,150\],\[0,null\],\[0,600\]')]),
    ("anthropic_pricing.html", ["$75", "$25", "$50", "$10", "approximately 30% more tokens",
                                "August 31", "September 1"]),
    ("google_gemini_pricing.html", ["gemini-3.5-flash", "gemini-3.6-flash", "$9.00",
                                    "$7.50", "$2.50", "$0.30"]),
    ("xai_models.html", ["$2.00", "$6.00", ("grok-4.3 입력 12500(=$1.25/1M)",
                          r'"grok-4\.3".{0,200}promptTextTokenPrice"?[:=]\s*"?12500'),
                         ("grok-4.3 출력 25000(=$2.50/1M)",
                          r'"grok-4\.3".{0,600}completionTextTokenPrice"?[:=]\s*"?25000')]),
    ("kimi_k3_pricing_rendered.txt", ["$3.00", "$15.00", "$0.30"]),
    ("kimi_k26_pricing_rendered.txt", ["$0.95", "$4.00"]),
    ("deepseek_pricing.html", ["0.435", "0.87", "0.14", "0.28"]),
    ("mistral_pricing.html", ["Medium 3.5", "Ministral 3", "$0.1"]),
    ("together_pricing.html", ["DeepSeek V4 Pro", "3.48"]),
    ("aa_cost_per_task_rendered.txt", ["$0.04", "$0.35", "$0.50", "$0.72", "$1.53",
                                       "$1.54", "$1.80", "$2.03", "$2.75",
                                       "Cost per Task", "with fallback",
                                       "Intelligence #16/190 = 53", "Intelligence #10/190 = 56",
                                       # 과제당 비용의 사이트 정의(출력 단가만의 함수가 아님)
                                       "input, cache hit, cache write, reasoning, and answer token prices",
                                       "divided by task count",
                                       # 과제당 출력 토큰은 별도 지표
                                       "Output Tokens per Intelligence Index Task"]),
    ("google_io2026_keynote.html", ["19 billion tokens per minute", "375"]),
    ("kimi_k3_blog_rendered.txt", ["2.8T-parameter", "16 out of 896",
                                   "July 27, 2026"]),
    ("tml_introducing_inkling.html", ["a third of the tokens"]),
    ("xai_grok45_announcement.html", ["Jul 16, 2026", "15,954", "67,020",
                                      "$2 per million input tokens and $6 per million output tokens"]),
    ("openai_gpt56_announcement.html", ["July 9, 2026"]),
    ("deepseek_updates.html", ["2026-04-24"]),
]

PDF_CHECKS = [
    ("alphabet_2026q1_earnings_transcript.pdf",
     ["more than 16 billion tokens per minute", "up from 10 billion last quarter",
      "330 Google Cloud customers"]),
    ("alphabet_2026q2_earnings_transcript.pdf",
     ["approximately 22 billion tokens per minute", "we continue to be supply constrained",
      "Nearly 500 Cloud customers"]),
    ("arxiv_2601.10088.pdf",
     ["0.5–0.7% increase in usage", "prompt tokens per request",
      "do not attempt to formally analyze the paradox or causality",
      "There is some evidence of", "from under 2,000 tokens in late 2023 to over 5,400"]),
]

fails = []
for fname, needles in CHECKS:
    body_raw = (DATA / fname).read_text(errors="ignore")
    body = text_of(fname)
    for n in needles:
        if isinstance(n, tuple):
            label, pat = n
            if not re.search(pat, body_raw, re.S):
                fails.append((fname, label))
        elif n not in body and n not in body_raw:
            fails.append((fname, n))

for fname, needles in PDF_CHECKS:
    body = pdf_text(fname)
    for n in needles:
        if n not in body:
            fails.append((fname, n))

# 파생 산수 검증(그림·본문에서 쓰는 계산)
import math


def _rank(vals):
    order = sorted(range(len(vals)), key=lambda i: vals[i])
    r = [0] * len(vals)
    for pos, i in enumerate(order):
        r[i] = pos + 1
    return r


def _pearson(x, y):
    mx, my = sum(x) / len(x), sum(y) / len(y)
    num = sum((a - mx) * (b - my) for a, b in zip(x, y))
    den = math.sqrt(sum((a - mx) ** 2 for a in x) * sum((b - my) ** 2 for b in y))
    return num / den


# 그림 2와 동일한 7종 (출력 단가, 과제당 비용)
_PAIRS = [(0.87, 0.04), (6.00, 0.35), (7.50, 0.50), (10.0, 1.53),
          (15.0, 0.72), (25.0, 1.80), (30.0, 1.54)]
_p = [a for a, _ in _PAIRS]
_c = [b for _, b in _PAIRS]
_rp, _rc = _rank(_p), _rank(_c)
_n = len(_PAIRS)
_spearman = 1 - 6 * sum((a - b) ** 2 for a, b in zip(_rp, _rc)) / (_n * (_n * _n - 1))
_logr = _pearson([math.log(v) for v in _p], [math.log(v) for v in _c])
_inv = sum(1 for i in range(_n) for j in range(_n) if _p[i] < _p[j] and _c[i] > _c[j])

calc = [
    ("180배(비교 15종)", abs(50 / 0.28 - 178.57) < 0.1),
    ("1,800배(표본 밖 두 사례)", abs(180 / 0.10 - 1800) < 1e-9),
    ("과제당 15%", abs(1 - 1.53 / 1.80 - 0.15) < 0.005),
    ("단가 60%", abs(1 - 10 / 25 - 0.60) < 1e-9),
    ("단가 3배·1센트", 30 / 10 == 3.0 and abs(abs(1.54 - 1.53) - 0.01) < 1e-9),
    ("K3는 Sonnet 단가 1.5배·과제당 절반 이하", 15.0 / 10.0 == 1.5 and 0.72 / 1.53 < 0.5),
    ("순위상관 0.93", abs(_spearman - 0.929) < 0.005),
    ("로그 상관 0.95", abs(_logr - 0.953) < 0.005),
    ("역전 두 쌍", _inv == 2),
]
for label, ok in calc:
    if not ok:
        fails.append(("(계산)", label))

if fails:
    print(f"FAIL: {len(fails)}건 불일치")
    for f in fails:
        print("  -", f)
    sys.exit(1)
n_str = sum(len(c[1]) for c in CHECKS) + sum(len(c[1]) for c in PDF_CHECKS)
print(f"OK: 문자열 대조 {n_str}건 + 계산 {len(calc)}건 전부 통과")
