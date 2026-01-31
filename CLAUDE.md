# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AIEconLab (인공지능경제연구소) - A Hugo static site for an AI Economics research lab. The site publishes Korean-language articles about AI trends, economics, and policy.

- **Site URL**: https://www.aieconlab.com/
- **Theme**: logbook-hugo
- **Deployment**: Netlify (auto-deploys from git)

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
- `post/` - Blog articles (main content)
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

### Assets
- `assets/images/` - Processed images (Hugo Pipes)
- `static/` - Unprocessed static files
- Images referenced in posts go in `assets/images/post/`

### Theme Customization
The logbook-hugo theme is in `themes/logbook-hugo/`. Override templates by creating matching files in the root `layouts/` directory. Color and font customization is done via `params.toml` under `[params.variables]`.
