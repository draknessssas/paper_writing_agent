---
name: ieee-page-compressor
description: Compress IEEE journal manuscript text while preserving technical claims, evidence, LaTeX structure, and reviewer-safe wording. Use when the user asks to reduce page length, shorten a section, tighten prose, or remove redundancy without weakening the paper.
argument-hint: "[section text or manuscript path] [target length/pages]"
---

# IEEE journal Page Compressor

## Purpose

Reduce length without damaging the argument or evidence chain.

Default output:

`working/compression_notes.md`

## Compression Priority

Cut first:
- repeated motivation;
- generic background;
- standard derivations known to IEEE journal readers;
- duplicated metric definitions;
- prose that repeats a figure/table caption;
- overlong transitions;
- unsupported promotional language.

Protect:
- contribution statements;
- evidence-bearing result sentences;
- definitions needed for reproducibility;
- baseline/protocol conditions;
- limitations and caveats;
- LaTeX labels, references, variables, and units.

## Workflow

1. Identify the paragraph/section job.
2. Mark claim-bearing sentences.
3. Mark removable or mergeable sentences.
4. Produce a compressed version.
5. List what was removed and whether any claim was weakened.

## Output Format

```md
# Compression Result

## Compressed text

## Removed or merged material
- ...

## Claim/evidence risk
- ...
```

## Rules

- Do not delete evidence needed to support a claim.
- Do not change numerical results.
- Do not break LaTeX citations, labels, equations, or figure/table references.
- When a target page limit or journal rule is mentioned, verify the latest author guidelines before treating it as fixed.
