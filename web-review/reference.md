Source: [Vercel Web Interface Guidelines](https://github.com/vercel-labs/web-interface-guidelines/blob/e3d624baaf29dc1fc645aff3e38f03e564d2d6b1/command.md).
Revision: `e3d624baaf29dc1fc645aff3e38f03e564d2d6b1`. Copyright (c) 2025 Vercel Labs. License: [MIT](LICENSE.txt).
Local adaptation: condensed checklist; read-only evidence reporting and copy/framework overrides are defined in SKILL.md. Consult the pinned source for details, never a mutable latest URL.

# Audit rules

## Accessibility and focus

- Give icon buttons accessible names and form controls labels. Hide decorative icons and use appropriate image alt text.
- Prefer semantic buttons, links, labels, tables, and hierarchical headings before ARIA. Provide a main-content skip link and anchor scroll margins.
- Make custom interactions keyboard-operable; announce async updates appropriately.
- Provide captions, transcripts, or descriptions for meaningful media, keyboard-operable media controls, and assistive-tech hiding for decorative media.
- Keep visible focus, preferably `:focus-visible`, and use `:focus-within` for compound controls. Never remove outlines without replacement or let sticky overlays obscure focus.

## Forms

- Use meaningful names, autocomplete, input types, and input modes. Do not block paste.
- Make labels clickable and share hit targets with checkboxes/radios. Disable spellcheck for emails, codes, and usernames.
- Keep submit enabled until the request starts; show pending state. Place errors near fields and focus the first error on submit.
- Show example patterns in placeholders ending with an ellipsis. Check non-auth autocomplete behavior and warn before losing unsaved changes.

## Animation

- Respect reduced motion, stopping decorative loops or providing a still alternative. Autoplay motion over five seconds alongside content needs pause, stop, or hide controls.
- Prefer transform/opacity; name transition properties rather than `transition: all`. Set transform origins deliberately, including SVG wrapper/origin behavior.
- Keep animations interruptible and responsive to input.

## Typography and content handling

- Use ellipses for loading states, non-breaking spaces for coupled units/shortcuts, tabular numerals for comparisons, and balanced headings where useful.
- Handle long text, empty states, and short/average/long user content. Flex children may need `min-width: 0`; choose wrapping or truncation intentionally.

## Images and performance

- Give images explicit dimensions. Lazy-load below-fold images and prioritize critical above-fold images.
- Review lists over 50 items for virtualization or `content-visibility`. Avoid layout reads during render and batch DOM reads/writes.
- Keep per-keystroke input work cheap; prefer uncontrolled inputs where suitable.
- Preconnect needed asset domains and preload critical fonts with an appropriate display strategy.
- Prefer compressed muted inline video to animated GIFs, with a still/reduced-motion fallback and Safari-compatible sources where needed.

## Navigation, touch, and layout

- Reflect shareable filters, tabs, pagination, and expanded state in URLs. Preserve native link behavior and require confirmation or undo for destructive actions.
- Set touch action and tap highlights intentionally. Contain overscroll in overlays.
- During drag, prevent unwanted selection and manage inert elements appropriately. Provide tap/click and keyboard alternatives to gesture-only actions unless essential.
- Use autofocus sparingly, with justification, not on mobile by default.
- Account for safe areas, fix horizontal overflow rather than merely masking it, and prefer flex/grid to JS layout measurements.

## Themes, locale, and hydration

- Set `color-scheme` for dark themes and match theme-color to the background. Give native selects explicit foreground/background colors when needed.
- Format dates/numbers with Intl; detect language from browser/request preferences rather than IP. Protect brand names and identifiers from unwanted translation.
- For hydrated frameworks, avoid server/client date mismatches and use suppression only where justified. Controlled React inputs need change handlers; this is not an instruction to add React.
- Provide visible hover/active/focus feedback with sufficient contrast.

## Copy and common failures

- Use active voice, consistent specific action labels, numerals for counts, second person, and actionable errors. Follow the local copy overrides in SKILL.md.
- Flag disabled zoom, blocked paste, missing labels/alt/dimensions, div/span click targets, script-only navigation, missing focus replacement, unjustified autofocus, hardcoded locale formats, and gesture-only actions.

For repeatable full-page theme/viewport evidence, reuse [capture.py](../design-brief/scripts/capture.py). Inspect its output and test the relevant interactions; do not equate a successful capture with a passed audit.
