#!/usr/bin/env python3
"""Offline backend/exit-code and atomic Rift-trust regression checks."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"


class Backends(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.job = self.root / "job"
        self.job.mkdir()
        (self.job / "name").write_text("test-agent\n")
        (self.job / "backend").write_text("claude\n")
        self.bin = self.root / "bin"
        self.bin.mkdir()
        self.env = dict(os.environ, PATH=f"{self.bin}:{os.environ['PATH']}",
                        HOME=str(self.root), STATE="working", CLOCK=str(self.root / "clock"))
        self.command("herdr", '''#!/usr/bin/env python3
import json, os
print(json.dumps({"result": {"agent": {"agent_status": os.environ["STATE"], "state_change_seq": 1}}}))
''')
        self.command("opencode", "#!/bin/sh\necho 'Unexpected OpenCode call' >&2\nexit 99\n")
        self.command("sleep", "#!/bin/sh\nexit 0\n")
        self.command("date", '''#!/usr/bin/env python3
import os
from pathlib import Path
p = Path(os.environ["CLOCK"])
n = int(p.read_text()) if p.exists() else 0
print(n)
p.write_text(str(n + int(os.environ.get("TICK", "1"))))
''')

    def command(self, name, text):
        path = self.bin / name
        path.write_text(text)
        path.chmod(0o755)

    def run_await(self, expected, state="working", timeout="60"):
        self.env["STATE"] = state
        result = subprocess.run([str(SCRIPTS / "await"), str(self.job), timeout],
                                env=self.env, capture_output=True, text=True)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        self.assertNotIn("Unexpected OpenCode", result.stderr)
        return result.stdout

    def test_done(self):
        (self.job / "DONE").touch()
        self.run_await(0)

    def test_blocked_file(self):
        (self.job / "BLOCKED").write_text("needs a human")
        self.assertIn("needs a human", self.run_await(2))

    def test_blocked_agent(self):
        self.run_await(2, "blocked")

    def test_idle_stalled(self):
        self.run_await(3, "idle")

    def test_working_timeout(self):
        self.run_await(4, timeout="0")

    def test_working_hung(self):
        self.env["TICK"] = "901"
        self.assertIn("herdr agent send-keys test-agent esc", self.run_await(5))

    def test_legacy_backend(self):
        (self.job / "backend").unlink()
        result = subprocess.check_output(["bash", "-c", '. "$1/lib.sh"; backend "$2"',
                                          "bash", str(SCRIPTS), str(self.job)], env=self.env, text=True)
        self.assertEqual(result.strip(), "opencode")

    def test_trust_preserves_config(self):
        # Exercise the exact embedded program without touching the real config.
        source = (SCRIPTS / "spawn").read_text().split("<<'PY'\n", 1)[1].split("\nPY\n", 1)[0]
        path = self.root / ".claude.json"
        original = {"other": [1, 2], "projects": {"/existing": {"keep": True},
                    "/new-rift": {"allowedTools": ["Read"]}}}
        path.write_text(json.dumps(original))
        path.chmod(0o600)
        subprocess.run(["python3", "-", "/new-rift"], input=source, text=True,
                       env=self.env, check=True)
        original["projects"]["/new-rift"]["hasTrustDialogAccepted"] = True
        self.assertEqual(json.loads(path.read_text()), original)
        self.assertEqual(path.stat().st_mode & 0o777, 0o600)
        self.assertEqual(list(self.root.glob(".claude.json.*")), [])
        path.unlink()
        subprocess.run(["python3", "-", "/fresh-rift"], input=source, text=True,
                       env=self.env, check=True)
        self.assertEqual(json.loads(path.read_text()),
                         {"projects": {"/fresh-rift": {"hasTrustDialogAccepted": True}}})


if __name__ == "__main__":
    unittest.main()
