# dml-401k — 시리즈 4편 「잔차끼리의 회귀」 재현 패키지

게시글: `content/english/post/analysis_dml_401k.md` (AI_분석, 2026-08)

## 원자료 대장

| 파일 | 출처 | 취득일 | SHA256 | 비고 |
|---|---|---|---|---|
| `data/raw-local/sipp1991.dta` | https://raw.githubusercontent.com/VC2015/DMLonGitHub/b91cbf96c01eccd73367fbd6601ecdd7aa78403b/sipp1991.dta (DML 원 논문 저자 공개 저장소, 커밋 고정) | 2026-08-04 | `1123d5f0abf6adae1d8e200f756d2a22b0ce0ce30cb228e69342a0098e57b4b2` | 260,726B. 1991 SIPP 기반 N=9,915 가구. **git 미추적(raw-local)** — 아래 명령으로 재취득 |

```bash
cd docs/03-analysis/dml-401k   # 저장소 루트 기준 — 이하 모든 명령은 이 디렉터리에서
mkdir -p data/raw-local        # gitignored 디렉터리 — 새 클론에는 없음
curl -L -o data/raw-local/sipp1991.dta \
  https://raw.githubusercontent.com/VC2015/DMLonGitHub/b91cbf96c01eccd73367fbd6601ecdd7aa78403b/sipp1991.dta
shasum -a 256 data/raw-local/sipp1991.dta   # 위 SHA256과 일치해야 함
```

URL은 취득 시점의 커밋(b91cbf9)에 고정했다(가변 `master` 참조 대신 — 고정 URL의
SHA256 일치를 2026-08-05 확인).

데이터 검증 기준점: 공변량 미조정 OLS로 e401 계수 **$19,559.3 (HC0 SE 1,412.8)** — 원 논문 §6.2의
보고치 "$19,559 (1,413)"와 일치. `02_401k.py` 실행 시 자동 검증(N=9,915, SHA256).

## 이론·수치의 1차 출처

- Chernozhukov, Chetverikov, Demirer, Duflo, Hansen, Newey, Robins (2018),
  *Double/debiased machine learning for treatment and structural parameters*,
  Econometrics Journal 21(1), C1–C68. 본 패키지의 대조 수치는 arXiv:1608.00060
  LaTeX 원문(§1.1, §3.1, §3.4, §4.1, §5.1, §6.2)에서 2026-08-04 직접 전사.
- 401(k) 원 논문 보고치(달러, DML2·100분할 중위수법, [비조정 중위수 SE](분할조정 SE)):
  - 미조정(무통제): 19,559 (1,413)
  - PLR 5-fold: lasso 8,187 [1,298] (1,558) · forest 9,247 [1,295] (1,328) · boosting 9,110 [1,314] (1,328)
  - IRM 5-fold: lasso 7,170 [1,201] (1,398) · forest 8,105 [1,242] (1,299) · boosting 7,713 [1,155] (1,177)
  - (2-fold 열도 원문에 있음 — 스크립트 `PAPER` 상수 참조)

## 스크립트

| 파일 | 역할 |
|---|---|
| `scripts/dml_core.py` | PLR 잔차화(partialling-out) DML2·정확 항 분해·IRM ATE(AIPW)·중위수법 — DML 전용 패키지(DoubleML·EconML 등) 없이 원 논문 정의를 직접 구현 |
| `scripts/01_simulation.py` | S1(세 절차 대결 + 오차 항별 실측) · S2(나머지항 스트레스 테스트, 희소 DGP, 폴드 내 벌점 선택; `--s2-only`) |
| `scripts/02_401k.py` | 401(k) 재추정. `--mode expA`(학습기 시드 고정·분할 100회, 본문 기준)·`expB`(분할 고정·학습기 시드 스윕): `--learner {lasso,forest,boosting}` / `--mode crossed`(10×10 교차): `--learner {forest,boosting}` |
| `scripts/03_figures.py` | fig01–fig06 + 커버 (3편 스타일) |
| `scripts/04_report_numbers.py` | 본문 기입용 수치 일괄 출력 (전사 오류 방지, 검수 게이트에서 재실행) |
| `scripts/05_aggregate.py` | expA/expB/crossed 집계 → `e401k_summary2.json` (중위수법·분산 성분·완전성 assertion) |

실행 환경: Python 3.13.9 —
`pip install "numpy==2.3.5" "pandas==2.3.3" "scikit-learn==1.7.2" "scipy==1.16.3" "matplotlib==3.10.6"`.
그림의 한글은 Apple SD Gothic Neo 폰트를 전제하므로 macOS 밖에서는 03_figures.py의
rcParams 폰트를 교체해야 한다. 난수는 `numpy.random.default_rng`. 분할 시드
(`20260000+split_seed`)와 학습기 시드(`90000+10*learner_seed` 파생)는 완전히 분리되어 있다.

재현 실행 순서:
```bash
cd scripts
python 01_simulation.py                        # S1+S2 (S2만은 --s2-only; K=5 기본값)
for L in lasso forest boosting; do
  python 02_401k.py --mode expA --learner $L --seeds 100 --kfolds 5
  python 02_401k.py --mode expB --learner $L --seeds 100 --kfolds 5
done
python 02_401k.py --mode crossed --learner forest --kfolds 5
python 02_401k.py --mode crossed --learner boosting --kfolds 5
python 05_aggregate.py && python 04_report_numbers.py
python 03_figures.py
```

예상 실행시간(Apple Silicon 기준, 코어 경합 없을 때): 01_simulation 약 20–30분,
02_401k는 expA·expB 각각 라쏘 ~1시간·부스팅 ~1시간·포레스트 ~10분, crossed ~1시간,
집계·그림은 수 분.

## 산출물 (`scripts/out/`)

- 시뮬레이션: `sim_s1_reps.csv`, `sim_s1_summary.json`, `sim_s2_reps.csv`, `sim_s2_summary.json`
- 401(k): `e401k_anchors.json`(미조정·선형 OLS 기준점),
  `e401k_expA_{lasso,forest,boosting}.csv`(분할 100회 — 표 1·그림 4·5의 원천),
  `e401k_expB_{lasso,forest,boosting}.csv`(학습기 시드 스윕),
  `e401k_crossed_{forest,boosting}.csv`(10×10), `e401k_summary2.json`(집계)
- 실행 로그는 공개 패키지에 포함하지 않는다(진행 출력일 뿐이며 일부가 수정 전
  구값을 담아 혼동을 부를 수 있음). 수치의 권위본은 위 CSV·JSON이다.
- 본문·그림의 모든 수치는 위 파일들과 `04_report_numbers.py` 출력으로 대조 가능.
  (교락 시드의 구 실행 산출물은 2026-08-05에 삭제 — 상태 로그 참조)

## 상태 로그

- 2026-08-04: 데이터 취득·SHA 기록, 무통제 앵커 일치 확인, S2 재설계(희소 DGP,
  c=1 커버리지 94.7%/150회, c→∞ 극한 = 무통제 OVB 수렴 확인).
- 2026-08-04 (1차 본실행 — **이후 대체됨**): S1 500회 결과는 현행과 동일(오라클 95.2%
  / A +0.080·65.2% / B −0.193·0% / Bsym −0.010·93.6% / C −0.008·94.8%). 당시의
  S2(전표본 벌점 선택)와 401(k) 실행(분할·학습기 시드 교락)은 아래 8/5 항목의
  재실행으로 대체되어 산출물에서 삭제 — 이 항목의 401(k) 관련 수치는 인용 금지.
- 로컬 프리뷰: Hugo 0.164 비호환 3종 중 2종을 임시 적용(og-twitter 주석,
  Amazon_Go.jpg 변환) — **게시 커밋 전 원복 필수** (PLAN 체크리스트 참조).
- 2026-08-05 (외부 검토 반영 재실행): 검토가 지적한 시드 교락(분할 시드가 학습기
  난수에도 전달)을 수정 — split_seed/learner_seed 분리, expA(분할만 100회, 본문
  표·그림 기준)·expB(내부 난수만 100회)·crossed(10×10, 2원 분산분해) 3실험 체제.
  S2는 벌점 선택을 학습 폴드 안으로 이동(누수 차단) 후 재실행(c=1 커버리지 95.4%,
  c=100 편향 +0.8389 — 해석적 극한 +0.8405와 MC 오차 범위 내 부합). 주요 식별 결과: 부스팅은 내부 난수 고정
  후에도 분할 민감도 최대(분할 SD $337·$250)이며 내부 난수만으로도 $270·$229;
  포레스트는 분할 지배(내부 몫 ~$50, 가법 주효과 0); LASSO는 PLR 결정적(100회
  동일값)·IRM 표준편차 $3.1.
  검산: PLR·부스팅 √(207²+269²)≈339 ≈ expA 337. 교락 실행의 산출물·로그
  (e401k_reps.csv, e401k_summary.json, e401k_run.log)는 혼동 방지를 위해 삭제 —
  본문·그림은 expA 계열과 e401k_summary2.json 기준.
  이론 서술 수정(교차적합 조건부 기대 논증, a* 명명,
  점수별 희소성 번역, §4 나머지항 스트레스 테스트 재프레임, PLR 추정 대상
  w=m(1-m) 가중 평균 도출, '절반 이하'→약 40~51%)과 제목 변경 반영.
- 2026-08-05 (2차 검토 반영): §3 불릿의 '독립' 잔재 삭제(조건부 기대 논증으로 통일),
  가토 도함수를 방향 h 표기로 정정(반례 방향 h=m₀ 명시), 본문 수치 범위 ~→en dash
  (Hugo 취소선 렌더 방지), §4 제목 평문화, 한국 자료 함의를 학습 가능 구조 전제로
  한정, overlap·이중강건·검산 서술 완화, fig03 범례 이동·fig04 제목 서술어 보강,
  crossed는 RF·부스팅 한정 명시, 집계에 완전성 assertion 추가, 패키지 .gitignore에
  __pycache__/·*.pyc 추가, README 산출물 목록 현행화. LASSO expB는 100회로 완주해
  결정성 서술을 산출물과 일치시킴.
- 2026-08-05 (3차 검토 반영): IRM 효율성에 조건(모집단 겹침·적률·곱-수렴률) 명시,
  절사는 겹침 가정의 대체가 아님을 본문에 부기, m₀≢0과 교란의 동일시 정정(무작위
  처치 반례 병기), '반드시·필연' 표현 완화, S2 극한을 몬테카를로에서 해석적 정확값
  (0.7775/0.925=+0.8405)으로 교체하고 'MC 오차 범위 내 부합'으로 재서술, description
  국문화, fig05에 패널 간 축 상이 명시, 로그 정리(expB 라쏘 100회 로그를 권위본으로
  일원화), 집계 assertion 강화(필수 파일 존재·expB 100회·crossed 라벨 0–9),
  03_figures 머리말 현행화, README 환경(scipy·폰트)·실행 순서 추가, 8/4 항목의
  교락 수치 인용 금지 표시.
- 2026-08-05 (4차 검토 반영): 중위수법 조정식을 표준오차(모수 단위) 표기로 정정
  (코드와 일치), 나이브 발산 주장을 비소거 조건부로 한정, 교차적합 논증에 학습기
  난수 조건화·조건부 분산 E[V²e²]·적률 유계 명시, 'A형 점수' 명칭을 점수식 직접
  표기로 교체, 정리 4.1 인용에 정칙 조건 병기, §8에서 통계 보장과 인과 해석 분리,
  부록 'DML 전용 패키지 없이'·scipy/matplotlib 병기, ovb_limit_method를 생성 코드에
  반영 + MC 교차확인 helper(s2_ovb_limit_mc, 시드 123) 추가, README 다운로드에
  mkdir -p 추가, 실행 로그는 구값 혼동 방지를 위해 공개 패키지에서 전부 제외,
  fig04 제목·x축 라벨 정밀화, frontmatter에 summary 추가(RSS 절단 방지),
  예상 실행시간 기재. fig05 공통 x축 제안은 패널별 해상도 우선으로 채택하지 않음.
- 2026-08-05 (5차 검토 반영): §3 오차 분해를 θ 단위 항(aligned 4행, Q̂ 정의)으로
  재표기(√n a* 정규수렴 서술, 페이지 overflow 해소 — 긴 수식은 내부 스크롤 유지),
  c→∞ 극한을 '폴드별 평균을
  뺀 원변수·고정 K 대표본 수렴'의 점근 명제로 정정, IRM에 성립·식별 조건
  (D∈{0,1}, E[U|D,X]=0, g₀·m₀ 정의, 일관성·비교란 아래 ATE 식별) 명시, README에
  cd 경로·데이터 URL 커밋 고정(b91cbf9, SHA256 재검증)·pinned pip·--kfolds 5 추가,
  본문 직선 인용부호 26쌍을 곡선부호로 통일(렌더 혼합부호 해소), Donsker '전통적
  경로' 한정·s^m=o(√N)·조건부 동분산 정의 보강, .gitignore에 *.log 추가,
  ovb_limit_method 문자열을 생성 코드와 일치화.
- 2026-08-05 (6차 검토 반영): §2 나이브 분해도 θ 단위 항(a_n, b_n, Q̂_D 정의)으로
  재표기하고 '√n a 정규수렴 / √n b 발산 가능'으로 서술 통일(§3·그림 2와 단위 일치),
  IRM ATE 식별 조건에 겹침(positivity) 추가, README 원자료 표 URL을 커밋 고정으로
  통일, .gitignore를 *.log로 일반화, crossed 명령에 --kfolds 5 명시, 'IRM 균등
  가중'을 모집단 P_X 평균 E[τ(X)]로 정밀화, 절사 무해 조건(참 성향점수가 절사
  구간 내부·점근 비활성) 부기, 5차 로그의 '모바일 넘침 해소' 표현을 '페이지
  overflow 해소·긴 수식 내부 스크롤'로 정정.
- 2026-08-05 (7차 검토 반영 — 용어·문체): dml_core 독스트링을 θ 단위 표기로 정정
  (√n 잔재 제거, Q̂ 정의 명시), '부분선형화'→'잔차화(partialling-out)'로 원고·
  README·코드 일괄 통일(부분선형 '모형'은 유지), '절사'→'클리핑'(np.clip 경곗값
  치환·관측치 미제거 명시, 클리핑 대상은 성향점수 예측치로 정정), '성가신 성분'→
  표준어 '장애모수(nuisance parameter)'(첫 등장 주해), 본문 em dash 72→4(표 행
  라벨만 잔존; 마침표·괄호·'즉'으로 재작성), 커버리지→포함률, 무늬→양상, 팔→
  모형·학습기 조합, 표본 대응물→표본 추정량, Donsker→돈스커류(Donsker class)
  조건, 검침·서명·회계·범인·물어뜯 등 연쇄 비유 완화, '내부 난수'를 개념(내부
  무작위성)/구현(학습기 시드)으로 구분, 정규화 첫 등장에 '복잡도 규제' 주해,
  무통제 첫 표기에 '공변량 미조정' 주해. 그림 6장+커버 재생성(제목·주석 용어 반영).
- 2026-08-05 (8차 검토 반영 — 문장 교정): 장애모수 치환에서 생긴 조사 오류 13건
  교정(은→는·을→를·이→가, 양상이라고만), 43행을 완성형 문장으로, DML2 권고문·
  '모두 원 논문과 다르므로' 문법 정정, '무통제 원차이'→'공변량을 조정하지 않은
  평균 차이(이하 미조정 차이)'로 본문·frontmatter·그림 4 통일, §6 장문단을
  첫째·둘째·셋째 세 문단으로 분리, '수백 달러 이내'·검증 기준점·'각주에서 명시'·
  '100개의 추정치'·분할 스윕 표현 정리, 나이브 첫 사용에 '단순한' 주해, fig04
  '분할 조정' 띄어쓰기·fig05 주석 괄호화, README 모드 설명과 '학습기 시드 스윕'
  통일. ※ 이 항목은 9차 검토가 '보고만 되고 기록은 누락'을 지적해 소급 기재함.
- 2026-08-05 (9차 검토 반영): README 8차 로그 소급 기재(누락 시인), crossed 모드
  표기를 learner 집합 분리형으로 명확화, 학습기 간 이견 통계량을 '분할별 세 학습기
  추정치의 최대–최소 범위, 그 중위값'으로 정의 명시, 미조정 통일 마무리(원차이
  잔재 2건·작은따옴표·표 1 '분할 조정' 띄어쓰기), '이중/편향 제거' 띄어쓰기,
  description 마지막 절을 '추정치 변동을 표본분할과 학습기 무작위성으로 나눈다'로,
  §5에 DML1=DML2 예외(IRM ATE) 병기, PVW(1995) 참고문헌 마침표 보완, fig06 주석
  em dash 제거·fig04 범례 흰 배경(기준선 겹침 해소), 02_401k·04_report의
  '학습기 난수'·'무통제' 라벨을 시드/미조정으로 정리(과거 상태 로그 표현은 보존).
- 2026-08-05 (10차 검토 반영): DML1=DML2 설명을 정확한 조건으로 교체(IRM ATE
  점수는 ψ=φ(W;η)−θ 꼴로 θ 계수가 상수 −1이어서 정확히 일치 — '선형·분리형'
  일반화 철회), README 43행 중복 문구 제거, crossed+lasso를 CLI에서 차단(argparse
  가드), 02_401k·05_aggregate 잔여 용어(무통제 회귀→공변량 미조정 회귀, 학습기
  난수→무작위성/시드) 정리, §4 제목 '조건이 요구하는 것'으로, '분해와 조문'→
  '오차 분해와 이 조건', §6 절차 문장 2문장 분리(중의성 제거), fig05 캡션
  '추정치 100개의 분포'로 수정.
- 2026-08-05 (게시 전 사용자 검토 반영): 본문 그림 6장에 클릭 확대 기능 — 글에
  한정된 자체 라이트박스(외부 라이브러리 없음: 클릭 시 화면 중앙 확대, 배경
  클릭/Esc로 닫기, 그림에 zoom-in 커서)를 넣고, JS 미동작 환경의 대체 경로로
  원본 열기 링크(새 탭,
  단일행 원시 HTML 앵커 — 테마 렌더 훅의 앵커 분열로 생기는 빈 클릭 줄을 피하기
  위해 마크다운 링크 대신 채택), 부록·참고문헌을 trend19 관례의 접이식(details)
  블록으로 전환(목차 앵커 유지, 기본 접힘). CLI 가드 메시지를 '본 실험 설계상
  forest/boosting 전용'으로 정정(IRM 라쏘의 미세 변동과 상충 제거). 로컬 검토용
  hugo server 구성(.claude/launch.json, 미추적)에 --disableFastRender 추가.
- 2026-08-06 (11차 검토 반영, 국문 문체 전면 교정): 비유적 명사 연쇄(장부·약속·
  처방·대가·세계·다이얼·몫·우연·자격·다리 등)를 검토 지시의 대응표대로 평문화.
  본문 182건 + 03_figures.py 22건 정확 일치 치환, 01_simulation.py·02_401k.py
  주석의 잔존 표현 7건 정리. description·summary 교체, 2·3·4·5·6·7절 제목 교체,
  '분할 다중우주'는 본문 1회(이른바~)로 한정. 표 1 제목·헤더(모형·출처) 수정,
  참고문헌 페이지 범위 en dash 통일, 부록 명사형 종결 완결형 전환 및 401(k)
  항목을 자료·설계·학습기·클리핑 하위 목록으로 분리. 그림 6장+커버 재생성
  (fig01 패널 B '결과모형 자기표본 적합', fig02·03·04·05·06 제목·라벨 교체,
  커버 부제 교체)하고 본문 alt/title 캡션 동기화. 검증: 검토 지정 금칙 표현
  30종 본문·스크립트 0건, 수치 전량 04_report_numbers.py 출력과 일치(재실행
  없음, 수치 변경 없음), Hugo 빌드 통과, <del> 0·혼합 인용부호 0·KaTeX 오류 0·
  모바일 넘침 없음. 부수 수정: 6절 '**$19,559 (표준오차 1,413)**입니다'가
  Goldmark 강조 규칙상 리터럴 **로 노출되던 잠복 결함을 강조 범위 조정으로
  해결(굵은 범위를 $19,559로 한정).
