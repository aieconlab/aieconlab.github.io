# 지능의 단가 — 토큰당 가격 vs 과제당 비용 (trend16)

`content/english/post/trend16_intelligence_price.md`(2026-07-28 07:00 KST 게시 예정)의 수치 근거와 그림 생성 스크립트.

## 상태

- **2차 개고(2026-07-27 오후, 외부 검토 NO-GO 반영).** 본문 수치는 사전 검증 프롬프트(`PROMPT_trend16_intelligence_price.md`, 메인 저장소 루트·미추적)의 확정 사실(2장)에서 출발했으나, 외부 검토가 지적한 차단 오류 4건을 원자료로 재검증해 모두 타당 판정하고 반영했다:
  1. **[확정] AA 지표 오해석** — 계획 프롬프트 2-2의 '지수 완주 비용'($4,010 등)은 원시 총비용이고, AA가 공표하는 정규화 지표는 **과제당 가중평균 비용(Cost per Task)**이다. 모델 페이지에서 직접 확인(Sonnet 5 max $1.53, Sol max $1.54, Opus 4.8 max $1.80 등 — `data/aa_cost_per_task_rendered.txt`). 이 지표로는 Sonnet이 Opus 4.8보다 15% 싸서, 구판의 '60% 싼 단가가 완주는 7% 비쌈' 역전 서사는 폐기하고 '단가 3배(Sol vs Sonnet)가 과제당 1센트 차'·'60% 우위가 15%로 압축'으로 재구성했다. Fable 5 측정이 Opus 4.8 폴백 포함이라는 점도 명기.
  2. **[확정] 스펙트럼 무한정** — 공식 정가표에 gpt-5.5-pro 출력 $180, Ministral 3 3B $0.10이 실재(사본 확인). '$0.28~$50 = 현행 최저·최고'를 '본문 비교 15종 기준'으로 한정하고 정가표 전체 극단(1,800배)을 별도 명기. **〔3차 개고에서 '전체 극단'은 오류로 판명돼 '표본 밖 두 사례' 표현으로 교체됨 — 아래 3차 항목 3 참조〕**
  3. **[확정] 제번스 기각 과잉** — 논문 원문에 "we do not attempt to formally analyze the paradox or causality"와 "There is some evidence of Jevons Paradox"(저비용 모델군)가 실재(PDF 확인). 탄력성은 모델 간 횡단면. 판정을 '기각'에서 '확인·기각 불가 + 단정 미지지'로 교체.
  4. **[확정] 요청당·표본 이전** — 논문 지표는 요청당 토큰. '작업당'을 '요청당'으로 고치고, 메커니즘 주장을 '관측된 유력한 후보'로 하향, 요청 수 분해 부재와 OpenRouter(2023~25)→알파벳(2026) 이전 불가를 본문에 명기.
  - 부수 수정: 제목·리드·결론 재작성(「토큰 단가와 과제 비용은 다르다」), '분모' 은유를 청구서 산식(입력단가×입력토큰+출력단가×출력·추론토큰+캐시)으로 교체, 공급 제약 해석을 '식별 불가'로 완화, 원문 미확보 OpenAI 매출 문단 삭제, 단가표를 모바일에서 숫자가 갈라지지 않는 3열로 축소.
- **3차 개고(2026-07-27 저녁, 2차 외부 검토 NO-GO 반영).** 지적 5건 + 개선 6건을 원자료로 재검증해 전부 타당 판정하고 반영:
  1. **[확정] 핵심 명제가 자료보다 강함** — 그림 2의 7종으로 직접 계산하면 단가·과제당 비용의 스피어만 순위상관 0.929, 로그값 피어슨 0.953이고 역전은 Sonnet 5–Kimi K3, Opus 4.8–GPT-5.6 Sol 두 쌍뿐. '단가는 청구서를 예측하지 못한다'를 **'대체로 함께 움직이되 일대일이 아니다(일부 쌍에서 압축·역전)'**로 전면 교체(제목 제외 description·리드·본문·굵은 결론·그림 2 제목·주석). fig02의 assert도 `by_price != by_cost` → 순위상관 0.85 초과 **및** 역전 쌍 수 확인으로 교체. 〔4차 개고에서 표본을 8종으로 넓혀 **0.898 / 0.958 / 역전 3쌍**으로 갱신됨 — 아래 4차 항목 3 참조. 이 줄의 7종 수치는 당시 기록이다〕
  2. **[확정] 정규화 지표를 원시 총량으로 설명** — AA 사이트에서 세 지표의 정의를 원문 확인: Cost per Task는 "입력·캐시 적중·캐시 기록·추론·답변 토큰 가격에서 산출해 **과제 수로 나누고** 지수 가중치 적용", Output Tokens per Task는 별도 지표, Verbosity(300M/120M)는 지수 전체 **원시 합계**. 정규화 비용을 원시 총량 비율(2.5배)로 설명한 문장과 "차이는 전부 토큰 양에서 나온다"를 삭제하고, 원인 분해를 하지 않았음을 명시. 그림 2 주석·README·verify_sources.py도 동시 수정.
  3. **[확정] $180/$0.10은 '정가표 전체 극단'이 아님** — 같은 가격표에 구세대 o1-pro 출력 $600 실재(보존 사본에서 `o1-pro],[0,150],[0,null],[0,600]` 확인). '전체 극단' 표현을 삭제하고 '표본 밖 두 사례만으로도 1,800배', 'o1-pro는 더 높음', '천장·바닥을 말하려면 모집단 정의가 먼저'로 교체.
  4. **[확정] 딥시크 인하 날짜 1차 출처 없음** — 보존한 공식 가격 문서·변경 기록에 `$3.48`·`2026-05-25/31`이 없고 2026년 항목은 04-24 V4 공개뿐. (계획 프롬프트가 제시한 '인하 전 $3.48'은 Together AI의 서드파티 서빙가 $3.48과 정확히 일치해 혼동 가능성이 있음.) 본문에서 날짜·이전 가격을 빼고, 그림 1의 딥시크 화살표를 제거해 현행가만 표시.
  5. **[확정] 실무 결론에 품질 조건 필요** — "예산 단위는 과제" → "**품질 기준을 통과한** 과제이며 재시도·폴백까지 포함"으로 보강.
  - 개선 반영: '7월 신모델들은 값을 내리지 않았다' → '전작 가격과 견줄 수 있는 세 계열은 동결 또는 인상', Fable 5 $50을 '시장 천장' → '자사 라인업 상단', Inkling '3분의 1 토큰'에 범위 명시(Terminal Bench 2.1에서 Nemotron 3 Ultra 대비), 출처 없는 '애널리스트 평가' 삭제, description 축약, 상대 날짜('지난 22일'·'어제 글'·'이틀 뒤')를 고정 날짜로, **그림 1·2 아래 HTML 요약표 추가**(모바일 축소 시 원본 링크만으로는 값 확인이 어렵다는 지적 반영).
- **4차 개고(2026-07-27 밤, 3차 외부 검토 NO-GO 반영).** 지적 5건을 원자료로 재검증해 전부 타당 판정하고 반영:
  1. **[P0 확정] 구글 7월 인하 누락** — 제미나이 API 공식 릴리스 노트에 "July 21, 2026 … Gemini 3.6 Flash … at a **lower price point than 3.5 Flash**"가 명시(사본 `data/google_gemini_changelog.html`). 즉 3.6 Flash는 **7월 신모델이고 인하**($9 → $7.50, −16.7%)다. 2차 개고에서 구글을 '5월 이후 세대'로 뺀 판단은 I/O(3.5 Flash 5월 출시)만 보고 3.6 Flash GA를 놓친 결과였다. 리드·1절·그림 1(비교 기준을 2.5 Flash → **3.5 Flash**로 교체, 인하 화살표)·요약표·커버·결론·description을 '**동결 하나·인상 둘·인하 하나**'로 전면 교체. 구글 한국어 발표문(`data/google_blog_gemini36_ko.html`)의 '출력 토큰 17% 감소(AA 지수 기준)·최대 65%·에이전틱 작업의 전체 비용' 서술은 2절(토큰 효율 경쟁)의 1차 근거로 편입.
  2. **[확정] 역전 쌍 오기** — 본문이 Sol–Sonnet을 '역전'이라 했으나 단가·과제당 모두 Sol이 높아 **압축**이다. 실제 역전으로 서술 정정.
  3. **[확정] 표본 선정 규칙 부재** — 7종 선정 근거가 없었고 실제로 결과가 표본에 종속됨(Opus 5 포함 시 역전 3쌍·순위상관 0.898). **규칙을 'AA 확인 9종 중 Fable 5만 제외(폴백이라 단가 대응 불가)'로 명문화하고 8종으로 재계산**(0.898 / 0.958 / 역전 3쌍). 그림 2에 Opus 5를 추가했고, 그 결과 '출력 단가가 $25로 동일한 Opus 4.8·Opus 5의 과제당 비용이 13% 다르다'는 더 강한 예시를 얻었다. 표본 민감도는 '숫자의 기준'에 명시.
  4. **[확정] README 잔존 모순** — '정가표 전체 1,800배', DeepSeek `$3.48→$0.87`·05-31, Gemini 출시일 '미확인', 검증 건수 82건 표기를 모두 현행으로 교정(이 항목).
  5. **[확정] 검증 스크립트 설명 과장** — `verify_sources.py`는 본문·그림을 파싱하지 않으므로 '원자료→본문 연동 검증'이 아니다. 스크립트 docstring과 아래 설명을 '보존 자료 문자열 존재 + 내부 계산 확인'으로 고치고, **이번 구글 오류를 이 스크립트가 통과시킨 사실을 docstring에 실명으로 기록**했다.
  - 부수: 제번스 절에 `|ε|>1`의 전제(다른 조건 동일·효율 개선의 비례 전가·단순 부분균형)를 명시하고, 오픈라우터 자료의 한계와 알파벳 시계열의 한계를 문단 분리. 그림 라벨의 U+2212(−) 두부 글자를 잡는 assert 추가.
- **5차 개고(2026-07-28, 4차 외부 검토 NO-GO 반영).** P0 1건 + P1 6건을 원자료로 재검증해 전부 타당 판정하고 반영:
  1. **[P0 확정] 7월 가격 방향 모집단 누락** — 4차까지의 '네 계열: 동결1·인상2·인하1'은 (a) OpenAI를 계열 하나로 묶어 **Terra·Luna를 누락**하고, (b) **Terra를 gpt-5.4와 비교해 등급을 어긋나게** 잡았으며(공식 모델 문서는 Terra="mini 등급", Luna="nano 등급"에 대응한다고 명시 — 사본 `data/openai_model_gpt-5.6-*.html`), (c) **7/24 출시 Claude Opus 5**(릴리스 노트: "the same pricing as Claude Opus 4.8")와 (d) **7/21 GA Gemini 3.5 Flash-Lite**($1.50→$2.50, +66.7%)를 빠뜨린 결과였다. 모집단 규칙을 '같은 회사·같은 등급·공식 단가가 있는 직전 모델이 존재하는 7월 모델'로 명문화해 **여덟 개**를 세니 **동결 2·인상 5·인하 1**. description·리드·개요·1절·요약표·그림 1(모델 단위 8행으로 전면 재설계)·커버·결론을 일괄 교체. 대응표는 `data/july_price_direction_roster.txt`.
     - 함께 확정된 사실: **Claude Fable 5는 2026-06-09 출시**로 7월 집계 대상이 아니다(4차까지 '7월 상단 신설'처럼 읽히던 서술을 교정).
  2. **[P1] '대폭 인하' 기준 부재** — '절반 이상의 인하'로 문턱을 명시.
  3. **[P1] 옛 가격 서사 잔존** — 절 제목 '값을 안 내리는 대신'과 '단가가 내려가지 않는 시장'이 구글 인하와 충돌해, '단가 대신'·'여덟 중 일곱은 올리거나 묶어 둔'으로 교체.
  4. **[P1] 동가 쌍을 역전에 포함** — Opus 4.8·Opus 5는 단가가 $25로 같아 순서를 매길 수 없으므로 역전 3쌍과 분리해 '순위로는 잡히지 않는 별도 사례'로 서술.
  5. **[P1] 총액 하락의 필요조건 오류** — '두 축을 함께 움직여야 총액이 내려간다'는 거짓(한 축만 내려도 총액은 감소). '둘 다 필요한 것은 아니지만 구글이 두 축을 나란히 내세웠다'는 관찰로 교정.
  6. **[P1] Together AI 단가 상충** — 모델 페이지 $3.48 / 서버리스 문서 $4.40으로 두 페이지가 달라, '정확히 4배' 대신 '자사 단가가 제3자 서빙가보다 크게 낮다'는 방향만 서술하고 확인 시점·두 페이지를 명시.
  7. **[P1] 제번스 측정 한계** — 토큰은 청구 단위이지 물리적 자원 소비가 아니라는 문단을 추가하고, '현재 공개 자료에 없다'를 '이 글이 확인한 두 자료에서는 찾지 못했다'로 한정.
  - 검증 확대: `verify_sources.py`에 **등급 대응 검사**(Terra=mini/Luna=nano/Sol=frontier 정규식), Opus 5 동가 문구, Fable 5 6월 9일, Flash-Lite GA, 7월 대응표 일치, 배수 산수를 추가 — 이번 P0 유형(가격은 맞지만 비교 기준이 틀린 오류)을 잡도록 설계. 96+15건 통과.
- **6차 개고(2026-07-28, 5차 외부 검토 NO-GO 반영).**
  1. **[P0 확정] 커버의 문구와 그래프가 다른 사례** — 좌측은 Opus 4.8·Opus 5의 '동일 단가·13% 차', 우측 그래프는 Sol·Sonnet의 '단가 3배·1센트 차'를 그려 서로 다른 사례를 말하고 있었다(검증 스크립트는 두 사례를 각각만 확인해 통과시킴). **좌측 문구를 우측 그래프에 그린 값에서 코드로 파생시키고**, 문구·그래프 라벨 일치 assert를 추가해 구조적으로 어긋날 수 없게 했다.
  2. **[P1] Together AI 현재값** — 2026-07-28 재확인 결과 서버리스 모델 표와 V4-Pro 퀵스타트가 **모두 $3.48**로 일치(서버리스 표 원문 행: `$1.74 $0.20 $3.48`). 5차의 '$4.40과 상충' 서술을 삭제하고 '자사 $0.87 대비 4.0배'로 복원, 두 페이지를 참고자료에 명시.
  3. **[P1] README 잔여 모순** — 핵심 수치 요약의 `7종·0.929·0.953·역전 2쌍`을 현행 `8종·0.898·0.958·역전 3쌍`으로, 중복된 게시본 SHA 제목 제거, 취득 기간에 7-28 추가분 반영, Kimi 대장 설명을 '공개 전 상태 보존'으로 명확화(공개 확인은 hf_api_kimi_k3.json).
  4. **[P1] 본문 국소 3건** — '1차 출처로 확인되는 절반 이상 인하'를 '이 글이 가격 이력을 대조한 범위에서'로 한정, 절 제목을 '단가 대신'→'**단가에 더해**'로 바꾸고 캐시 적중률·1회 성공률도 청구서를 바꾼다는 점을 본문에 추가, 제번스 판정 범위를 리드·개요·결론 모두 '이 글이 확인한 두 자료'로 통일.
- **7차 개고(2026-07-28, 6차 외부 검토 반영).** P1 5건 + P2 5건:
  1. **두 '여덟'이 서로 다른 집합** — 7월 가격 방향 8개 SKU와 AA 과제당 비용 8종은 공통 5개뿐이다(가격에만 Terra·Luna·Flash-Lite / AA에만 V4-Pro·Sonnet 5·Opus 4.8). 본문에서 같은 표본으로 오인되지 않도록 AA 절 첫머리에 **"개수만 같을 뿐 다른 집합"**과 각 집합의 포함·제외 사유를 명시.
  2. **집계 범위 한정** — '이번 달 데이터에서 성립하지 않는다'를 '이 글이 추적한 출시 목록에서 조건을 만족한 8개 API SKU를 **같은 무게로** 센 결과'로 좁히고, 사용량 가중은 하지 않았음을 본문에 명시.
  3. **'대부분' 근거 보강** — '대부분 단가가 아니라 토큰 수' → '이 글이 대조한 7월 발표문들에서 되풀이되는 것은'으로 관찰 범위 한정.
  4. **AA 값의 성격** — '실제로 청구되는 비용'은 과장. 사이트가 **측정한 토큰 사용량에 공개 단가를 곱해 산출**한 값임을 본문에 명시하고 '실제 청구서의 집계가 아니다'를 덧붙임.
  5. **메커니즘 표현 하향** — '관측된 유력한 메커니즘' → '총사용량 폭증과 나란히 관측된 구성 변화'로 낮추고, 원인이라 하려면 요청 수/요청당 토큰 분해가 필요한데 하지 못했음을 명시.
  - P2: Kimi 링크 문구를 '가중치 공개 저장소'로, '지난달 출시된 Fable 5'를 '6월 9일 출시된'으로, README 검증 건수·대조 날짜 동기화, description 축약. **원자료 사본의 후행 공백은 수정하지 않고**(SHA 무결성) 저장소 루트에 `.gitattributes`를 두어 `docs/03-analysis/*/data/**`를 공백 검사에서 제외. `scripts/out/`은 trend15 관례에 맞춰 **추적**으로 확정.
- **게시 직전 재확인 — 2026-07-28 01:0x KST 완료(둘 다 통과)**
  - ✅ **Kimi K3 가중치 공개 확인** — 공식 저장소(moonshotai, private/gated 아님)에 safetensors 96분할 공개. 라이선스는 표준 오픈소스가 아닌 자체 `kimi-k3`(cardData: license=other, license_name=kimi-k3). 본문 서술을 '공개를 공언한' → '공개한'으로 확정하고 '숫자의 기준'에 라이선스 성격을 명기. 근거: `data/hf_api_kimi_k3.json`, `data/kimi_k3_release_confirmed.txt`. (HF `lastModified`는 공개일 근거로 쓰지 않음 — 계획 프롬프트 금지 항목)
  - ✅ **AA 과제당 비용 9개 값 유지 확인** — Sonnet 5·Opus 4.8 두 페이지 차트에서 $0.04/$0.35/$0.50/$0.72/$1.53/$1.54/$1.80/$2.03/$2.75 전부 27일 확인값과 동일. 근거: `data/aa_cost_per_task_rendered.txt` 말미.
- **〔이력〕 게시 직전 재확인 절차(원안)**
  1. **Kimi K3 가중치** — 2026-07-27 14:1x KST 확인 시점 `huggingface.co/moonshotai/Kimi-K3`는 공개 예고(카운트다운 잔여 9시간 47분, 예고 시점 약 07-28 00:00 KST) 상태. 공식 발표문에 "The full model weights will be released by July 27, 2026" 명시. 본문·'숫자의 기준'은 이 상태가 게시 후에도 참으로 남게 과거형으로 서술했으나, 게시 30분 전 저장소를 다시 열어 safetensors 존재·라이선스를 확인하고 필요하면 문장을 강화(공개 확인)하거나 조정(지연)할 것. 저장소가 `moonshotai` 조직인지도 재확인(가짜 미러 주의).
  2. **Artificial Analysis 과제당 비용(Cost per Task) 9건** — 동적 렌더 사이트라 이 세션의 브라우저 스냅숏(`data/aa_cost_per_task_rendered.txt`, 2026-07-27 15:1x KST)이 근거. 게시 직전 모델 페이지에서 값 유지 여부 확인($1.53/$1.54/$1.80이 핵심).
  3. **한시 가격** — 본문에 "2026년 7월 28일 기준" 명시 완료(Sonnet 5 도입가 8/31까지, 9/1부터 $3/$15 예고를 표 각주·본문에 반영).
  4. **출시일** — Grok 4.5·GPT-5.6 발표일을 이 세션에서 공식 발표문 원문으로 직접 확인(각각 2026-07-16, 2026-07-09). **주의: 계획 프롬프트 2-6 표의 Grok 4.5 '7/8'은 2차 보도 기반 오류로 판명, 본문은 7/16로 게재.**
- **미확인으로 남긴 것**: WSJ 2026-04-28로 인용되는 'OpenAI 연환산 매출 2~4월 횡보' 원문(2차 개고에서 해당 문단 자체를 삭제 — 본문 미사용), Muse Spark 1.1 단가(공식 발표문에 없음)는 7월 가격 방향 집계에서도 제외 사유로 명시했다. **Kimi K3 라이선스는 게시 직전 재확인에서 자체 라이선스 `kimi-k3`(license=other, license_name=kimi-k3)로 확인돼 이 목록에서 빠졌고, Gemini 3.6 Flash 출시일도 공식 릴리스 노트로 확정(2026-07-21 GA)돼 빠졌다.**
- **적대적 검수 반영(2026-07-27)**: ① [P0] 구글을 '7월 신모델'로 묶은 그림 1 주석·캡션·본문을 교정 — I/O 키노트 보존본에 "Gemini 3.5 Flash is available for everyone today"(2026-05-19)가 명시돼 3.5 Flash는 5월 출시이고, 리드의 7월 발표 여섯 건에도 구글이 없어 내적 모순이었음. ② [P1] 'Fable 5가 현행 최고 지능'이라는 AA 전체 1위 주장을 '이 비교(4개 모델) 안에서 최고'로 한정. ③ [P2] 리드의 220억 귀속(발표문)과 공급 제약 인용처(콜) 분리, GPT-5.6 '표제'→'부제', '하나같이'→'잇따라', 단가표를 출력 내림차순으로 재정렬, 결론의 무기간 '플래그십 동결·인상'에 '이번 달에도' 한정.

## 스크립트

```bash
# 반드시 아래 '재현성 계약'의 인터프리터를 사용할 것 (PATH의 python3에는 matplotlib이 없을 수 있음)
/opt/anaconda3/bin/python3 scripts/fig01_output_price_moves.py   # 그림 1: 플래그십 출력 단가의 이동(전작 대비, 로그 눈금)
/opt/anaconda3/bin/python3 scripts/fig02_task_cost_slope.py      # 그림 2: 출력 단가 vs 과제당 비용(Cost per Task) 기울기 그래프
/opt/anaconda3/bin/python3 scripts/make_cover.py                 # 커버 1600x800
/opt/anaconda3/bin/python3 scripts/verify_sources.py             # 보존 자료 문자열·내부 계산 확인(98+16건)
```

- 그림 스크립트는 수치를 상수로 내장하되(집계 관례), `verify_sources.py`가 그 값들이 `data/` 원자료 사본에 문자열·정규식으로 실재하는지(98건)와 파생 산수(180배·15%·구글 16.7% 인하·순위상관 0.898·로그상관 0.958·역전 3쌍·Together $3.48 등 16건)를 재계산해 대조한다. 2026-07-28 7차 개고 후 전부 통과.
- **이 스크립트의 한계를 명확히 해 둔다.** 본문(.md)이나 그림 스크립트를 파싱하지 않으므로 '원자료 → 본문·그림 연동 검증'이 아니다. 어떤 값이 원자료에 존재하기만 하면 **그것을 잘못된 비교 기준으로 쓰는 오류는 통과시킨다.** 실제로 3차 개고까지 `$9`와 `$7.50`이 모두 원자료에 있었지만 구글의 비교 기준을 2.5 Flash로 잘못 잡은 P0 오류를 이 스크립트는 잡지 못했다. 비교 기준의 타당성은 사람이 검토해야 한다.

- 공통: matplotlib(Agg), dpi 200(커버 100), `--out`/`--font`(기본 Apple SD Gothic Neo) 인자. 각 스크립트는 수치 assert와 렌더링 후 레이아웃(겹침·잘림, 그림 1은 x축 라벨-주석 충돌 포함) assert를 통과해야 저장된다. `plt.rcParams["text.parse_math"]=False`로 `$` 두 개짜리 라벨의 mathtext 오파싱을 차단했다.
- **재현성 계약(2026-07-27 게시본 생성 기준):** 생성 인터프리터는 `/opt/anaconda3/bin/python3`(Python 3.13.9 + matplotlib 3.10.6). `savefig`의 `metadata={"Date": None}` 적용. 같은 머신·같은 스택에서는 연속 실행 시 같은 바이트가 나오지만, 하위 스택(zlib 등)이 다르면 픽셀이 같아도 바이트는 달라진다 — 무결성 검증은 아래 SHA-256 대조로, 교차 환경 재생성 검증은 픽셀 비교로 한다(trend15 README의 픽셀 비교 명령 참조).
- 게시본 SHA-256 (scripts/out/과 게시 경로 동일, 2026-07-28 6차 개고 재생성):
  - `fig01_output_price_moves.png` `463ecc66b4cbd401381088978d04f3dde40d07401fd527d8e6c99e623d08da48` (모델 단위 8행으로 전면 재설계 — 인상 5·동결 2·인하 1)
  - `fig02_task_cost_slope.png` `b33845273423630c0346a5f99b259ea959abc45776d03d9b62f7e7b18f2c5ff5` (Opus 5 추가로 8종, 순위상관 0.90·역전 3쌍)
  - `trend16_cover.png` `b4784f01075028b6b5abace7e0ffbabe087735791809f677790fb86962238647` (좌측 문구를 우측 그래프 값에서 파생 — '단가 3배·1센트 차', 일치 assert 추가)
- 출력 → 게시 경로 복사:
  - `scripts/out/fig01_output_price_moves.png` → `static/images/post/trend16/`
  - `scripts/out/fig02_task_cost_slope.png` → `static/images/post/trend16/`
  - `scripts/out/trend16_cover.png` → `assets/images/post/trend16_cover.png`

## 원자료 대장 (`data/`, 취득 2026-07-27 14:15~15:5x KST + 2026-07-28 00:5x~01:2x KST 추가분)

curl 수집이 차단되거나 JS 렌더인 페이지는 Claude Code 내장 브라우저로 확인하고 렌더 텍스트 발췌를 `*_rendered.txt`로 보존했다(해당 파일에 취득 방법 명기).

| 파일 | 출처 URL | SHA-256 |
|---|---|---|
| openai_pricing.html | https://developers.openai.com/api/docs/pricing | `7ddabc495fcc709f155fa5e63adaba37a28e7a6c3d8f167be42dbfc9c0837712` |
| openai_reasoning.html | https://developers.openai.com/api/docs/guides/reasoning | `b7c31bb7b42892b01d7c595ff3165f678ad3fefacbe8a7fe1225037981b50a93` |
| openai_gpt56_announcement.html | https://openai.com/index/gpt-5-6/ | `da37ab7702db3fe740868140dc6d38982e1980dff2442d5961bf0a349793fe42` |
| anthropic_pricing.html | https://platform.claude.com/docs/en/about-claude/pricing | `46e5dc8d4928f3b794c71944423ce5b01d509b9144de35ac86b702dd8d8b3a71` |
| google_gemini_pricing.html | https://ai.google.dev/gemini-api/docs/pricing | `aa30c1343b0e8e30d20e90c8ef5660c199b56e32c51aa4c23485256ca3e465fb` |
| google_gemini_changelog.html | https://ai.google.dev/gemini-api/docs/changelog (2026-07-21 3.6 Flash GA·"lower price point than 3.5 Flash") | `53a3c68eb7d97d452cdf927ff7dd5cbeae6348bbf7dcbba41269b919ef93db5e` |
| google_blog_gemini36_ko.html | https://blog.google/intl/ko-kr/company-news/technology/gemini-3-6-flash-3-5-flash-lite-3-5-flash-cyber/ (2026-07-22, 출력 토큰 17% 감소·인하·"에이전틱 작업의 전체 비용") | `58ec1efe56b0442fb1e3623f68df0a33081c98a783ac72c2eecbabc5934d6c99` |
| google_io2026_keynote.html | https://blog.google/innovation-and-ai/sundar-pichai-io-2026/ | `2dec1de1f8e02fd81f8f5960ebedfa53c6fc471fc3c65d35f1f4dae8c46c9d20` |
| xai_models.html | https://docs.x.ai/docs/models (grok-4.3 단가는 페이지 내 데이터 블롭) | `b3b9c9e2c2b7dd9486c57efa6b7fba416788cd5a71bfbb3e524349d9abff6011` |
| xai_grok45_announcement.html | https://x.ai/news/grok-4-5 | `55c7de5703b687782db81b2e5c91ab537032db3fd8efcf4b45c1f76f0de55956` |
| kimi_k3_pricing.html / _rendered.txt | https://platform.kimi.ai/docs/pricing/chat-k3 (JS 렌더) | `e6cac7377e0389b4e4669ba50111fc5119fa2360df849a4bbc6756713accca23` / `d4206f4431d0fde0ac9238cb9bc93ff3400c61050ee171d77606d3cee8629fa7` |
| kimi_k26_pricing.html / _rendered.txt | https://platform.kimi.ai/docs/pricing/chat-k26 (JS 렌더) | `f30ee6aad29229ce82ec4012d43a82fca2bda9fa07525be9fb6a2abb7bd795b4` / `9e369c21c2735b54090ca12d09d5112c10ea51471ebe37a81af32ff18fdb5f26` |
| moonshot_kimi_k3_announcement.html / kimi_k3_blog_rendered.txt | https://www.kimi.com/blog/kimi-k3 (JS 렌더 — 정적본에는 게시일 목록만) | `7c62004dd26208987ed09d17cf440d5a33142b30cf9b215de4fde21d8af3a0cd` / `26003790826a48daaad8a82a7bd2b1f9879021e547d646c7dd345c146ebb6a52` |
| hf_kimi_k3_upcoming.html | https://huggingface.co/moonshotai/Kimi-K3 (2026-07-27 14:1x KST **공개 전** 예고 페이지 상태 보존 — 공개 확인은 hf_api_kimi_k3.json) | `35e4b849ae4c5c814d09033fecef284418968ac40908c8e25a5b92cd23c706db` |
| deepseek_pricing.html | https://api-docs.deepseek.com/quick_start/pricing | `08773e4021852f3c5cd4defdf91ccdc57573a7b4e859d84f0a18ba35156d4e69` |
| deepseek_updates.html | https://api-docs.deepseek.com/updates (Change Log — 2026년 항목은 04-24 하나) | `b1064782723805a228941d14815de341ef54d758af01a6aab35ad00350b3eb62` |
| deepseek_news260424.html | https://api-docs.deepseek.com/news/news260424 (V4 Preview Release) | `e1917ed7c53be33ab835dbaf0244a694c30d0e47d55b1265a21b14f8fae55ad5` |
| mistral_pricing.html | https://mistral.ai/pricing/api | `08dbfd8a9fcd1e91ff4ec564870a437234459d75caf3a21cf943d1135cda34ee` |
| jevons_coal_question_yale.html | https://energyhistory.yale.edu/w-stanley-jevons-the-coal-question-1865/ (각주의 제번스 역설 서지) | `52b62eda2da8747b56cacb1597e4570f172997c529a4bb8b40ccd1b12d74b840` |
| together_serverless_models.html | https://docs.together.ai/docs/serverless/models (2026-07-28 재확인: DeepSeek-V4-Pro $1.74 / $0.20 / **$3.48**) | `77f2b2810a56e226ed03cb46f1eab2d069a29c656971e061c1fd24d372359161` |
| together_v4pro_quickstart.html | https://docs.together.ai/docs/deepseek-v4-quickstart (같은 값 확인) | `388c20a56db5bbfecb8c26e0db39a1fcd28e1dbe7a40288979dbba60f0f02a02` |
| together_pricing.html | https://www.together.ai/pricing (DeepSeek V4 Pro 행) | `5e3c5a81b3f9ffed384de61bf1634a52853d4713b8d525665952702c6a36bddf` |
| tml_introducing_inkling.html | https://thinkingmachines.ai/news/introducing-inkling/ | `b316dd46d2ae666dfd96626e979be396a729e4dfc07d3aecec52a74dde7fe0ef` |
| meta_muse_spark11_rendered.txt | https://ai.meta.com/blog/introducing-muse-spark-meta-model-api/ (curl 400 — 브라우저 확인) | `60a4da302f5f7972e516cd2c150230ed66b1a62f8b4212f4f5ba22d4aac7a3a4` |
| hf_tencent_hy3.html | https://huggingface.co/tencent/Hy3 (295B/21B active·apache-2.0 태그) | `b8e19fb6aa6e6d7ef6f551a0983d61778998ed21c29349db2076582988d0084e` |
| alphabet_2026q1_earnings_transcript.pdf | https://s206.q4cdn.com/479360582/files/doc_events/2026/Apr/29/Alphabet-2026_Q1_Earnings_Transcript.pdf | `a484838849e73a4d13dd34a4f4d0e3b030b4543839ad8808f34b64af706242e2` |
| alphabet_2026q2_earnings_transcript.pdf | https://s206.q4cdn.com/479360582/files/doc_events/2026/Jul/22/2026_Q2_Earnings_Transcript.pdf | `de938411f77818b147ff51d8ca2f70081f9a44401d396f1779ab5b5adfbd9123` |
| (교차 참조) 2026q2-alphabet-earnings-release.pdf | `docs/03-analysis/alphabet-receipts/data/`에 기보존 (분당 220억 문구 재확인) | trend14 README 참조 |
| arxiv_2601.10088.html / .pdf | https://arxiv.org/abs/2601.10088 (State of AI: An Empirical 100 Trillion Token Study) | `8b75672ac4ecb67657c3dea27b79256a0f3abe79c42332be94ac2944b36bf59e` / `0a3cc52bad6961424c9e6fe83351d2208c5311f99e7e7d6afa65e494de3c4535` |
| artificialanalysis_models.html | https://artificialanalysis.ai/models (동적 렌더 — 지표 정의 텍스트만 정적) | `edb540850be8d929666e0a1b5544239d4425f8f75821a3c7035570cdb8e6874c` |
| aa_cost_per_task_rendered.txt | https://artificialanalysis.ai/models/claude-sonnet-5 · /claude-opus-4-8 (브라우저 렌더 발췌 — Cost per Task 13종·Verbosity·지능지수) | `9bb903c9df8adad09ede59a6616b2d106a7992ea8b4e85ff1a57a2b3bef4e803` |
| openai_model_gpt-5.6-sol.html | https://developers.openai.com/api/docs/models/gpt-5.6-sol ("frontier model in the GPT-5.6 family") | `91c3c74f6a35b5532ba4ea0522269df00caacd1d987bc8f8ce64b786bfb4b5e4` |
| openai_model_gpt-5.6-terra.html | 동 /gpt-5.6-terra ("corresponds to the **mini** model tier") | `cdaa226ca799f5f8927cfa1af9acf0b50039be4d382a8b140212231169681474` |
| openai_model_gpt-5.6-luna.html | 동 /gpt-5.6-luna ("corresponds to the **nano** model tier") | `a8cf10205974ddfbe88d271c2471966629d81ac3ce84d92f9bee191e442161c4` |
| anthropic_release_notes.html | https://platform.claude.com/docs/en/release-notes/overview (2026-07-24 Opus 5 "same pricing as Opus 4.8", 2026-06-09 Fable 5) | `eda57f4d94379a6ff789a805d05165529f7e06776291e8393dc76cc823a7e99e` |
| july_price_direction_roster.txt | 7월 가격 방향 대응표(모집단 규칙·등급 근거·원문 인용, 필자 정리) | `2f2c332af3b3ba058e55fb6258c91fc7fd75a97a85a9e8398b10ec7b42ef5c9a` |
| hf_api_kimi_k3.json | https://huggingface.co/api/models/moonshotai/Kimi-K3 (게시 직전 공개 확인 — safetensors 96분할·license_name kimi-k3) | `7812d489b800893dc0ae0b1094df3fe6b4d2df65a519d6bb56cd38377eaf30ee` |
| kimi_k3_release_confirmed.txt | 위 API·페이지 확인 기록(2026-07-28 01:0x KST) | `133147c7ab49e730b1bb0f0920ebd46d96fe43093cad3bfb1822c6185328d1d0` |
| artificialanalysis_methodology.html | https://artificialanalysis.ai/methodology | `05b9f3615182b6b7deee3dd1472d17d6deba2cff2334e0c5e3cf1fdedcbb3106` |

## 원자료 1:1 대조 결과 (최초 2026-07-27, 최종 갱신 2026-07-28)

- **단가표(본문 표·그림 1)**: OpenAI(gpt-5.6-sol/terra/luna·gpt-5.5·gpt-5.4), Anthropic(Fable 5 $10/$50·Opus 5 $5/$25·Sonnet 5 $2/$10 도입가와 8/31·9/1 문구·Haiku 4.5·Opus 4.1 $15/$75), Google(3.6-flash $1.50/$7.50·3.5-flash $1.50/$9.00·2.5-flash $0.30/$2.50), Mistral(Medium 3.5 $1.5/$7.5), DeepSeek(V4-Pro $0.435/$0.87·캐시히트 $0.003625·V4-Flash $0.14/$0.28) — 각 보존 HTML에서 문자열 검출로 일치 확인. xAI grok-4.5 $2.00/$6.00은 본문 텍스트, grok-4.3 $1.25/$2.50은 같은 페이지 데이터 블롭(promptTextTokenPrice=12500, completionTextTokenPrice=25000; 단위 1/10000달러/1M)에서 확인. Kimi k3 $0.30/$3.00/$15.00·k2.6 $0.16/$0.95/$4.00은 브라우저 렌더 표에서 확인.
- **토크나이저 30%**: anthropic_pricing.html에 "approximately 30% more tokens" 문자열 존재 확인.
- **추론 토큰 과금**: openai_reasoning.html에 "billed as output tokens"·"25,000" 존재 확인.
- **Inkling 토큰 효율**: tml_introducing_inkling.html에 "a third of the tokens" 존재 확인(라이선스 문구는 이 페이지에 없음 — Apache 2.0은 계획 프롬프트의 공식 확인 항목).
- **Grok 4.5 발표문**: "Jul 16, 2026"·"$2 per million input tokens and $6 per million output tokens"·15,954·67,020 존재 확인. **발표일 7/16이 계획 프롬프트 표(7/8, 2차 출처)와 달라 본문은 7/16 채택.**
- **GPT-5.6 발표문**: "July 9, 2026" 확인.
- **Kimi K3 발표문(브라우저)**: "2.8T-parameter"·"activating 16 out of 896 experts"·"The full model weights will be released by July 27, 2026" 확인, 게시일 2026/07/16(리서치 인덱스). 라이선스 언급 없음.
- **Hy3**: HF 페이지에서 "295B-parameter … 21B active"·license:apache-2.0 태그 확인.
- **Muse Spark 1.1(브라우저)**: "July 9, 2026"·Meta Superintelligence Labs·Meta Model API public preview 확인, 단가 없음(계획 프롬프트 금지 목록과 부합).
- **알파벳**: Q1 트랜스크립트 "more than 16 billion tokens per minute … up from 10 billion last quarter"·"330 Google Cloud customers each processed over one trillion tokens" / Q2 트랜스크립트 "approximately 22 billion tokens per minute. That's up from 16 billion just a quarter ago"·"we continue to be supply constrained"·"Nearly 500 Cloud customers" / I/O 기조연설 "roughly 19 billion tokens per minute"·"over 375 Google Cloud customers" — 전부 원문 검출로 일치 확인.
- **arXiv 2601.10088 PDF**: "a 10% decrease in price corresponds to only about a 0.5–0.7% increase in usage" / "At a macro level, demand is inelastic, but this masks different micro behaviors" / "roughly fourfold from around 1.5K to over 6K while completions have nearly tripled from about 150 to 400 tokens" / "from under 2,000 tokens in late 2023 to over 5,400 by late 2025" — 원문 검출로 일치 확인. 추론 모델 토큰 비중 50% 초과·코딩 11%→50% 초과는 계획 프롬프트 확정 항목(그림 10 부근)으로, 이 세션에서는 그림 캡션 존재까지 확인.
- **Together AI**: "DeepSeek V4 Pro $1.74 / $0.20 (cached) / $3.48" 행 확인 → 본문 '자사가의 4배'(3.48÷0.87=4.0).
- **DeepSeek 체인지로그**: 2026년 항목이 2026-04-24(V4-Pro/V4-Flash API 추가, 구 모델명 2026-07-24 종료) 하나뿐임을 확인 — '7월 GA' 류 서술을 본문에서 배제한 근거.
- **AA 과제당 비용(2차 개고에서 추가)**: Sonnet 5·Opus 4.8 모델 페이지의 Cost per Task 차트에서 13종 값과 정의("Weighted average cost (USD) per Intelligence Index task"), Verbosity(Sonnet 300M·Opus 4.8 120M), 지능지수(53·56), "Claude Fable 5 (with fallback)" 표기를 브라우저로 직접 확인해 `data/aa_cost_per_task_rendered.txt`에 보존. 구판이 쓴 원시 총비용($4,010 등)과 다른 지표임을 확인.
- **스펙트럼(2차 개고에서 추가, 3차에서 한정)**: openai_pricing.html에서 gpt-5.5-pro 출력 $180.00·구세대 o1-pro 출력 $600, mistral_pricing.html에서 Ministral 3 3B $0.1 확인 — 본문은 이를 '표본 밖 두 사례만으로도 1,800배'로만 쓰며 **'정가표 전체 극단'이라고 하지 않는다**(o1-pro가 더 높다).
- **제번스 관련 원문(2차 개고에서 추가)**: arXiv PDF에서 "we do not attempt to formally analyze the paradox or causality", "There is some evidence of Jevons Paradox"(efficient giants 문단), "prompt tokens per request" 확인 — 본문 '판정 불가' 서술과 요청당 표기의 근거.
- **미대조 잔여**: 없음. (계획 프롬프트의 DeepSeek '2026-05-25 발표·05-31 발효·인하 전 $3.48'은 3차 개고에서 **근거 없음으로 폐기**했다 — 공식 변경 기록의 2026년 항목은 04-24뿐이고, 그 $3.48은 Together AI 서드파티 서빙가와 정확히 일치한다. 본문·그림 모두 미사용.)

## 핵심 수치 요약

| 수치 | 값 | 출처 |
|---|---|---|
| 출력 단가 스펙트럼 | **본문 비교 15종 기준** $0.28(V4-Flash) ~ $50(Fable 5) = 178.6배(약 180배). 표본 밖 두 사례(gpt-5.5-pro $180 / Ministral 3 3B $0.10)만으로도 1,800배 — **'전체 극단' 아님**(o1-pro $600) | 각 사 공식 가격 문서 |
| 7월 가격 방향 | **여덟 개 기준 동결 2·인상 5·인하 1**. 인상: Luna ×4.8(vs nano), K3 ×3.75, Terra ×3.3(vs mini), Grok 4.5 ×2.4, 3.5 Flash-Lite ×1.67 / 동결: Sol $30, Opus 5 $25 / 인하: 3.6 Flash −16.7% | 각 사 공식 가격·모델 문서·릴리스 노트 |
| 인하 | **7월**: 구글 3.5 Flash $9 → 3.6 Flash $7.50(−16.7%, 2026-07-21 GA). **7월 이전**: Opus 4.1→4.5 $75→$25(2025-11-24). DeepSeek 인하 이력은 근거 없어 폐기 | 구글 릴리스 노트·Anthropic 문서 |
| 과제당 비용(Cost per Task) | Sonnet 5(max) $1.53 ≈ Sol(max) $1.54 (단가 $10 vs $30, 3배) / Opus 4.8(max) $1.80 → Sonnet 단가 60% 우위가 과제당 15%로 압축 / Grok 4.5(high) $0.35, K3 $0.72, 3.6F $0.50, V4-Pro(max) $0.04, Opus 5(max) $2.03, Fable 5(폴백 포함) $2.75 | Artificial Analysis(2026-07-27 확인, 렌더 스냅숏) |
| 단가-과제당 상관 | **8종 기준(AA 확인 9종 중 Fable 5만 제외)** 스피어만 0.898, 로그값 피어슨 0.958, 역전 3쌍(Sonnet 5–K3, Opus 4.8–Sol, Opus 5–Sol). 별개로 Opus 4.8·Opus 5는 단가 동일($25)인데 과제당 13% 차 | 위 값으로 필자 계산(verify_sources.py가 재계산·검증) |
| 정규화 주의 | Verbosity(Sonnet 5 max 300M·Opus 4.8 max 120M)는 지수 전체 **원시 합계**여서 과제당 비용과 직접 견줄 수 없음 → 본문에서 제외. AA는 'Output Tokens per Task'를 별도 공표 | 동 |
| 사용량 | 분당 100억→160억 초과→약 190억→약 220억, 1조+ 고객 330→375 초과→거의 500 | 알파벳 콜·I/O·발표문 |
| 가격-사용량 횡단면 | 가격 -10% ↔ 사용량 +0.5~0.7%(모델 간 산점도, 인과 아님·논문이 역설/인과 미분석 명시) | arXiv 2601.10088 |
| 요청당 워크로드 | 프롬프트 1.5K→6K+(×4), 완성 150→400(×3), 시퀀스 2,000-→5,400+(2023말→2025말) | 동 |
