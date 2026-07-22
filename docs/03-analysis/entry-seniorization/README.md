# entry-seniorization 재현성 기록

게시글 [`analysis_entry_seniorization.md`](../../../content/english/post/analysis_entry_seniorization.md)
("첫 계단은 높아졌나: 신입 일자리 시니어화의 증거와 빈칸", 2026-07-24 게시)의
그림 생성 스크립트와 원자료 출처·다운로드 시점·해시 기록.

> **관행 안내**: `docs/03-analysis/`는 원래 사이트 개선 문서 폴더였다. 이 폴더는
> 글별 분석 재현성 기록이라는 **새 관행**의 첫 사례다(2026-07-22 도입).
> 원자료 파일 자체는 용량·라이선스를 고려해 저장소에 포함하지 않고,
> URL·다운로드 시각·SHA-256만 기록한다.

## 그림 ↔ 스크립트 ↔ 원자료

| 그림 | 스크립트 | 원자료 | 다운로드(UTC) | SHA-256 |
|---|---|---|---|---|
| fig01 (미국 신규 대졸자 실업률) | `scripts/analyze_nyfed.py` (분석) + `scripts/plot_fig01.py` (플롯) | [NY Fed College Labor Market CSV](https://www.newyorkfed.org/medialibrary/research/interactives/data/college-labor-market/college-labor-unemployment-data.csv) (1990-01~2026-03, 2026-05-05 갱신분) | 2026-07-21T23:58:44Z | `bc1014335fe1dade67994c15f0182526c468160b3df40c76610a903e3c40e39e` |
| fig01 보조 (계열 정의 메타) | 〃 | [chart-meta JSON](https://www.newyorkfed.org/medialibrary/research/interactives/data/college-labor-market/college-labor-chart-meta.json) | 2026-07-21T23:58:44Z | `af1074fa206e066bd70a7bf40d5ca7f81194342b09027707784a42ce78f14290` |
| fig02 (BOK 연령×노출도 분해) | `scripts/fig02_bok_pension.py` | [BOK 이슈노트 제2025-30호 PDF](https://www.bok.or.kr/fileSrc/portal/0181982e745449ca93456319a31cc0e6/1/47d99348479249c1a5ff48e9adf38ec9.pdf) (한진수·오삼일, 2025-10-30) — 수치는 노트 그림 4에 인쇄된 값만 사용 | 2026-07-21T23:49:53Z | `4939c0e355c63d17d44a9b82da2b1013cfec568a70658f27dd7089214dfd0e96` |
| fig03 (조건부 산수) | `scripts/fig03_sim.py` | 외부 자료 없음 (모형 정의는 스크립트와 `sim_results.json` 참조) | — | — |
| 커버 | `scripts/make_cover.py` | 외부 자료 없음 | — | — |

## 추출·검증 기록 (JSON)

- `nyfed_facts.json` — NY Fed 계열 정의(원문), 역전 에피소드 목록, 최신치·분기 평균, 교차검증 결과
- `bok_facts.json` — BOK 2025-30호 서지·방법·전체 분해 수치·저자 명시 한계(페이지 인용 포함)
- `sim_results.json` — 시나리오×가중 프로파일별 연도별 편차 전체 표
- `citation_checks.json` — 게시글 인용 8건의 1차 출처 대조 결과(확인/교정 판정 포함)

## 재실행 방법

```bash
python3 scripts/analyze_nyfed.py   # CSV 재다운로드·재계산 (해시 변동 시 데이터 갱신분)
python3 scripts/plot_fig01.py
python3 scripts/fig02_bok_pension.py
python3 scripts/fig03_sim.py
python3 scripts/make_cover.py
```

의존성: `python3` + `pandas`, `matplotlib`, `openpyxl`. 그림 폰트는 macOS의
`Apple SD Gothic Neo`를 사용한다(다른 환경에서는 나눔고딕 등으로 대체 필요).
스크립트 내 경로는 작성 당시 세션의 절대경로이므로 재실행 시 경로 상수를 수정할 것.

## 주의

- NY Fed 계열의 '전체 근로자'는 CPS 16~65세·계절조정·3개월 이동평균 기준으로,
  BLS 공표 U-3와 정의가 다르다(언론의 "4.3%"와 이 데이터의 4.2% 차이의 원인).
- BOK 노트 인용 시 "BOK 이슈노트 No.2025-30에서 인용" 표기 요구(노트 p.16)를 따를 것.
- 2026-07-23 12:00 발표 청년층 부가조사 수치는 게시 전 본문의 TODO 주석 위치에 기입.
