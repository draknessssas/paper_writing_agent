---
name: intro-reference-miner
description: Analyze current Introduction reference papers or provided reference paths to extract citation anchors, prior-art categories, limitations, research gaps, and safe-to-use literature claims for a target IEEE journal Introduction.
argument-hint: "[corpora/current_intro_refs or explicit file paths]"
---

# Intro Reference Miner

## Purpose

Build a current-paper Introduction reference map from papers provided for this manuscript.

The output should normally be saved to:

`working/intro_reference_map.md`

## Inputs

Possible sources:
- `processed/current_intro_refs/`
- `corpora/current_intro_refs/` after ingestion
- explicit paths supplied in the current conversation
- pasted summaries from the user

Full papers are acceptable in this folder. They are mined for the current manuscript's citation map, prior-art categories, and gap support, not for long-term style imitation.

## What To Extract

For each reference paper:

1. Bibliographic anchor
   - filename or citation key;
   - title if available;
   - year if available;
   - topic.

2. Technical role
   - what problem it addresses;
   - what method, system, theory, experiment, device, topology, control, or model it uses;
   - what result or capability it demonstrates;
   - what limitation is relevant to the user's current paper.

3. Safe citation claims
   - claims the manuscript may cite this paper for;
   - claims that should not be attributed to this paper.

4. Prior-art category
   Group references into categories such as:
   - theory or modeling methods;
   - system or device methods;
   - control, algorithm, or optimization methods;
   - experimental or implementation methods;
   - application-specific solutions.

5. Gap support
   Identify what remains unresolved across the group:
   - operating condition;
   - performance tradeoff;
   - scalability;
   - parameter sensitivity;
   - hardware implementation burden;
   - dynamic response;
   - efficiency, performance, reliability, cost, complexity, or scalability issue.

## Output Format

Create or update `working/intro_reference_map.md`:

```md
# Introduction Reference Map

## Current manuscript topic
[Filled from user prompt if provided]

## Prior-art categories

### Category 1: ...
| Ref | What it does | Useful claim | Relevant limitation | Do not claim |
|---|---|---|---|---|

## Cross-paper synthesis

## Candidate Introduction flow
1. Application context:
2. Technical challenge:
3. Prior-art category A:
4. Prior-art category B:
5. Remaining gap:
6. Need for proposed approach:

## Safe citation anchors
- Claim:
  - Supported by:
  - Strength:
  - Risk:

## Missing information
- [NEED: ...]
```

## Rules

- Do not invent citations.
- Do not overstate a reference paper's limitation.
- Do not copy wording.
- Do not use reference papers as proof of the user's experimental results.
- Keep claims citation-safe.
