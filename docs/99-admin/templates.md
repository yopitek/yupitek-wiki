---
slug: templates
id: admin-templates
title: Templates
sidebar_position: 4
description: Recommended page templates for writing and translating wiki content, matching the article scheme.
---

# Templates

These templates describe the recommended structure for each page type. They are defined in full in the project's `article_scheme.md` and summarized here for quick reference.

## Frontmatter

Every page starts with YAML frontmatter:

```yaml
---
id: <unique-id>
title: <Page Title>
sidebar_position: <number>
description: <one-line summary shown in search and listings>
---
```

## Page Type Templates

### Product page (`products/{model}/index.md`)

Used for any single product.

1. One-line positioning statement ("what is this and who is it for").
2. **Specifications** table.
3. **Overview** paragraph(s).
4. **Driver / firmware install** (add a Mermaid flow when steps are non-trivial).
5. **Advanced usage**.
6. **Compatibility** table.
7. **Troubleshooting**.
8. Related resources links (absolute paths).

### Setup / guide page

1. Learning objective.
2. Concept explanation.
3. Prerequisites checklist.
4. Step-by-step `Step 1..N` blocks, each with a ```bash command and its **expected output**.
5. Verification step.
6. Common errors table.
7. References.

### Comparison page

1. Conclusion first.
2. Quick comparison table.
3. Deep-dive analysis.
4. Scenario-based recommendation.
5. Test data (if any).

### Troubleshooting page

1. **Diagnosis-first decision tree** (Mermaid flowchart).
2. Problem index table.
3. For each issue: Symptom / Diagnostic / Root cause / Fix.
4. "Still stuck?" → Review Queue.

## Diagram Rules

- Inline flow/sequence diagrams: **Mermaid**.
- Hero / highlight diagrams: standalone SVG stored under `static/img/{article-id}/`.

## DoD (Definition of Done)

- Frontmatter present and `id` unique.
- Structure matches the matching template.
- At least one diagram on setup/guide/troubleshooting pages.
- Every ```bash command actually tested; include expected output.
- Internal links use absolute route paths (no `../`).
- No `TODO` / `TBD` placeholders.
- `npm run build:en` passes with zero broken links.

## Related

- [`Review Queue`](/admin/review-queue/) — where new content is checked before it ships.
- [`Change Log`](/admin/change-log/) — records what changed and when.
