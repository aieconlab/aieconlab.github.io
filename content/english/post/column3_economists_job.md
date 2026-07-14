---
title: "예측이 값싸지는 시대, 경제학자의 일"
date: 2026-07-14T10:30:00+09:00
# post thumb
images:
  - "images/post/column3_cover.png"
#author
author: "송하윤 (Hayun Song)"
# description
description: "예측 비용이 하락하는 시대, 경제학자의 역할 변화: 질문의 설계, 식별, 판단과 책임"
# Taxonomies
categories: ["AI_칼럼"]
tags: ["AI","ECONOMICS","PREDICTION","JUDGMENT","POLICY"]
type: "featured" # available type (regular or featured)
draft: false
---

7월 8일 IMF는 세계경제전망(WEO) 7월 업데이트에서 2026년 세계 성장률 전망을 0.1%포인트 낮추는 한편, 한국의 전망은 30개 선정 경제 가운데 이란과 공동 최대 폭인 0.7%포인트 올렸습니다. 그런데 [이 소식을 전한 글](/post/trend10_imf_korea/)과 [그 후속 분석](/post/analysis_forecast_errors/)에서 확인했듯, 정작 1분기의 이례적인 성장은 공식 전망이 갱신되기 전에 월간 수출 지표가 먼저 신호하고 있었습니다. 정해진 시점에 갱신되는 공식 전망과, 매달 도착하는 자료에 얹은 간단한 모형. 이 대비가 필자에게 남긴 질문은 전망의 정확도가 아니라 다른 것이었습니다. **예측을 생산하는 비용이 눈에 띄게 낮아지고 있다면, 경제학자의 일은 무엇이 되는가.**

## 예측 비용의 하락이라는 관점

인공지능의 경제학적 본질을 한 문장으로 정리한 시도 가운데 필자가 가장 유용하다고 생각하는 것은 Agrawal, Gans, and Goldfarb (2018)의 관점입니다. 이들은 AI를 지능의 문제가 아니라 가격의 문제로 읽습니다. 기계학습의 발전이 한 일은 **예측이라는 투입물의 가격을 극적으로 낮춘 것**이며, 따라서 그 파급은 예측을 투입물로 쓰는 모든 활동의 재편으로 나타난다는 것입니다.

가격이 급락한 재화 앞에서 경제학이 묻는 표준적인 질문은 두 가지입니다. 첫째, 그 재화의 사용은 어디까지 확대되는가. 둘째, **그 재화의 보완재는 무엇이며, 그 수요와 상대적 가치는 어떻게 달라지는가.** 조명 서비스의 실질가격이 수백 년에 걸쳐 극적으로 하락하면서 빛의 사용이 비교할 수 없이 흔해진 것처럼(Nordhaus 1996), 어떤 투입물이 값싸지면 변화의 중심은 그 투입물 자체가 아니라 그것과 결합되는 요소들로 이동합니다.

예측에 이 질문을 적용하면 첫째 답은 이미 눈앞에 있습니다. 나우캐스팅은 자동화되고, 수요 예측과 위험 분류는 상품이 되었으며, 대형 언어모형은 폭넓은 텍스트 과업에서 낮은 한계비용으로 답변의 초안을 만들어 냅니다. 흥미로운 것은 둘째 질문입니다. 예측이 값싸질 때 더 중요해지는 보완재는 무엇인가. 필자는 경제학자의 일과 관련해 세 가지를 꼽습니다.

## 더 중요해지는 세 가지

**첫째, 질문의 설계입니다.** [지도학습을 다룬 글](/post/analysis_prediction_vs_causation/)에서 정리했듯, 정책 문제에는 개입의 인과효과를 별도로 추정하지 않고 결과의 예측과 주어진 손실구조만으로 풀 수 있는 문제(우산을 챙길지)와, 개입 자체의 효과를 알아야 하는 문제(기우제가 비를 부르는지)가 섞여 있습니다(Kleinberg et al. 2015). 예측 기계는 주어진 질문에 답하는 속도를 높여 주고 문제의 후보를 제안할 수도 있지만, 지금 마주한 문제가 어느 유형인지, 어떤 변수의 예측이 의사결정에 실제로 필요한지를 최종 확정하는 데에는 인간의 판단이 필요합니다. 값싼 예측이 흔해질수록, 무엇을 예측하게 할 것인가를 정하는 능력의 상대가치는 오히려 올라갑니다.

**둘째, 식별입니다.** 같은 글의 시뮬레이션이 보여주듯, 교란이 존재할 때 동일한 관측변수와 수집 방식으로 표본만 늘리면 정밀해지는 것은 연관이지 개입의 효과가 아닙니다. 물론 새로운 교란변수의 관측, 도구변수, 자연실험의 변이가 추가되면 식별의 상태는 달라질 수 있습니다. 요점은 인과 문제가 계산력이나 표본 크기만으로 풀리지는 않으며, 식별 가정과 연구 설계가 핵심이라는 것입니다. 자연실험을 찾고 도구변수를 고안하며 정책의 내생성을 의심하는 일은 경제학이 오래 축적해 온 핵심 역량 중 하나입니다. 예측 기계의 시대에 이 능력은 대체되기보다 더 자주 호출됩니다. 값싼 예측이 만들어 낸 그럴듯한 연관들이 인과의 언어로 잘못 번역되는 일 역시 그만큼 흔해지기 때문입니다.

**셋째, 판단과 책임입니다.** Agrawal, Gans, and Goldfarb (2018)의 논의에서 많은 의사결정의 핵심 보완요소는 판단(judgment), 즉 목표와 제약, 상태별 보수와 오류의 비용을 정하는 역할입니다. 예측은 가능한 결과와 그 확률에 관한 정보를 제공하고 때로 불확실성을 줄여 주지만, 그것을 결정으로 바꾸려면 어느 방향의 오류가 더 비싼지에 대한 가치판단이 필요합니다. 과대 전망과 과소 전망의 비용은 정책 맥락에 따라 대칭적이지 않을 수 있으며, 그 비용에는 경험적으로 추정할 수 있는 부분과 규범적·제도적으로 정해야 하는 무게가 함께 들어갑니다. 다만 이 보완성의 크기는 과업의 복잡성과 자동화 가능성에 따라 달라지며, 일부 판단은 그 자체로 자동화의 대상이 되기도 합니다(Agrawal, Gans, and Goldfarb 2019). 그리고 판단에는 책임이 따릅니다. 전망이 틀렸을 때 해명하고 수정하며 그 결과를 감당하는 주체는 여전히 사람과 기관이며, 이 책임은 성능이 아무리 좋은 기계에도 위임되지 않습니다.

## 분업의 재배치

이 블로그의 [3년 전 칼럼](/post/column_2_div_labor/)은 분업과 비교우위의 원리로 인간과 인공지능의 협업 구조를 전망한 바 있습니다. 지금 일어나는 일은 그 원리가 지식노동의 내부, 연구자의 책상 위까지 들어온 것이라고 필자는 이해합니다. 예측이라는 과업이 기계 쪽으로 재배치될 때, 경제학자의 일에서는 숫자의 정확도를 높이고 검증하는 역할에 더해 그 숫자를 어디에 배치하고 어떻게 읽을지를 정하는 역할의 비중이 커집니다.

정책연구의 현장에 이 논리를 적용하면 함의는 구체적입니다. 전망 숫자의 공급은 점점 상시화되고 자동화될 것입니다. 그때 연구기관의 부가가치는 정기적인 점 전망을 내놓는 데서, 시나리오를 설계하고 불확실성을 정직하게 정량화하며 전환점의 신호를 해석하는 쪽으로 이동할 것입니다. 숫자의 공급자에서 질문과 해석의 공급자로 옮겨 가는 이 변화는, 필자가 보기에 위협이 아니라 경제학이 본래 잘하는 일로의 복귀에 가깝습니다.

예측이 값싸질수록 좋은 질문의 희소성과 상대적 가치는 커질 수 있습니다. 경제학자의 일은 사라지는 것이 아니라 재배치되고 있으며, 그 방향은 기계와의 경쟁이 아니라 기계를 전제로 다시 설계된 분업의 안쪽입니다.

### 🔗 참고자료

* Agrawal, A., J. Gans, and A. Goldfarb (2018). [Prediction Machines: The Simple Economics of Artificial Intelligence](https://www.predictionmachines.ai). Harvard Business Review Press.
* Agrawal, A., J. Gans, and A. Goldfarb (2019). [Prediction, Judgment, and Complexity: A Theory of Decision-Making and Artificial Intelligence](https://www.nber.org/books-and-chapters/economics-artificial-intelligence-agenda/prediction-judgment-and-complexity-theory-decision-making-and-artificial-intelligence). In *The Economics of Artificial Intelligence: An Agenda*, pp. 89-110. University of Chicago Press.
* IMF (2026). [World Economic Outlook Update, July 2026](https://www.imf.org/en/publications/weo/issues/2026/07/08/world-economic-outlook-update-july-2026).
* Kleinberg, J., J. Ludwig, S. Mullainathan, and Z. Obermeyer (2015). [Prediction Policy Problems](https://www.aeaweb.org/articles?id=10.1257/aer.p20151023). *American Economic Review: Papers and Proceedings*, 105(5), 491-495.
* Nordhaus, W. D. (1996). [Do Real-Output and Real-Wage Measures Capture Reality? The History of Lighting Suggests Not](https://www.nber.org/books-and-chapters/economics-new-goods/do-real-output-and-real-wage-measures-capture-reality-history-lighting-suggests-not). In *The Economics of New Goods*, University of Chicago Press.

### 🔍 함께 읽기

* [인간-인공지능 분업구조를 통한 지속가능한 성장 (AIEconLab 칼럼, 2023.7)](/post/column_2_div_labor/)
* [경제 전망은 왜 빗나가는가: 35년의 데이터, 그리고 하나의 실험 (2026.7)](/post/analysis_forecast_errors/)
* [지도학습의 경제학: 예측과 인과 사이 (2026.7)](/post/analysis_prediction_vs_causation/)

---

*본 글은 필자 개인의 의견으로, 소속 기관의 공식 입장과 무관합니다.*
