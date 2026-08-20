# trend21 '국가대표 AI 2차 평가' 재현 패키지

게시글: `content/english/post/trend21_dokpamo_2nd_eval.md` (frontmatter date 2026-08-20 17:30 KST — 8/20 15:14 게재된 보도설명자료 인용을 반영해 그 이후로 설정. 실제 공개 시점은 main 커밋·배포 시각)
과기정통부·NIPA가 2026-08-18 발표한 ‘독자 AI 파운데이션 모델’ 프로젝트 2차 단계평가 결과(3팀 진출·모티프테크놀로지스 탈락)를 배점 설계·점수 공개 범위·예산 재편 예고의 관점에서 읽는 글의 원자료 대장과 그림 스크립트.

## 원자료 대장

`data/raw/PROVENANCE.md` 참조. 요약:

| 파일 | 내용 | 용도 |
|---|---|---|
| `data/raw/260818_msit_dokpamo_2nd_eval_result.odt.txt`(원본 hwpx·odt는 raw-local, hwpx SHA-256 `ccf642a8…6ad4`) | 2차 단계평가 결과 보도자료(korea.kr 전재 newsId=156774699 첨부) | 배점(40=25+15/35=10+10+15/25=15+10), 평균·격차, "근소한 차이로", GPU 500→768→1,000장, AAII 상위 10 표, 전문가위 평가 의견, "새로운 지원체계" 문장 |
| `data/raw/260115_msit_dokpamo_1st_eval_result.odt.txt`(원본은 raw-local) | 1차 단계평가 결과 보도자료(newsId=156739871) | 1차 배점, 부문별 최고점(33.6/31.6/25.0), 독자성 최소조건 문장, 네이버클라우드 제외 사유 |
| `data/raw/260220_msit_dokpamo_motif_added.odt.txt`(원본은 raw-local) | 정예팀 추가 선정 보도자료(newsId=156745298) | 모티프 지원 내용(B200 768장, 데이터 17.5억+100억), 2차 평가 방식 예고 |
| `data/raw/260820_msit_dokpamo_2nd_eval_explain.odt.txt`(원본은 raw-local) | 2차 단계평가 보도설명자료(korea.kr newsId=148970354, 2026-08-20) | 항목별 1위·점수(11.9/13.4/29.5/11.6/7.6)와 평균, 환산 산식(AAII×25/100 등), 공개 범위 변경 경위 |
| `data/aaii_snapshot.json` | Artificial Analysis 사이트 조회값(2026-08-18 11:38 UTC, Intelligence Index v4.1.1) | 4팀 모델과 상위 모델의 지수 값. 원 HTML은 `data/raw-local/`(git 제외) |

`.odt.txt`는 ODT의 `content.xml`을 태그 제거·표 셀 구분자(` | `) 처리해 뽑은 검증용 텍스트다. **원본 hwpx·odt는 korea.kr의 공공누리 표시가 "텍스트에 한하여"이므로 공개 저장소에 올리지 않고 `data/raw-local/`(git 제외)에 보관한다** — 무결성은 PROVENANCE의 SHA-256으로 검증. 브리핑 공식 속기(2026-08-19 게재)와 국회예산정책처 2025 결산 분석 PDF(2,136억 = 1,586+500+50억 확인)도 raw-local에 보존했다(PROVENANCE 1-1절).

## 재현 순서

1. `data/raw/`에는 보도자료의 텍스트 추출본이 있고, 원본 바이너리(hwpx·odt)는 `data/raw-local/`(git 제외)에 있다. 원본을 다시 받으려면 PROVENANCE의 URL로 내려받아 SHA-256을 대조한다.
2. `python3 scripts/extract_aaii_snapshot.py`(기대 모델 누락 시 FAIL 종료) — `data/raw-local/`의 AA 페이지 스냅샷에서 지수 값을 추출해 `data/aaii_snapshot.json`을 만들고, 보도자료 표(정수)와 반올림 대조 결과를 출력한다(2026-08-18 실행 결과 PASS). 스냅샷이 없으면 https://artificialanalysis.ai/models/motif-3 를 저장해 같은 이름 패턴으로 둔다(지수는 비정기 갱신이라 값이 달라질 수 있다).
3. `/opt/anaconda3/bin/python3 scripts/make_figs.py` — 본문 그림 3종을 `static/images/post/dokpamo_eval/`에, 표지를 `assets/images/post/trend21_cover.png`에 생성한다(fig01_tournament=그림 1, fig02_weights=그림 2, fig03_aaii=그림 3). 그림 3의 점수는 `data/aaii_snapshot.json`에서 읽어 반올림하고(하드코딩 없음), 나머지 수치는 보도자료 원문 값이다. 필수 입력의 존재·숫자형·유한값 검증을 첫 저장 전에 모두 마치며(파일 단위 원자적 교체는 아님), 모바일 가독성을 위해 그림을 단순 구성으로 나누고 출처·긴 주석은 본문 캡션이 담당한다. `savefig(metadata={"Date": None})`.

## 검증 범위

- 본문의 진출·탈락, 배점, 평균·격차, GPU 추이, AAII 표, 전문가위 평가 의견, "새로운 지원체계" 문장은 2차 결과 보도자료 원문(`.odt.txt`)과 1:1 대조했다. 1차 배점·최고점·독자성 문장, 모티프 지원 내용도 각 보도자료 원문 기준.
- 브리핑 발언은 2026-08-19 게재된 korea.kr 공식 속기를 확보(raw-local)해 주 출처로 전환했고, 발화자(400억·1,200억 = 최동원 인공지능인프라정책관)와 자구를 속기 기준으로 대조·수정했다(2026-08-20). 속기에 없는 일부 문답은 언론 일문일답으로 보완.
- '팀당 약 400억·총 1,200억'은 최동원 정책관의 브리핑 발언(6개월 임차 가정 예상치)이며 보도자료에는 없다. GPU '1,000장 수준'의 팀당 여부는 보도자료 미명시(본문에 그렇게 적었다).
- 2,136억 원은 NABO 2025 결산 분석 기준 2025년 1차 추경 편성액(GPU 임차 1,586억+데이터 500억+인재 50억)이다. K-공감의 "2027년까지 2,136억가량"과 정부 안내 페이지의 "GPU 임차 1,576억"은 이와 표기가 갈린다 — 본문은 결산 문서를 따르고 갈림을 명시했다. 3.5조/5조/50~70조는 서로 성격이 다른 값이라 합산하지 않았다.
- 모티프3의 '1위'는 AAII 안에서만 확인되며 정부 벤치마크 부문(AAII+NIA 40점) 순위는 비공개(본문에 한정 표기).
- 제3자 기사 전문·상용 페이지 스냅샷은 저작권 관례에 따라 `data/raw-local/`(git 제외)에만 보관하고 URL·취득시각을 PROVENANCE에 남겼다.
