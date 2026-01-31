# PDCA Plan: Typography & Readability Improvement

> **Feature**: typography-readability
> **Created**: 2026-02-01
> **Phase**: Plan
> **Status**: Draft

---

## 1. Overview

AIEconLab 사이트 전반의 타이포그래피와 가독성을 개선하여 한국어 콘텐츠를 더 읽기 편하게 만드는 프로젝트입니다.

### 1.1 Goals

- 본문 텍스트 크기 및 행간 최적화
- 한국어 최적화 폰트 적용
- 포스트 콘텐츠 가독성 대폭 개선
- 제목/본문 시각적 계층 구조 강화
- 모바일 가독성 개선

### 1.2 Scope

| In Scope | Out of Scope |
|----------|--------------|
| 폰트 패밀리 변경 | 레이아웃 구조 변경 |
| 폰트 크기 조정 | 새 페이지 추가 |
| 행간(line-height) 최적화 | 콘텐츠 수정 |
| 자간(letter-spacing) 조정 | 이미지 처리 |
| 제목 스타일 개선 | 네비게이션 변경 |
| 본문/포스트 콘텐츠 스타일 | |

---

## 2. Current State Analysis

### 2.1 현재 타이포그래피 설정

**_typography.scss 분석:**
```scss
body {
  line-height: 1.7;
  font-size: 0.875rem;     // 14px - 너무 작음
}

p, .paragraph {
  font-size: 0.875rem;     // 14px
  line-height: 1.7;
}

h1,h2,h3,h4,h5,h6 {
  font-weight: 600;
  line-height: 1.2;
}
```

**params.toml 폰트 설정:**
- font_primary: 기본값 "Lato" (설정 안 됨)
- font_secondary: 기본값 "Lato" (설정 안 됨)
- font_size: 기본값 "16px"
- font_scale: 기본값 "1.2"

### 2.2 문제점 분석

| 문제 | 현재 값 | 영향 |
|------|---------|------|
| **본문 크기 작음** | 14px (0.875rem) | 한국어 읽기 불편 |
| **한국어 폰트 없음** | Lato (라틴 전용) | 한글 폰트 일관성 부재 |
| **콘텐츠 행간 부족** | 1.7 | 긴 글 읽기 피로 |
| **제목 간격 좁음** | margin-bottom: 0.65em | 섹션 구분 약함 |
| **단락 간격 부족** | 기본값 | 시각적 휴식 부재 |
| **모바일 최적화 부족** | 동일 크기 | 작은 화면에서 불편 |

### 2.3 영향 받는 파일

| 파일 | 역할 |
|------|------|
| `config/_default/params.toml` | 폰트 변수 정의 |
| `themes/.../scss/_typography.scss` | 기본 타이포그래피 |
| `themes/.../scss/_common.scss` | 콘텐츠 영역 스타일 |
| `themes/.../scss/style.scss` | 폰트 변수 로드 |
| `themes/.../layouts/partials/essentials/head.html` | 폰트 로드 |

---

## 3. Proposed Solution

### 3.1 Task 1: 한국어 최적화 폰트 적용

**추천 폰트 조합:**

| 용도 | 폰트 | 특징 |
|------|------|------|
| **본문** | Pretendard | 한/영 조화, 가독성 우수 |
| **제목** | Pretendard | 두께 다양 (100-900) |
| **대안** | Noto Sans KR | Google Fonts 지원 |

**구현 방법 (Pretendard CDN):**
```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
```

**params.toml 설정:**
```toml
[variables]
font_primary = "Pretendard"
font_primary_type = "sans-serif"
font_secondary = "Pretendard"
font_secondary_type = "sans-serif"
```

---

### 3.2 Task 2: 본문 폰트 크기 최적화

**제안 크기:**

| 요소 | 현재 | 제안 | 비고 |
|------|------|------|------|
| body | 14px | 16px | 기본 크기 증가 |
| p, .paragraph | 14px | 16px (1rem) | 본문 가독성 |
| .content p | 14px | 17px (1.0625rem) | 포스트 전용 |
| 모바일 body | 14px | 15px | 작은 화면 대응 |

**SCSS 수정:**
```scss
body {
  font-size: 1rem;           // 16px

  @media (max-width: 768px) {
    font-size: 0.9375rem;    // 15px
  }
}

.content {
  p, li {
    font-size: 1.0625rem;    // 17px (포스트 본문)
  }
}
```

---

### 3.3 Task 3: 행간 및 단락 간격 최적화

**제안 행간:**

| 요소 | 현재 | 제안 | 비고 |
|------|------|------|------|
| body | 1.7 | 1.75 | 기본 행간 |
| p, .paragraph | 1.7 | 1.8 | 본문 행간 |
| .content p | 1.7 | 1.9 | 포스트 (한국어 최적) |
| h1-h6 | 1.2 | 1.3 | 제목 행간 |

**단락 간격:**
```scss
.content {
  p {
    margin-bottom: 1.5rem;   // 현재 1rem → 1.5rem
  }

  h2, h3, h4 {
    margin-top: 2.5rem;      // 섹션 구분 강화
    margin-bottom: 1rem;
  }
}
```

---

### 3.4 Task 4: 제목 계층 구조 개선

**제안 제목 스타일:**

```scss
// 포스트 제목 스타일
.content {
  h1 {
    font-size: 2rem;         // 32px
    font-weight: 700;
    margin-bottom: 1.5rem;
  }

  h2 {
    font-size: 1.5rem;       // 24px
    font-weight: 600;
    border-bottom: 1px solid $border-color;
    padding-bottom: 0.5rem;
  }

  h3 {
    font-size: 1.25rem;      // 20px
    font-weight: 600;
  }

  h4 {
    font-size: 1.125rem;     // 18px
    font-weight: 600;
  }
}
```

---

### 3.5 Task 5: 추가 가독성 개선

**인용문 (blockquote) 개선:**
```scss
blockquote {
  font-size: 1.1rem;
  line-height: 1.8;
  padding: 1.5rem 2rem;
  border-left: 4px solid $color-primary;
  background: $light;
  margin: 2rem 0;

  p {
    margin-bottom: 0;
  }
}
```

**코드 블록 개선:**
```scss
pre, code {
  font-family: 'JetBrains Mono', 'Fira Code', monospace;
  font-size: 0.9rem;
}

pre {
  padding: 1.25rem;
  border-radius: 8px;
  overflow-x: auto;
}
```

**리스트 간격 개선:**
```scss
.content ul, .content ol {
  margin-bottom: 1.5rem;

  li {
    margin-bottom: 0.75rem;  // 현재 0.62rem
    line-height: 1.8;
  }
}
```

---

## 4. Implementation Order

```
Phase 1: 폰트 설정
├── [1] Pretendard 폰트 CDN 추가 (head.html)
├── [2] params.toml 폰트 변수 설정
└── [3] 폰트 적용 확인

Phase 2: 크기 및 행간
├── [4] _typography.scss 본문 크기/행간 수정
├── [5] _common.scss 콘텐츠 스타일 수정
└── [6] 반응형 크기 설정

Phase 3: 계층 구조
├── [7] 제목 스타일 개선
├── [8] 단락/섹션 간격 조정
└── [9] 인용문/코드 블록 개선

Phase 4: 검증
├── [10] 다양한 포스트에서 테스트
├── [11] 모바일 가독성 확인
└── [12] 크로스 브라우저 테스트
```

---

## 5. Success Criteria

| Criteria | Metric |
|----------|--------|
| 본문 폰트 크기 | 16px 이상 |
| 포스트 본문 행간 | 1.8 이상 |
| 한국어 폰트 | Pretendard 또는 Noto Sans KR 적용 |
| 제목 계층 | h2, h3, h4 시각적 구분 명확 |
| 모바일 가독성 | 15px 이상, 행간 1.7 이상 |
| 단락 간격 | 1.5rem 이상 |

---

## 6. Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| 폰트 로딩 속도 | Medium | 폰트 서브셋, preload 적용 |
| 레이아웃 깨짐 | Medium | 충분한 테스트 후 배포 |
| 기존 스타일 충돌 | Low | SCSS 계층 구조 활용 |
| CDN 장애 | Low | 로컬 폰트 폴백 설정 |

---

## 7. Visual Reference

### A. 폰트 크기 비교

```
Current (14px):         Proposed (16-17px):
┌─────────────────┐    ┌─────────────────┐
│ 작은 텍스트로   │    │ 편안한 크기의   │
│ 읽기 불편함     │ →  │ 가독성 높은     │
│                 │    │ 텍스트          │
└─────────────────┘    └─────────────────┘
```

### B. 행간 비교

```
Current (1.7):          Proposed (1.9):
┌─────────────────┐    ┌─────────────────┐
│ 줄 간격이 좁아  │    │ 충분한 간격으로 │
│ 읽기 피로함     │ →  │                 │
│ 특히 한국어에서 │    │ 한국어 가독성   │
│ 불편            │    │ 크게 개선       │
└─────────────────┘    └─────────────────┘
```

### C. 제목 계층 구조

```
Before:                 After:
─────────────────      ═══════════════════════
H2 제목                 H2 제목 (border-bottom)
─────────────────      ═══════════════════════

H3 제목                 H3 제목

H4 제목                 H4 제목
```

---

## 8. Estimated Changes

| Category | Files | Lines (Est.) |
|----------|-------|--------------|
| Config | 1 | ~10 |
| SCSS | 3 | ~150 |
| Template | 1 | ~5 |
| **Total** | **5** | **~165** |

---

## 9. Next Steps

1. **Plan 승인** → `/pdca design typography-readability`
2. **Design 완료** → 구현 시작
3. **구현 완료** → `/pdca analyze typography-readability`

---

**Document Version**: 1.0
**Last Updated**: 2026-02-01
