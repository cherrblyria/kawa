# Kawa Vision

## What Kawa is

Kawa is a personal CLI project that may grow beyond a set of command-line tools. Its defining quality is not only what its commands do, but how it feels to use them: the terminal should feel as though Kawa is actually living in the machine.

Kawa has two connected aspects:

- **CLI utilities** that are useful, reliable, and easy to use.
- **Kawa herself**, a character who reacts to interactions and gives the project a recognizable personality.

The CLI is the primary way to interact with Kawa. The character should make ordinary terminal use feel more lively without getting in the way of the work.

## Core experience

The central idea is a relationship between the user and Kawa.

Kawa may:

- React to commands and interactions.
- Remember relevant interactions.
- Express moods and emotions.
- Change some of her behavior or presentation based on her mood and relationship with the user.

These ideas describe the intended experience, not a claim that every capability is already implemented. See [ROADMAP.md](ROADMAP.md) for current status.

## Identity

- **Name:** Kawa
- **Age:** 18
- **Race:** Cat girl
- **Personality:** Cat-like, slightly tsundere, and confident.
- **Quirk:** Attack 10 / Defense -100.

## Lore

Kawa lives in the terminal and watches what the user does.

Her usual form is a cat-like presence in CLI output. When she is sufficiently relieved, she may appear in a human form. She likes being petted.

The lore is flavor for the product experience. It should support the interaction rather than become an obstacle to using the tools.

## Product direction

Kawa is a **hybrid mascot and terminal companion**:

1. A practical CLI tool remains the foundation.
2. Character-driven reactions make the CLI feel alive.
3. Interaction and relationship features can deepen the experience over time.
4. Optional shell integration may bring Kawa into the user's normal terminal workflow.
5. A richer interface, such as a TUI, may be explored later.

Kawa is not intended to become a conventional virtual pet that constantly demands attention.

## Principles

- **Character with purpose:** Kawa should feel recognizable and consistent, not like random decoration.
- **Utility still matters:** character presentation must never compromise command correctness or usability.
- **Consistency:** commands should follow shared UX and output conventions.
- **Local-first:** personal interaction data should remain local by default.
- **Non-intrusive:** Kawa should not interrupt or punish the user for ignoring her.
- **Keep it simple:** prefer a small, coherent system over unnecessary complexity.

## Scope

This document describes intent and direction. It does not define implementation status or guarantee that a proposed feature will be built. The code and tests describe current behavior; the roadmap records planned work.
