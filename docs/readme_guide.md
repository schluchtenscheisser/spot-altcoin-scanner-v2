# README Writing & Maintenance Guide
Version: v1.0  
Language: English  
Audience: Developer + GPT

---

## 1. Purpose

This guide defines how the project README must be written and maintained.  
The README serves as the **primary onboarding document** for a developer or user interacting with the scanner repository.

The README must **not** be a technical spec — that role belongs to `/docs/*.md`.

---

## 2. Responsibilities of README

The README must explain:

- what the scanner does (conceptual summary)
- why it exists (high-level motivation)
- how to install dependencies
- how to configure it
- how to run it
- how to schedule it (cron / GitHub Actions)
- how to interpret outputs
- how to update + version
- optional: how to backtest

The README must not contain:

- scoring formulas
- feature definitions
- market theory
- architectural diagrams
- refactoring instructions
- context/history of development

These belong to spec or docs.

---

## 3. Required Sections for README

Recommended README structure:

```
Project Title

Short Description

Key Features

Getting Started

Requirements

Installation

Config Setup

Running the Scanner

CLI examples

cron / GitHub Actions

Output & Reports

Backtesting (optional)

Versioning

Contributing (optional)

License (optional)
```

Minimal is acceptable for v1; sections may expand as project grows.

---

## 4. Writing Style

README style requirements:

- concise
- declarative
- beginner-friendly
- no trading jargon unless defined
- avoid ambiguity
- minimize dependency on deep market context

Tone is technical, not sales or hype.

---

## 5. Maintenance Rules

README must be updated when:

- installation changes
- dependencies change
- run instructions change
- config format changes
- output format changes
- scheduling changes

README must **not** be updated when:

- scoring model changes internally
- features are tuned
- minor refactors occur
- context-level docs change

---

## 6. README vs Code Map

README ≠ Code Map.

| Document | Purpose |
|---|---|
| README | onboarding, running the tool |
| code_map.md | architecture, structure, navigation |
| spec.md | technical truth + definitions |
| context.md | personal trading context |
| backtest.md | evaluation rules |

These documents must remain separate.

---

## 7. README + GPT Workflow

When GPT is assisting development, GPT must:

1. read `README.md` before providing run instructions
2. update README only after structural changes
3. ask before overwriting README
4. preserve formatting + sections

README overwrites must not remove user-specific instructions.

---

## 8. Example Minimal README Feel (v0.1)

Example summary block:

```
Spot Altcoin Scanner (v1)
Identifies short-term trading setups in MidCap Altcoins across Breakout, Pullback, and Reversal categories.
Outputs daily ranked reports + JSON snapshots for evaluation and backtesting.
Tradeable universe: MEXC Spot USDT MidCaps.
```

This is descriptive but not implementation-specific.

---

## 9. Anti-Goals

README must not:

- justify design decisions
- become a changelog
- become a spec
- contain verbose trading narratives
- embed market opinions
- embed code

These belong to other documents.

---

## 10. Future Extensions

README may later include:

- screenshots of outputs
- performance metrics
- backtest highlights
- deployment automation
- Docker instructions
- metadata badges

These are optional and not required for v1.

---

## End of `readme_guide.md`
