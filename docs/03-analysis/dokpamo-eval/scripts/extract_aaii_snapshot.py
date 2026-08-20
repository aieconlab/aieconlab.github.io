#!/usr/bin/env python3
"""artificialanalysis.ai 모델 페이지(HTML 스냅샷)에 내장된 JSON에서 Intelligence Index를 추출한다.

입력: data/raw-local/artificialanalysis_models_motif-3_*.html (제3자 페이지 사본, git 제외)
출력: data/aaii_snapshot.json (모델 슬러그·이름·AA 등재일·intelligenceIndex·오픈웨이트 여부)
실행: cd docs/03-analysis/dokpamo-eval && python3 scripts/extract_aaii_snapshot.py
"""
import glob, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
files = sorted(glob.glob(str(ROOT / 'data/raw-local/artificialanalysis_models_motif-3_*.html')))
if not files:
    sys.exit('raw-local HTML 스냅샷이 없습니다 (재취득 필요: https://artificialanalysis.ai/models/motif-3)')
x = open(files[-1], encoding='utf-8', errors='ignore').read().replace('\\"', '"')
recs = {}
for m in re.finditer(r'"slug":"([a-z0-9\-\.]+)","name":"([^"]+)","shortName":"([^"]+)","releaseDate":"([^"]*)"', x):
    slug, name, short, rel = m.groups()
    seg = x[m.start(): m.start() + 6000]
    ii = re.search(r'"intelligenceIndex":([0-9.]+)', seg)
    ow = re.search(r'"isOpenWeights":(true|false)', seg)
    if ii and slug not in recs:
        recs[slug] = {'name': name, 'aa_release_date': rel, 'intelligence_index': round(float(ii.group(1)), 1),
                      'open_weights': (ow.group(1) == 'true') if ow else None}
KR = ['motif-3', 'solar-open2-250b', 'a-x-k2', 'k-exaone-2-0-0803']
TOP = ['claude-opus-5', 'gpt-5-6-sol', 'grok-4-6', 'kimi-k3', 'qwen3-8-max', 'qwen3-8-2-4t-a95b',
       'muse-spark-1-2', 'gemini-3-7-flash', 'deepseek-v4-pro', 'glm-5-2']
missing = [k for k in KR + TOP if k not in recs]
if missing:
    sys.exit(f'FAIL: 스냅샷에서 다음 모델을 찾지 못했습니다(빈 HTML이거나 페이지 구조 변경): {missing}')
# 검증을 먼저 통과해야 JSON을 쓴다: 보도자료 표(반올림 정수)와 대조, 불일치면 비정상 종료
expect = {'motif-3': 47, 'solar-open2-250b': 37, 'a-x-k2': 35, 'k-exaone-2-0-0803': 31,
          'claude-opus-5': 63, 'gpt-5-6-sol': 61, 'grok-4-6': 61, 'kimi-k3': 60, 'qwen3-8-max': 58,
          'muse-spark-1-2': 57, 'gemini-3-7-flash': 56, 'deepseek-v4-pro': 53, 'glm-5-2': 53}
bad = {k: (recs[k]['intelligence_index'], v) for k, v in expect.items() if round(recs[k]['intelligence_index']) != v}
if bad:
    sys.exit(f'FAIL: 보도자료 표(정수)와 반올림 불일치 — JSON을 저장하지 않음: {bad}')
out = {'source_file': Path(files[-1]).name, 'korean_models': {k: recs[k] for k in KR},
       'reference_models': {k: recs[k] for k in TOP}}
(ROOT / 'data/aaii_snapshot.json').write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
for k in KR + TOP:
    print(f"{recs[k]['intelligence_index']:5.1f}  {k:22s} {recs[k]['name']}")
print('보도자료 표 대조: PASS')
