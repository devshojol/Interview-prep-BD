# Writing blog articles

Articles live here as Markdown files. `tools/build_blog.py` turns them into static HTML under `/blog/`. This README is skipped by the build.

## Frontmatter

```yaml
---
title: How to predict JavaScript output with promises, timers and async/await   # required, shown as the h1
description: One or two sentences, at most 200 characters.                      # required, meta description + listing text
publishedAt: 2026-10-13                                                         # required, real date
category: JavaScript                                                            # required
tags: [event loop, promises]                                                    # optional, shown as text
practice: [javascript, nodejs]                                                  # optional, app technology ids for the "Practise this topic" box
seoTitle: Shorter title for search results                                      # optional, used in <title> when the h1 is long
updatedAt: 2026-11-02                                                           # optional, ONLY when the content really changed
slug: custom-slug                                                               # optional, defaults to the file name
lang: bn                                                                        # optional, en (default) or bn; bn articles live at /blog/bn/<slug>/
translationKey: event-loop                                                      # optional, same key on an en + bn pair -> hreflang + reciprocal links
featured: true                                                                  # optional, the "Start here" article on the index
draft: true                                                                     # optional, drafts are never written, listed or put in the sitemap
coverImage: assets/og/custom.png                                                # optional, must exist; needs coverAlt
coverAlt: Description of the image
canonicalUrl: https://<production origin>/blog/other/                           # optional, must be on the production origin
author: Interview Prep BD                                                       # optional, defaults to site.json "author"
---
```

## Body

A safe subset of Markdown. Raw HTML is rejected, and everything else is escaped.

- `##`, `###`, `####` headings (the title is the only h1). Four or more `##` sections add a table of contents.
- Paragraphs, `-` and `1.` lists, `>` quotes, pipe tables (`---:` right-aligns a column).
- Fenced code with a language: `js`, `jsx`, `ts`, `sql`, `bash`, `json` are highlighted; anything else is plain.
- `` `code` ``, `**bold**`, `*emphasis*`.
- Links, which are checked at build time:
  - `[text](https://...)`: external, https only.
  - `[text](post:other-slug)`: another published article. Linking to a draft fails the build.
  - `[text](app:#/q/js-016)`: a question in the app (the id must exist in `questions.js`).
  - `[text](app:#/questions?tech=react)`, `app:#/technologies`, `app:#/practice`, `app:#/interview`, `app:#/flashcards`, `app:#/daily`, `app:#/review`, `app:#/sources`: public app screens.

## Rules for content

- Run every code example and paste the real output. Say which version you ran it on.
- Link official documentation for every API you rely on.
- No invented statistics, hiring claims, testimonials or personal stories.
- Only set `updatedAt` when the article itself changed; it drives `lastmod` in the sitemap.

## Build

```bash
python3 tools/build_blog.py --check                          # validate only
python3 tools/build_og_images.py                             # share images (needs Chrome), when titles change
SITE_URL=https://your-domain python3 tools/build_blog.py     # production build
```

Without `SITE_URL` (or `origin` in `content/site.json`) the build is a preview: every page is `noindex`, and there is no canonical, JSON-LD, sitemap, robots.txt or feed.
