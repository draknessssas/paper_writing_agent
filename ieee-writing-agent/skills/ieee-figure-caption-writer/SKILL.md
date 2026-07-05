---
name: ieee-figure-caption-writer
description: Write or audit IEEE journal figure and table captions, figure callouts, and figure-text alignment. Use when the user asks for captions, figure descriptions, table notes, graphical-result interpretation, or whether a figure supports a manuscript claim.
argument-hint: "[figure/table path or description] [related manuscript paragraph]"
---

# IEEE journal Figure Caption Writer

## Purpose

Make figures and tables stand alone while keeping their claims bounded.

Default output:

`working/figure_caption_plan.md`

## Caption Pattern

For each figure/table, capture:

1. What is shown.
2. Operating/evaluation condition.
3. Metric, signal, material, converter, or dataset context.
4. Main visible trend or comparison.
5. Supported interpretation.
6. Boundary or caveat when needed.

## Workflow

1. Identify the figure/table role:
   - setup schematic;
   - waveform reconstruction;
   - loss/energy/efficiency result;
   - dynamic response;
   - ablation;
   - baseline comparison;
   - stress case;
   - summary table.
2. Check the manuscript sentence that cites the figure.
3. Draft a caption that can be understood without reading the full paragraph.
4. Flag any caption claim that needs evidence.
5. Suggest text callouts that connect the figure to the Results narrative.

## Output Format

```md
# Figure/Table Caption Plan

## Figure X
Caption:

Text callout:

Supported claim:

Risk / missing evidence:
```

## Rules

- Do not add numerical values that are not visible in the figure or provided by the user.
- Do not make the caption do more work than the figure supports.
- Preserve LaTeX labels, subfigure references, units, variables, and material names.
- For IEEE journal, connect the caption to physical behavior, operating condition, and validation purpose.
