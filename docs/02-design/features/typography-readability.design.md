# PDCA Design: Typography & Readability Improvement

> **Feature**: typography-readability
> **Plan Reference**: [typography-readability.plan.md](../../01-plan/features/typography-readability.plan.md)
> **Created**: 2026-02-01
> **Phase**: Design
> **Status**: Ready for Implementation

---

## 1. Design Overview

한국어 콘텐츠 가독성을 극대화하기 위한 타이포그래피 개선 설계 문서입니다.
Pretendard 폰트 적용, 본문 크기 증가, 행간 최적화를 통해 읽기 편안한 경험을 제공합니다.

### 1.1 Key Changes Summary

| Category | Before | After |
|----------|--------|-------|
| **Font** | Lato (라틴 전용) | Pretendard (한/영 최적화) |
| **Body Size** | 14px (0.875rem) | 16px (1rem) |
| **Content Size** | 14px | 17px (1.0625rem) |
| **Line Height** | 1.7 | 1.8 (본문), 1.9 (콘텐츠) |
| **Paragraph Gap** | 1rem | 1.5rem |

---

## 2. File Modifications

### 2.1 Task 1: Pretendard Font CDN 추가

**File**: `themes/logbook-hugo/layouts/partials/essentials/head.html`

**Location**: Line 17 근처 (theme-color meta 태그 이후)

**Add After Line 18**:
```html
<!-- Pretendard Font (Korean Typography) -->
<link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css" />
```

**Full Context**:
```html
<meta name="msapplication-TileColor" content="{{site.Params.variables.color_primary | default `#ddd`}}">
<meta name="theme-color" content="{{site.Params.variables.body_color | default `#ffffff` }}">

<!-- Pretendard Font (Korean Typography) -->
<link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css" />

<!-- multilingual SEO optimizations -->
```

---

### 2.2 Task 2: Font Family 변수 설정

**File**: `config/_default/params.toml`

**Location**: `[variables]` 섹션 내 (line 33-43)

**Add After `light = "#f1f5f9"` (line 43)**:
```toml
# Typography Settings
font_primary = "Pretendard"
font_primary_type = "sans-serif"
font_secondary = "Pretendard"
font_secondary_type = "sans-serif"
```

**Full Context**:
```toml
[variables]
# Modern Color Palette (Updated 2026-02-01)
color_primary = "#2563eb"      # Modern Blue (Tailwind blue-600)
body_color = "#ffffff"         # Pure white
text_color = "#334155"         # Slate-700 (더 진한 본문)
text_color_dark = "#0f172a"    # Slate-900 (제목용)
text_color_light = "#64748b"   # Slate-500 (보조 텍스트)
border_color = "#e2e8f0"       # Slate-200 (부드러운 테두리)
black = "#0f172a"              # Slate-900
white = "#ffffff"
light = "#f1f5f9"              # Slate-100 (Surface)

# Typography Settings
font_primary = "Pretendard"
font_primary_type = "sans-serif"
font_secondary = "Pretendard"
font_secondary_type = "sans-serif"
```

---

### 2.3 Task 3: 기본 타이포그래피 수정

**File**: `themes/logbook-hugo/assets/scss/_typography.scss`

**Replace Entire File With**:
```scss
/*  typography */

body {
  line-height: 1.75;
  font-family: $font-primary;
  -webkit-font-smoothing: antialiased;
  color: $text-color;
  font-size: 1rem;                    // 16px (기존 14px)

  @media (max-width: 768px) {
    font-size: 0.9375rem;             // 15px (모바일)
  }
}

p, .paragraph {
  font-weight: 400;
  color: $text-color;
  font-size: 1rem;                    // 16px
  line-height: 1.8;                   // 기존 1.7
  font-family: $font-primary;
  margin-bottom: 1.25rem;
}

h1,h2,h3,h4,h5,h6 {
  color: $text-color-dark;
  font-family: $font-secondary;
  font-weight: 600;
  line-height: 1.3;                   // 기존 1.2
}


// List in descending order to prevent extra sort function
$type-levels: 6,5,4,3,2,1;

@each $level in $type-levels {
  $font-size: $font-size * $font-scale;

  // Output heading styles
  h#{$level},
  .h#{$level} {
    font-size: calc(#{$font-size} * .80);
    line-height: calc(2px + 2ex + 2px);
    margin-bottom: 0.75em;            // 기존 0.65em

    &:not(h2, .h2, h3, .h3, h4, .h4, h5, .h5, h6, .h6) {
      font-size: calc(#{$font-size} * 1);
    }


  }
}
```

---

### 2.4 Task 4: 콘텐츠 영역 타이포그래피 개선

**File**: `themes/logbook-hugo/assets/scss/_common.scss`

**Modify `.content` section (lines 191-489)**

**Replace content section starting at line 191**:

Find this block (line 191-196):
```scss
// content style
.content {

  * {
    word-break: break-word;
    overflow-wrap: break-word;
  }
```

Replace with:
```scss
// content style
.content {

  * {
    word-break: break-word;
    overflow-wrap: break-word;
  }

  // Typography Enhancement for Korean Readability
  p {
    font-size: 1.0625rem;             // 17px (포스트 본문)
    line-height: 1.9;                 // 한국어 최적화
    margin-bottom: 1.5rem;            // 단락 간격 확대
    color: $text-color;
  }

  li {
    font-size: 1.0625rem;
    line-height: 1.85;
    margin-bottom: 0.75rem;           // 기존 0.62rem
  }
```

---

**Add heading styles after line 263 (after `strong { font-weight: 600; }`)**:

Find:
```scss
  strong {
    font-weight: 600;
  }
```

Add after:
```scss
  strong {
    font-weight: 600;
  }

  // Heading Hierarchy Enhancement
  h2 {
    font-size: 1.5rem;                // 24px
    font-weight: 600;
    margin-top: 2.5rem;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid $border-color;
  }

  h3 {
    font-size: 1.25rem;               // 20px
    font-weight: 600;
    margin-top: 2rem;
    margin-bottom: 0.875rem;
  }

  h4 {
    font-size: 1.125rem;              // 18px
    font-weight: 600;
    margin-top: 1.5rem;
    margin-bottom: 0.75rem;
  }
```

---

**Update blockquote styles (replace lines 441-475)**:

Find:
```scss
  blockquote{
    font-size: 1em;
    width:95%;
    margin:50px auto;
```

Replace entire blockquote section with:
```scss
  blockquote {
    font-size: 1.0625rem;             // 17px
    line-height: 1.85;
    width: 95%;
    margin: 2rem auto;
    font-family: $font-primary;
    font-style: italic;
    color: $text-color;
    padding: 1.5rem 2rem 1.5rem 3rem;
    border-left: 4px solid $color-primary;
    position: relative;
    background: $light;
    border-radius: 0 8px 8px 0;

    p {
      margin-bottom: 0;
      font-size: inherit;
      line-height: inherit;
    }
  }

  blockquote::before {
    font-family: Georgia, serif;
    content: "\201C";
    color: $color-primary;
    font-size: 3rem;
    position: absolute;
    left: 0.5rem;
    top: 0;
    line-height: 1;
  }

  blockquote::after {
    content: '';
  }

  blockquote span {
    display: block;
    color: $text-color-dark;
    font-style: normal;
    font-weight: 600;
    margin-top: 1.5rem;
  }
```

---

**Update code block styles (replace lines 478-488)**:

Find:
```scss
  pre {
    display: block;
    padding: 9.5px;
    margin: 10px 0px 0.62rem;
    white-space: pre-wrap;
  }

  code {
    margin-bottom: 0 !important;
    font-size: 100%;
  }
```

Replace with:
```scss
  pre {
    display: block;
    padding: 1.25rem;
    margin: 1rem 0 1.5rem;
    white-space: pre-wrap;
    border-radius: 8px;
    overflow-x: auto;
    font-size: 0.9rem;
    line-height: 1.6;
  }

  code {
    margin-bottom: 0 !important;
    font-size: 0.9rem;
    font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
    padding: 0.15rem 0.35rem;
    border-radius: 4px;
    background: rgba($text-color-light, 0.1);
  }

  pre code {
    padding: 0;
    background: transparent;
    border-radius: 0;
  }
```

---

## 3. Implementation Checklist

### Phase 1: Font Setup
- [ ] Add Pretendard CDN link to head.html
- [ ] Add font variables to params.toml
- [ ] Verify font loads correctly

### Phase 2: Typography Base
- [ ] Update _typography.scss with new sizes and line heights
- [ ] Test body text rendering

### Phase 3: Content Styles
- [ ] Update _common.scss content section
- [ ] Add heading hierarchy styles
- [ ] Update blockquote styles
- [ ] Update code block styles

### Phase 4: Verification
- [ ] Test on multiple posts
- [ ] Verify mobile responsiveness
- [ ] Check cross-browser rendering

---

## 4. Visual Comparison Reference

### 4.1 Font Size Comparison

| Element | Before | After |
|---------|--------|-------|
| `body` | 0.875rem (14px) | 1rem (16px) |
| `p, .paragraph` | 0.875rem (14px) | 1rem (16px) |
| `.content p` | 0.875rem (14px) | 1.0625rem (17px) |
| Mobile body | 0.875rem | 0.9375rem (15px) |

### 4.2 Line Height Comparison

| Element | Before | After |
|---------|--------|-------|
| `body` | 1.7 | 1.75 |
| `p` | 1.7 | 1.8 |
| `.content p` | 1.7 | 1.9 |
| `h1-h6` | 1.2 | 1.3 |

### 4.3 Heading Sizes (Content)

| Level | Size | Description |
|-------|------|-------------|
| h2 | 1.5rem (24px) | Section heading with border |
| h3 | 1.25rem (20px) | Subsection heading |
| h4 | 1.125rem (18px) | Minor heading |

---

## 5. Dependencies

| File | Depends On |
|------|------------|
| _typography.scss | params.toml font variables |
| _common.scss | _typography.scss, params.toml colors |
| head.html | None (CDN external) |

---

## 6. Rollback Plan

If issues occur, revert these files:
1. `themes/logbook-hugo/layouts/partials/essentials/head.html` - Remove Pretendard CDN
2. `config/_default/params.toml` - Remove font variables
3. `themes/logbook-hugo/assets/scss/_typography.scss` - Restore original
4. `themes/logbook-hugo/assets/scss/_common.scss` - Restore content section

---

## 7. Success Metrics

| Metric | Target |
|--------|--------|
| Body font size | 16px minimum |
| Content line height | 1.9 |
| Korean font | Pretendard applied |
| Heading hierarchy | h2/h3/h4 visually distinct |
| Paragraph spacing | 1.5rem |
| Mobile font size | 15px minimum |

---

**Document Version**: 1.0
**Last Updated**: 2026-02-01
