#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""보존 자료의 문자열 존재와 내부 계산을 확인하는 회귀 장치.

**이 스크립트가 하는 일과 하지 않는 일을 분명히 해 둔다.**
- 한다: 본문·그림이 쓰는 값들이 `data/` 원자료 사본에 문자열(또는 정규식)로 실재하는지
  확인하고, 파생 산수(배수·인하율·상관계수·역전 쌍 수)를 자체 재계산해 표기와 대조한다.
- 하지 않는다: 본문(.md)이나 그림 스크립트를 파싱해 값을 끌어오지 않는다. 따라서 어떤 값이
  원자료에 존재하기만 하면, 그것을 **잘못된 비교 기준으로 쓰는 오류는 잡지 못한다**
  (실제로 3차 개고 전까지 $9와 $7.50이 모두 원자료에 있었지만 구글의 비교 기준을 2.5 Flash로
  잘못 잡은 오류를 이 스크립트는 통과시켰다). 비교 기준의 타당성은 사람이 검토해야 한다.
하나라도 실패하면 비영(non-zero)으로 종료한다.

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
    # 3.6 Flash는 2026-07-21 GA이고 공식 릴리스 노트가 3.5 Flash보다 싸다고 명시
    ("google_gemini_changelog.html", ["July 21, 2026", "gemini-3.6-flash",
                                      "lower price point than 3.5 Flash"]),
    ("google_blog_gemini36_ko.html", ["출력 토큰 사용량을 17% 줄였", "7.50 달러",
                                      "에이전틱 작업의 전체 비용"]),
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
    """동점은 평균 순위(Opus 4.8·Opus 5의 출력 단가가 $25로 동일)."""
    n = len(vals)
    idx = sorted(range(n), key=lambda i: vals[i])
    r = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and vals[idx[j + 1]] == vals[idx[i]]:
            j += 1
        avg = (i + j) / 2 + 1
        for k in range(i, j + 1):
            r[idx[k]] = avg
        i = j + 1
    return r


def _pearson(x, y):
    mx, my = sum(x) / len(x), sum(y) / len(y)
    num = sum((a - mx) * (b - my) for a, b in zip(x, y))
    den = math.sqrt(sum((a - mx) ** 2 for a in x) * sum((b - my) ** 2 for b in y))
    return num / den


# 그림 2와 동일한 8종 (출력 단가, 과제당 비용) — AA 9종 중 Fable 5(폴백)만 제외
_PAIRS = [(0.87, 0.04), (6.00, 0.35), (7.50, 0.50), (10.0, 1.53),
          (15.0, 0.72), (25.0, 1.80), (25.0, 2.03), (30.0, 1.54)]
_p = [a for a, _ in _PAIRS]
_c = [b for _, b in _PAIRS]
_n = len(_PAIRS)
_spearman = _pearson(_rank(_p), _rank(_c))   # _rank는 동점 평균 순위
_logr = _pearson([math.log(v) for v in _p], [math.log(v) for v in _c])
_inv = sum(1 for i in range(_n) for j in range(_n) if _p[i] < _p[j] and _c[i] > _c[j])

calc = [
    ("180배(비교 15종)", abs(50 / 0.28 - 178.57) < 0.1),
    ("1,800배(표본 밖 두 사례)", abs(180 / 0.10 - 1800) < 1e-9),
    ("과제당 15%", abs(1 - 1.53 / 1.80 - 0.15) < 0.005),
    ("단가 60%", abs(1 - 10 / 25 - 0.60) < 1e-9),
    ("단가 3배·1센트", 30 / 10 == 3.0 and abs(abs(1.54 - 1.53) - 0.01) < 1e-9),
    ("K3는 Sonnet 단가 1.5배·과제당 절반 이하", 15.0 / 10.0 == 1.5 and 0.72 / 1.53 < 0.5),
    ("동일 단가 $25의 과제당 13% 차", abs(2.03 / 1.80 - 1 - 0.128) < 0.002),
    ("구글 인하 16.7%", abs((1 - 7.5 / 9.0) - 0.1667) < 0.0005),
    ("순위상관 0.90(8종)", abs(_spearman - 0.898) < 0.005),
    ("로그 상관 0.96(8종)", abs(_logr - 0.958) < 0.005),
    ("역전 세 쌍(8종)", _inv == 3),
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
