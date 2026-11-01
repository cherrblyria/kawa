# Kawa Design

This document describes shared product and CLI experience conventions. It is intended to keep commands and character presentation coherent as the project grows.

## Design priorities

When making a design decision, prioritize:

1. Correctness.
2. Consistency.
3. Readability and usability.
4. Character expression.

Character is important, but it must not make the tool harder to use.

## Output modes

Kawa has three output modes:

### Cute

- The default mode.
- May include Kawa's personality, kaomoji, and decorative presentation.
- Keep decoration proportional to the command's result.
- The actual result must remain easy to identify and copy.

### Plain

- No character dialogue or decorative presentation.
- Prefer straightforward, readable output.
- Suitable for users who want minimal output and for workflows where decoration is unwanted.

### JSON

- Must be valid machine-readable JSON.
- Do not print dialogue, banners, or other text outside the JSON document.
- Do not emit non-standard numeric values such as NaN or Infinity.
- Keep the structure predictable and appropriate to the command.

### Mode resolution

The current convention is:

1. A leaf command's explicit mode flag.
2. A parent command group's explicit mode flag.
3. Cute mode by default.

`--json` and `--plain` are mutually exclusive.

New commands must follow the existing `output_mode` convention documented in [AGENTS.md](../AGENTS.md).

## Command UX

Commands should:

- Use names that describe their purpose.
- Follow existing naming and alias conventions.
- Use consistent argument and option patterns.
- Provide useful help text.
- Handle invalid input clearly.
- Avoid surprising behavior.

Aliases should be useful and memorable. Do not add aliases solely for decoration.

## Output consistency

- Use consistent terminology, number formatting, and units.
- Make the important result visually easy to find.
- Keep decorative text from obscuring the result.
- Preserve stable output where users may copy, script, or rely on it.
- When changing user-facing output, update tests and relevant README examples.

## Errors

- Explain what input or operation was invalid when practical.
- Prefer actionable messages over vague failure notices.
- Do not silently accept invalid input.
- Do not expose unnecessary internal implementation details.
- Keep errors readable in all supported output modes.

## Kawa's personality

Kawa's established personality is cat-like, slightly tsundere, and confident.

Her presentation should feel:

- Recognizable across commands.
- Lively without being noisy.
- Playful without obscuring useful information.
- Consistent rather than randomly changing tone.

Avoid repetitive dialogue, excessive cuteness, and interactions that interrupt the user's workflow.

## Separate behavior from presentation

Where practical, keep functional results separate from character presentation.

The character layer must not compromise:

- Calculation or command correctness.
- JSON validity.
- Plain-mode readability.
- Exit codes and error behavior.
- Piping, scripting, and automation.

A command should remain useful even when character presentation is disabled.

## Terminal experience

- Keep ordinary CLI interactions quick and natural.
- Avoid clutter and blocking prompts unless input is genuinely required.
- Treat shell integration as optional; it must not be required to use Kawa.
- Do not make Kawa demand attention on every command.

## Accessibility and readability

- Do not rely on color alone to communicate meaning.
- Keep important information understandable in plain text.
- Consider terminal width and environments with limited Unicode support.
- Decorative elements should remain secondary to the content.

## Adding or changing features

Before adding a feature, consider:

1. Does it fit the direction in [VISION.md](VISION.md)?
2. Does it follow the conventions in this document?
3. Does it duplicate an existing command or capability?
4. Does it introduce state, dependencies, or complexity that the feature justifies?
5. Do the architecture, tests, and user documentation need updates?

If an existing convention is insufficient, propose a change rather than silently inventing a new one.
