# 지능의 단가 — 토큰당 가격 vs 과제당 비용 (trend16)

`content/english/post/trend16_intelligence_price.md`(2026-07-28 07:00 KST 게시 예정)의 수치 근거와 그림 생성 스크립트.

## 상태

- **2차 개고(2026-07-27 오후, 외부 검토 NO-GO 반영).** 본문 수치는 사전 검증 프롬프트(`PROMPT_trend16_intelligence_price.md`, 메인 저장소 루트·미추적)의 확정 사실(2장)에서 출발했으나, 외부 검토가 지적한 차단 오류 4건을 원자료로 재검증해 모두 타당 판정하고 반영했다:
  1. **[확정] AA 지표 오해석** — 계획 프롬프트 2-2의 '지수 완주 비용'($4,010 등)은 원시 총비용이고, AA가 공표하는 정규화 지표는 **과제당 가중평균 비용(Cost per Task)**이다. 모델 페이지에서 직접 확인(Sonnet 5 max $1.53, Sol max $1.54, Opus 4.8 max $1.80 등 — `data/aa_cost_per_task_rendered.txt`). 이 지표로는 Sonnet이 Opus 4.8보다 15% 싸서, 구판의 '60% 싼 단가가 완주는 7% 비쌈' 역전 서사는 폐기하고 '단가 3배(Sol vs Sonnet)가 과제당 1센트 차'·'60% 우위가 15%로 압축'으로 재구성했다. Fable 5 측정이 Opus 4.8 폴백 포함이라는 점도 명기.
  2. **[확정] 스펙트럼 무한정** — 공식 정가표에 gpt-5.5-pro 출력 $180, Ministral 3 3B $0.10이 실재(사본 확인). '$0.28~$50 = 현행 최저·최고'를 '본문 비교 15종 기준'으로 한정하고 정가표 전체 극단(1,800배)을 별도 명기.
  3. **[확정] 제번스 기각 과잉** — 논문 원문에 "we do not attempt to formally analyze the paradox or causality"와 "There is some evidence of Jevons Paradox"(저비용 모델군)가 실재(PDF 확인). 탄력성은 모델 간 횡단면. 판정을 '기각'에서 '확인·기각 불가 + 단정 미지지'로 교체.
  4. **[확정] 요청당·표본 이전** — 논문 지표는 요청당 토큰. '작업당'을 '요청당'으로 고치고, 메커니즘 주장을 '관측된 유력한 후보'로 하향, 요청 수 분해 부재와 OpenRouter(2023~25)→알파벳(2026) 이전 불가를 본문에 명기.
  - 부수 수정: 제목·리드·결론 재작성(「토큰 단가와 과제 비용은 다르다」), '분모' 은유를 청구서 산식(입력단가×입력토큰+출력단가×출력·추론토큰+캐시)으로 교체, 공급 제약 해석을 '식별 불가'로 완화, 원문 미확보 OpenAI 매출 문단 삭제, 단가표를 모바일에서 숫자가 갈라지지 않는 3열로 축소.
- **게시 직전 재확인(2026-07-28 06:30 KST 전후, 필수)**
  1. **Kimi K3 가중치** — 2026-07-27 14:1x KST 확인 시점 `huggingface.co/moonshotai/Kimi-K3`는 공개 예고(카운트다운 잔여 9시간 47분, 예고 시점 약 07-28 00:00 KST) 상태. 공식 발표문에 "The full model weights will be released by July 27, 2026" 명시. 본문·'숫자의 기준'은 이 상태가 게시 후에도 참으로 남게 과거형으로 서술했으나, 게시 30분 전 저장소를 다시 열어 safetensors 존재·라이선스를 확인하고 필요하면 문장을 강화(공개 확인)하거나 조정(지연)할 것. 저장소가 `moonshotai` 조직인지도 재확인(가짜 미러 주의).
  2. **Artificial Analysis 과제당 비용(Cost per Task) 9건** — 동적 렌더 사이트라 이 세션의 브라우저 스냅숏(`data/aa_cost_per_task_rendered.txt`, 2026-07-27 15:1x KST)이 근거. 게시 직전 모델 페이지에서 값 유지 여부 확인($1.53/$1.54/$1.80이 핵심).
  3. **한시 가격** — 본문에 "2026년 7월 28일 기준" 명시 완료(Sonnet 5 도입가 8/31까지, 9/1부터 $3/$15 예고를 표 각주·본문에 반영).
  4. **출시일** — Grok 4.5·GPT-5.6 발표일을 이 세션에서 공식 발표문 원문으로 직접 확인(각각 2026-07-16, 2026-07-09). **주의: 계획 프롬프트 2-6 표의 Grok 4.5 '7/8'은 2차 보도 기반 오류로 판명, 본문은 7/16로 게재.**
- **미확인으로 남긴 것**: WSJ 2026-04-28로 인용되는 'OpenAI 연환산 매출 2~4월 횡보' 원문(2차 개고에서 해당 문단 자체를 삭제 — 본문 미사용), Muse Spark 1.1 단가(공식 발표문에 없음 — 본문 미사용), Kimi K3 라이선스(미공개 — 본문 미기재), Gemini 3.6 Flash 출시일(미확인 — 본문·그림은 '2026년 5월 이후 세대'로만 서술).
- **적대적 검수 반영(2026-07-27)**: ① [P0] 구글을 '7월 신모델'로 묶은 그림 1 주석·캡션·본문을 교정 — I/O 키노트 보존본에 "Gemini 3.5 Flash is available for everyone today"(2026-05-19)가 명시돼 3.5 Flash는 5월 출시이고, 리드의 7월 발표 여섯 건에도 구글이 없어 내적 모순이었음. ② [P1] 'Fable 5가 현행 최고 지능'이라는 AA 전체 1위 주장을 '이 비교(4개 모델) 안에서 최고'로 한정. ③ [P2] 리드의 220억 귀속(발표문)과 공급 제약 인용처(콜) 분리, GPT-5.6 '표제'→'부제', '하나같이'→'잇따라', 단가표를 출력 내림차순으로 재정렬, 결론의 무기간 '플래그십 동결·인상'에 '이번 달에도' 한정.

## 스크립트

```bash
# 반드시 아래 '재현성 계약'의 인터프리터를 사용할 것 (PATH의 python3에는 matplotlib이 없을 수 있음)
/opt/anaconda3/bin/python3 scripts/fig01_output_price_moves.py   # 그림 1: 플래그십 출력 단가의 이동(전작 대비, 로그 눈금)
/opt/anaconda3/bin/python3 scripts/fig02_task_cost_slope.py      # 그림 2: 출력 단가 vs 과제당 비용(Cost per Task) 기울기 그래프
/opt/anaconda3/bin/python3 scripts/make_cover.py                 # 커버 1600x800
/opt/anaconda3/bin/python3 scripts/verify_sources.py             # 그림·본문 하드코딩 수치 ↔ data/ 원자료 기계 대조(82건)
```

- 그림 스크립트는 수치를 상수로 내장하되(집계 관례), `verify_sources.py`가 그 상수들이 `data/` 원자료 사본에 실재하는지와 파생 산수(180배·15%·3배 등)를 기계 대조한다. 2026-07-27 실행 결과 전부 통과.

- 공통: matplotlib(Agg), dpi 200(커버 100), `--out`/`--font`(기본 Apple SD Gothic Neo) 인자. 각 스크립트는 수치 assert와 렌더링 후 레이아웃(겹침·잘림, 그림 1은 x축 라벨-주석 충돌 포함) assert를 통과해야 저장된다. `plt.rcParams["text.parse_math"]=False`로 `$` 두 개짜리 라벨의 mathtext 오파싱을 차단했다.
- **재현성 계약(2026-07-27 게시본 생성 기준):** 생성 인터프리터는 `/opt/anaconda3/bin/python3`(Python 3.13.9 + matplotlib 3.10.6). `savefig`의 `metadata={"Date": None}` 적용. 같은 머신·같은 스택에서는 연속 실행 시 같은 바이트가 나오지만, 하위 스택(zlib 등)이 다르면 픽셀이 같아도 바이트는 달라진다 — 무결성 검증은 아래 SHA-256 대조로, 교차 환경 재생성 검증은 픽셀 비교로 한다(trend15 README의 픽셀 비교 명령 참조).
- 게시본 SHA-256 (scripts/out/과 게시 경로 동일, 2026-07-27 2차 개고 재생성):
  - `fig01_output_price_moves.png` `951e591d1427176bf1c117debd8bd96aed618ee03cdd2ce381e6a6d5ab69e667` (브래킷을 '본문 비교 15종' 기준으로 한정)
  - `fig02_task_cost_slope.png` `4da932a32885d7429aba6dfbf40cf8c225efd7e1c6d25d5b45c12dddd53d9ee6` (Cost per Task 기준 7개 모델로 전면 재설계)
  - `trend16_cover.png` `3c9a76db5f41ada6c77ed37d496c720b15278d58676ac8002e8dc1c5d01685a1` (새 제목·수렴 그래픽)
- 출력 → 게시 경로 복사:
  - `scripts/out/fig01_output_price_moves.png` → `static/images/post/trend16/`
  - `scripts/out/fig02_task_cost_slope.png` → `static/images/post/trend16/`
  - `scripts/out/trend16_cover.png` → `assets/images/post/trend16_cover.png`

## 원자료 대장 (`data/`, 취득 2026-07-27 14:15~14:50 KST)

curl 수집이 차단되거나 JS 렌더인 페이지는 Claude Code 내장 브라우저로 확인하고 렌더 텍스트 발췌를 `*_rendered.txt`로 보존했다(해당 파일에 취득 방법 명기).

| 파일 | 출처 URL | SHA-256 |
|---|---|---|
| openai_pricing.html | https://developers.openai.com/api/docs/pricing | `7ddabc495fcc709f155fa5e63adaba37a28e7a6c3d8f167be42dbfc9c0837712` |
| openai_reasoning.html | https://developers.openai.com/api/docs/guides/reasoning | `b7c31bb7b42892b01d7c595ff3165f678ad3fefacbe8a7fe1225037981b50a93` |
| openai_gpt56_announcement.html | https://openai.com/index/gpt-5-6/ | `da37ab7702db3fe740868140dc6d38982e1980dff2442d5961bf0a349793fe42` |
| anthropic_pricing.html | https://platform.claude.com/docs/en/about-claude/pricing | `46e5dc8d4928f3b794c71944423ce5b01d509b9144de35ac86b702dd8d8b3a71` |
| google_gemini_pricing.html | https://ai.google.dev/gemini-api/docs/pricing | `aa30c1343b0e8e30d20e90c8ef5660c199b56e32c51aa4c23485256ca3e465fb` |
| google_io2026_keynote.html | https://blog.google/innovation-and-ai/sundar-pichai-io-2026/ | `2dec1de1f8e02fd81f8f5960ebedfa53c6fc471fc3c65d35f1f4dae8c46c9d20` |
| xai_models.html | https://docs.x.ai/docs/models (grok-4.3 단가는 페이지 내 데이터 블롭) | `b3b9c9e2c2b7dd9486c57efa6b7fba416788cd5a71bfbb3e524349d9abff6011` |
| xai_grok45_announcement.html | https://x.ai/news/grok-4-5 | `55c7de5703b687782db81b2e5c91ab537032db3fd8efcf4b45c1f76f0de55956` |
| kimi_k3_pricing.html / _rendered.txt | https://platform.kimi.ai/docs/pricing/chat-k3 (JS 렌더) | `e6cac7377e0389b4e4669ba50111fc5119fa2360df849a4bbc6756713accca23` / `d4206f4431d0fde0ac9238cb9bc93ff3400c61050ee171d77606d3cee8629fa7` |
| kimi_k26_pricing.html / _rendered.txt | https://platform.kimi.ai/docs/pricing/chat-k26 (JS 렌더) | `f30ee6aad29229ce82ec4012d43a82fca2bda9fa07525be9fb6a2abb7bd795b4` / `9e369c21c2735b54090ca12d09d5112c10ea51471ebe37a81af32ff18fdb5f26` |
| moonshot_kimi_k3_announcement.html / kimi_k3_blog_rendered.txt | https://www.kimi.com/blog/kimi-k3 (JS 렌더 — 정적본에는 게시일 목록만) | `7c62004dd26208987ed09d17cf440d5a33142b30cf9b215de4fde21d8af3a0cd` / `26003790826a48daaad8a82a7bd2b1f9879021e547d646c7dd345c146ebb6a52` |
| hf_kimi_k3_upcoming.html | https://huggingface.co/moonshotai/Kimi-K3 (공개 예고 페이지 상태 보존) | `35e4b849ae4c5c814d09033fecef284418968ac40908c8e25a5b92cd23c706db` |
| deepseek_pricing.html | https://api-docs.deepseek.com/quick_start/pricing | `08773e4021852f3c5cd4defdf91ccdc57573a7b4e859d84f0a18ba35156d4e69` |
| deepseek_updates.html | https://api-docs.deepseek.com/updates (Change Log — 2026년 항목은 04-24 하나) | `b1064782723805a228941d14815de341ef54d758af01a6aab35ad00350b3eb62` |
| deepseek_news260424.html | https://api-docs.deepseek.com/news/news260424 (V4 Preview Release) | `e1917ed7c53be33ab835dbaf0244a694c30d0e47d55b1265a21b14f8fae55ad5` |
| mistral_pricing.html | https://mistral.ai/pricing/api | `08dbfd8a9fcd1e91ff4ec564870a437234459d75caf3a21cf943d1135cda34ee` |
| together_pricing.html | https://www.together.ai/pricing (DeepSeek V4 Pro 행) | `5e3c5a81b3f9ffed384de61bf1634a52853d4713b8d525665952702c6a36bddf` |
| tml_introducing_inkling.html | https://thinkingmachines.ai/news/introducing-inkling/ | `b316dd46d2ae666dfd96626e979be396a729e4dfc07d3aecec52a74dde7fe0ef` |
| meta_muse_spark11_rendered.txt | https://ai.meta.com/blog/introducing-muse-spark-meta-model-api/ (curl 400 — 브라우저 확인) | `60a4da302f5f7972e516cd2c150230ed66b1a62f8b4212f4f5ba22d4aac7a3a4` |
| hf_tencent_hy3.html | https://huggingface.co/tencent/Hy3 (295B/21B active·apache-2.0 태그) | `b8e19fb6aa6e6d7ef6f551a0983d61778998ed21c29349db2076582988d0084e` |
| alphabet_2026q1_earnings_transcript.pdf | https://s206.q4cdn.com/479360582/files/doc_events/2026/Apr/29/Alphabet-2026_Q1_Earnings_Transcript.pdf | `a484838849e73a4d13dd34a4f4d0e3b030b4543839ad8808f34b64af706242e2` |
| alphabet_2026q2_earnings_transcript.pdf | https://s206.q4cdn.com/479360582/files/doc_events/2026/Jul/22/2026_Q2_Earnings_Transcript.pdf | `de938411f77818b147ff51d8ca2f70081f9a44401d396f1779ab5b5adfbd9123` |
| (교차 참조) 2026q2-alphabet-earnings-release.pdf | `docs/03-analysis/alphabet-receipts/data/`에 기보존 (분당 220억 문구 재확인) | trend14 README 참조 |
| arxiv_2601.10088.html / .pdf | https://arxiv.org/abs/2601.10088 (State of AI: An Empirical 100 Trillion Token Study) | `8b75672ac4ecb67657c3dea27b79256a0f3abe79c42332be94ac2944b36bf59e` / `0a3cc52bad6961424c9e6fe83351d2208c5311f99e7e7d6afa65e494de3c4535` |
| artificialanalysis_models.html | https://artificialanalysis.ai/models (동적 렌더 — 지표 정의 텍스트만 정적) | `edb540850be8d929666e0a1b5544239d4425f8f75821a3c7035570cdb8e6874c` |
| aa_cost_per_task_rendered.txt | https://artificialanalysis.ai/models/claude-sonnet-5 · /claude-opus-4-8 (브라우저 렌더 발췌 — Cost per Task 13종·Verbosity·지능지수) | `0bf749de5fe514c6dec6b0c16212075390ae2e6090a624bcd1fc8fc1d117999d` |
| artificialanalysis_methodology.html | https://artificialanalysis.ai/methodology | `05b9f3615182b6b7deee3dd1472d17d6deba2cff2334e0c5e3cf1fdedcbb3106` |

## 원자료 1:1 대조 결과 (2026-07-27, 이 세션)

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
- **스펙트럼 극단(2차 개고에서 추가)**: openai_pricing.html에서 gpt-5.5-pro 출력 $180.00, mistral_pricing.html에서 Ministral 3 3B $0.1 확인 — 본문 '정가표 전체 1,800배'의 근거.
- **제번스 관련 원문(2차 개고에서 추가)**: arXiv PDF에서 "we do not attempt to formally analyze the paradox or causality", "There is some evidence of Jevons Paradox"(efficient giants 문단), "prompt tokens per request" 확인 — 본문 '판정 불가' 서술과 요청당 표기의 근거.
- **미대조 잔여**: DeepSeek 인하 공지 원문(2026-05-25 발표·05-31 발효는 계획 프롬프트 확정 항목 — 공식 뉴스 인덱스에는 별도 항목 없음).

## 핵심 수치 요약

| 수치 | 값 | 출처 |
|---|---|---|
| 출력 단가 스펙트럼 | **본문 비교 15종 기준** $0.28(V4-Flash) ~ $50(Fable 5) = 178.6배(약 180배). 정가표 전체 극단은 gpt-5.5-pro $180 / Ministral 3 3B $0.10 = 1,800배 | 각 사 공식 가격 문서 |
| 전작 대비 | GPT-5.6 Sol 동결($30), Grok 4.5 ×2.4, Kimi K3 ×3.75, Gemini 3.5F ×3.6(3.6F ×3.0, 2026-05~ 세대), Fable 5 신설 | 동 |
| 7월 이전 인하 | Opus 4.1→4.5 $75→$25(2025-11-24), V4-Pro $3.48→$0.87(2026-05-31 발효) | Anthropic 문서·계획 프롬프트 |
| 과제당 비용(Cost per Task) | Sonnet 5(max) $1.53 ≈ Sol(max) $1.54 (단가 $10 vs $30, 3배) / Opus 4.8(max) $1.80 → Sonnet 단가 60% 우위가 과제당 15%로 압축 / Grok 4.5(high) $0.35, K3 $0.72, 3.6F $0.50, V4-Pro(max) $0.04, Opus 5(max) $2.03, Fable 5(폴백 포함) $2.75 | Artificial Analysis(2026-07-27 확인, 렌더 스냅숏) |
| 지수 출력 토큰(Verbosity) | Sonnet 5(max) 300M vs Opus 4.8(max) 120M (2.5배) | 동 |
| 사용량 | 분당 100억→160억 초과→약 190억→약 220억, 1조+ 고객 330→375 초과→거의 500 | 알파벳 콜·I/O·발표문 |
| 가격-사용량 횡단면 | 가격 -10% ↔ 사용량 +0.5~0.7%(모델 간 산점도, 인과 아님·논문이 역설/인과 미분석 명시) | arXiv 2601.10088 |
| 요청당 워크로드 | 프롬프트 1.5K→6K+(×4), 완성 150→400(×3), 시퀀스 2,000-→5,400+(2023말→2025말) | 동 |
