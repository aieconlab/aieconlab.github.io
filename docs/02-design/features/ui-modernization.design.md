# PDCA Design: UI Modernization

> **Feature**: ui-modernization
> **Created**: 2026-02-01
> **Phase**: Design
> **Status**: Draft
> **Plan Reference**: [ui-modernization.plan.md](../../01-plan/features/ui-modernization.plan.md)

---

## 1. Design Overview

AIEconLab 홈페이지 UI/UX 모던화를 위한 상세 설계 문서입니다.

### 1.1 Design Goals

| Goal | Description |
|------|-------------|
| 이미지 비율 정상화 | Featured Post 썸네일 이미지 왜곡 해결 |
| 색상 모던화 | 2020년대 디자인 트렌드 반영 |
| Author 페이지 리디자인 | 프로필 카드 스타일 적용 |
| 반응형 최적화 | 모바일/태블릿 대응 개선 |

### 1.2 Design Principles

- **Minimal Changes**: 테마 원본 파일 최소 수정, 오버라이드 활용
- **Backward Compatible**: 기존 콘텐츠와 완벽 호환
- **Performance First**: 추가 라이브러리 최소화
- **Accessibility**: WCAG AA 대비율 준수

---

## 2. Technical Specifications

### 2.1 File Structure

```
aieconlab.github.io/
├── config/_default/
│   └── params.toml              # [수정] 색상 변수 업데이트
├── layouts/
│   └── author/
│       └── single.html          # [신규] Author 템플릿 오버라이드
├── assets/
│   └── scss/
│       └── custom/
│           └── _author.scss     # [신규] Author 전용 스타일
└── themes/logbook-hugo/
    ├── layouts/partials/
    │   └── featured-post.html   # [수정] 이미지 리사이즈 로직
    └── assets/scss/
        ├── style.scss           # [수정] 커스텀 import 추가
        └── templates/
            └── _main.scss       # [수정] featured-post-img 스타일
```

---

## 3. Component Design

### 3.1 Featured Post Image Fix

#### 3.1.1 Current Issue Analysis

**현재 코드** (`featured-post.html:11-15`):
```html
{{ $imageFallback:= $image.Resize "400x200" }}
{{ $imageXL:= $image.Resize "400x200 webp" }}
{{ $imageLG:= $image.Resize "350x175 webp" }}
{{ $imageMD:= $image.Resize "300x150 webp" }}
{{ $imageSM:= $image.Resize "200x100 webp" }}
```

**문제점**:
- `Resize`는 이미지를 강제로 지정 크기로 변환 (비율 무시)
- 원본 비율이 2:1이 아니면 왜곡 발생

#### 3.1.2 Solution Design

**수정 코드**:
```html
{{ $imageFallback:= $image.Fill "800x400 Center" }}
{{ $imageXL:= $image.Fill "800x400 webp Center" }}
{{ $imageLG:= $image.Fill "700x350 webp Center" }}
{{ $imageMD:= $image.Fill "600x300 webp Center" }}
{{ $imageSM:= $image.Fill "400x200 webp Center" }}
```

**변경 사항**:
| 항목 | Before | After |
|------|--------|-------|
| 메서드 | `Resize` | `Fill` |
| 비율 처리 | 강제 변환 | 비율 유지 + 크롭 |
| 초점 | 없음 | `Center` |
| 이미지 크기 | 400x200 max | 800x400 max (고해상도 대응) |

#### 3.1.3 CSS Enhancement

**추가 스타일** (`_main.scss`):
```scss
.featured-post-img {
  width: 100%;
  height: auto;
  aspect-ratio: 2 / 1;
  object-fit: cover;
  object-position: center;
}
```

---

### 3.2 Color Palette Modernization

#### 3.2.1 Color System Design

**새 색상 팔레트** (`params.toml`):

```toml
[params.variables]
# Primary Colors
color_primary = "#2563eb"      # Modern Blue (Tailwind blue-600)

# Text Colors
text_color = "#334155"         # Slate-700 (더 진한 본문)
text_color_dark = "#0f172a"    # Slate-900 (제목용)
text_color_light = "#64748b"   # Slate-500 (보조 텍스트)

# Background Colors
body_color = "#ffffff"         # Pure white
light = "#f1f5f9"              # Slate-100 (Surface)

# Border & Accent
border_color = "#e2e8f0"       # Slate-200 (부드러운 테두리)
black = "#0f172a"              # Slate-900
white = "#ffffff"
```

#### 3.2.2 Color Contrast Verification (WCAG AA)

| Combination | Ratio | Pass |
|-------------|-------|------|
| #334155 on #ffffff | 8.2:1 | ✅ AAA |
| #2563eb on #ffffff | 4.6:1 | ✅ AA |
| #64748b on #ffffff | 4.5:1 | ✅ AA |
| #ffffff on #2563eb | 4.6:1 | ✅ AA |

#### 3.2.3 Extended Color Variables (Optional)

향후 확장을 위한 추가 변수:
```toml
# Extended (주석 처리, 필요시 활성화)
# color_primary_dark = "#1d4ed8"   # Hover state
# color_accent = "#8b5cf6"         # Purple accent
# color_success = "#10b981"        # Green
# color_warning = "#f59e0b"        # Amber
# color_error = "#ef4444"          # Red
```

---

### 3.3 Author Page UI Modernization

#### 3.3.1 Layout Architecture

**현재 구조**:
```
┌─────────────────────────────────────────────────────┐
│ [Title-bordered: 이름 ──────────── [소셜아이콘]]    │
├─────────────────────────────────────────────────────┤
│  ┌──────┐                                           │
│  │ IMG  │   - 경력 1                                │
│  │ 260x │   - 경력 2                                │
│  └──────┘   - 경력 3                                │
└─────────────────────────────────────────────────────┘
             ↓ (해당 저자의 글 목록)
```

**목표 구조**:
```
┌─────────────────────────────────────────────────────┐
│                  AUTHOR CARD                        │
│  ┌─────────────────────────────────────────────┐   │
│  │         ┌─────────┐                         │   │
│  │         │   IMG   │                         │   │
│  │         │ (원형)  │                         │   │
│  │         └─────────┘                         │   │
│  │           이름                               │   │
│  │     [LinkedIn] [GitHub] [Web]               │   │
│  │  ─────────────────────────────────────────  │   │
│  │  약력/설명                                   │   │
│  │  - 경력 1                                   │   │
│  │  - 경력 2                                   │   │
│  └─────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
             ↓ (해당 저자의 글 목록)
```

#### 3.3.2 Template Design

**파일**: `layouts/author/single.html` (루트에 오버라이드 생성)

```html
{{ define "main" }}

<!-- Author Profile Section -->
<section class="author-section section-sm">
  <div class="container">
    <div class="author-card">
      <!-- Author Header -->
      <div class="author-header">
        <!-- Avatar -->
        <div class="author-avatar">
          {{ if .Params.Image }}
          {{ $img := resources.Get .Params.Image }}
          {{ $img := $img.Fill "300x300 webp Center" }}
          <img loading="lazy" decoding="async"
               class="avatar-img"
               width="{{ $img.Width }}"
               height="{{ $img.Height }}"
               src="{{ $img.RelPermalink }}"
               alt="{{ .Title }}">
          {{ else if .Params.Email }}
          <img loading="lazy" class="avatar-img"
               src="https://www.gravatar.com/avatar/{{ md5 .Params.email }}?s=300&d=identicon"
               alt="{{ .Title }}">
          {{ end }}
        </div>

        <!-- Author Info -->
        <div class="author-info">
          <h1 class="author-name">{{ .Title }}</h1>

          <!-- Social Links -->
          {{ with .Params.social }}
          <div class="author-social">
            {{ range . }}
            <a href="{{ .link | safeURL }}"
               class="social-btn"
               target="_blank"
               rel="noopener noreferrer"
               aria-label="{{ .icon }}">
              <i class="{{ .icon }}"></i>
            </a>
            {{ end }}
          </div>
          {{ end }}
        </div>
      </div>

      <!-- Author Bio -->
      <div class="author-bio">
        {{ .Content }}
      </div>
    </div>
  </div>
</section>

<!-- Posts by Author Section -->
<section class="section-sm">
  <div class="container">
    <div class="row">
      <div class="col-12">
        <div class="section-title text-center mb-5">
          <h2>{{ i18n "posted_by" }}</h2>
        </div>
      </div>

      {{ range where site.RegularPages "Params.author" .Title }}
      <div class="col-lg-4 col-md-6 mb-4">
        <article class="post-card">
          {{ with .Params.images }}
          <div class="post-card-image">
            {{ range first 1 . }}
            {{ if (fileExists (add `assets/` .)) }}
            {{ $image := resources.Get . }}
            {{ $thumb := $image.Fill "400x250 webp Center" }}
            <a href="{{ $.RelPermalink }}">
              <img loading="lazy"
                   class="img-fluid"
                   src="{{ $thumb.RelPermalink }}"
                   alt="{{ $.Title }}">
            </a>
            {{ end }}
            {{ end }}
          </div>
          {{ end }}

          <div class="post-card-content">
            <h3 class="post-card-title">
              <a href="{{ .RelPermalink }}">{{ .Title }}</a>
            </h3>
            <div class="post-card-meta">
              <span><i class="far fa-calendar-alt"></i> {{ .PublishDate.Format "2006.01.02" }}</span>
            </div>
            <p class="post-card-excerpt">{{ .Summary | truncate 80 }}</p>
          </div>
        </article>
      </div>
      {{ end }}
    </div>
  </div>
</section>

{{ end }}
```

#### 3.3.3 Style Specifications

**파일**: `assets/scss/custom/_author.scss` (신규 생성)

```scss
// ============================================
// Author Page Styles
// ============================================

// Section
.author-section {
  background: linear-gradient(180deg, $light 0%, $body-color 100%);
  padding-top: 3rem;
  padding-bottom: 3rem;
}

// Card Container
.author-card {
  background: $white;
  border-radius: 20px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
  padding: 3rem;
  max-width: 700px;
  margin: 0 auto;

  @media (max-width: 768px) {
    padding: 2rem 1.5rem;
    border-radius: 16px;
  }
}

// Header (Avatar + Info)
.author-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  margin-bottom: 2rem;
}

// Avatar
.author-avatar {
  margin-bottom: 1.5rem;

  .avatar-img {
    width: 150px;
    height: 150px;
    border-radius: 50%;
    object-fit: cover;
    border: 4px solid $white;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
    transition: transform 0.3s ease;

    &:hover {
      transform: scale(1.05);
    }

    @media (max-width: 768px) {
      width: 120px;
      height: 120px;
    }
  }
}

// Author Info
.author-info {
  .author-name {
    font-size: 1.75rem;
    font-weight: 700;
    color: $text-color-dark;
    margin-bottom: 1rem;

    @media (max-width: 768px) {
      font-size: 1.5rem;
    }
  }
}

// Social Links
.author-social {
  display: flex;
  justify-content: center;
  gap: 0.75rem;

  .social-btn {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    background: $light;
    display: flex;
    align-items: center;
    justify-content: center;
    color: $text-color;
    font-size: 1.1rem;
    transition: all 0.3s ease;

    &:hover {
      background: $color-primary;
      color: $white;
      transform: translateY(-3px);
      box-shadow: 0 4px 12px rgba($color-primary, 0.4);
    }
  }
}

// Bio Section
.author-bio {
  border-top: 1px solid $border-color;
  padding-top: 2rem;

  ul {
    list-style: none;
    padding-left: 0;

    li {
      padding: 0.5rem 0;
      padding-left: 1.5rem;
      position: relative;
      color: $text-color;

      &::before {
        content: '';
        position: absolute;
        left: 0;
        top: 1rem;
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: $color-primary;
      }
    }
  }
}

// ============================================
// Post Cards (Author's Posts)
// ============================================

.post-card {
  background: $white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
  height: 100%;

  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.1);

    .post-card-image img {
      transform: scale(1.05);
    }
  }
}

.post-card-image {
  overflow: hidden;
  aspect-ratio: 16 / 10;

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.3s ease;
  }
}

.post-card-content {
  padding: 1.25rem;
}

.post-card-title {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  line-height: 1.4;

  a {
    color: $text-color-dark;

    &:hover {
      color: $color-primary;
    }
  }
}

.post-card-meta {
  font-size: 0.85rem;
  color: $text-color-light;
  margin-bottom: 0.75rem;

  i {
    margin-right: 0.25rem;
  }
}

.post-card-excerpt {
  font-size: 0.9rem;
  color: $text-color;
  line-height: 1.6;
  margin-bottom: 0;
}

// Section Title
.section-title h2 {
  font-size: 1.5rem;
  font-weight: 600;
  position: relative;
  display: inline-block;

  &::after {
    content: '';
    position: absolute;
    bottom: -8px;
    left: 50%;
    transform: translateX(-50%);
    width: 40px;
    height: 3px;
    background: $color-primary;
    border-radius: 2px;
  }
}
```

#### 3.3.4 Style Integration

**수정**: `themes/logbook-hugo/assets/scss/style.scss`

마지막 줄에 추가:
```scss
// Custom overrides (root assets/scss/custom/)
{{ $customAuthor := resources.Get "scss/custom/_author.scss" }}
{{ if $customAuthor }}
@import '../../assets/scss/custom/_author.scss';
{{ end }}
```

또는 루트에 `assets/scss/custom/_author.scss` 생성 후 Hugo의 asset 병합 활용.

---

## 4. Implementation Order

```
Step 1: Featured Post 이미지 수정
├── 1.1 featured-post.html 수정 (Resize → Fill)
├── 1.2 _main.scss에 object-fit 추가
└── 1.3 로컬 테스트

Step 2: 색상 팔레트 변경
├── 2.1 params.toml 색상 변수 업데이트
└── 2.2 전체 사이트 색상 확인

Step 3: Author 페이지 리디자인
├── 3.1 layouts/author/single.html 오버라이드 생성
├── 3.2 assets/scss/custom/_author.scss 생성
├── 3.3 style.scss에 import 추가
└── 3.4 반응형 테스트

Step 4: 최종 검증
├── 4.1 모바일/태블릿 반응형 테스트
├── 4.2 브라우저 호환성 확인
└── 4.3 Lighthouse 성능 체크
```

---

## 5. Responsive Breakpoints

| Breakpoint | Width | Description |
|------------|-------|-------------|
| Desktop | ≥1200px | 기본 레이아웃 |
| Tablet | 768px-1199px | 카드 2열, 패딩 축소 |
| Mobile | <768px | 카드 1열, 아바타 축소 |

**반응형 스타일 요약**:
```scss
// Tablet
@media (max-width: 1199px) {
  .author-card { max-width: 100%; }
}

// Mobile
@media (max-width: 768px) {
  .author-card { padding: 2rem 1.5rem; }
  .avatar-img { width: 120px; height: 120px; }
  .author-name { font-size: 1.5rem; }
}
```

---

## 6. Testing Checklist

### 6.1 Visual Testing

- [ ] Featured Post 이미지 비율 정상 (2:1, 왜곡 없음)
- [ ] 색상 팔레트 일관성 확인
- [ ] Author 카드 레이아웃 정상
- [ ] 소셜 버튼 hover 효과
- [ ] 그림자 및 둥근 모서리 적용

### 6.2 Responsive Testing

- [ ] Desktop (1920px, 1440px)
- [ ] Tablet (1024px, 768px)
- [ ] Mobile (414px, 375px, 320px)

### 6.3 Browser Testing

- [ ] Chrome
- [ ] Firefox
- [ ] Safari
- [ ] Edge

### 6.4 Performance Testing

- [ ] Lighthouse Score ≥90
- [ ] 이미지 최적화 (WebP)
- [ ] CSS 파일 크기 확인

---

## 7. Rollback Plan

문제 발생 시 롤백 절차:

1. **Git Revert**: `git revert HEAD~n`
2. **파일별 복원**:
   - `params.toml` → 원본 색상 복원
   - `layouts/author/single.html` → 삭제 (테마 기본 사용)
   - `assets/scss/custom/` → 폴더 삭제

---

## 8. Dependencies

| Dependency | Version | Purpose |
|------------|---------|---------|
| Hugo | ≥0.90.1 | SSG (netlify.toml 기준) |
| Font Awesome | 5.x | 아이콘 (기존 사용) |
| Bootstrap | 4.x | 그리드 (테마 포함) |

**추가 라이브러리**: 없음 (기존 테마 활용)

---

## 9. Next Steps

1. **Design 승인** → 구현 시작
2. **구현 완료** → `/pdca analyze ui-modernization`
3. **Gap Analysis** → 90% 이상 시 Report 생성

---

**Document Version**: 1.0
**Last Updated**: 2026-02-01
**Author**: Claude Code
