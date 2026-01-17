# Code Map Specification
Version: v1.0  
Language: English  
Audience: Developer + GPT

---

## 1. Purpose

The Code Map is the **structural representation of the codebase**.  
It serves as:

- architectural index
- navigation tool
- refactoring companion
- communication bridge between GPT and human
- context-preservation layer across iterations

The Code Map must always reflect **current repository structure**, not historical intent.

---

## 2. Code Map Characteristics

The Code Map must be:

- hierarchical
- deterministic
- high-signal, low-noise
- kept in sync with repo changes
- descriptive but not verbose
- versioned implicitly via git history

It must contain module/function/class names and ownership, but not source code.

---

## 3. Code Map Scope

The Code Map covers:

- modules
- packages
- folders
- entrypoints
- pipelines
- dependencies between internal modules

It must **not** document:

- external libraries
- package lock details
- deployment scripts
- low-level API implementation

---

## 4. Code Map Format

Recommended structure:

```
/package
  /module
    functions()
    classes()
    dependencies -> [...]
```

Dependencies expressed one-directionally (DAG-style) whenever possible.

---

## 5. Minimal Viable Code Map for v1

For v1 scanning tool, minimal structure:

```
scanner/
  main.py -> orchestration / pipeline runner
  config.py -> config loading + validation

  data/
    mexc_client.py -> MEXC API client
    marketcap_client.py -> CMC client

  mapping.py -> mapping logic

  pipeline/
    filters.py -> universe filters
    shortlist.py -> cheap → expensive reduction
    ohlcv.py -> OHLCV fetch + caching
    features.py -> feature engine

  scoring/
    breakout.py
    pullback.py
    reversal.py

  output.py -> JSON + Markdown reports
  snapshot.py -> snapshot creation
  backtest.py -> forward return evaluation

  utils/
    time.py
    math.py
    logging.py
    caching.py

tests/
  unit/
  integration/
```

This structure is illustrative; actual structure must match implementation.

---

## 6. Updating the Code Map

Rules for updates:

- update on file/module additions
- update on file/module removals
- update on function signature changes (if relevant)
- update on structural refactors
- update on pipeline re-ordering
- update on scoring changes

Do **not** update when:

- editing implementation details only
- fixing bugs without structural change
- updating comments or configs only

---

## 7. Code Map and GPT Collaboration

When GPT participates in coding:

GPT must:

1. read current Code Map before refactoring
2. propose structural changes
3. wait for confirmation
4. update Code Map after implementing changes

Without Code Map discipline GPT tends to:

- hallucinate missing components
- create namespace inconsistencies
- duplicate modules
- rewrite without reason

---

## 8. Code Map + Spec Integration

Spec defines **what** to build.  
Code Map defines **where** implementation lives.

Workflow:

```
spec.md → code implementation → code_map.md
```

Spec changes do **not** automatically change Code Map.

---

## 9. Anti-Goals

Code Map must not:

- include code
- embed docs
- become a README
- justify design decisions
- freeze structure permanently

It is a **living map**, not a manifesto.

---

## 10. Extended Usage (future)

Future Code Map extensions may include:

- module ownership (for teams)
- graph visualization
- code metrics
- dependency linting
- cycle detection
- refactor planning

These features are optional and outside v1 scope.

---

## 11. Summary

The Code Map:

- tracks architecture
- communicates structure
- supports GPT-assisted development
- prevents silent structural drift
- integrates with `dev_workflow.md`

---

## End of `code_map.md`
