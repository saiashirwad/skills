---
name: response-to-file
description: Export an assistant response to Neovim for annotation and submit a compact feedback diff, only when the user asks.
---

In Pi, call `response_to_file` (via codemode) with no arguments to export the latest completed response from session history. Use `nth: 2` for the previous response, and so on. Do not retype or regenerate its text. The tool saves under `/tmp` and runs the existing Ghostty/Neovim opener.

The user can run `/response-to-file [number]` directly with no model call. It saves a read-only `original.md` beside the editable `response.md`. After editing, save in Neovim (`:w`) and run `/response-feedback`: it sends only the diff against the original, with one line of context before and after each change, and starts an assistant turn. No special comment syntax, watchers, or automatic submissions. It uses the latest export on the active branch and skips unchanged/already-submitted content.

If the extension is not loaded, ask them to run `/reload`, then export again; exports made before feedback tracking was added are not tracked. For annotation submission, prefer `/response-feedback` over reading the whole file into context. Temporary files may be cleaned up by the OS; save elsewhere for long-term notes.
