# gdp-q2-surprise 재현성 기록

게시글 [`trend13_gdp_q2_surprise.md`](../../../content/english/post/trend13_gdp_q2_surprise.md)
("0.2%가 0.6%가 됐다: 2분기 깜짝 성장은 'AI 경제'의 실증인가", 2026-07-24 게시)의
그림 생성 스크립트와 원자료 출처·다운로드 시점·해시 기록.

> 관행: `docs/03-analysis/`의 글별 재현성 기록(2026-07-22 도입, 첫 사례
> `entry-seniorization/`)을 따른다. 원자료 파일 자체는 저장소에 포함하지 않고
> URL·다운로드 시각·SHA-256만 기록한다(`scripts/data/`, `scripts/out/`은 gitignore).

## 그림 ↔ 스크립트 ↔ 원자료

| 그림 | 스크립트 | 원자료 | 다운로드(UTC) | SHA-256 |
|---|---|---|---|---|
| fig01 (연간 성장률 등가 경로) | `scripts/fig01_growth_paths.py` (다운로드·환산·검산·플롯 통합) | [FRED NGDPRSAXDCKRQ CSV](https://fred.stlouisfed.org/graph/fredgraph.csv?id=NGDPRSAXDCKRQ) (분기 실질 GDP 수준, 계절조정, 원자료 IMF IFS, 1960Q1~2026Q1) | 2026-07-23T08:28:40Z | `02c1cf857933937b127c7d0819fe9cf77ca21acbd04e242ce5b09db48337d6d0` |
| fig01 입력 상수 | `Q2_QOQ = 0.0062` | 2026Q2 전기비 비반올림치. 공표 반올림치는 0.6%. [이데일리](https://www.edaily.co.kr/News/Read?mediaCodeNo=257&newsId=03535846645517472)·[프라임경제](https://www.newsprime.co.kr/news/article/?no=741240) 2026.7.23 보도(기자설명회 확인치)로 교차 확인 | - | - |
| (수치 대조용) | - | [한국은행 2026년 2/4분기 실질 국내총생산(속보) PDF](https://www.bok.or.kr/fileSrc/portal/5da95fdb53e84fdda0195ea72aea9f51/2/8afc636f6dd444f29725d9420df1f832.pdf) (공보 2026-07-23호, [상세 페이지](https://www.bok.or.kr/portal/bbs/B0000501/view.do?menuNo=201264&nttId=11063107)) | 2026-07-23T10:43Z | `ecab52e61aa3c02685d95a9766cb348ff2b642edf110e793e8f4a77d5e721448` |
| 커버 | `scripts/make_cover.py` | 외부 자료 없음 (0.2%·0.6%는 본문 수치) | - | - |

## 재현 명령

```bash
cd docs/03-analysis/gdp-q2-surprise
python3 -m venv .venv                     # matplotlib이 없는 환경 대비 격리 환경
.venv/bin/pip install -r requirements.lock
cd scripts
../.venv/bin/python fig01_growth_paths.py            # 캐시(data/krgdp.csv)가 있으면 캐시 우선 사용
../.venv/bin/python fig01_growth_paths.py --refresh  # 검증 통과한 응답만 캐시를 원자적으로 교체
../.venv/bin/python fig01_growth_paths.py --offline  # 캐시 필수, 네트워크 미사용
../.venv/bin/python make_cover.py
# 산출물: out/fig01_growth_paths.png, out/trend13_cover.png, ../calc_results.json
# 게시 경로 복사: static/images/post/trend13/fig01_growth_paths.png,
#                assets/images/post/trend13_cover.png
```

데이터 보호 장치: ① 원자료 SHA-256이 아래 표의 기록과 다르면 실행이 중단되며,
개정 데이터를 반영하려면 `--allow-updated-data`로 실행해 검산 assert 통과를
확인한 뒤 스크립트의 `EXPECTED_SHA256`과 이 표를 갱신한다. ② 수치 assert는
주요 파생값의 범위 검사이고, 계열 자체의 변경 감지는 SHA 검사가 담당한다.
③ `--refresh`는 임시 파일로 받아 CSV 스키마·필수 분기 검증과 SHA 승인까지
통과한 응답만 캐시를 원자적으로 교체하므로, 오류 응답도 미승인 개정 데이터도
기존 캐시를 파괴하지 않는다.

게시된 PNG 2장(그림 1, 커버)은 위 잠금 환경(`.venv`)에서 생성한 정본이다
(동일 환경 2회 실행에서 바이트 일치 확인). matplotlib을 다른 방식으로 설치한
환경(예: 시스템 파이썬의 다른 빌드)은 내장 폰트 래스터라이저 차이로 픽셀이
미세하게 달라질 수 있어, 바이트 재현은 잠금 환경 기준으로만 보장한다.

`calc_results.json`에는 원자료의 공식 URL(`data_source`)과 저장소 상대 캐시
경로(`cache_path_repo_relative`)만 기록한다(저장소 밖 경로를 지정하면 null로
비식별 처리). `cache_mtime_utc`는 사용/갱신된 캐시 파일의 수정 시각으로, 파일
복사 방식에 따라 실제 다운로드 시각과 다를 수 있다. 다운로드 시각의 공식
기록은 위 표를 따르고, `verified_at_utc`는 스크립트 실행 시각이다. JSON과
PNG는 수치 검산과 그림 레이아웃 검사(라벨·주석·축 제목 겹침, 렌더러 좌표
기준)를 모두 통과한 뒤에만 기록된다.

## 계산 방법과 검산(assert)

- 연간 성장률 = 2026년 4개 분기 평균 수준 / 2025년 4개 분기 평균 수준 - 1.
  2026Q2 = 2026Q1 x 1.0062(비반올림 전기비), 이후 분기는 공통 전기비 g 적용.
- '7월 15일 기준' 곡선은 trend11 글(그림 1)과 동일 규칙(1분기까지 실적,
  남은 3개 분기에 g). 스크립트가 다음을 assert로 확인한다:
  - 2026Q1 전기비 1.83% 내외(trend11 본문과 일치. 공표 반올림치 1.8%)
  - 2025년 분기 경로: FRED 계열이 속보 PDF 표(-0.2, 0.6, 1.4, -0.1)와
    반올림 일치함을 수기 대조(2026-07-23)
  - 구곡선: g=0 → 2.6% 내외, 3.0% 필요 g = 0.26% 내외(trend11 본문과 일치)
  - 신곡선: g=0 → 3.078%(반올림 3.1%), g=-0.1% → 3.001%(한국은행 설명회
    '하반기 평균 -0.1%여도 연 3%' 산술과 오차 0.02%p 이내로 일치)
  - 2025년 연간 성장률 1.1% 내외([한국은행 2025년 국민계정(잠정) 1.1%](https://www.bok.or.kr/portal/bbs/B0000501/view.do?menuNo=201264&nttId=10098382)와 정합. FRED 기준 필자 계산 1.14%)
- 핵심 결과값은 `calc_results.json` 참조: 정체 지속 3.078%, -0.1% 지속 3.001%,
  3.0% 등가 -0.101%, 2.6% 등가 -0.619%, 0.62% 지속 3.559%.

## 추출·검증 기록

- `calc_results.json` - 스크립트가 출력한 파생 수치 전체(등가점, 이월효과 등)
- `citation_checks.json` - 게시글 인용 수치의 출처 대조 결과(속보 PDF 원문 대조 포함)

## 원문 대조 상태

한국은행 통계 보도자료 게시판은 7/23 저녁 한때 '콘텐츠 준비중' 상태였으나
같은 날 복구되어, 속보 PDF(공보 2026-07-23호)를 내려받아 본문 수치 전체를
원문 대조 완료했다(2026-07-23, 해시 위 표 참조). 게시글 참고자료도 상세
페이지 링크로 교체했다.

## 게시 기록

사용자 지시로 2026-07-24 오전 게시. 푸시 시점(07시대)에 frontmatter 게시
시각이 미래(09:00)면 빌드에서 제외되므로, 게시 시각을 이미 지난
07:00(KST)으로 조정해 포함을 보장했다(과거 trend12·entry-seniorization과
동일한 방식). 본문의 '어제(7월 23일)' 시제는 게시일이 7/24이므로 그대로
유효하다.
