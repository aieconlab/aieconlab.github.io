# entry-seniorization 재현성 기록

게시글 [`analysis_entry_seniorization.md`](../../../content/english/post/analysis_entry_seniorization.md)
("첫 계단은 높아졌나: 신입 일자리 시니어화의 증거와 빈칸", 게시 예정일 2026-07-24)의
그림 생성 스크립트와 원자료 출처·다운로드 시점·해시 기록.

> **관행 안내**: `docs/03-analysis/`는 원래 사이트 개선 문서 폴더였다. 이 폴더는
> 글별 분석 재현성 기록이라는 **새 관행**의 첫 사례다(2026-07-22 도입).
> 원자료 파일 자체는 용량·라이선스를 고려해 저장소에 포함하지 않고,
> URL·다운로드 시각·SHA-256만 기록한다.

## 그림 ↔ 스크립트 ↔ 원자료

| 그림 | 스크립트 | 원자료 | 다운로드(UTC) | SHA-256 |
|---|---|---|---|---|
| fig01 (미국 신규 대졸자 실업률) | `scripts/fig01_us_recent_grads.py` (다운로드·역전 에피소드 계산·플롯 통합) | [NY Fed College Labor Market CSV](https://www.newyorkfed.org/medialibrary/research/interactives/data/college-labor-market/college-labor-unemployment-data.csv) (1990-01~2026-03, 2026-05-05 갱신분) | 2026-07-21T23:58:44Z | `bc1014335fe1dade67994c15f0182526c468160b3df40c76610a903e3c40e39e` |
| fig01 보조 (계열 정의 메타) | 〃 | [chart-meta JSON](https://www.newyorkfed.org/medialibrary/research/interactives/data/college-labor-market/college-labor-chart-meta.json) | 2026-07-21T23:58:44Z | `af1074fa206e066bd70a7bf40d5ca7f81194342b09027707784a42ce78f14290` |
| fig02 (BOK 연령×노출도 분해) | `scripts/fig02_bok_pension.py` | [BOK 이슈노트 제2025-30호 PDF](https://www.bok.or.kr/fileSrc/portal/0181982e745449ca93456319a31cc0e6/1/47d99348479249c1a5ff48e9adf38ec9.pdf) (한진수·오삼일, 2025-10-30) — 수치는 노트 그림 4에 인쇄된 값만 사용 | 2026-07-21T23:49:53Z | `4939c0e355c63d17d44a9b82da2b1013cfec568a70658f27dd7089214dfd0e96` |
| fig03 (조건부 산수) | `scripts/fig03_sim.py` | 외부 자료 없음 (모형 정의는 스크립트와 `sim_results.json` 참조) | — | — |
| 커버 | `scripts/make_cover.py` | 외부 자료 없음 | — | — |

## 추출·검증 기록 (JSON)

- `nyfed_facts.json` — NY Fed 계열 정의(원문), 역전 에피소드 목록, 최신치·분기 평균, 교차검증 결과
- `bok_facts.json` — BOK 2025-30호 서지·방법·전체 분해 수치·저자 명시 한계(페이지 인용 포함)
- `sim_results.json` — 시나리오×가중 프로파일별 연도별 편차 전체 표
- `citation_checks.json` — 게시글 인용의 1차 출처 대조 결과(확인/교정 판정 포함)
- `pwc_method_check.json` — PwC ‘7배’·‘신규 스킬’·‘시니어화’ 정의의 원문(PDF 페이지·인용) 검증
- `denmark_check.json` — Humlum·Vestergaard 2026 개정판의 채용·이직/초기경력 비중 분석 범위 검증
- `anthropic_metric_check.json` — Anthropic 14% 지표(월간 신규 취업 이행률) 정의 검증

## 재실행 방법

스크립트는 실행 위치와 무관하게 동작하지만(`Path(__file__)` 기준 상대경로),
아래 명령은 이 디렉토리에서 그대로 복사해 실행할 수 있게 작성했다.
기본 출력은 `scripts/out/`, 다운로드 캐시는 `scripts/data/`이며(둘 다 커밋 제외),
`--out` 인자로 최종 경로를 지정한다.

```bash
cd docs/03-analysis/entry-seniorization   # 저장소 루트 기준
python3 -m venv .venv
.venv/bin/pip install -r requirements.lock

.venv/bin/python scripts/fig01_us_recent_grads.py --access-date 2026-07-22 \
  --out ../../../static/images/post/entry_seniorization/fig01_us_recent_grads.png
.venv/bin/python scripts/fig02_bok_pension.py --access-date 2026-07-22 \
  --out ../../../static/images/post/entry_seniorization/fig02_bok_pension.png
.venv/bin/python scripts/fig03_sim.py --json sim_results.json \
  --out ../../../static/images/post/entry_seniorization/fig03_pipeline_arithmetic.png
.venv/bin/python scripts/make_cover.py \
  --out ../../../assets/images/post/entry_seniorization_cover.png
```

- **버전 고정**: `requirements.lock`이 커밋 그림을 생성한 검증 환경
  (Python 3.13.9, pandas 2.3.3, numpy 2.3.5, matplotlib 3.10.6)을 잠근다.
  `requirements.txt`(하한만 지정)로 설치하면 렌더링이 커밋본과 미세하게 달라질 수 있다.
- **조회일 고정**: `fig01`·`fig02`의 푸터 조회일은 기본값이 실행일이므로,
  커밋본과 동일한 PNG를 원하면 `--access-date 2026-07-22`를 지정한다.
- `fig01`은 실행 시 NY Fed CSV를 재다운로드해 SHA-256을 위 표의 값과 대조하고,
  **해시가 다르면 기본값으로 중단**한다(갱신 데이터로 계속하려면 `--allow-updated-data`).
  `--data`로 로컬 CSV를 쓸 수 있다. 역전 에피소드(2021-01 시작, 63개월)는
  하드코딩이 아니라 매 실행 때 데이터에서 계산된다.
- `fig02`의 수치는 BOK 노트 그림 4에서 전사한 상수이며 출처·해시가 스크립트 머리말에 있다.
- `fig03`은 외부 자료가 없고, −0.6δ 산술을 assert로 자체 검증하며, 위 명령은
  이 폴더의 `sim_results.json`을 같은 스키마로 재생성한다.

그림 폰트 기본값은 macOS의 `Apple SD Gothic Neo`이며 다른 환경에서는
`--font`로 한글 폰트를 지정한다(폰트가 다르면 PNG는 당연히 커밋본과 달라진다).

**JSON 파일의 성격**: 스크립트가 재생성하는 것은 그림 4장과
`scripts/out/nyfed_facts_regen.json`·`sim_results.json`뿐이다. 그 밖의
`*_facts.json`·`*_check.json`은 게시 전 검증 세션에서 리뷰 에이전트가 1차 자료
(PDF·웹페이지)를 정독해 추출·기록한 **검증 기록**으로, 스크립트만으로는 재생성되지
않는다(추출 근거는 각 파일의 인용문·페이지 표기 참조).

## 주의

- NY Fed 계열의 '전체 근로자'는 CPS 16~65세·계절조정·3개월 이동평균 기준으로,
  BLS 공표 U-3와 정의가 다르다(언론의 "4.3%"와 이 데이터의 4.2% 차이의 원인).
- BOK 노트 인용 시 "BOK 이슈노트 No.2025-30에서 인용" 표기 요구(노트 p.16)를 따를 것.
- 2026-07-23 12:00 발표 청년층 부가조사 수치는 게시 전 본문의 TODO 주석 위치에 기입.
