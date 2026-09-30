Source: [Anthropic frontend-design](https://github.com/anthropics/skills/blob/8a1541c4a3ffa5a20a5a91de0dcf3f0bab1d1ef4/skills/frontend-design/SKILL.md).
Revision: `8a1541c4a3ffa5a20a5a91de0dcf3f0bab1d1ef4`. License: [Apache-2.0](LICENSE.txt).
Local adaptation: condensed planning guidance; build ownership moved to delegate, fixed constraints take precedence, and captures are required rather than optional.

# Method

1. Establish the subject, audience, and primary job from existing context. Separate confirmed constraints from unresolved questions. Keep the project's stack, assets, palette, type, and copy rules unless the user opens them for change.
2. Plan only the free axes: named color values and roles, type roles and scale, layout/hierarchy (a small wireframe helps), and a few subject-specific principles. Use one memorable element; remove decoration that conveys no information. Number things only when they are a sequence; use motion purposefully, not on every section.
3. Review the plan for fidelity and restraint before building. Explain why each variation helps this audience do its job. Generic warnings against fonts, rounded cards, or common palettes never invalidate the agreed brief.
4. Use real content throughout. Name actions consistently and describe what they do from the reader's perspective. Make error and empty states useful; do not fill missing evidence with invented claims or generated product screenshots.
5. Inspect the complete rendered page at desktop/phone sizes and in light/dark themes. Check responsive overflow, keyboard focus, image/font readiness, and reduced-motion behavior. Record observed defects and untested behavior; captures are evidence, not a compliance certificate.

For a build brief, state the question, fixed constraints, permitted variation, content/asset paths, acceptance checks, and handoff paths. Do not create a competing design-system file hierarchy.
