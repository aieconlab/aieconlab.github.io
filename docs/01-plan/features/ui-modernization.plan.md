# PDCA Plan: UI Modernization

> **Feature**: ui-modernization
> **Created**: 2026-01-31
> **Updated**: 2026-02-01
> **Phase**: Plan
> **Status**: Updated

---

## 1. Overview

AIEconLab 홈페이지의 UI/UX를 현대적이고 세련되게 개선하는 프로젝트입니다.

### 1.1 Goals
- 메인페이지 Featured Post 썸네일 이미지 비율 문제 해결
- 전체적인 색상 팔레트 및 디자인 모던화
- **Author 페이지 UI 모던화** (프로필 카드 스타일)

### 1.2 Scope
| In Scope | Out of Scope |
|----------|--------------|
| Featured Post 이미지 수정 | 새로운 페이지 추가 |
| 색상 팔레트 변경 | 콘텐츠 구조 변경 |
| 타이포그래피 개선 | 백엔드 기능 추가 |
| 버튼/UI 컴포넌트 스타일링 | 다국어 기능 확장 |
| **Author 페이지 UI 리디자인** | |

### 1.3 Progress Status
| Task | Status |
|------|--------|
| ~~Author 페이지 정보 업데이트 (주영민)~~ | ✅ 완료 |
| Featured Post 이미지 비율 수정 | ⏳ 대기 |
| UI/색상 모던화 | ⏳ 대기 |
| Author 페이지 UI 모던화 | 🆕 신규 |

---

## 2. Current State Analysis

### 2.1 Problem 1: Featured Post 썸네일 이미지 늘어남

**현재 상태 (미해결):**
```html
<!-- themes/logbook-hugo/layouts/partials/featured-post.html -->
{{ $imageFallback:= $image.Resize "400x200" }}
{{ $imageXL:= $image.Resize "400x200 webp" }}
{{ $imageLG:= $image.Resize "350x175 webp" }}
{{ $imageMD:= $image.Resize "300x150 webp" }}
{{ $imageSM:= $image.Resize "200x100 webp" }}
```

**문제점:**
- 고정 비율(2:1)로 이미지 강제 리사이즈
- 원본 이미지 비율과 불일치 시 늘어나거나 찌그러짐
- `object-fit` 속성 미적용

**영향 받는 파일:**
- [featured-post.html](themes/logbook-hugo/layouts/partials/featured-post.html)
- [_main.scss](themes/logbook-hugo/assets/scss/templates/_main.scss)

---

### 2.2 Problem 2: 구식 UI/색상 디자인

**현재 색상 설정 (params.toml):**
```toml
color_primary = "#3d85c6"    # 기본 파란색
body_color = "#fff"
text_color = "#696c6d"
text_color_dark = "#1c1d1f"
border_color = "#ddd"
light = "#f0f0f0"
```

**문제점:**
- 단조로운 단일 Primary 색상
- Accent/Secondary 색상 부재
- 그라데이션, 섀도우 효과 미활용
- 2020년대 디자인 트렌드 미반영

---

### 2.3 Problem 3: Author 페이지 구식 디자인 (신규)

**현재 상태:**
```html
<!-- themes/logbook-hugo/layouts/author/single.html -->
<div class="col-lg-3 col-md-4 mb-4 mb-md-0 text-center text-md-left">
  <img loading="lazy" decoding="async" class="rounded-lg img-fluid" ...>
</div>
<div class="col-lg-9 col-md-8 content text-center text-md-left">
  {{ .Content }}
</div>
```

**문제점:**
- 단순한 2컬럼 레이아웃 (이미지 + 텍스트)
- 프로필 카드 스타일 부재
- 소셜 링크가 상단 제목 옆에만 위치
- 프로필 이미지에 스타일링 부재 (기본 rounded만)
- 시각적 계층 구조가 약함
- 모바일 반응형 최적화 부족

**영향 받는 파일:**
- [author/single.html](themes/logbook-hugo/layouts/author/single.html)
- [_common.scss](themes/logbook-hugo/assets/scss/_common.scss)
- 신규: `_author.scss` 또는 커스텀 스타일

---

## 3. Proposed Solution

### 3.1 Task 1: Featured Post 이미지 수정

| Step | Action | File |
|------|--------|------|
| 1-1 | Hugo 이미지 리사이즈를 Fill 모드로 변경 | featured-post.html |
| 1-2 | CSS에 `object-fit: cover` 적용 | _main.scss |
| 1-3 | 이미지 컨테이너 aspect-ratio 설정 | _main.scss |

**수정 방향:**
```html
<!-- Fill 모드: 비율 유지하며 자르기 -->
{{ $imageXL:= $image.Fill "800x400 webp Center" }}
```

```scss
.featured-post-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  aspect-ratio: 16 / 9;
}
```

---

### 3.2 Task 2: UI/색상 모던화

#### 3.2.1 새로운 색상 팔레트 (제안)

| Role | Current | Proposed | Description |
|------|---------|----------|-------------|
| Primary | #3d85c6 | #2563eb | Modern Blue |
| Primary Dark | - | #1d4ed8 | Hover state |
| Accent | - | #8b5cf6 | Purple accent |
| Success | - | #10b981 | Green |
| Background | #fff | #fafafa | Slight warm |
| Surface | #f0f0f0 | #f1f5f9 | Card bg |
| Text | #696c6d | #334155 | Darker text |
| Text Light | #888c8e | #64748b | Secondary |
| Border | #ddd | #e2e8f0 | Softer |

#### 3.2.2 디자인 개선 항목

| Component | Enhancement |
|-----------|-------------|
| **카드** | 부드러운 그림자, border-radius 증가 |
| **버튼** | 그라데이션, hover 애니메이션 |
| **네비게이션** | 글래스모피즘 효과 (선택) |
| **타이포그래피** | 더 큰 제목, 개선된 행간 |
| **Featured Slider** | 더 부드러운 전환 효과 |

#### 3.2.3 수정 파일 목록

| File | Changes |
|------|---------|
| [params.toml](config/_default/params.toml) | 색상 변수 업데이트 |
| [_common.scss](themes/logbook-hugo/assets/scss/_common.scss) | 공통 스타일 |
| [_main.scss](themes/logbook-hugo/assets/scss/templates/_main.scss) | 컴포넌트 스타일 |
| [_buttons.scss](themes/logbook-hugo/assets/scss/_buttons.scss) | 버튼 스타일 |
| [_typography.scss](themes/logbook-hugo/assets/scss/_typography.scss) | 폰트 스타일 |

---

### 3.3 Task 3: Author 페이지 UI 모던화 (신규)

#### 3.3.1 목표 디자인 컨셉

**모던 프로필 카드 스타일:**
```
┌─────────────────────────────────────────────────┐
│                                                 │
│     ┌──────────┐                               │
│     │  PHOTO   │  이름 (Title)                 │
│     │ (원형/   │  직함/소속                     │
│     │  그림자) │  [LinkedIn] [GitHub] [Web]    │
│     └──────────┘                               │
│                                                 │
│  ─────────────────────────────────────────────  │
│                                                 │
│  약력/설명                                      │
│  - 경력 1                                       │
│  - 경력 2                                       │
│  - Specialty: ...                              │
│                                                 │
└─────────────────────────────────────────────────┘
```

#### 3.3.2 디자인 개선 사항

| 요소 | 현재 | 개선안 |
|------|------|--------|
| **프로필 이미지** | 단순 rounded-lg | 원형 + 그림자 + 테두리 효과 |
| **레이아웃** | 2컬럼 분리 | 통합 카드 형태 |
| **소셜 링크** | 상단 제목 옆 (작음) | 프로필 아래 아이콘 버튼 |
| **배경** | 없음 | 부드러운 그라데이션 또는 패턴 |
| **카드 스타일** | 없음 | 그림자 + 둥근 모서리 |
| **타이포그래피** | 기본 | 계층 구조 개선 |
| **애니메이션** | 없음 | Hover 효과 추가 |

#### 3.3.3 수정 파일 및 작업

| Step | Action | File |
|------|--------|------|
| 3-1 | Author 템플릿 리디자인 | layouts/author/single.html (override) |
| 3-2 | Author 전용 스타일 추가 | assets/scss/_author.scss (신규) |
| 3-3 | 프로필 이미지 원형 스타일링 | _author.scss |
| 3-4 | 소셜 아이콘 버튼 스타일 | _author.scss |
| 3-5 | 카드 그림자 및 배경 효과 | _author.scss |
| 3-6 | 반응형 모바일 최적화 | _author.scss |

#### 3.3.4 제안 HTML 구조

```html
<section class="author-profile section-sm">
  <div class="container">
    <div class="author-card">
      <div class="author-header">
        <div class="author-avatar">
          <img src="..." class="avatar-img" alt="author">
        </div>
        <div class="author-info">
          <h1 class="author-name">{{ .Title }}</h1>
          <p class="author-title">현직/소속</p>
          <div class="author-social">
            {{ range .Params.social }}
            <a href="{{ .link }}" class="social-btn"><i class="{{ .icon }}"></i></a>
            {{ end }}
          </div>
        </div>
      </div>
      <div class="author-bio">
        {{ .Content }}
      </div>
    </div>
  </div>
</section>
```

#### 3.3.5 제안 CSS 스타일

```scss
// _author.scss
.author-card {
  background: $white;
  border-radius: 16px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
  padding: 2.5rem;
  max-width: 800px;
  margin: 0 auto;
}

.author-avatar {
  .avatar-img {
    width: 150px;
    height: 150px;
    border-radius: 50%;
    object-fit: cover;
    border: 4px solid $white;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  }
}

.author-social {
  display: flex;
  gap: 0.75rem;
  margin-top: 1rem;

  .social-btn {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: $light;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;

    &:hover {
      background: $color-primary;
      color: $white;
      transform: translateY(-2px);
    }
  }
}
```

---

## 4. Implementation Order

```
Phase 1: Quick Fixes (즉시 적용 가능)
└── [1] Featured Post 이미지 수정

Phase 2: UI Modernization
├── [2] 색상 팔레트 변경 (params.toml)
├── [3] 공통 스타일 업데이트 (_common.scss)
├── [4] 버튼 스타일 개선 (_buttons.scss)
├── [5] 카드/위젯 스타일 개선 (_main.scss)
└── [6] 타이포그래피 개선 (_typography.scss)

Phase 3: Author Page Modernization (신규)
├── [7] Author 템플릿 오버라이드 생성 (layouts/author/single.html)
├── [8] Author 전용 스타일 생성 (_author.scss)
├── [9] 프로필 카드 스타일링
├── [10] 소셜 버튼 스타일링
└── [11] 반응형 최적화

Phase 4: Polish
├── [12] 애니메이션/트랜지션 추가
└── [13] 전체 반응형 디자인 검증
```

---

## 5. Success Criteria

| Criteria | Metric |
|----------|--------|
| 이미지 비율 | Featured Post 이미지가 원본 비율 유지 |
| 색상 일관성 | 새 팔레트가 전체 사이트에 적용 |
| 모던 느낌 | 그림자, 둥근 모서리, 개선된 타이포 |
| **Author 페이지** | 모던 프로필 카드 스타일 적용 |
| **소셜 링크** | 눈에 띄는 아이콘 버튼으로 표시 |
| 반응형 | 모바일/태블릿에서도 정상 표시 |

---

## 6. Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| 테마 업데이트 시 덮어씌워짐 | High | layouts/ 폴더에 오버라이드 파일 생성 |
| 색상 변경으로 가독성 저하 | Medium | 대비율 검증 (WCAG AA) |
| 이미지 자르기로 중요 내용 손실 | Low | Center focus 적용 |
| Author 페이지 레이아웃 깨짐 | Medium | 기존 템플릿 백업 후 작업 |

---

## 7. Estimated Changes

| Category | Files | Lines (Est.) |
|----------|-------|--------------|
| Template (Featured) | 1 | ~20 |
| Template (Author) | 1 | ~60 |
| SCSS (기존) | 4 | ~100 |
| SCSS (Author 신규) | 1 | ~80 |
| Config | 1 | ~15 |
| **Total** | **8** | **~275** |

---

## 8. Next Steps

1. **Plan 승인** → `/pdca design ui-modernization`
2. **Design 완료** → 구현 시작
3. **구현 완료** → `/pdca analyze ui-modernization`

---

## Appendix: Visual Reference

### A. 현재 vs 목표 색상

```
Current:                    Proposed:
┌─────────────────┐        ┌─────────────────┐
│ #3d85c6 Primary │   →    │ #2563eb Primary │
│ #696c6d Text    │   →    │ #334155 Text    │
│ #f0f0f0 Light   │   →    │ #f1f5f9 Surface │
│ #ddd Border     │   →    │ #e2e8f0 Border  │
└─────────────────┘        └─────────────────┘
```

### B. Featured Post 이미지 수정 전후

```
Before (stretched):        After (cropped, proper ratio):
┌──────────────────┐      ┌──────────────────┐
│    ↕ stretched   │  →   │   object-fit:    │
│      image       │      │     cover        │
└──────────────────┘      └──────────────────┘
```

### C. Author 페이지 UI 비교

```
Before (현재):                    After (목표):
┌────────────────────────┐       ┌─────────────────────────────┐
│ [img] │ 이름           │       │  ┌────────────────────────┐ │
│       │ - 경력1        │  →    │  │    ┌─────┐            │ │
│       │ - 경력2        │       │  │    │ IMG │  이름      │ │
│       │ - 경력3        │       │  │    └─────┘  [링크들]  │ │
└───────┴────────────────┘       │  │                        │ │
                                 │  │  약력/설명             │ │
                                 │  └────────────────────────┘ │
                                 └─────────────────────────────┘
                                       (카드 + 그림자)
```

---

**Document Version**: 2.0
**Last Updated**: 2026-02-01
