# 중국 반도체 수출 96% vs 7% 분석 (trend15)

`content/english/post/trend15_china_chip_exports.md`(2026-07-27 게시 예정)의 수치 근거와 그림 생성 스크립트.

## 상태

- **초안 단계.** 본문 수치는 집필 계획서(`PLAN_trend15_china_chip_exports.md`, 메인 저장소)의 확정 사실 표(C1~C17, K1~K13, P1~P12)를 따랐다. 계획서 머리말 기준으로 핵심 수치(해관총서 6월판 수량·금액표의 수량·금액·YoY)는 2026-07-26 영문 원표에서 직접 확인된 값이다.
- **원자료 보관·대조(2026-07-26 완료):** 아래 '원자료 대장'의 **총 29개 파일**(해관총서 13 + 국가통계국 1 + UIBE 1 + 트렌드포스 3 + ECOS 7 + 언론 보도 4)을 `data/`에 내려받아 SHA-256을 기록했고, 본문의 중국·트렌드포스·UIBE·ECOS 수치를 원자료와 1:1 대조해 모두 일치를 확인했다(아래 대조 결과).
- **ECOS 재호출 검증(2026-07-26 12:16 KST 완료):** 정식 인증키로 403Y001·403Y002(M, 202501~202606, 총지수·3091AA·309112AA) 6개 시리즈를 재호출해 원본 JSON을 `data/`에 보존했다. K1~K5 전 항목과 K6 중 초안에 사용한 총지수 3개 항목이 계획서 값과 소수점까지 일치했고, 2026년 6월 총지수 YoY(금액 +74.8%, 물량 +29.8%, 단가 +34.7%)가 한국은행 7월 15일 보도자료 공표치와 일치해 계산 방식이 검증됐다(K6의 컴퓨터·전자및광학기기 물량 +40.0% 계열은 미호출 — 초안 미사용). 인증키는 저장 파일·문서에 기록하지 않는다.
- **게시 전 남은 일:** ① 관세청 7/1~20 보도자료 원문 확인(현재 본문은 보도 귀속·증감률만 인용), ② 서울경제 중량·kg당 단가 원기사 확인(보도 귀속 상태), ③ 삼성·SK 컨콜 공식 IR 자료 대조(P8·P9는 LIKELY, 본문은 디일렉 귀속), ④ (신선도) UIBE 최신호가 상반기를 커버하는지 확인. — 국가통계국 +23.1%는 NBS 공식 원표를 보존해 1차 자료로 닫았고, K12 역사 비교는 ECOS 직접 대조로 닫았다.

## 스크립트

```bash
# 반드시 아래 '재현성 계약'의 인터프리터를 사용할 것 (PATH의 python3에는 matplotlib이 없을 수 있음)
/opt/anaconda3/bin/python3 scripts/fig01_value_vs_volume.py        # 그림 1: 누계 금액·수량 YoY 두 경로
/opt/anaconda3/bin/python3 scripts/fig02_price_volume_contribution.py  # 그림 2: 물량 기여도 4계열
/opt/anaconda3/bin/python3 scripts/make_cover.py                   # 커버 1600x800
```

- 공통: matplotlib(Agg), dpi 200, `--out`/`--font`(기본 Apple SD Gothic Neo) 인자. 각 스크립트는 수치 assert와 렌더링 후 레이아웃(겹침·잘림) assert를 통과해야 저장된다.
- **재현성 계약(2026-07-26 게시본 생성 기준):** 생성 인터프리터는 `/opt/anaconda3/bin/python3`(Python 3.13.9 + matplotlib 3.10.6). `savefig`의 `metadata={"Date": None}`으로 **같은 머신·같은 스택에서는** 연속 실행 시 같은 바이트(SHA-256)가 나온다(검증 완료). 다만 Python·matplotlib 버전을 맞춰도 하위 스택(zlib vs zlib-ng, freetype 등)이 다르면 픽셀이 같아도 바이트는 달라진다 — **버전 명세만으로 바이트 재현은 보장되지 않는다.** 따라서 ① 게시 파일의 무결성 검증은 아래 등록된 SHA-256과의 대조로, ② 다른 환경에서의 재생성 검증은 픽셀 비교로 한다:

  ```bash
  /opt/anaconda3/bin/python3 -c "from PIL import Image; import sys; a,b=(Image.open(p).convert('RGBA') for p in sys.argv[1:3]); print('pixel-identical:', a.size==b.size and list(a.getdata())==list(b.getdata()))" scripts/out/fig01_value_vs_volume.png ../../../static/images/post/trend15/fig01_value_vs_volume.png
  ```
- 게시본 SHA-256 (out/과 게시 경로 동일 확인, 2026-07-26):
  - `fig01_value_vs_volume.png` `94dba0a9a9e2cfea54a4c5345566035310a56e708e6e47e03655eb4508f66a4c`
  - `fig02_price_volume_contribution.png` `ee007c48c3293e9e10310ef5933dcb18a419dfd8e5a5809cf87b1f53abadda54`
  - `trend15_cover.png` `efa89623203f7a243c3f5942266bc83a55292b5b6574978ebda34c1e976115f6`
- 출력 → 게시 경로 복사:
  - `scripts/out/fig01_value_vs_volume.png` → `static/images/post/trend15/`
  - `scripts/out/fig02_price_volume_contribution.png` → `static/images/post/trend15/`
  - `scripts/out/trend15_cover.png` → `assets/images/post/trend15_cover.png`

## 원자료 대장 (`data/`, 취득 2026-07-26 — GACC·UIBE·TrendForce 12:00 KST, ECOS 무역지수 12:16, ECOS GDI 12:18, 언론 보도 12:30~12:36, NBS 원표 13:02)

| 파일 | 출처 URL | SHA-256 |
|---|---|---|
| gacc_2026-06_exports_usd.html | http://english.customs.gov.cn/Statics/d0b7e61e-7535-499e-9de5-ffccbfd48bef.html | `70b30e1f91e49a698701fe7aab088fc56be4d6ce035a7b6cd5d4df7fea1cfdab` |
| gacc_2026-06_exports_cny.html | http://english.customs.gov.cn/Statics/0549e67d-b68f-4258-b848-01396e12b49e.html | `952b91c8677e91002ba8c063c73bc86e3102f77cd5819be95ea2295ed2c44094` |
| gacc_2026-06_imports_usd.html | http://english.customs.gov.cn/Statics/e821dd30-c0f5-4455-981a-d59f307f3237.html | `1b6a28078dea94baac2d0ae6c82a11625fd4509a24fa81122f7254ee6bbe44d7` |
| gacc_2026-06_regimes_exports.html | http://english.customs.gov.cn/Statics/98185af2-acfb-406e-8dfa-050961c53ed7.html | `27e647c12165acdb0449eab7f9e5f8b8beb7e4ff83de7ff339b5fe1f306a2e7b` |
| gacc_2026-02_exports_usd.html | http://english.customs.gov.cn/Statics/bd273400-717c-41ab-ac57-8f85a2add7a5.html | `fd53a91393d98d93c1fe2d9235aba8b11c9b7bf99fb115669b888ccd9ca5d47b` |
| gacc_2026-03_exports_usd.html | http://english.customs.gov.cn/Statics/e685d609-01eb-470c-804e-08ae239e53a1.html | `7215fb516b067a6f0ea4ce50c898200f7a26a812ba3df453571ec9d1bde4530d` |
| gacc_2026-04_exports_usd.html | http://english.customs.gov.cn/Statics/0556071c-9550-4dd3-abdf-369ebd986c3c.html | `12ae3c7383bd151a3bdab785a2ecdcd967ada732cd5256490560416b35dddae9` |
| gacc_2026-05_exports_usd.html | http://english.customs.gov.cn/Statics/1f00d543-64ef-482d-830f-7eee41a7c576.html | `4a1d6bcc3cbe38ee68583b836dce2c21bb0b979ab9593f11cedabc82b4a9e381` |
| gacc_2025-06_exports_usd.html | http://english.customs.gov.cn/Statics/aeab99d8-1029-471e-85db-72412a5dd0a5.html | `12e168de4b7c15cb615174397fa76dfb1965233f46cc7b1a5f609bc6112ef7b8` |
| gacc_2025-12_exports_usd.html | http://english.customs.gov.cn/Statics/7367d7db-7fbd-42a5-8f75-442a7f989e64.html | `1213e1353965bb8fa3162453f201fb71e97c2299a1a7535d578e313ff8d271f5` |
| gacc_coverage_2024.xls | http://english.customs.gov.cn/Excel/Coverage%20of%20major%20exports%20for%20preliminary%20release(2024).xls | `a0f12406476094dd22bd3a759d1f86c9cc0add0db3a6df04d475fbeb917b06ac` |
| gacc_index_2026.html | http://english.customs.gov.cn/statics/report/preliminary.html | `4aca9a59fc93a3ce1f104515b9cfbf996ba393128685ae304710c421e76708d2` |
| gacc_index_2025.html | http://english.customs.gov.cn/statics/report/preliminary2025.html | `3de1dc6febcb43726e512cca12609ee2675a07caf347cf86092d938cbac7c654` |
| uibe_chip_trade_2026q1.pdf | https://delab.uibe.edu.cn/docs/2026-05/71b10626c88e4e58a130930789d16f53.pdf | `b4cb942bbec5db0809d487f39ba7a6572cee062b00cc4fb31ee87f50a7087fcf` |
| trendforce_20260601_1q26_dram.html | https://www.trendforce.com/presscenter/news/20260601-13070.html | `d91ff9d07a84f95372ddf813fc4f9370c409b4fac91b976965b4dd6d891a7458` |
| trendforce_20260331_2q26_forecast.html | https://www.trendforce.com/presscenter/news/20260331-12995.html | `be744a6a0e71e7cc20b9e2270a1274dcd592d2fa8998dd90eafc562b7453a2ff` |
| trendforce_20260709_3q26_server_dram.html | https://www.trendforce.com/presscenter/news/20260709-13140.html | `61b9c8e137106031a223cd7cda72d58d480600f8bb4bce2168874073d715ec04` |
| ecos_403Y001_totalAA.json | ECOS StatisticSearch 403Y001/M/202501~202606/\*AA (2026-07-26 12:16 KST, 키 마스킹) | `c835b4ef9af0d670848c83bb3ecd05657c6331c289557558ab927e80ada24d10` |
| ecos_403Y001_3091AA.json | 동 403Y001 · 3091AA | `0ca623da7426a713f56e95b1836073ff1b1ca09fd96409dd4f5dbcfbe14d42b7` |
| ecos_403Y001_309112AA.json | 동 403Y001 · 309112AA | `9ba0cdb6f6bca5c9202427724723f0eb386a7d72c7e25076e90a66716e95e507` |
| ecos_403Y002_totalAA.json | 동 403Y002 · \*AA | `fc11ec861978333d9ca2341697ffcadcdc286078041e2b67c8ed30c9d3730ba7` |
| ecos_403Y002_3091AA.json | 동 403Y002 · 3091AA | `fc0f35ec3de646412ac220bfa8825ac4f84f7ea85e762754530145152fc67744` |
| ecos_403Y002_309112AA.json | 동 403Y002 · 309112AA | `57bc783a794c4fc31df3fb65bd5a9466e8500aa0e22a6cf4255f941db9df8c04` |
| ecos_200Y106_GDI_quarterly.json | ECOS StatisticSearch 200Y106/Q/1986Q1~2026Q2/1600(실질 GDI, 원계열) | `78c80d0f5a6ed1b7a029c9d4cac62a8337a2a06836106312708738dcc996c90b` |
| nbs_20260715_industrial_output.html | https://www.stats.gov.cn/zwfwck/sjfb/202607/t20260715_1964123.html (NBS 공식 원표, P5 1차 근거: 集成电路（亿块） 517/18.8/2798/23.1) | `b1dda860324cc8bd051549f5acd4fbd6031f69a8921c6a6aac45411fb168546e` |
| chinanews_20260715_ic_output.html | https://www.chinanews.com.cn/cj/2026/07-15/10659810.shtml (NBS 대변인 국무원 브리핑 보도: 생산량 2798억 개·+23.1%, P5 보조 근거) | `228c8e69bb2bdaaf9358446ac149710bc07c69fbedfedb644bb8bdb412d0bfa2` |
| 21jingji_20260715_ic_top_export.html | https://m.21jingji.com/article/20260715/a589891cb154205d3670aa45ce7a5e36.html (6월 382.1억 달러·9.3%·제1대 수출상품·기여 6.5%p, C17 근거) | `00d0ab7f6a8c48eb4dcc18704be2d4cfdc1b13ebd96f05937ad921b5568801fc` |
| ecns_20260720_ic_output.html | http://www.ecns.cn/cns-wire/2026-07-20/detail-ihfhkrtk6181675.shtml (위안화 기준 수출 +88.7% 보도, C5 방증) | `8197fda074d9696fe8b8d6a4a58519cb73f5031268dfd1d0ba9b2930bfbcae48` |
| huaon_ic_output_series.html | https://www.huaon.com/channel/tradedata/1157922.html (월별 수출 시계열 재인용, 1~2월 +13.7%/+72.6% 방증) | `749be59a1105bc4d2741e14a526e24abdaeff1ea28526323d50095c1c11b4598` |

## 원자료 1:1 대조 결과 (2026-07-26)

- **(5) 수출 2026년 6월판(USD)** IC 행 원문: `316.8 | 38,205.0 | 1,794.4 | 177,281.6 | 1,677.1 | 90,402.8 | 7.0 | 96.1` — 본문의 수출액 1,772.8억 달러(+96.1%), 수량 1,794.4억 개(+7.0%), 6월 단월 382.1억 달러와 일치. CNY판 `12,263.5 | 6,497.5 | 88.7` 일치.
- **(6) 수입 6월판(USD)** IC 행: `3,047.5 | 298,020.5 | 2,818.7 | 191,279.8 | 8.1 | 55.8` — 수입액 2,980.2억 달러(+55.8%), 수량 +8.1% 일치. 적자 재계산: 2025H1 1,008.77억 → 2026H1 1,207.39억, 확대 198.62억 달러 = 표기 199억. 순수입 개수 1,141.6억 → 1,253.1억(+9.8%) 일치.
- **누계 경로(2~6월판)**: 수량 +13.7/+13.4/+10.6/+8.7/+7.0, 금액 +72.6/+77.5/+83.7/+90.0/+96.1 — 그림 1 데이터와 일치. 단월 차분: 3월 +13.0%, 4월 +3.8%, 5월 +2.1%, 6월 -0.4%(2025년 원표 단월 318.4 기준 -0.5%), 6월 금액 +122.3%, 단월 단가 $0.896/0.970/1.157/1.206 — 본문과 일치.
- **2025년 6월판**: `1,677.7 | 90,473.3 | 1,390.6 | 76,108.9 | 20.6 | 18.9` — 전년 물량 +20.6%·금액 +18.9%(C8), 기준 개정(1,677.7→1,677.1 / 904.733→904.028억 달러, 0.1% 미만) 일치. 3개년 단가 $0.5473→$0.5393→$0.9880(C14) 재계산 일치.
- **2025년 12월판**: `3,494.7 | 201,901.0 | 17.4 | 26.8` — C15 일치(단가 +7.9% 재계산 일치).
- **(17) 무역방식별**: 일반 676억 개/$322.2억, 가공 664/$750.1억, 보세 450/$697.2억, 기타 5/$3.3억 — 수량 합 1,795 ≈ 총계 1,794.4, 금액 합 177,281.6백만 달러로 (5) 표 총계와 정확히 합산 일치. 금액 비중 18.2/42.3/39.3%(가공+보세 81.6%), 수량 비중 37.7/37.0/25.1%, 단가 $0.477/1.130/1.549 재계산 일치. C10의 수량 YoY(+13.7/-0.6/+9.6%)는 계획서의 역산 방식(수준값+증감률)을 따름 — 원표 보존됨.
- **coverage_2024.xls**: 문자열 `85423` 포함 확인 — 품목 범위 HS 85423.
- **TrendForce**: 1Q26 범용 D램 계약가 "approximately 93% to 98% QoQ"·업계 매출 +81% QoQ, 2Q26 전망 58–63%(낸드 70–75%), 3Q26 서버 D램 13–18% QoQ 전망 — 본문 인용과 일치.
- **UIBE PDF(8쪽)**: 459.9/174.2/63.3(메모리), 160.6/4.9(프로세서), 318.8/43.9(홍콩), 108.9/173.2(산시), 186.8/93.4(장쑤) 모두 검출 — 본문 인용과 일치.
- **ECOS(정식 키 재호출, 2026-07-26)**: K1 집적회로 금액 149.47→404.22(+170.4%)·물량 189.28→215.56(+13.9%)·단가 +137.5%·기여 13.1% / K2 반도체 145.56→388.17(+166.7%)·179.29→209.12(+16.6%)·기여 15.7% / K3 총수출 129.54→195.40(+50.8%)·117.23→141.58(+20.8%)·기여 45.9% / K4 월별 물량 YoY +18.5/+41.9/+17.6/+12.4/+3.5/+12.8% / K5 반기 연결 +2.9%(집적회로 +1.2%) / K6 중 총지수 3개 항목: 6월 금액 +74.8%·물량 +29.8%·단가 +34.7%(BOK 보도자료 일치; 컴퓨터·전자및광학기기 물량 +40.0% 계열은 미호출) — **재검증한 항목 전부 계획서·본문·그림 2와 일치.**
- **K12 역사 비교(ECOS 직접 대조, 2026-07-26)**: 200Y106 실질 GDI(원계열, 분기) 1986Q1~2026Q2 재계산 — 1988Q1 +16.4%, 2026Q2 +15.6%, 1988Q2~2026Q1 사이 +15.6% 이상 분기 없음(차순위 1988Q4 +14.5%, 2026Q1 +13.2%) → **'1988년 1분기 이후 38년 3개월 만 최고' 성립, CONFIRMED로 격상.**
- **국가통계국 +23.1%(P5)**: NBS 공식 원표(stats.gov.cn, 2026-07-15 발표)를 보존하고 행 `集成电路（亿块） 517 / 18.8 / 2798 / 23.1`(6월 단월 517억 개·+18.8%, 상반기 누계 2,798억 개·+23.1%)을 직접 확인 — **1차 자료 요건 충족**. 중국신문망 보도(국무원 브리핑 발표 인용)는 보조 근거로 보존. **21世纪经济报道 원문**에서 "6月集成电路出口额达382.1亿美元…占比9.3%…第一大类出口商品…拉动作用达6.5个百分点"(C17의 2차 부분) 확인·보존.
- 미대조 잔여(3건 + 신선도 1건): 관세청 7/1~20 원문, 서울경제 중량·kg당 단가 원기사(보도 귀속 상태), 컨콜 공식 IR(디일렉 귀속 상태) + UIBE 최신호의 상반기 커버 여부.

## 핵심 수치 요약 (출처: 계획서 확정 사실 표)

| 수치 | 값 | 출처 |
|---|---|---|
| 중국 IC 수출액 2026H1 | 1,772.816억 달러, +96.1% | GACC (5) 수량·금액표 6월판(USD) |
| 중국 IC 수출 수량 2026H1 | 1,794.4억 개, +7.0% (표 인쇄 공표치) | 동 표 |
| 단가 | $0.5390 → $0.9880, +83.3% | 계산 |
| 로그 분해 | 단가 기여 90.0% / 수량 기여 10.0% | ln(1.8328)/ln(1.9610), ln(1.0699)/ln(1.9610) |
| 전년(2025H1) | 수량 +20.6%, 금액 +18.9% | GACC (5) 2025년 6월판 |
| 수입 2026H1 | 3,047.5억 개(+8.1%), 2,980.21억 달러(+55.8%), 단가 +44.1% | GACC (6) 6월판(USD) |
| IC 무역적자 | 1,008.8 → 1,207.4억 달러(+198.6억) | 계산 |
| 무역방식 | 가공 42.3% + 보세물류 39.3% = 81.6%(금액), 일반무역 수량 +13.7% | GACC 월보 (17) |
| 한국 집적회로(ECOS) | 금액 +170.4%, 물량 +13.9%, 물량 기여 13.1% | 403Y001/403Y002, H1 월평균 |
| 한국 반도체(ECOS) | 금액 +166.7%, 물량 +16.6%, 물량 기여 15.7% | 동 |
| 한국 총수출(ECOS) | 금액 +50.8%, 물량 +20.8%, 물량 기여 45.9% | 동 |
