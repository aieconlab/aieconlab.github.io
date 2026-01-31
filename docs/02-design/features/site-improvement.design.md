# Site Improvement Design

> AIEconLab Hugo 사이트 개선 - 구체적 구현 설계

## 1. Overview

| 항목 | 내용 |
|------|------|
| Feature | site-improvement |
| Phase | Design |
| Plan Reference | [site-improvement.plan.md](../../01-plan/features/site-improvement.plan.md) |
| Created | 2026-02-01 |

---

## 2. Phase 1: Critical Fixes (즉시 구현)

### 2.1 이미지 파일 최적화

#### 대상 파일 및 작업
| 파일 경로 | 현재 | 목표 | 작업 |
|----------|------|------|------|
| `assets/images/Hayun_Song.png` | 10.5 MB | < 300 KB | 리사이즈 + 압축 |
| `assets/images/JungHyuk_Lee.jpg` | 5.5 MB | < 300 KB | 리사이즈 + 압축 |
| `assets/images/Youngmin_Ju.jpg` | 2.9 MB | < 300 KB | 리사이즈 + 압축 |
| `assets/images/post/AI_in_America.png` | 1.6 MB | < 500 KB | 압축 |
| `assets/images/post/data frontier.png` | 1.5 MB | < 500 KB | 압축 |

#### 구현 방법
```bash
# 방법 1: Hugo 내장 이미지 처리 활용 (권장)
# 템플릿에서 자동 리사이즈 - 이미 적용되어 있음

# 방법 2: 원본 이미지 수동 최적화
# 저자 이미지: 400x400px, 품질 80%
# 포스트 이미지: 1200px 너비, 품질 85%
```

#### 체크리스트
- [ ] 저자 이미지 3개 리사이즈 (400x400)
- [ ] 저자 이미지 압축 (품질 80%)
- [ ] 포스트 이미지 압축 (품질 85%)
- [ ] 빌드 후 processed images 크기 확인

---

### 2.2 hugo.toml 정리

#### 현재 상태
```toml
# hugo.toml (루트)
baseURL = 'http://example.org/'
languageCode = 'en-us'
title = 'My New Hugo Site'
```

#### 구현 방법
```bash
# 옵션 A: 파일 삭제 (권장)
rm hugo.toml

# 옵션 B: .gitignore에 추가
echo "hugo.toml" >> .gitignore
```

#### 체크리스트
- [ ] `hugo.toml` 삭제 또는 수정
- [ ] 빌드 테스트 확인

---

### 2.3 메타데이터 수정

#### 파일: `config/_default/params.toml`

#### 변경 사항
```toml
# Line 79-83: [metadata] 섹션
# Before:
keywords = ["Boilerplate", "Hugo", "Themefisher", "GetHugoThemes"]
description = "This is meta description"
author = "Themefisher"
image = "images/favicon.png"

# After:
keywords = ["AI", "인공지능", "경제학", "AI트렌드", "머신러닝", "AIEconLab", "인공지능경제연구소"]
description = "인공지능경제연구소(AIEconLab) - AI 경제학 연구, 트렌드 분석, 정책 연구"
author = "AIEconLab"
image = "images/logo.png"
```

#### 체크리스트
- [ ] `params.toml` 메타데이터 수정
- [ ] OpenGraph 미리보기 테스트

---

## 3. Phase 2: High Priority (1주일 내)

### 3.1 Hugo 버전 업데이트

#### 파일: `netlify.toml`

#### 변경 사항
```toml
# Line 6
# Before:
HUGO_VERSION = "0.90.1"

# After:
HUGO_VERSION = "0.121.0"
```

#### 호환성 체크
- [ ] 로컬에서 Hugo 0.121.0으로 빌드 테스트
- [ ] 템플릿 문법 호환성 확인
- [ ] 이미지 처리 정상 동작 확인

---

### 3.2 보안 헤더 강화

#### 파일: `netlify.toml`

#### 추가 헤더
```toml
# [headers] 섹션에 추가
[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-XSS-Protection = "1; mode=block"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"
    Permissions-Policy = "geolocation=(), microphone=(), camera=()"
    Strict-Transport-Security = "max-age=31536000; includeSubDomains; preload"
```

#### 체크리스트
- [ ] 보안 헤더 추가
- [ ] https://securityheaders.com/ 에서 테스트

---

### 3.3 캐시 헤더 설정

#### 파일: `netlify.toml`

#### 추가 설정
```toml
# 정적 에셋 캐싱
[[headers]]
  for = "/images/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[headers]]
  for = "/*.css"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[headers]]
  for = "/*.js"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[headers]]
  for = "/*.woff2"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"
```

#### 체크리스트
- [ ] 캐시 헤더 추가
- [ ] Chrome DevTools Network 탭에서 캐시 확인

---

## 4. Phase 3: Medium Priority (1개월 내)

### 4.1 콘텐츠 일관성 수정

#### 4.1.1 elements.md 저자 수정
```yaml
# content/english/post/elements.md
# Line 9
# Before:
author: "Youngmin Ju"

# After:
author: "주영민 (Youngmin Ju)"
```

#### 4.1.2 드래프트 포스트 처리
| 파일 | 현재 상태 | 권장 조치 |
|------|----------|----------|
| `post-3.md` | draft: true | 삭제 또는 완성 |
| `post-4.md` | draft: true | 삭제 또는 완성 |
| `post-6.md` | draft: true | 삭제 또는 완성 |
| `elements.md` | draft: true | 삭제 (테마 예제) |

---

### 4.2 JSON-LD Schema 수정

#### 파일: `themes/logbook-hugo/layouts/_default/single.html`

#### 변경 사항 (Line 93-118)
```html
<!-- Before (Line 103) -->
"image": "{{.Params.images | relURL}}",

<!-- After -->
{{ if .Params.images }}
"image": "{{ (index .Params.images 0) | absURL }}",
{{ else }}
"image": "{{ site.Params.image | absURL }}",
{{ end }}
```

#### 체크리스트
- [ ] JSON-LD 수정
- [ ] Google Rich Results Test로 검증

---

### 4.3 Contact Form 연동 (선택)

#### 옵션 A: Netlify Forms
```html
<!-- content/english/contact.md 또는 관련 템플릿 -->
<form name="contact" method="POST" data-netlify="true">
  <!-- form fields -->
</form>
```

#### 옵션 B: Formspree
```toml
# config/_default/params.toml
contact_form_action = "https://formspree.io/f/YOUR_FORM_ID"
```

---

## 5. Phase 4: Low Priority (분기 내)

### 5.1 불필요 파일 정리

#### 삭제 대상
```bash
# 드래프트 포스트 (확인 후 삭제)
content/english/post/post-3.md
content/english/post/post-4.md
content/english/post/post-6.md
content/english/post/elements.md

# 사용하지 않는 홈페이지 레이아웃
content/english/homepage/full-left.md
content/english/homepage/full-right.md
content/english/homepage/grid-left.md
content/english/homepage/grid-right.md
content/english/homepage/list-left.md
content/english/homepage/list-right.md

# 비활성화된 언어 콘텐츠
content/french/  (전체 디렉토리)
```

### 5.2 접근성 개선

#### 이미지 Alt 텍스트 템플릿 수정
```html
<!-- 현재 -->
alt="post-thumb"

<!-- 개선 -->
alt="{{ .Title }}"
```

#### 대상 파일
- `themes/logbook-hugo/layouts/_default/single.html`
- `themes/logbook-hugo/layouts/partials/default.html`
- `themes/logbook-hugo/layouts/partials/featured-post.html`

---

## 6. 구현 순서

```
Phase 1 (Day 1)
├── 2.1 이미지 최적화
├── 2.2 hugo.toml 삭제
└── 2.3 메타데이터 수정

Phase 2 (Day 2-3)
├── 3.1 Hugo 버전 업데이트
├── 3.2 보안 헤더 추가
└── 3.3 캐시 헤더 설정

Phase 3 (Week 2-4)
├── 4.1 콘텐츠 일관성
├── 4.2 JSON-LD 수정
└── 4.3 Contact Form (선택)

Phase 4 (Month 2-3)
├── 5.1 파일 정리
└── 5.2 접근성 개선
```

---

## 7. 테스트 계획

| 항목 | 테스트 방법 | 성공 기준 |
|------|------------|----------|
| 이미지 최적화 | `hugo --minify` 빌드 | 총 이미지 < 5MB |
| Hugo 버전 | 로컬 빌드 | 에러 없음 |
| 보안 헤더 | securityheaders.com | Grade A+ |
| SEO 메타데이터 | opengraph.xyz | 정상 표시 |
| JSON-LD | Google Rich Results | Valid |
| Lighthouse | Chrome DevTools | Performance > 90 |

---

## 8. 롤백 계획

모든 변경은 Git으로 관리:
```bash
# 문제 발생 시 롤백
git revert HEAD
hugo --minify
# Netlify 자동 배포
```

---

*Generated by bkit PDCA System*
