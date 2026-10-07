#!/usr/bin/env python3
"""Reuse a foreground Neovim in the current Ghostty tab, otherwise split right."""
import pathlib
import subprocess
import sys

SCRIPT = r'''
on run argv
  set filePath to item 1 of argv
  set editCommand to item 2 of argv
  tell application "Ghostty"
    set currentTab to selected tab of front window
    set candidates to {focused terminal of currentTab} & (terminals of currentTab)
    repeat with term in candidates
      set processName to ""
      try
        set processName to do shell script "/bin/ps -p " & (pid of term as text) & " -o comm="
      end try
      if processName is "nvim" or processName ends with "/nvim" then
        focus term
        -- Ctrl-\ Ctrl-N returns to Normal mode, including from terminal mode.
        if not (perform action "text:\\x1c\\x0e:" on term) then error "Could not enter Neovim command mode"
        input text editCommand to term
        send key "enter" to term
        return "Reused Neovim terminal " & (id of term)
      end if
    end repeat
    set config to new surface configuration
    set initial input of config to "nvim -- " & quoted form of filePath & linefeed
    set newTerminal to split (focused terminal of currentTab) direction right with configuration config
    focus newTerminal
    return "Created Neovim split " & (id of newTerminal)
  end tell
end run
'''


def edit_command(path: str) -> str:
    # Vim single-quoted strings escape quotes by doubling them; fnameescape
    # handles spaces, bars, percent signs and other Ex filename metacharacters.
    if any(ord(char) < 32 or ord(char) == 127 for char in path):
        raise ValueError("Control characters in file paths are not supported")
    return "execute 'hide edit ' . fnameescape('" + path.replace("'", "''") + "')"


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: open.py FILE")
    path = str(pathlib.Path(sys.argv[1]).expanduser().resolve(strict=True))
    if not pathlib.Path(path).is_file():
        raise SystemExit("Expected a file")
    result = subprocess.run(
        ["osascript", "-", path, edit_command(path)], input=SCRIPT,
        text=True, capture_output=True, timeout=15,
    )
    if result.returncode:
        raise SystemExit(result.stderr.strip() or "Ghostty could not open the file")
    print(result.stdout.strip())


if __name__ == "__main__":
    main()
