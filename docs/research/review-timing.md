# Review timing and depth-first study drills

Research for [ticket #10](https://github.com/saiashirwad/skills/issues/10), under [map #1](https://github.com/saiashirwad/skills/issues/1). Sources checked 2026-09-30.

## Recommendation

Keep one hard core problem with variants as the **unit of instruction**, not the sole unit of evidence for mastery. Combine a focused, feedback-rich initial drill with later closed-notes retrieval and mixed, uncued transfer problems. Use a transparent judgement-based interval ladder initially; do not call it SM-2 or FSRS, or claim its dates are scientifically optimal. These are design recommendations derived from the evidence below, not a tested intervention.

This fits the existing decision: map → topics → drill/learn/mock tickets; attempts under `drills/<topic>/`; a closing comment with `review: YYYY-MM-DD`; `study-due` reopens the same ticket. The map's explicit pass bar remains authoritative. [P1]

## What the evidence establishes—and does not

### 1. Space retrieval over days; immediate fluency is not the target

Cepeda et al. taught more than 1,350 people facts, varied the gap before review up to 3.5 months, and tested retention after delays up to one year. Increasing the gap initially improved and eventually reduced retention. The best gap grew with the intended retention horizon, but not in a fixed proportion: approximately 20% of the test delay at a few weeks versus 5% at a year. This supports spacing and attention to the target horizon, **not** a universal “review every N days” prescription or applying those percentages to repeated coding drills. The task was factual learning, not algorithm design. [S1]

There is more directly relevant mathematics evidence. Rohrer and Taylor's first experiment contrasted practice of one problem type massed in one session against practice spaced across sessions; performance one week later favored spacing. Their second experiment contrasted blocked and mixed practice of multiple problem types, with mixed practice producing better delayed performance despite worse practice performance. Spacing and interleaving are distinct manipulations, even though a mixed curriculum often supplies both. [S2]

Retrieval is more than rereading a solution: Butler's four experiments compared repeated testing with repeated studying of prose. Testing improved one-week retention and transfer to new inferential questions, including questions in other knowledge domains. This is evidence that retrieval benefits need not be confined to verbatim recall, but it does not establish transfer to unfamiliar programming problems or an optimal coding-review interval. [S3]

**Design implication:** start a review without the old solution or a named technique. Ask for the governing idea/invariant and a solution to a comparable variant. Read notes and provide feedback *after* the attempt. A successful rewrite immediately after seeing the answer is useful repair, not evidence of retention across days.

### 2. Depth and interleaving solve different problems

A preregistered cluster-randomized trial involved 54 seventh-grade mathematics classes over four months. After a common interleaved review and a further month, the interleaved group scored 61% versus 38% on an unannounced test (`d = 0.83`). Mixing problem types creates occasions to choose a strategy from the problem itself rather than from the preceding lesson's label. [S4, abstract and discussion]

Important qualifications from the authors: time on task was not measured and teachers reported that mixed assignments took longer; the advantage per minute may therefore be smaller. Initial blocked practice may be needed, corrective feedback may be essential, and the intervention also supplied spacing and retrieval opportunities. It is not a clean estimate of “mixing alone,” nor a reason to forbid all blocked practice. [S4, manuscript pp. 21–22]

**Design implication:** preserve the deep initial drill, then mix *between* ticket families at later reviews. Ten consecutive variants of a known DP problem still largely cue “use DP.” Include a neighboring problem where greedy works, or where the familiar DP state fails, and ask the learner to justify the choice. Interleaving means changing the required strategy, not interrupting a single line of reasoning every few minutes. Use a small teaching block when a concept is new; do not spend every later session in that block.

### 3. Deliberate practice means targeted improvement, not maximum difficulty

Ericsson, Krampe, and Tesch-Römer distinguish deliberate practice from routine work or play: activities are specifically designed to improve current performance. Their account emphasizes tasks adapted to existing knowledge, informative feedback, repeated same/similar attempts, individualized error diagnosis, and progression to more complex tasks. Their original studies of musicians include diaries and retrospective practice estimates; they are not a randomized demonstration that one hard problem outperforms many easier ones. [S5, pp. 367–368 and Study 1]

**Design implication:** each deep drill needs a named weakness and an observable correction—for example, state definition, invariant proof, complexity argument, or boundary handling. Try → diagnose → explain/teach → retry a changed case. If prerequisites are missing, route to `study:learn` or a smaller subproblem rather than prolonging unproductive struggle. Difficulty is relative to the learner; an arbitrary “hard” label is not the learning objective. Feedback quality must be checked: generated tests do not establish that Claude's explanation or reference algorithm is correct.

**Bottom line:** the reviewed evidence supports the components of depth-first drilling, but does not establish the package “one original hard coding problem plus Claude-generated variants and grading” as superior to alternatives.

## Scheduling algorithms

| Approach | Mechanism in its owning documentation | Fit for this study family |
| --- | --- | --- |
| **SM-2** | Split knowledge into small items; initialize ease at 2.5; successful interval sequence starts at 1 and 6 days, then previous interval × ease, rounded up. A 0–5 response-quality rating adjusts ease, with a floor of 1.3; quality below 3 restarts the interval sequence. The original also repeats low-quality responses within a session. [A1] | Transparent and cheap, but an entire hard problem is not a small recall item. Its historical heuristic is not a calibrated estimate of interview readiness. Do not silently equate Anki's modified legacy scheduler with the original SM-2 specification. |
| **FSRS** | Models difficulty and stability; retrievability is the time-dependent probability of recall. Stability is the interval at which modeled recall is 90%. Grades are Again/Hard/Good/Easy. A desired retention target determines the interval from the forgetting curve. Current algorithm docs describe FSRS-6 with 21 parameters, including a trainable decay parameter and same-day updates. [A2] | Appropriate if there are stable review units and consistent histories. It can start with defaults and later fit parameters to review history; sparse data limits personalization. [A3] Changing problem difficulty and grading criteria between reviews weakens the interpretation of a single item's memory state. |
| **Judgement ladder (recommended first)** | A small explicit policy below, with dated evidence and an explanation. | Low machinery and auditable; knowingly uncalibrated. Useful until the unit of review and grading are stable. |

Anki defaults desired retention to 90%; higher targets increase review workload sharply. Its manual explicitly warns that **Hard is a successful recall**, not a euphemism for failure; using it when the answer was forgotten gives unsuitable intervals. Neither a 90% target nor a model's probability means a 90% chance of solving a new interview problem. [A2–A3]

Do not have Claude imitate FSRS equations in prose. If later adopted, use an implementation with a recorded version, actual review timestamps and ratings, and separate stable subskills from changing challenge tasks. Evaluate delayed *transfer performance and minutes spent*, not only correctness on remembered solutions. This is an implementation recommendation, not a claim that FSRS has been validated for this workflow.

## A simple rule Claude can apply by judgement

**Proposed policy, not an empirically optimized schedule:** interval ladder `1, 3, 7, 14, 30, 60` days. Days are measured from the actual assessment date; retain the scheduled date too so lateness is visible.

1. **Grade the first cold attempt, before hints or repairs.** Record technique selection, correctness, explanation/proof, complexity, assistance, and time against the map's pass bar. A new variant must be comparable in difficulty; failure on a genuinely new concept is not automatically forgetting of an old one.
2. **First assessment:** failure/solution dependence → repair and reassess in **1 day**; unaided but shaky → **3 days**; clean unaided pass with a justified variant → **7 days**.
3. **Later assessments:** failure → **1 day** and targeted repair; unaided but shaky → move **one rung shorter** than the previous assigned interval; clean pass → move **one rung longer**, capped at 60 days. A stable clean pass at the cap stays at 60. Do not promote several rungs because a review was overdue or because multiple same-day variants succeeded.
4. **Separate scheduling from passing.** “Shaky” means genuine unaided success with hesitation or self-correction, not rescue by a decisive hint. If the attempt misses the map's pass bar, keep the ticket open and record its next assessment date; close only when that bar is met. A same-day repaired pass may close the ticket, but must preserve the poor cold-attempt evidence and short next interval. Due-date handling for open tickets should be explicit in `study-due` rather than falsely marking failure as completion.
5. **Do not let one weakness reset everything.** If only the proof is weak but implementation is solid, record that subskill and target it next time. Repeated failures call for a prerequisite/teaching ticket or better task design, not an endless sequence of identical daily full solves.
6. **Review across families.** At least some due reviews should be uncued contrast/transfer variants, not exact repeats. Keep an occasional full timed mock to test integrated performance; a short explanation-only review cannot certify a timed coding bar.
7. **Allow explained overrides.** Bring a check before a known interview/exam, or shorten a date when assessment evidence is unreliable. Record the reason; do not label subjective confidence a recall probability. When reviews exceed available time, record deferrals and reduce new work rather than claiming the backlog was cleared.

Example closing comment (illustrative policy output):

```text
Cold attempt: unaided, correct O(n log n), 22 min; hesitant invariant proof.
Map bar: passed. Transfer: solved changed boundary case without hints.
Previous interval: 14 days. Judgement: shaky → one rung shorter (7 days).
Next target: justify the invariant on an uncued comparable variant.
review: 2026-10-07
```

For reproducibility, commit assessment date, variant ID, assistance, pass verdict, elapsed time, weak subskill, prior assigned interval, next interval/date, and rationale with the attempt. A materially changed rubric or task should be marked rather than silently treated as the same measurement. These fields are recommendations; no scheduling code or skill edits are implemented here.

## What remains unconfirmed

- No reviewed study tests this exact Claude-led coding-drill workflow, its grading reliability, or its transfer to hiring outcomes.
- The six ladder intervals, promotion rules, 60-day cap, ideal number of variants, and optimal mix of deep blocks versus mixed reviews are design defaults, not findings from the papers.
- The reviewed sources do not establish SM-2 versus FSRS superiority for multi-step problem solving. Recall modeling and novel problem-solving assessment are different targets.
- This is a focused primary-source investigation, not a systematic review. Butler and Rohrer–Taylor claims here are limited to the accessible/indexed author abstracts; detailed methods were not independently audited. Cepeda's author-hosted abstract, the interleaving trial's full manuscript, Ericsson's original full paper, and algorithm documentation were inspected. Some publisher/PubMed HTML fetches were inaccessible.

## Sources

- **[P1]** [Study-map decision, ticket #2 resolution](https://github.com/saiashirwad/skills/issues/2#issuecomment-5911131277), read together with map #1's Destination, Notes, and Decisions so far.
- **[S1]** Cepeda, N. J., et al. (2008). *Spacing effects in learning: A temporal ridgeline of optimal retention.* Psychological Science, 19, 1095–1102. [Author-hosted abstract and paper](https://www.yorku.ca/ncepeda/publications/CVRWP2008.html). DOI: [10.1111/j.1467-9280.2008.02209.x](https://doi.org/10.1111/j.1467-9280.2008.02209.x).
- **[S2]** Rohrer, D., & Taylor, K. (2007). *The shuffling of mathematics problems improves learning.* Instructional Science, 35, 481–498. [Author abstract indexed by ERIC](https://eric.ed.gov/?id=EJ786797). DOI: [10.1007/s11251-007-9015-8](https://doi.org/10.1007/s11251-007-9015-8).
- **[S3]** Butler, A. C. (2010). *Repeated testing produces superior transfer of learning relative to repeated studying.* Journal of Experimental Psychology: Learning, Memory, and Cognition, 36, 1118–1133. [Indexed abstract](https://pubmed.ncbi.nlm.nih.gov/20804289/); [publisher record](https://www.psycnet.org/fulltext/2010-17631-003.html). DOI: [10.1037/a0019902](https://doi.org/10.1037/a0019902).
- **[S4]** Rohrer, D., Dedrick, R. F., Hartwig, M. K., & Cheung, C.-N. (2020; manuscript 2019). *A randomized controlled trial of interleaved mathematics practice.* Journal of Educational Psychology, 112, 40–52. [Original grantee manuscript](https://files.eric.ed.gov/fulltext/ED595322.pdf). DOI: [10.1037/edu0000367](https://doi.org/10.1037/edu0000367).
- **[S5]** Ericsson, K. A., Krampe, R. T., & Tesch-Römer, C. (1993). *The role of deliberate practice in the acquisition of expert performance.* Psychological Review, 100, 363–406. [Original paper, hosted copy](https://graphics8.nytimes.com/images/blogs/freakonomics/pdf/DeliberatePractice(PsychologicalReview).pdf). DOI: [10.1037/0033-295X.100.3.363](https://doi.org/10.1037/0033-295X.100.3.363).
- **[A1]** Wozniak, P. A. (1990; web adaptation 1998). [Original SM-2 algorithm specification](https://super-memory.com/english/ol/sm2.htm), including the heuristic origins and quality scale.
- **[A2]** Open Spaced Repetition. [FSRS algorithm documentation](https://github.com/open-spaced-repetition/awesome-fsrs/wiki/The-Algorithm), especially Symbols and FSRS-6; current owning wiki, replacing the old fsrs4anki page.
- **[A3]** Anki Manual. [FSRS guide, desired retention, parameters, and health checks](https://docs.ankiweb.net/deck-options.html#fsrs). Product documentation, not independent experimental evidence for complex skills.
