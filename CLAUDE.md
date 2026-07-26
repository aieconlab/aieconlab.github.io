# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AIEconLab (인공지능경제연구소) - A Hugo static site for an AI Economics research lab. The site publishes Korean-language articles about AI trends, economics, and policy.

- **Site URL**: https://www.aieconlab.com/
- **Theme**: logbook-hugo
- **Deployment**: GitHub Pages via GitHub Actions (`.github/workflows/hugo.yml`, Hugo 0.124.0 extended). Every push to `main` builds and deploys automatically — do NOT commit the `public/` build output.
- **Scheduled posts**: the build has no `--buildFuture` and the config sets no `buildFuture`, so a post whose frontmatter `date` is later than the build clock (UTC on the runner) is dropped silently — no error, and it is missing from the page, home, list, RSS and sitemap alike. The only triggers are `push` to `main` and `workflow_dispatch`, so nothing rebuilds it later on its own. Merge a scheduled post to `main` **after** its publish time, or if it was merged early, run the "Deploy Hugo site to Pages" workflow manually once that time passes. Do not add `--buildFuture` globally — it would publish every future-dated post early (this is separate from `draft: true`, which `--buildDrafts` controls).

## Common Commands

```bash
# Development server with live reload
hugo server -D

# Build for production
hugo --minify --gc

# Create new blog post
hugo new post/your-post-name.md

# Create new author
hugo new author/author-name.md
```

## Architecture

### Configuration
- `config/_default/config.toml` - Main Hugo config (base URL, theme, pagination)
- `config/_default/params.toml` - Site parameters (logo, colors, widgets, social links)
- `config/_default/languages.toml` - Language settings (English enabled, French disabled)
- `config/_default/menus.en.toml` - Navigation menu structure

### Content Structure
All content lives in `content/english/`:
- `post/` - Blog articles (main content, Markdown)
- `post/html/` - Standalone HTML articles (see below)
- `author/` - Author profiles
- `homepage/` - Homepage layout variants
- Single pages: `about.md`, `contact.md`, `privacy-policy.md`, `terms-conditions.md`

### Post Frontmatter Format
```yaml
---
title: "Post Title"
date: 2023-06-18T01:00:00+09:00
images:
  - "images/post/your-image.png"
author: "Author Name"
description: "Meta description"
categories: ["Category"]
tags: ["tag1", "tag2"]
type: "regular"  # or "featured"
draft: false
---
```

### 게시 방식 2: 완성형 HTML 문서 (`content/english/post/html/`)

마크다운 대신 **자체 `<html>/<head>/<style>/<script>`를 모두 갖춘 완성형 HTML 문서**를 그대로 게시하는 경로다. 파일을 `content/english/post/html/*.html`에 넣고 맨 위에 프런트매터만 붙이면 된다.

```yaml
---
title: "글 제목"                      # 문서의 <title>을 이 값으로 덮어씀 ("제목 | AIEconLab")
date: 2026-07-26T09:00:00+09:00
author: "주영민 (Youngmin Ju)"
description: "메타 설명 (검색·공유 카드용, 100~160자)"
summary: "목록/검색/RSS에 쓰이는 요약 — 완성형 HTML은 자동 요약이 불가능하므로 반드시 직접 지정"
categories: ["AI_칼럼"]
tags: ["AI", "ECONOMICS"]
type: "regular"                       # regular 또는 featured
url: "/post/글-슬러그/"                # (선택) 없으면 /post/html/파일명/ 으로 나감
draft: false
---
<!DOCTYPE html>
...
```

동작 방식:
- `config.toml`의 `[[cascade]]`(`path = "/post/html/**"`)가 이 폴더의 모든 파일에 `layout = "standalone"`을 자동 부여한다. 프런트매터에 `layout`을 따로 쓸 필요는 없다.
- `layouts/_default/standalone.html`은 `main` 블록을 정의하지 않으므로 Hugo가 `baseof.html`을 건너뛴다. 즉 **테마 헤더/푸터/CSS가 전혀 섞이지 않는다** — 문서의 전역 CSS(`body`, `h1`, `section`, `footer` …)가 테마와 충돌하지 않게 하려는 의도적 설계다.
- 문서 원본은 그대로 두고 다음만 주입한다: `<title>`(프런트매터 기준으로 교체), `</head>` 앞에 canonical·description·author·favicon·OG/트위터 카드·Article JSON-LD·애널리틱스, `<body>` 바로 뒤에 상단 고정(sticky) 사이트 바(`partials/standalone/site-bar.html`).
- 사이트 바는 화면 최상단에 계속 붙어 있어 뒤로 가는 경로가 항상 보인다. 문서가 자체 sticky 헤더(`top:0`)를 갖고 있으면 바에 가려지므로, 바에 포함된 스크립트가 바 높이를 재서 다른 top-고정 요소를 그만큼 아래로 밀고 `scroll-padding-top`도 맞춘다(문서 내 `#앵커` 링크가 바 밑에 숨지 않게).
- 섹션은 여전히 `post`이므로 홈, `/post/`, 카테고리·태그, RSS, 사이트맵, 검색에 마크다운 글과 똑같이 노출된다.
- 검색 색인은 `layouts/index.json`이 `partials/standalone/plaintext.html`을 통해 `<style>/<script>`를 걷어낸 본문 텍스트만 넣는다 (안 그러면 CSS 전체가 색인에 들어감).

주의:
- `summary`가 없으면 목록 카드·RSS에 CSS 조각이 노출된다. 필수로 넣을 것.
- 대표 이미지가 필요하면 `images: ["images/post/....png"]`를 넣는다. 없으면 카드가 텍스트만으로 나오고 공유 카드는 사이트 기본 OG 이미지를 쓴다.
- 문서 안에서는 사이트 상대경로 대신 절대경로(`/post/...`)나 절대 URL을 쓸 것. 이 페이지에는 `<base>` 태그가 없다(있으면 문서 내부 `#앵커`가 깨진다).
- 마크다운 글은 기존 방식 그대로 `content/english/post/*.md`에 두면 된다. 두 방식은 서로 영향을 주지 않는다.

### Assets
- `assets/images/` - Processed images (Hugo Pipes)
- `static/` - Unprocessed static files
- Images referenced in posts go in `assets/images/post/`

### Theme Customization
The logbook-hugo theme is in `themes/logbook-hugo/`. Override templates by creating matching files in the root `layouts/` directory. Color and font customization is done via `params.toml` under `[params.variables]`.
