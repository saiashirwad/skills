---
name: open-in-neovim-ghostty-split
description: Show or open a file in Neovim in Ghostty, reusing an existing Neovim split or creating a right split automatically.
---

On macOS in Ghostty, run:

```bash
python3 ~/.agents/skills/open-in-neovim-ghostty-split/scripts/open.py '/absolute/path/to/file'
```

The helper checks foreground processes in the current tab, reuses and focuses Neovim (preferring the focused split), or creates a right split. `hide edit` preserves unsaved buffers. Paths are safely quoted. Report failures; don't send commands blindly to another process.
