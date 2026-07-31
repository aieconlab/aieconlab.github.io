#!/usr/bin/env python3
"""BEA NIPA Section 1 워크북에서 이 글이 쓰는 계열만 뽑아 CSV로 저장한다.

입력: ../data/Section1All_xls.xlsx
      (https://apps.bea.gov/national/Release/XLS/Survey/Section1All_xls.xlsx,
       2026-07-30 미국 2분기 GDP 속보치 반영본)
출력: ../data/bea_extract.csv

인터프리터: /opt/anaconda3/bin/python3
"""
import csv
import hashlib
import os

import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
SRC = os.path.join(DATA, "Section1All_xls.xlsx")
OUT = os.path.join(DATA, "bea_extract.csv")
# 원천 워크북 SHA-256 (README 원자료 대장과 일치해야 한다)
SRC_SHA = "ddcd0c5b693cb5d179198e67dda60f817e0e97196e6f1c158152971bbc80b136"

# (시트, 표 이름, 계열코드) — 코드는 BEA NIPA 시리즈 코드
SHEETS = {
    "T10502-Q": "T1.5.2 기여도(%p, 연율)",
    "T10501-Q": "T1.5.1 실질 증가율(%, 연율)",
    "T10504-Q": "T1.5.4 가격지수(2017=100)",
    "T10505-Q": "T1.5.5 명목 수준(백만 달러)",
}
CODES = [
    "A191RL", "A191RC",          # GDP
    "A008RL", "A008RC", "A008RY",  # 비주거 고정투자
    "Y033RL", "Y033RC", "Y033RY", "Y033RG",  # 장비
    "Y034RL", "Y034RC", "Y034RY", "Y034RG",  # 정보처리장비
    "Y001RL", "Y001RC", "Y001RY", "Y001RG",  # 지식재산생산물
    "B985RL", "B985RC", "B985RY", "B985RG",  # 소프트웨어
    "Y006RY", "Y020RY",          # R&D, 오락·문학·예술 원작
    "A014RY", "A020RY", "A021RY",  # 재고, 수출, 수입
]
QUARTERS = [f"{y}Q{q}" for y in range(2015, 2027) for q in range(1, 5)]


def main() -> None:
    with open(SRC, "rb") as fh:
        got = hashlib.sha256(fh.read()).hexdigest()
    if got != SRC_SHA:   # assert는 python -O에서 제거되므로 명시적 예외로 검사한다
        raise SystemExit(f"원천 워크북이 바뀌었다: {got}")
    wb = openpyxl.load_workbook(SRC, read_only=True)
    rows_out = []
    for sheet, table in SHEETS.items():
        ws = wb[sheet]
        rows = list(ws.iter_rows(values_only=True))
        header = [str(c) for c in rows[7]]
        cols = {q: header.index(q) for q in QUARTERS if q in header}
        for r in rows[8:]:
            if not r or len(r) < 4 or r[2] not in CODES:
                continue
            label = str(r[1]).strip()
            for q, i in cols.items():
                rows_out.append(
                    {"table": table, "code": r[2], "label": label,
                     "quarter": q, "value": r[i]}
                )
    # --- 검산: 워크북이 2026년 2분기 속보치 반영본인지, 공표치가 맞는지 -------
    meta = str(wb["T10502-Q"]["A3"].value) + " " + str(wb["T10502-Q"]["A5"].value)
    assert "2026Q2" in meta, meta          # "Quarterly data from 1947Q2 to 2026Q2"
    assert "July 30, 2026" in meta, meta   # "Data published July 30, 2026"

    v = {(r["code"], r["quarter"]): r["value"] for r in rows_out
         if r["table"].startswith("T1.5.2") or r["table"].startswith("T1.5.1")}
    checks = {                              # BEA 공표치
        ("A191RL", "2026Q2"): 1.5, ("A191RL", "2026Q1"): 2.1,
        ("Y034RY", "2026Q2"): 0.19, ("Y034RY", "2026Q1"): 0.77,
        ("Y001RY", "2026Q2"): 0.48, ("Y001RY", "2026Q1"): 0.74,
        ("Y034RL", "2026Q2"): 8.3, ("Y034RL", "2026Q1"): 39.9,
        ("A021RY", "2026Q2"): -1.51,
    }
    for key, expected in checks.items():
        got = v.get(key)
        assert got is not None and abs(got - expected) < 0.005, (key, got, expected)

    # 중단 시 CSV가 반쯤 쓰인 채 남지 않도록 임시파일에 쓴 뒤 원자적으로 교체한다
    tmp = OUT + ".tmp"
    with open(tmp, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["table", "code", "label", "quarter", "value"])
        w.writeheader()
        w.writerows(rows_out)
    os.replace(tmp, OUT)
    print(f"{len(rows_out)} rows -> {OUT}  ({len(checks)}건 공표치 대조 통과)")


if __name__ == "__main__":
    main()
