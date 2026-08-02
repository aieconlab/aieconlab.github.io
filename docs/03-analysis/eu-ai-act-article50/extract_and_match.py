#!/usr/bin/env python3
"""trend18: EU 투명성 행동강령 서명자 명단에서 국내 주요 기업·서비스 후보를 대조한다.

입력:  data/ec_signatories_news_20260802.html (집행위 페이지 스냅샷)
       data/aliases.json                      (후보 29종 + 보조검사 패턴)
출력:  data/signatory_table_extracted.json    (표 행 단위 추출)
       data/signatories_flat.json             (섹션1·섹션2 평탄화 목록)
       data/match_results.json                (후보별 대조 결과)

실행:  python3 extract_and_match.py   (이 파일이 있는 디렉터리에서)
"""
import html
import json
import re
from pathlib import Path

DATA = Path(__file__).parent / "data"

raw = (DATA / "ec_signatories_news_20260802.html").read_text(encoding="utf-8")

# 1) 페이지 유일의 <table>에서 행/셀 추출
table = re.search(r"<table.*?</table>", raw, re.S).group(0)
rows = []
for tr in re.findall(r"<tr.*?</tr>", table, re.S):
    cells = [
        html.unescape(re.sub(r"<[^>]+>", "", td)).strip()
        for td in re.findall(r"<t[dh].*?</t[dh]>", tr, re.S)
    ]
    rows.append(cells)
(DATA / "signatory_table_extracted.json").write_text(
    json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8"
)

# 2) 섹션별 평탄화 (첫 행은 머리글)
s1 = [r[0] for r in rows[1:] if r and r[0]]
s2 = [r[1] for r in rows[1:] if len(r) > 1 and r[1]]
(DATA / "signatories_flat.json").write_text(
    json.dumps({"section1": s1, "section2": s2}, ensure_ascii=False, indent=1),
    encoding="utf-8",
)
allnames = s1 + s2

# 3) 후보 대조
spec = json.loads((DATA / "aliases.json").read_text(encoding="utf-8"))
results = {"counts": {"section1": len(s1), "section2": len(s2)}, "matches": [], "auxiliary": []}
for group_key, out_key in (("aliases", "matches"), ("보조검사", "auxiliary")):
    for item in spec[group_key]:
        rx = re.compile(item["pattern"], re.I)
        hit = [n for n in allnames if rx.search(n)]
        results[out_key].append({"label": item["label"], "pattern": item["pattern"], "hits": hit})
(DATA / "match_results.json").write_text(
    json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8"
)

total_hits = sum(len(m["hits"]) for m in results["matches"])
aux_hits = sum(len(m["hits"]) for m in results["auxiliary"])
print(f"섹션1 {len(s1)}건 / 섹션2 {len(s2)}건 / 후보 {len(results['matches'])}종 매칭 {total_hits}건 / 보조검사 매칭 {aux_hits}건")

# 게시 시점 확정치 검증: 집계·검색 그룹 수·매칭 결과가 기대값과 다르면 비정상 종료한다.
assert len(s1) == 83, f"섹션1 기대 83건, 실제 {len(s1)}건"
assert len(s2) == 152, f"섹션2 기대 152건, 실제 {len(s2)}건"
assert len(results["matches"]) == 29, f"후보 기대 29종, 실제 {len(results['matches'])}종"
assert total_hits == 0 and aux_hits == 0, f"매칭 기대 0건, 실제 후보 {total_hits}건·보조 {aux_hits}건"
print("검증 통과: 83 / 152 / 29종 0건 / 보조 0건")
