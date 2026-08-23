---
draft: true
slug: review-queue
id: admin-review-queue
title: Review Queue
sidebar_position: 5
description: Workflow for triaging, reviewing, and publishing new or updated wiki content.
---

# Review Queue

The Review Queue is the triage workflow for any new, edited, or translated wiki content before it is considered done. It mirrors the `support-policy` decision flow.

## Workflow

```mermaid
flowchart TD
    A[Content submitted] --> B{Follows template?}
    B -- No --> C[Fix structure per Templates]
    B -- Yes --> D{Commands tested?}
    D -- No --> E[Re-test, add expected output]
    D -- Yes --> F{Links absolute & valid?}
    F -- No --> G[Fix internal links]
    F -- Yes --> H{Build passes?}
    H -- No --> I[Run build:en, fix broken links]
    H -- Yes --> J[Publish / merge]
    J --> K[Update Change Log]
```

## Checklist

Before a page is approved:

- [ ] Frontmatter `id` is unique across the whole wiki.
- [ ] Structure matches the matching template in `Templates`.
- [ ] At least one diagram on setup/guide/troubleshooting pages.
- [ ] Every ```bash command tested with expected output shown.
- [ ] No `TODO` / `TBD` placeholders.
- [ ] All internal links use absolute route paths.
- [ ] `npm run build:en` passes with zero broken links.
- [ ] Translated locales updated in the same change (see `Translation Glossary`).

## After Approval

Record the change in the [`Change Log`](/admin/change-log/).

If the change adds or renames a product, update the `Product Registry` and `Driver Registry` in the same commit.
