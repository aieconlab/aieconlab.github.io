---
title: "미국이 AI 모델 접근을 막은 18일: 한국의 소버린 AI는 어떤 보험이어야 하나"
date: 2026-07-18T01:00:00+09:00
# post thumb
images:
  - "images/post/trend12_cover.png"
#author
author: "송하윤 (Hayun Song)"
# description
description: "6월 12일 미국의 수출통제로 최첨단 AI 모델 접근이 18일간 멈췄고, 복원조차 차등적이었다. 국가대표 AI 4팀의 현재, 공공 GPU, AI for All, 사이버보안 특화 모델까지, 한국이 사들이고 있는 '보험'들을 실물옵션의 관점에서 점검한다."
# Taxonomies
categories: ["AI_트렌드"]
tags: ["AI","ECONOMICS","KOREA","POLICY","Sovereign AI","SECURITY"]
type: "featured" # available type (regular or featured)
draft: false
---

7월 16일 이재명 대통령 주재로 열린 정부 하반기 정책 브리핑에서, 배경훈 과학기술정보통신부 장관은 사이버보안에 특화된 소버린 AI 모델을 연내 개발·출시하겠다는 계획을 발표했습니다. 개발 중인 독자 모델에 보안 데이터를 추가 학습시키는 방식이며, 장기적으로는 해외 선도 모델에 견줄 프런티어급 모델의 개발도 검토하겠다고 했습니다. [코리아타임스는 이 발표의 배경으로 최근 미국의 AI 모델 수출통제 사태를 짚었습니다](https://www.koreatimes.co.kr/business/tech-science/20260716/korea-to-launch-sovereign-ai-for-cybersecurity-this-year-science-minister).

무슨 사태였는지부터 정리하고 시작하겠습니다. 지난 한 달 사이, '소버린 AI'라는 오래된 논쟁의 조건이 하나 바뀌었기 때문입니다.

## 미국이 모델 접근을 막은 18일

[6월 12일, Anthropic은 미국 정부의 수출통제 지시에 따라 최신 모델인 Fable 5와 Mythos 5의 접근을 중단한다고 공지했습니다](https://www.anthropic.com/news/fable-mythos-access). 지시의 내용은 자사의 외국인 직원까지 포함한 외국인의 접근 제한이었지만, 이용자의 국적을 실시간으로 확인할 방법이 없었던 회사는 준수를 위해 모든 이용자의 접근을 차단했습니다. 정부는 국가안보 권한을 근거로 들었을 뿐 구체적인 사유를 공개하지 않았고, Anthropic은 Fable 5의 안전장치를 우회하는 이른바 탈옥 기법이 보고된 데 따른 조치로 이해한다며, 시연된 기법으로 발견되는 취약점은 다른 공개 모델로도 찾을 수 있는 수준이었다고 반박했습니다. 함께 차단된 Mythos 5는 취약점 탐지에 특화된 모델로, [사이버 공격에 악용될 가능성이 전문가들 사이에서 우려되어 온 모델입니다](https://www.cnn.com/2026/06/30/tech/anthropic-export-control-ban-lifted-white-house).

[통제는 6월 30일 해제되었습니다](https://www.anthropic.com/news/redeploying-fable-5). 해제와 함께 Anthropic은 국가안보와 관련된 모델의 출시 전 정부 접근·평가, 탈옥 기법과 안전장치에 관한 신속한 정보 공유, 정부와의 공동 연구, 업계 공동 보안 표준에 대한 기여 등 정부 협력을 강화하겠다고 약속했습니다. 다만 복원의 범위는 같지 않았습니다. 7월 1일 Fable 5는 전 세계 이용자에게 복원된 반면, **Mythos 5는 미국 정부의 승인을 받은 일부 미국 기관에만 우선 복원**됐고, 국내외 파트너로의 확대는 협의가 이어지고 있습니다.

사고라고 부를 만한 일은 없었습니다. 그러나 두 가지가 남았습니다. 첫째, 세계에서 가장 강력한 축에 드는 AI 모델에 대한 접근이 **사전 예고 없이, 공개된 사유 없이, 한 번의 행정 결정으로** 사라질 수 있다는 사실이 실증되었습니다. 동맹국의 기업과 이용자도 예외가 아니었고, 복원조차 국적과 기관 단위로 차등적이었습니다. 둘째, 반도체 장비와 칩에서 시작된 수출통제의 대상이 이제 모델 그 자체로 확장될 수 있음이 확인되었습니다. 7월 16일의 사이버보안 모델 발표는 이 직후에 나온 것이고, [같은 날 업무보고 자료는 독자 모델 확보의 배경으로 미국의 AI 접근통제를 명시했습니다](https://www.korea.kr/news/policyFocusView.do?newsId=148968284).

## 소버린 AI는 무엇을 보장하는가

소버린 AI는 정의부터 논쟁적인 용어입니다. 국산 모델을 뜻하는지, 국내 데이터센터를 뜻하는지, 데이터에 대한 통제를 뜻하는지가 논자마다 다르고, [스탠퍼드 HAI는 이 정의의 혼란 자체가 정책의 초점을 흐릴 수 있다고 지적합니다](https://hai.stanford.edu/news/ai-sovereigntys-definitional-dilemma). 이 글에서는 경제학의 언어로 좁혀 보겠습니다.

소버린 AI는 사고가 나면 보험금이 지급되는 일반적인 보험이라기보다, **공급이 끊겼을 때 전환할 수 있는 경로를 평시에 유지하는 실물옵션**에 가깝습니다. 그 연간 기대가치는 대략 다음처럼 쓸 수 있습니다.

> 소버린 AI의 연간 기대가치 ≈ 연간 차단 확률 × 기간당 피해 × 예상 차단 기간 × 대체역량의 피해 감축률 − 연간 유지비용

엄밀한 실물옵션 가치평가라기보다 기대손실의 감소를 보여주는 개념적 근사식이고, 각 항은 측정하기 어렵습니다. 그럼에도 이 식은 6월의 18일이 무엇을 바꿨는지 분명히 해 줍니다. 바뀐 것은 첫째 항에 대한 인식입니다. 공급 차단의 확률은 0이 아니며, 그것이 가정이 아니라 실제 사건으로 갱신되었습니다.

이 관점의 또 다른 쓸모는 '소버린이냐 아니냐'라는 이분법을 해체한다는 데 있습니다. AI는 컴퓨트, 모델, 데이터, 응용으로 이어지는 스택이고, 레이어마다 위험도 합리적인 보험도 다릅니다.

| 레이어 | 주요 위험 | 합리적인 '보험' |
|---|---|---|
| 컴퓨트·클라우드 | GPU·클라우드 공급 차단 | 공공 최소 용량, 복수 공급자, 워크로드 이식성 |
| 모델 | API·가중치 접근 제한 | 국산·오픈웨이트 대체 모델, 다중 모델 조달 |
| 데이터·평가 | 역외 규제, 언어·문화 부적합 | 국내 데이터 거버넌스, 독립적 평가 체계 |
| 핵심 응용 | 사이버보안·국방·공공서비스 중단 | 국내 통제하의 최소 실행 가능 역량 |

해외의 논의에서도 같은 방향이 보입니다. [카네기국제평화재단의 분석은](https://carnegieendowment.org/research/2026/06/early-lessons-in-the-pursuit-of-sovereign-ai) 모든 레이어의 완전한 자급자족이 대부분의 나라에서 비현실적이므로, 어느 레이어에서 의존을 허용하고 어디에서 선택권을 보존할지 고르는 관리된 상호의존(managed interdependence)을 더 정직한 목표로 제시합니다. 자국어 모델을 키우면서 미국의 칩과 클라우드에 의존하는 인도, 지분 투자를 접근 보장의 지렛대로 쓰는 UAE가 그런 사례로 분석됩니다.

## 한국이 이미 사들인 보험들

이 표 위에 한국 정부의 최근 행보를 얹어 보면, 흩어져 보이던 정책들이 하나의 그림이 됩니다. 거의 모든 레이어에서 동시에 보험을 사들이는 중입니다.

**모델: 국가대표 AI.** 공식 명칭은 '독자 AI 파운데이션 모델' 사업입니다. [GPU 임차(1차 추경 1,576억 원)와 데이터·인재 지원을 2027년까지 단계적으로 제공하며](https://www.korea.kr/news/policyNewsView.do?newsId=148944741), [GPU·데이터·인재를 합친 지원의 경제적 가치는 약 5,300억 원 규모로 보도되었습니다](https://www.newspim.com/news/view/20250814001157). 사업은 평가 시점의 최신 선도 모델 대비 95% 수준이라는 '이동 목표'를 따라갑니다. 지난해 8월 5개 정예팀으로 출발해 [올해 1월 1차 평가에서 네이버클라우드와 NC AI가 탈락했고](https://www.koreaherald.com/article/10656367), [2월 패자부활전으로 스타트업 모티프테크놀로지스가 합류해](https://www.sisajournal-e.com/news/articleView.html?idxno=419380) 현재 4팀 체제입니다. 4팀의 현재 상황은 다음과 같습니다.

| 정예팀 | 모델·개발 방향 | 7월 18일 현재 |
|---|---|---|
| LG AI연구원 | K-EXAONE 고도화, 1차 모델(236B MoE)로 종합 1위 | 6월 말 개발 완료 |
| SK텔레콤 | A.X K2(2차 평가용), 에이전트 능력·효율성과 산업 실증 | 6월 말 완료, 7월 14일 공식 발표 |
| 업스테이지 | Solar Open 2, 1차 '솔라 오픈 100B'의 후속 | 6월 말 개발 완료 |
| 모티프테크놀로지스 | 모티프-2-12.7B 기반 300B급 추론형 개발, 이후 VLM·VLA 목표 | 7월 말 제출 예정 |

<small>자료: [과기정통부 1차 평가 브리핑](https://www.korea.kr/news/policyNewsView.do?newsId=156740468), [SKT 뉴스룸](https://news.sktelecom.com/227799), [ZDNet코리아](https://zdnet.co.kr/view/?no=20260706164236), [머니투데이](https://www.mt.co.kr/amp/tech/2026/07/15/2026071514532688639), [데이터넷](https://www.datanet.co.kr/news/articleView.html?idxno=209450), [인더스트리뉴스](https://www.industrynews.co.kr/news/articleView.html?idxno=78295)</small>

네 팀은 단일 기업 네 곳이 아니라 모델·클라우드·데이터·대학·산업 적용 기업이 결합한 컨소시엄입니다(모티프 팀에만 17개 기관이 참여합니다). 정부가 사들이는 보험이 모델 파일 하나가 아니라 **훈련·운영·고도화 역량을 갖춘 생태계**에 가깝다는 뜻입니다. 8월 초에는 4팀을 3팀으로 압축하기 위한 2차 평가에 들어가고, 이후 3차 평가를 거쳐 최종 2팀을 선정합니다. [ZDNet코리아는 재공모를 거치며 당초 연말이던 최종 선발이 내년 초로 밀렸다고 보도했습니다](https://zdnet.co.kr/view/?no=20260706164236).

**컴퓨트: 공공 GPU.** [지난해 10월 엔비디아와 한국 정부·기업들은 향후 수년에 걸쳐 GPU 26만 장 이상을 도입하는 계획을 발표했습니다](https://nvidianews.nvidia.com/news/south-korea-ai-infrastructure). 정부 부문 최대 5만 장, 삼성전자·SK 각 5만 장 이상, 현대차그룹 5만 장, 네이버클라우드 6만 장 이상의 구성으로, 소버린 모델 전용이 아니라 국가 전반의 AI 인프라 계획입니다. [정부 확보분은 대학과 연구기관, 국가 AI 프로젝트를 대상으로 배분이 시작되었고](https://www.koreaherald.com/article/10678398), [6월에는 차세대 GPU '베라 루빈'의 우선 공급 계획도 보도되었습니다](https://en.sedaily.com/finance/2026/06/08/korea-secures-priority-supply-of-nvidias-vera-rubin-gpus).

**서비스: AI for All.** [7월 13일 공고된 전 국민 무료 AI 서비스 사업입니다](https://en.sedaily.com/technology/2026/07/13/korea-launches-ai-for-all-project-deploying-512-gpus-for). 정부의 독자 파운데이션 모델 기준을 충족하는 국산 모델을 시스템의 50% 이상 쓰되, **자사 외 다른 국내 기업의 모델도 30% 이상** 사용해야 합니다. 수요를 여러 국산 모델에 배분하는 장치입니다. 선정되는 2~3개 사업자에는 개발과 초기 서비스를 위한 B200 GPU 총 512장이 지원되며, 8월 11일 접수 마감 후 9월 말 베타를 거쳐 연내 정식 서비스가 목표입니다.

**응용: 사이버보안 특화 모델.** 서두의 7월 16일 발표입니다. 기존 독자 모델에 보안 데이터를 추가 학습시켜 연내 출시를 추진하고, 장기적으로는 프런티어급 모델도 검토합니다.

**제도: AI 기본법.** [1월 22일 시행된 포괄적 AI 법제는](https://www.cooley.com/news/insight/2026/2026-01-27-south-koreas-ai-basic-act-overview-and-key-takeaways) 국내에서 쓰이는 AI를 어떻게 규율할지에 대한 권한을 확보한다는 점에서, 위 레이어들을 관통하는 또 하나의 선택권입니다.

## 보험료는 적정한가

가장 흔한 회의론은 규모에서 출발합니다. [스탠퍼드 AI Index 2026에 따르면](https://hai.stanford.edu/ai-index/2026-ai-index-report/economy) 2025년 민간 AI 투자는 미국이 2,858.8억 달러로 중국(124.1억 달러)의 23배였고, 영국은 59억 달러, 한국은 17.8억 달러였습니다.

![2025년 민간 AI 투자 국가 비교](/images/post/sovereign_ai/fig01_private_ai_investment.png "그림 1: 2025년 민간 AI 투자, 미국·중국·영국·한국. 아래 패널은 미국을 제외한 확대 비교. 중국은 정부 주도 기금을 통한 투자가 민간 통계에 충분히 잡히지 않을 수 있어 실제 격차는 이보다 작을 수 있다. (자료: Stanford HAI, AI Index Report 2026)")

미국의 민간 투자 총액과 약 5,300억 원 상당의 정부 지원은 성격이 다른 돈이므로 직접 비교할 수 없습니다. 그러나 시장의 절대 규모가 이만큼 다르다는 사실은 프런티어 경쟁의 조건을 규정합니다. 이 지원 규모는 프런티어 랩들이 반복 실험과 인재, 데이터, 추론 인프라 운영에 쏟는 총비용과 정면으로 경쟁하기에는 제한적입니다. [해외에서는 이런 격차를 근거로, 소버린 AI가 정치적으로는 매력적이지만 경제적으로는 공허한 약속이 될 수 있다는 경고도 나옵니다](https://www.ictworks.org/resist-the-sovereign-generative-ai-trap/).

그래서 이 사업의 목표 설정을 다시 볼 필요가 있습니다. '선도 모델 대비 95%'는 특정 시험의 합격선이 아니라 사업 전체가 따라가는 이동 목표이고, 실물옵션의 관점에서 이 사업이 사는 것은 1등이 아니라 **끊겨도 돌아가는 경로**입니다. 다만 정부의 목표가 보험에 그치는 것도 아닙니다. [7월 16일 업무보고는 올 하반기 내 '글로벌 10위권 성능'의 독자 모델 확보를 함께 내걸었습니다](https://www.korea.kr/news/policyFocusView.do?newsId=148968284). 독파모는 공급 차단에 대비한 보험인 동시에 프런티어 경쟁을 겨냥한 산업정책이며, **제한된 예산으로 두 목표를 동시에 이룰 수 있느냐**가 보험료 논쟁의 실체입니다. 그 위에 남은 논점이 세 가지 더 있습니다.

첫째, **'독자성'의 정의입니다.** [1차 평가에서 네이버클라우드는 외부 모델의 학습된 가중치를 동결 상태로 활용한 점이 문제가 되어 탈락했습니다. 정부 기준은 오픈소스 아키텍처의 사용 자체를 막는 것이 아니라, 이미 학습된 외부 가중치를 그대로 쓰는 것과 가중치를 초기화해 처음부터 학습하는 것을 구분하고, 후자를 독자성의 최소조건으로 봅니다](https://www.korea.kr/news/policyNewsView.do?newsId=156740468). 보험의 언어로 옮기면 두 종류의 보험을 구분한 것입니다. 공개된 가중치를 확보해 해외 API가 끊겨도 운영을 이어가는 **접근 보험**과, 위협과 기술 변화에 맞춰 구조를 바꾸고 처음부터 재학습할 수 있는 **역량 보험**. 정부는 후자에 더 높은 값을 쳐준 셈입니다. 다만 오픈웨이트 모델 위에 쌓은 역량도 접근 보험으로는 유효하기에 이 기준이 과하다는 반론이 가능하고, [국내에서는 파운데이션 모델 편중과 선발-경쟁-탈락 구조가 실험보다 과제 수주를 우선하게 만들 수 있다는 생태계 비판도 있습니다](https://www.mobizen.pe.kr/1482).

둘째, **레이어 간 불균형입니다.** 모델 레이어의 선택권은 늘리는 동안, 공공 GPU 조달과 독파모 지원 인프라는 여전히 엔비디아 중심입니다. 앞의 표로 보면 이는 위선이 아니라 선택입니다. 모든 레이어에서 같은 수준의 주권을 추구할 수는 없기 때문입니다. [업스테이지가 AMD 가속기(MI355)를 개발에 도입하는 것처럼 다변화 시도도 시작됐지만](https://zdnet.co.kr/view/?no=20260319092507), 복수 공급자와 워크로드 이식성이 구조화되지 않는 한 모델 주권은 공급자 한 곳의 결정에 여전히 노출된 보험으로 남습니다.

셋째, **민간의 포트폴리오와의 정합성입니다.** [삼성전자와 SK하이닉스는 5월 Anthropic의 650억 달러 시리즈 H 조달 발표에 '전략적 인프라 파트너'로 이름을 올렸고](https://www.anthropic.com/news/series-h), [삼성과 Anthropic의 커스텀 칩 협력 가능성에 대한 초기 논의도 보도되었습니다](https://techcrunch.com/2026/07/02/anthropic-is-discussing-a-new-custom-chip-with-samsung/). 국내 소버린 정책의 이해당사자이기도 한 기업들이 동시에 글로벌 프런티어 랩의 공급망에 자리를 확보하는 셈인데, 이를 이중 플레이로 읽을 이유는 없습니다. 국내 역량과 글로벌 공급망 접근을 함께 확보하는 헤징이고, 개별 기업으로서는 합리적인 포트폴리오입니다. 국가의 소버린 AI 전략도 같은 눈으로 읽어야 앞뒤가 맞습니다. 목표는 글로벌 공급망으로부터의 이탈이 아니라, 이탈'당할' 가능성에 대한 대비입니다.

## 자급자족이 아닌 관리된 상호의존

질문을 다시 정리하겠습니다. 6월의 18일 이후에 '소버린 AI를 할 것인가'는 좋은 질문이 아닙니다. 한국은 이미 하고 있기 때문입니다. 좋은 질문은 '어느 레이어에서, 어느 정도의 선택권을, 얼마에 유지할 것인가'이고, 이 질문에는 올해 하반기에 확인할 수 있는 시금석이 세 개 있습니다.

첫째, **8월 초 착수되는 국가대표 AI 2차 평가.** 글로벌 벤치마크와 독자성 평가 등을 포함하는 시험대로, 4팀이 3팀으로 압축되면서 정부가 접근 보험과 역량 보험 중 무엇에 얼마의 값을 쳐주는지가 드러납니다. 둘째, **AI for All의 9월 말 베타와 연내 정식 서비스.** 국산 모델 비중 요건을 단 전 국민 서비스가 실제 이용자를 얼마나 확보하는지는 국산 모델 수요의 가장 직접적인 검증대입니다. 셋째, **연내 사이버보안 특화 모델.** 안보 응용 레이어에서 '국내 통제하의 최소 실행 가능 역량'이 작동하는지 보여줄 첫 사례입니다.

[앞서 다룬 '3·4·5 비전'](/post/trend11_345_vision/)이 AI를 성장의 엔진으로 놓는 전략이라면, 소버린 AI는 그 엔진의 연료 공급이 끊길 가능성에 대한 보험입니다. [IMF가 공식화한 AI 경제 격차](/post/trend10_imf_korea/)의 세계에서 한국이 고른 위치이기도 합니다. 보험의 최선의 시나리오는 끝내 쓰일 일이 없는 것입니다. 그러나 보험료가 적정한지는 사고가 나기 전에만 물을 수 있는 질문입니다. 6월의 18일은 짧았지만, 그 질문을 더는 미룰 수 없게 만들었습니다.

### 🔗 참고자료

* 📄 [Anthropic - A restriction on access to Fable 5 and Mythos 5 (2026.6.12)](https://www.anthropic.com/news/fable-mythos-access)
* 📄 [Anthropic - Redeploying Fable 5 and Mythos 5 (2026.7.1)](https://www.anthropic.com/news/redeploying-fable-5)
* 📰 [CNN - White House lifts export control on Anthropic that froze its most advanced models (2026.6.30)](https://www.cnn.com/2026/06/30/tech/anthropic-export-control-ban-lifted-white-house)
* 📰 [The Korea Times - Korea to launch sovereign AI for cybersecurity this year: science minister (2026.7.16)](https://www.koreatimes.co.kr/business/tech-science/20260716/korea-to-launch-sovereign-ai-for-cybersecurity-this-year-science-minister)
* 📄 [대한민국 정책브리핑 - 과기정통부 2026년 업무보고: 국민과 함께 여는 AI 시대 (2026.7.16)](https://www.korea.kr/news/policyFocusView.do?newsId=148968284)
* 📄 [대한민국 정책브리핑 - 독자 AI 파운데이션 모델 1차 평가 결과 브리핑 (2026.1)](https://www.korea.kr/news/policyNewsView.do?newsId=156740468)
* 📄 [대한민국 정책브리핑 - 독자 AI 파운데이션 모델 사업 지원 안내](https://www.korea.kr/news/policyNewsView.do?newsId=148944741)
* 📰 [The Korea Herald - LG, SKT, Upstage advance in Korea's sovereign AI project; Naver, NC dropped in 1st round (2026.1)](https://www.koreaherald.com/article/10656367)
* 📰 [시사저널e - '국가대표 AI' 패자부활전 모티프테크놀로지스 선정…8월 2차 평가 진행 (2026.2)](https://www.sisajournal-e.com/news/articleView.html?idxno=419380)
* 📰 [ZDNet Korea - 독파모 일정 지연, 최종 선발은 내년 초로 (2026.7.6)](https://zdnet.co.kr/view/?no=20260706164236)
* 📰 [ZDNet Korea - 업스테이지, AMD MI355 도입…소버린 AI 인프라 다변화 (2026.3.19)](https://zdnet.co.kr/view/?no=20260319092507)
* 📰 [머니투데이 - 독파모 4팀 2차 평가 모델 제출 현황 (2026.7.15)](https://www.mt.co.kr/amp/tech/2026/07/15/2026071514532688639)
* 📰 [뉴스핌 - '5300억 지원' 국가대표 AI (2025.8.16)](https://www.newspim.com/news/view/20250814001157)
* 📰 [SKT 뉴스룸 - 독자 AI 파운데이션 모델 'A.X K2' 구축 (2026.7.14)](https://news.sktelecom.com/227799)
* 📰 [데이터넷 - [독자 AI 파운데이션 모델②] 기술 자립 넘어 실리로 (2026.2.24)](https://www.datanet.co.kr/news/articleView.html?idxno=209450)
* 📰 [인더스트리뉴스 - 독자 AI 파운데이션 모델 사업에 모티프 추가 선정 (2026.2)](https://www.industrynews.co.kr/news/articleView.html?idxno=78295)
* 📄 [NVIDIA - NVIDIA, South Korea Government and Industrial Giants Build AI Infrastructure and Ecosystem (2025.10)](https://nvidianews.nvidia.com/news/south-korea-ai-infrastructure)
* 📰 [The Korea Herald - Korea begins rollout of 10,000 Nvidia GPUs under 260,000-unit plan](https://www.koreaherald.com/article/10678398)
* 📰 [Seoul Economic Daily - Korea Secures Priority Supply of Nvidia's Vera Rubin GPUs (2026.6)](https://en.sedaily.com/finance/2026/06/08/korea-secures-priority-supply-of-nvidias-vera-rubin-gpus)
* 📰 [Seoul Economic Daily - Korea Launches 'AI for All' Project, Deploying 512 GPUs for Service Within Year (2026.7.13)](https://en.sedaily.com/technology/2026/07/13/korea-launches-ai-for-all-project-deploying-512-gpus-for)
* 📄 [Cooley - South Korea's AI Basic Act: Overview and Key Takeaways (2026.1.27)](https://www.cooley.com/news/insight/2026/2026-01-27-south-koreas-ai-basic-act-overview-and-key-takeaways)
* 📊 [Stanford HAI - AI Index Report 2026: Economy](https://hai.stanford.edu/ai-index/2026-ai-index-report/economy)
* 📄 [Stanford HAI - AI Sovereignty's Definitional Dilemma](https://hai.stanford.edu/news/ai-sovereigntys-definitional-dilemma)
* 📄 [Carnegie Endowment - Early Lessons in the Pursuit of Sovereign AI (2026.6)](https://carnegieendowment.org/research/2026/06/early-lessons-in-the-pursuit-of-sovereign-ai)
* 📄 [ICTworks - We Must Help Countries Resist the Sovereign Generative AI Trap](https://www.ictworks.org/resist-the-sovereign-generative-ai-trap/)
* 📄 [Anthropic - Series H (2026.5.28)](https://www.anthropic.com/news/series-h)
* 📰 [TechCrunch - Anthropic is discussing a new custom chip with Samsung (2026.7.2)](https://techcrunch.com/2026/07/02/anthropic-is-discussing-a-new-custom-chip-with-samsung/)
* 📄 [모비즌 - 정부의 K-AI 사업에 대한 까칠한 소고](https://www.mobizen.pe.kr/1482)
* 🔍 함께 읽기: ['3·4·5 비전'의 세 가지 시험대](/post/trend11_345_vision/) · [세계는 내리고, 한국은 올렸다: IMF가 공식화한 'AI 경제 격차'](/post/trend10_imf_korea/) · [대한민국 정부와 AI](/post/trend7_korea_ai/)

---

*본 글은 필자 개인의 의견으로, 소속 기관의 공식 입장과 무관합니다.*
