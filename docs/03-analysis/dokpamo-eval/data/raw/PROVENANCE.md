# 원자료 대장 — 국가대표 AI(독자 AI 파운데이션 모델) 2차 단계평가 글

취득 시각은 UTC. SHA-256은 취득 직후 계산.

**보관 원칙(2026-08-20 개정)**: korea.kr 보도자료 페이지는 공공누리 적용 범위를 "텍스트에 한하여"로 표시하므로, 이미지가 포함된 원본 바이너리(hwpx·odt)는 공개 저장소에 올리지 않고 `raw-local/`(data/.gitignore로 git 제외)에 보관한다. `raw/`에는 텍스트 추출본(`.odt.txt`)과 이 대장만 둔다. 원본의 무결성은 아래 SHA-256으로 검증한다.

## 1. 정부 1차 출처 (원본 바이너리는 raw-local/, 텍스트 추출본은 raw/)

| 파일 | 원 URL | 취득 | 크기 | SHA-256 |
|---|---|---|---|---|
| `260818_msit_dokpamo_2nd_eval_result.hwpx` | https://www.korea.kr/common/download.do?fileId=198526362&tblKey=GMN (korea.kr 전재 newsId=156774699; 원 게시는 msit.go.kr 보도자료 nttSeqNo=3187672) | 2026-08-18T11:37Z | 334,094 B | `ccf642a8cc30d0f59e28d37714e581aaf43ca712b5a70528c5279009d2ba6ad4` |
| `260818_msit_dokpamo_2nd_eval_result.odt` | 같은 게시물 fileId=198526363 | 2026-08-18T11:37Z | 255,438 B | `49d613b9f8e2345a39b4fb90402b6ede213c55975bb38908496e1fd566a7d650` |
| `260818_…result.odt.txt` | 위 ODT의 content.xml 텍스트 추출본(검증용 파생물) | — | — | — |
| `260115_msit_dokpamo_1st_eval_result.hwpx` | korea.kr newsId=156739871 fileId=198362239 (원 파일명 "260116 조간 (보도) 독파모 프로젝트 1차 단계평가 결과(수정).hwpx") | 2026-08-18T11:38Z | 135,919 B | `f57f24c2b9e9050ebc7a6fdd6b4e5e28848edb130b3d00616d8b29985576dd3b` |
| `260115_msit_dokpamo_1st_eval_result.odt` | 같은 게시물 fileId=198362240 | 2026-08-18T11:38Z | 74,330 B | `577819080e56cd9010f192bde62b6bd5671229348c6a7b1cee24c1a5500d932a` |
| `260220_msit_dokpamo_motif_added.hwpx` | korea.kr newsId=156745298 fileId=198364923 | 2026-08-18T11:38Z | 128,804 B | `8b6f2c3b82fbf876cd33009a47c0ceb31a0c3a84c68f175be5d6be86dd70dc61` |
| `260220_msit_dokpamo_motif_added.odt` | 같은 게시물 fileId=198364924 | 2026-08-18T11:38Z | 61,851 B | `2c1c2082fa9e9693f4e16112d68c545c3cc9f199a2119b91131acd9ba03df61b` |

원문 대조 결과(2026-08-18): 2차 결과 보도자료의 배점(40=25+15 / 35=10+10+15 / 25=15+10), 평균·격차(22.5·4.0 / 28.8·2.4 / 17.6·5.0), "근소한 차이로", GPU 추이(500→768→1,000장 수준), "기존의 방식을 뛰어넘는 새로운 지원체계" 문장, AAII 표(1~10위) — 본문 인용과 1:1 일치 확인. 1차 결과 보도자료의 부문별 최고점(33.6/31.6/25.0, 평균 30.4/28.56/20.76)과 독자성 최소조건 문장, 모티프 선정 보도자료의 지원 내용(B200 768장·데이터 17.5억+100억)도 일치.

## 1-1. 추가 확보(2026-08-20, 검수 반영 라운드)

| 파일(raw-local/) | 원 URL | 취득 | SHA-256(앞 16자리) | 용도 |
|---|---|---|---|---|
| `koreakr_briefing_156774781_2026-08-20T0518Z.{html,txt}` | https://www.korea.kr/briefing/policyBriefingView.do?newsId=156774781 (2026-08-19 게재, 류제명 제2차관 브리핑 공식 속기) | 2026-08-20T05:18Z | `fabc0a17477f97b8` | 브리핑 직접 인용의 주 출처("표면적인 목표", "사용성·활용성 부분", 점수 비공개 사유, 국민 평가 당락 무영향, 분산·집중, 최동원 정책관 GPU 400억·1,200억 발언). txt는 태그 제거 추출본 |
| `260820_msit_dokpamo_2nd_eval_explain.{hwpx,odt}` + `koreakr_actually_148970354_2026-08-20T0652Z.html` | https://www.korea.kr/briefing/actuallyView.do?newsId=148970354 첨부 fileId=198527599(hwpx)·198527600(odt) — 과기정통부 보도설명자료 「2차 단계평가 기준과 결과에 대해 상세히 설명드립니다」(2026-08-20 즉시) | 2026-08-20T06:52Z | hwpx `fcf8022de9a534da`… / odt `237b18884a2444b3`… | 항목별 1위·점수(AAII 모티프 11.9·평균 9.48, NIA SKT 13.4·13.05, 전문가 LG 29.5·28.75, 전문 사용자 SKT 11.6·10.53, 국민 LG 7.6·7.03), 환산 산식, AAII 벤치마크 9종 가중치, 전문가위 구성(산 3·학 5·연 2), 모티프 파급효과 평가 특례(기존 모델 실적 포함, 정예팀 합의). 텍스트 추출본은 raw/에 공개 |
| `nabo_2025결산_과방위_fid33319407.pdf` | https://www.nabo.go.kr/board/file/down.do?fid=33319407 (국회예산정책처 '2025회계연도 결산 위원회별 분석[과학기술정보방송통신위원회]', 387쪽) | 2026-08-20T05:15Z | `cd8d1975923c1bb7` | 2,136억 = GPU 임차 1,586억(예산현액·집행 동일) + 데이터 500억(WBL 이관 200억 포함) + 인재 50억이 2025년 1차 추경 편성액임을 확인(41~43쪽). 정부 안내 페이지(korea.kr newsId=148944741)의 'GPU 임차 1576억' 표기와 갈림 — 본문은 결산 문서를 따름 |

## 2. 제3자 스냅샷 (raw-local/, git 제외)

| 파일 | 원 URL | 취득 | 용도 · 제외 사유 |
|---|---|---|---|
| `artificialanalysis_models_motif-3_2026-08-18T1138Z.html` | https://artificialanalysis.ai/models/motif-3 | 2026-08-18T11:38Z | 내장 JSON에서 Intelligence Index v4.1.1 추출(`scripts/extract_aaii_snapshot.py` → `data/aaii_snapshot.json`). 3.1 MB 상용 페이지 전문이라 공개 저장소 제외 |
| `koreakr_pressRelease_156774699.html` 등 3건 | korea.kr 게시 페이지 | 2026-08-18T11:37~38Z | 첨부 링크·게시 메타 확인용 페이지 스냅샷 |

추출 결과(`data/aaii_snapshot.json`, 소수 첫째 자리): Motif 3 47.4 / Solar Open2 250B 37.4 / A.X-K2 35.0 / K-EXAONE 2.0 0803 31.0; Claude Opus 5 63.1 / GPT-5.6 Sol 60.9 / Grok 4.6 60.9 / Kimi K3 59.7 / Qwen3.8 Max 58.1 / Muse Spark 1.2 56.8 / Gemini 3.7 Flash 56.0 / DeepSeek V4 Pro 0813 53.2 / GLM-5.2 52.6 — 보도자료 표(정수)와 반올림 일치(스크립트 내 대조 PASS). 네 국산 모델의 AA 등재일은 모두 2026-08-12.

## 3. 언론 보도 (전문 사본 미보관 — URL·일시만)

브리핑 발언은 당초(2026-08-18) 이데일리 종합·디지털데일리 일문일답 등 언론 보도를 근거로 인용했으나, 2026-08-20 공식 속기(1-1절, 2026-08-19 게재)를 확보해 주 출처를 속기로 전환하고 발화자·자구를 대조·수정했다. 속기에서 확인되지 않는 일부 문답만 언론 보도로 보완했다. 그 외 인용 매체·일시는 본문 참고자료 목록 참조.
