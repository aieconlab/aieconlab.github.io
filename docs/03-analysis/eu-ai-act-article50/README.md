# trend18 원자료 대장 — EU AI법 제50조 투명성 행동강령 서명자 명단

게시글: `content/english/post/trend18_eu_ai_act_article50.md`

## 파일 대장 (SHA-256)

| 파일 | 성격 | SHA-256 |
|---|---|---|
| `data/ec_signatories_news_20260802.html` | 원문 스냅샷 | `a2addb870df3c76231bff5ec45a245386e232bd6ca9b6ed7857fd8b47746864b` |
| `data/aliases.json` | 검색 그룹 29종 + 보조검사 패턴 사전 | `3963c0b024109334bd8e310e4ffc71bbd4075aa423e4d07d6e9759802a6c7ce1` |
| `extract_and_match.py` | 추출·대조 파이프라인 (재현 스크립트, 83/152/29종 0건 assertion 포함) | `ef404cf34857d1094e864a6910acd6679e7d38df09edd74e1b2fad459479020a` |
| `data/signatory_table_extracted.json` | 파생: 표 행 단위 추출 | `d6594f96e6bfff2a6f3a894e433436e751d1616d9c6726b877fb0b8ade1f4861` |
| `data/signatories_flat.json` | 파생: 섹션1·섹션2 평탄화 | `73aee52ec2241b23fd5007062156f5a205678d2b3b42eee6bd589ef02ed4bd6c` |
| `data/match_results.json` | 파생: 후보별 대조 결과 (전 항목 0건) | `5b1c80ee598de8c361941838bfa22218eb0f465ed1e0964d8e20971dbe4a7747` |
| `scripts/make_figures.py` | 그림 3종 생성 스크립트 (커버·그림1·그림2, 서명 수치는 match_results.json에서 검산) | `135be10d1ce3fb21763d2c25792b1f0ae2c6f3c710123d69370227a169884767` |

- 원문 출처 URL: <https://digital-strategy.ec.europa.eu/en/news/strong-backing-code-practice-transparency-ai-generated-content>
- 취득 시각: 2026-08-02 12:45:06 KST

## 재현

```bash
python3 extract_and_match.py
# 기대 출력: 섹션1 83건 / 섹션2 152건 / 후보 29종 매칭 0건 / 보조검사 매칭 0건
```

스크립트가 원문 HTML에서 표 추출 → 평탄화 → `aliases.json` 대조 → `match_results.json` 기록까지 전 과정을 수행한다. 파생 JSON 3종은 스크립트 실행으로 재생성된다.

그림 3종은 `scripts/make_figures.py`로 재생성한다(인터프리터 `/opt/anaconda3/bin/python3`, 실행시각 메타데이터 제거). 출력은 `scripts/out/`이며 게시 경로는 커버 `assets/images/post/trend18_cover.png`, 본문 그림 `static/images/post/trend18/fig01_schedule_shift.png`·`fig02_kr_eu_timeline.png`.

## 집계 대조

- 섹션 1(제공자) 서명 **83건**, 섹션 2(배포자) 서명 **152건** — 집행위 본문 서술("83 signatures ... 152 signatures", "about 190 organisations")과 일치.
- 83 + 152 = 235건 > 약 190곳: 양쪽 섹션 중복 서명 존재의 산술적 근거.

## '국내 주요 AI 기업·서비스 명칭 비확인' 판정 기준과 한계

- **모집단 정의**: 이 판정의 모집단은 '한국 기업 전체'가 아니라 **분석을 위해 구성한 국내 AI 생태계 관련 기업·서비스 검색 그룹 29종**이다. 한국 본사 기업(카카오·네이버·삼성 등), 한국계 창업 해외법인(몰로코, 트웰브랩스), 국내 대기업 계열(LG·SK·KT·현대 등), 대표 서비스·모델명(클로바, 엑사원, 솔라)을 포함한다. 후보 전체 목록과 정규식 패턴은 `data/aliases.json` 참조.
- 짧은 토큰(LG, SK, KT, LINE, NC, KR)은 단어 경계(`\b`)로 오탐을 방지했다.
- 보조 검사: `Korea`·`Seoul` 문자열 및 `KR` 토큰(단어 경계) 검사.
- **결과**: 서명 235건 전체 대비 후보 29종 매칭 0건, 보조검사 0건 (2026-08-02 12:45 KST 스냅샷 기준). 항목별 결과는 `data/match_results.json`.
- **한계 (본문에 명시)**: ① 명단에 국적·본점 소재지 열이 없어 약 190개 서명 주체 전체의 국적을 전수 판정한 것은 아님. ② 후보 목록에 없는 소규모 한국 기업이나 해외 법인명으로 서명한 계열사는 놓칠 수 있음. ③ 명단은 상시 갱신되므로 스냅샷 이후 달라질 수 있음. → 본문·제목은 "한국 기업 0곳"이 아니라 "**국내 주요 AI 기업은 보이지 않았다 / 분석을 위해 정한 검색 그룹 29종의 명칭이 확인되지 않았다**"로 표기한다.
