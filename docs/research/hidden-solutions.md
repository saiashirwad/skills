# Hidden reference solutions for study drills

Research date: 2026-09-30. Resolves [ticket #9](https://github.com/saiashirwad/skills/issues/9) in [map #1](https://github.com/saiashirwad/skills/issues/1).

## Recommendation

**Use explicit `age` encryption for a pre-written, tested reference bundle; commit only the ciphertext to the study repo. Keep the decryption identity outside the repo and decrypt only at review.** This is the simplest *self-contained, accidental-spoiler-resistant* option that preserves the reference written before the attempt: age encrypts arbitrary files with a public recipient and decrypts explicitly with a secret identity, without Git filters or an additional GitHub repository. [1]

This is an engineering recommendation, not a claim that age can stop the learner who owns the computer. Define “hidden” as **not exposed by normal browsing, searching, diffs, tests, or routine assistant replies**, not “impossible for the owner to access.” If Claude and the learner use the same account and credentials, a locally available key is a deliberate-peeking escape hatch. Strict concealment requires a separate trusted grader holding the key/solution outside the learner's account and releasing it after submission. This follows from the documented key-based decryption and repository permissions, not from a special Claude security boundary. [1][4]

[Study decision #2](https://github.com/saiashirwad/skills/issues/2#issuecomment-5911131277) calls for original problems, tests, a hidden reference, committed attempts/review notes, and recurring reviews. Keep that contract: do not silently replace it with generating an unvalidated reference after the learner finishes.

## Comparison

The convenience and spoiler-risk rankings below are design judgments derived from the cited mechanics; they are not benchmark results.

| Option | Claude write/read mechanics | Accidental exposure and limitations | Verdict |
| --- | --- | --- | --- |
| **Explicit age file** | Encrypt a bundle to a public key; explicitly decrypt using an external identity. Supports stdin/stdout and output files. [1] | Repo contains ciphertext, not source. Still leaks payload size/recipient metadata; transcripts and temporary plaintext need separate care. Key holder can decrypt. [1] | **Default.** One tool and one external key; deliberate reveal, no transparent unlock state. |
| **git-crypt** | Configure `.gitattributes`; encryption on commit and decryption on checkout after unlock. [2] | Its convenience defeats our goal in an unlocked learner workspace: ordinary editors/search see plaintext. Rules must exist before adding sensitive files; filenames and commit messages are not encrypted. [2] | Good shared-secret workflow, poor anti-spoiler default. |
| **SOPS** | Encrypted-file editor supporting YAML, JSON, ENV, INI and binary; uses age, PGP or cloud key services. [3] | Still requires key custody. It introduces another encryption/editor layer when all we need is an opaque bundle. [1][3] | Use only if a SOPS/key-service setup already exists; otherwise unnecessary machinery. |
| **Separate private repository** | Write and fetch reference files in another repository; copy the selected drill into the study repo at reveal. Access is repository-scoped. [4] | Prevents normal study-repo search from finding it, but an owner can browse the private repo. True denial requires a different trusted owner and credentials the learner cannot use. [4] | Reasonable runner-up if a grader repo already exists; adds repository/authentication/synchronization work. |
| **Separate branch in the study repo** | Commit references on another branch, switch or read that branch for review. | A branch is a parallel version inside the same repo; normal clone creates remote-tracking branches for each branch. It is not a private permission compartment. [4][5] | Reject: easy accidental branch/history discovery, no meaningful access boundary. |
| **GitHub secret gist** | Create/view a gist, retain its URL; gist is itself a Git repository. [6] | “Secret” means unlisted, **not private**. Anyone finding the URL can read it; the author sees it in their gist list. [6] | Reject as a secrecy mechanism; an extra link to manage with weaker protection. |
| **Hashes-only tests** | Publish hashes of expected outputs, compare hashes of normalized candidate outputs. Standard hash APIs support this. [7] | Does not store a recoverable reference implementation. Small answer spaces can be guessed and hashed; code-hash equality would reject different correct programs. Output normalization and multiple valid outputs add complexity. These are deductions from digest comparison, not hash weaknesses. [7] | Not a reference-storage solution. Use ordinary public tests plus a sealed reference. |
| **Generate reference only at review** | No reference file or key exists before review. | Minimal storage machinery and no stored answer to stumble upon, but no retained pre-attempt reference to validate the original tests or compare with later. This is a workflow trade-off, not a model-performance claim. | Only an explicit fallback if the user relaxes the pre-written/tested-reference requirement. |

## Proposed minimal workflow

These are proposed implementation requirements, not scripts implemented by this research ticket.

### One-time setup

- Install age and generate a dedicated study identity outside every study repo. Its public recipient may be committed; the secret identity must not be. The age README documents `age-keygen -o`, public recipient encryption, and identity decryption. [1]
- For self-study, use a backed-up, access-restricted external key location. Restricting file access helps other local accounts, not the learner who owns the key. For strict concealment, provision the identity only on a trusted grader; do not claim that a hidden local directory or a skill instruction enforces secrecy. [1]
- Use neutral names such as `reference.tar.age`, not `use-tarjan-scc.age`: metadata can itself spoil the approach. Explicit age encryption protects the bundle's contents, not a revealing filename outside it. [1]

### Author and seal before the attempt

1. In an authoring workspace outside the learner's repository, write the original problem, reference implementation, explanation, complexity analysis and checks. Run the reference against the advertised tests; use independent small-case checks where practical. Freeze the problem/test revision associated with this bundle.
2. Publish the statement, starter code and useful public tests under `drills/<topic>/<id>/`. Public tests should import the learner's implementation, **not decrypt or import the reference**. A normal test run must never create reference plaintext.
3. Bundle reference material and encrypt it to the public recipient. Copy only the ciphertext into `drills/<topic>/<id>/reference.tar.age`. Keep reference filenames and explanations inside the bundle. Verify that the sealed bundle can be decrypted and its tests rerun before declaring the drill ready; in strict mode this happens only on the trusted grader. age's documented archive-pipe example supports this packaging pattern. [1]
4. Commit only an explicit allowlist of public assets and ciphertext. Never stage plaintext in the study repo, even temporarily. Review the staged file list/diff before publishing. A repo contains file revision history, so deleting a mistakenly committed answer later does not undo its earlier availability. [4]
5. Remove temporary plaintext after successful sealing. Do not represent deletion as secure erasure of backups, editor history or agent logs. Keep authoring tool calls/transcripts out of the learner's normal attempt view; report only readiness and test status, not the answer.

Illustrative operations (paths are placeholders, not a complete safe wrapper):

```sh
# Seal: AUTHOR_BUNDLE is outside the study checkout; recipient.txt is public.
age -R recipient.txt -o drills/graphs/drill-001/reference.tar.age "$AUTHOR_BUNDLE"

# Review only: identity and output directory are outside the study checkout.
age -d -i "$STUDY_IDENTITY" -o "$REVIEW_DIR/reference.tar" \
  drills/graphs/drill-001/reference.tar.age
```

These flags and the separation of public recipients from secret identities are documented by age. [1] A wrapper should refuse existing outputs, use restricted temporary directories, clean up on failure, and never print plaintext/key contents. age itself overwrites an existing output, so the wrapper's refusal is an additional policy, not an age guarantee. [1]

### Submit, grade, reveal

- “Done” means the learner submits an attempt or explicitly ends it, not necessarily that they pass. Record the submitted commit before reveal. Do not let local public-test success automatically authorize decryption.
- At review, decrypt deliberately, compare behavior and reasoning rather than source-code equality, then reveal the explanation/reference and commit review notes as already required by #2. [8]
- If adding hidden grading tests, keep them with the grader until submission; running them locally against learner-controlled code is not a strong isolation boundary. A strict grader must execute that code without exposing the solution/key or returning raw secret-bearing traces. This is a required design constraint, not an audited grader implementation.
- **Reopened reviews cannot un-reveal an answer.** Once plaintext has been committed, repository history retains the prior version. Use an explicit no-peeking agreement for repeat practice, or a new variant/new sealed bundle when a fresh unseen task matters; re-encrypting the old file cannot revoke knowledge. [4][8]

## What remains unconfirmed

- This is primary-source/documentation research, not an installation or end-to-end test of age, SOPS, git-crypt, or a study runner. No keys or solution stores were created.
- Agent/harness transcript retention, visibility, temporary-file cleanup, and external workspace isolation were not audited. Encryption at rest alone cannot meet a literal “learner must never see it” promise if authoring calls expose plaintext in their session.
- No existing trusted grader/key custodian is specified in the map. Default to the stated self-study anti-spoiler boundary; treat strict access control as a separate infrastructure requirement.
- The workflow should be smoke-tested before implementation is called ready: normal repo search/diffs/tests expose no reference; restart/review can recover a sealed bundle with the external key; failed sealing never publishes plaintext; a due review does not pretend previously revealed history is hidden.

## Primary sources

All accessed 2026-09-30.

1. [age official README](https://github.com/FiloSottile/age/blob/main/README.md): key generation, archive encryption, explicit encryption/decryption, identities, output overwrite behavior and inspectable metadata.
2. [git-crypt official README](https://github.com/AGWA/git-crypt/blob/master/README.md): transparent checkout/commit behavior, attribute ordering and metadata/history limitations.
3. [SOPS official documentation](https://getsops.io/docs/): supported formats and key backends.
4. [GitHub: About repositories](https://docs.github.com/en/repositories/creating-and-managing-repositories/about-repositories): revision history, branch definition, private visibility and ownership permissions.
5. [Git: git-clone](https://git-scm.com/docs/git-clone#_description): default remote-tracking branches and single-branch behavior.
6. [GitHub: Creating gists](https://docs.github.com/en/get-started/writing-on-github/editing-and-sharing-content-with-gists/creating-gists): secret gists are not private; URL access, author listing and Git history.
7. [Node.js: crypto.createHash](https://nodejs.org/api/crypto.html#cryptocreatehashalgorithm-options): hash/update/digest mechanics used by an output-digest checker.
8. [Study map ticket #2 resolution](https://github.com/saiashirwad/skills/issues/2#issuecomment-5911131277): original drills/tests, hidden reference, grading and reopened review tickets.
