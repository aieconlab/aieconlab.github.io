#!/opt/anaconda3/bin/python3
# -*- coding: utf-8 -*-
"""
trend20 본문·보조 수치(README 포함) 46건 검증 스크립트.

../data/ 의 원자료(취득 대장 _fetch_log.txt)만으로 본문이 '재계산'으로 표기한
모든 수치를 다시 계산해 PASS/FAIL을 출력한다(12개월 평균 +34,000처럼 발표문
수치와 겹치는 항목도 재현 가능하면 포함한다). 발표문에만 있는 수치(수정 폭,
헬스케어 등 산업 평균, 노동분배율 52.9%, 약식 90% 오차한계 ±122,000 등)는 이 스크립트의
대상이 아니며 발표문 수동 대조로 확인한다(README 참조).
실행: /opt/anaconda3/bin/python3 verify_claims.py  (모든 행이 PASS면 종료코드 0)
"""
import csv
import math
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "..", "data")


def load(name):
    rows = {}
    with open(os.path.join(DATA, name + ".csv")) as f:
        r = csv.reader(f)
        next(r)
        for row in r:
            if len(row) < 2:
                continue
            try:
                rows[row[0]] = float(row[1])
            except ValueError:
                pass
    return rows


def ann_rate(cur, prev):
    return ((cur / prev) ** 4 - 1) * 100


def log_ann(series, a, b):
    n = (int(b[:4]) - int(a[:4])) * 4 + (int(b[5:7]) - int(a[5:7])) // 3
    return math.log(series[b] / series[a]) / n * 4 * 100


def compound_ann(series, a, b):
    n = (int(b[:4]) - int(a[:4])) * 4 + (int(b[5:7]) - int(a[5:7])) // 3
    return ((series[b] / series[a]) ** (4 / n) - 1) * 100


FAILS = []


def check(label, computed, claimed, tol):
    ok = abs(computed - claimed) <= tol
    print(f"{'PASS' if ok else 'FAIL'}  {label}: 계산 {computed:+.3f} / 본문 {claimed:+g} (허용오차 {tol})")
    if not ok:
        FAILS.append(label)


def check_bool(label, cond, detail=""):
    print(f"{'PASS' if cond else 'FAIL'}  {label}{(' [' + detail + ']') if detail else ''}")
    if not cond:
        FAILS.append(label)


q2, q1, q4_25 = "2026-04-01", "2026-01-01", "2025-10-01"

# ---- 생산성 발표 블록 (전기 대비 연율, (당기/전기)^4-1) ----
oph, out_, hrs = load("OPHNFB"), load("OUTNFB"), load("HOANBS")
ulc, comp, rcomp = load("ULCNFB"), load("COMPNFB"), load("COMPRNFB")
check("2026Q2 생산성 +1.4%", ann_rate(oph[q2], oph[q1]), 1.4, 0.05)
check("2026Q2 산출 +1.7%", ann_rate(out_[q2], out_[q1]), 1.7, 0.05)
check("2026Q2 노동시간 +0.3%", ann_rate(hrs[q2], hrs[q1]), 0.3, 0.05)
check("2026Q2 ULC +1.3%", ann_rate(ulc[q2], ulc[q1]), 1.3, 0.05)
check("2026Q2 시간당 보수 +2.7%", ann_rate(comp[q2], comp[q1]), 2.7, 0.06)
check("2026Q2 실질 보수 -3.1%", ann_rate(rcomp[q2], rcomp[q1]), -3.1, 0.06)
check("생산성 전년동기비 +2.2%", (oph[q2] / oph["2025-04-01"] - 1) * 100, 2.2, 0.05)
check("2026Q1 생산성(현 빈티지) +0.8%", ann_rate(oph[q1], oph[q4_25]), 0.8, 0.05)
check("2009Q2 생산성 +9.5%", ann_rate(oph["2009-04-01"], oph["2009-01-01"]), 9.5, 0.06)
check("2009Q3 생산성 +6.5%", ann_rate(oph["2009-07-01"], oph["2009-04-01"]), 6.5, 0.06)
check("2022Q4~2026Q2 로그 연평균 약 2.5%", log_ann(oph, "2022-10-01", q2), 2.5, 0.06)
check("직전 순환(2007Q4~2019Q4) 로그 연율 1.5%", log_ann(oph, "2007-10-01", "2019-10-01"), 1.5, 0.05)
check("현 순환 로그 연율 2.0%(방법 절)", log_ann(oph, "2019-10-01", q2), 2.0, 0.05)
check("현 순환 복리 연율 2.1%(방법 절, BLS 공표 방식과 부합)", compound_ann(oph, "2019-10-01", q2), 2.1, 0.06)
check("장기(1947Q1~) 로그 연율 2.1%", log_ann(oph, "1947-01-01", q2), 2.1, 0.05)

# ---- 노동분배율 지수 ----
ls = load("PRS85006173")
check_bool("노동분배율 지수 2026Q2 = 93.5", abs(ls[q2] - 93.5) <= 0.05, f"{ls[q2]}")
check_bool("노동분배율 지수 2026Q2가 1947년 이후 시계열 최저", ls[q2] == min(ls.values()))

# ---- 고용(CES) 블록 ----
pay = load("PAYEMS")
dates = sorted(pay)
d = {dates[i]: pay[dates[i]] - pay[dates[i - 1]] for i in range(1, len(dates))}
check("2026-07 증감 -23천", d["2026-07-01"], -23, 0.5)
check("2026-02 증감 -156천", d["2026-02-01"], -156, 0.5)
check("2026-05(현 빈티지) +63천", d["2026-05-01"], 63, 0.5)
check("2026-06(현 빈티지) +20천", d["2026-06-01"], 20, 0.5)
neg12 = [k for k in dates if "2025-08-01" <= k <= "2026-07-01" and d.get(k, 0) < 0]
check_bool("2025-08~2026-07 점추정치 음수 5회", len(neg12) == 5, ",".join(k[:7] for k in neg12))
w1 = [d[k] for k in dates if "2025-07-01" <= k <= "2026-06-01"]
w2 = [d[k] for k in dates if "2025-08-01" <= k <= "2026-07-01"]
check("직전 12개월(2025-07~2026-06) 평균 +34천(BLS 창)", sum(w1) / len(w1), 34, 0.6)
check("12개월(2025-08~2026-07) 평균 +26천", sum(w2) / len(w2), 26, 0.6)
priv, govt = load("USPRIV"), load("USGOVT")
check("민간 2026-07 +30천", priv["2026-07-01"] - priv["2026-06-01"], 30, 0.5)
check("정부 2026-07 -53천", govt["2026-07-01"] - govt["2026-06-01"], -53, 0.5)
edu, ret, fin = load("CES9093161101"), load("USTRADE"), load("USFIRE")
check("지방정부 교육 -50천", edu["2026-07-01"] - edu["2026-06-01"], -50, 0.6)
check("소매 -19천", ret["2026-07-01"] - ret["2026-06-01"], -19, 0.6)
check("금융 -14천", fin["2026-07-01"] - fin["2026-06-01"], -14, 0.6)
ahe = load("CES0500000003")
check_bool("시간당 평균임금 $37.62(+2센트)", abs(ahe["2026-07-01"] - 37.62) < 0.005 and abs(ahe["2026-07-01"] - ahe["2026-06-01"] - 0.02) < 0.005)
yy = (ahe["2026-07-01"] / ahe["2025-07-01"] - 1) * 100
lower = [k for k in sorted(ahe) if k >= "2021-06-01" and k >= sorted(ahe)[12] and (ahe[k] / ahe[sorted(ahe)[sorted(ahe).index(k) - 12]] - 1) * 100 < yy]
check("임금 전년비 +3.2%", yy, 3.2, 0.06)
check_bool("임금 전년비가 2021년 5월 이후 최저", len(lower) == 0, f"2021-06 이후 더 낮았던 달: {[k[:7] for k in lower]}")

# ---- 가구조사(CPS) 블록 ----
part, emr, unr, unl = load("CIVPART"), load("EMRATIO"), load("UNRATE"), load("UNEMPLOY")
check_bool("실업률 4.1%(전월 4.2%)", unr["2026-07-01"] == 4.1 and unr["2026-06-01"] == 4.2)
check_bool("실업자 약 690만", abs(unl["2026-07-01"] - 6900) < 50, f"{unl['2026-07-01']:.0f}천")
check_bool("참가율 61.4%(1월 62.1%, 차 -0.7%p)", part["2026-07-01"] == 61.4 and part["2026-01-01"] == 62.1)
since = [k for k in sorted(part) if "2021-03-01" <= k <= "2026-06-01" and part[k] <= 61.4]
check_bool("61.4%는 2021년 2월 이후 처음", len(since) == 0, f"그 사이 61.4 이하: {[k[:7] for k in since]}")
check_bool("고용률 58.9%(1월 59.4%, 차 -0.5%p)", emr["2026-07-01"] == 58.9 and emr["2026-01-01"] == 59.4 and abs(emr["2026-07-01"] - emr["2026-01-01"] + 0.5) < 1e-6)
y1, y2, y3 = load("LNS14000012"), load("LNS14000036"), load("LNS14000089")
check_bool("16~19세 12.1%(전월 14.6%, 전년 15.2%)", y1["2026-07-01"] == 12.1 and y1["2026-06-01"] == 14.6 and y1["2025-07-01"] == 15.2)
check_bool("20~24세 7.1%(전년 7.9%)", y2["2026-07-01"] == 7.1 and y2["2025-07-01"] == 7.9)
check_bool("25~34세 4.6%(전년 4.3%)", y3["2026-07-01"] == 4.6 and y3["2025-07-01"] == 4.3)
ree, new = load("LNS13023557"), load("LNS13023569")
dr = ree["2026-07-01"] - ree["2026-06-01"]
dn = new["2026-07-01"] - new["2026-06-01"]
check("재진입자 -114천", dr, -114, 0.5)
check("신규 진입자 -11천", dn, -11, 0.5)
check("진입자 합산 -125천", dr + dn, -125, 0.5)

# ---- 뉴욕 연은 블록 ----
rows = list(csv.DictReader(open(os.path.join(DATA, "nyfed_college_unemployment.csv"))))
streak, start = 0, None
for r in rows:
    if float(r["Recent graduates"]) > float(r["All workers"]):
        if streak == 0:
            start = r["Date"]
        streak += 1
    else:
        streak, start = 0, None
last = rows[-1]
check_bool("뉴욕 연은 역전 66개월(2021-01~2026-06)", streak == 66 and start == "1/1/2021" and last["Date"] == "6/1/2026",
           f"{start}~{last['Date']}, {streak}개월")
check("신규 대졸자 2026-06 5.7%", float(last["Recent graduates"]), 5.7, 0.05)
check("같은 계열 전체 근로자 2026-06 4.1%", float(last["All workers"]), 4.1, 0.06)

print()
if FAILS:
    print(f"FAIL {len(FAILS)}건: {FAILS}")
    sys.exit(1)
print("모든 주장 PASS")
