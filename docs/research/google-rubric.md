# Google coding-interview rubric: what is public, and what to use for study mocks

Research date: 2026-09-30. Resolves [ticket #11](https://github.com/saiashirwad/skills/issues/11) under [the swe + study map](https://github.com/saiashirwad/skills/issues/1).

## Answer

**Use a Google-informed practice rubric, not “Google's actual coding scorecard.”** Google's current public hiring guidance confirms structured, role-relevant questions, detailed evidence, standardized rubrics, and interviewer calibration. It explicitly describes **poor / borderline / solid / outstanding** response anchors. It does **not**, in the sources verified here, publish a current coding-round matrix, numerical weights, or a hiring cutoff. [1][2]

The strongest directly verified coding-related first-party material here is older: an engineering recruiter's preparation advice covers coding, algorithms, complexity, explaining implementations, and debugging; Google's hiring team describes technical interviews as engineering work samples that reveal both skills and problem-solving approach. These support the *content* of practice, not a claim about today's internal rating formula. [3][4]

For `study:mock`, adopt evidence-backed, question-specific anchors for **problem framing, algorithmic reasoning, implementation, validation, and communication**. Those five dimensions and the concrete anchors below are **our proposed teaching design**, not an official Google taxonomy. Do not translate the result into a predicted Google hiring decision.

## First-party findings

| Verified finding | Source and scope | Consequence for a mock |
|---|---|---|
| Google says it uses structured interviewing: the same interview questions, an identical scale, and consistent predetermined qualifications. It also says questions must be refreshed. | Current re:Work guide, updated March 2026, introduction. This is general hiring guidance, not a promise that every Google candidate receives identical coding problems. [1] | Fix the question, assessment criteria, and follow-ups before the attempt; do not improvise the scoring after seeing the answer. |
| Its four stated practices are vetted role-relevant questions, comprehensive response feedback, standardized rubrics, and interviewer training/calibration. | Current re:Work guide, introduction. [1] | Preserve evidence of the attempt and calibrate examples; do not grade only whether the final code passes. |
| Google “often documents with illustrative examples” what **poor, borderline, solid, and outstanding** answers cover for the attributes a question tests. | Current guide, “Use a rubric.” These are response-quality anchors; the page does not call them an overall hire/no-hire scale. [1] | The words can inform a four-band practice scale. Our coding-specific definitions still need an explicit local label. |
| Current suggested attribute categories are **role-related knowledge, problem solving, and leadership**. Problem solving includes processing information, breaking a problem into parts, and proposing a logical, data-driven solution. Leadership expectations vary by role level. | Current guide, “Define hiring attributes.” It calls these three categories helpful, not an exhaustive coding-round scorecard. [1] | Coding can elicit role knowledge and problem solving. A single code exercise is not sufficient evidence to rate all leadership attributes. |
| Initial prompts and planned follow-ups should elicit thought processes. Some interview questions assess analytical exploration rather than a single correct answer. | Current guide, “Draft your interview questions,” in a broad behavioral/hypothetical context. [1] | Ask for reasoning, but **do not infer that coding correctness is optional** from guidance about other question formats. |
| Feedback should contain examples, not vague impressions, resume summaries, or restatements of a rubric. Google cautions against personality/“fit” judgments and unrelated attributes. | Current interviewer-training guide, “Write clear feedback.” [2] | Cite observed code and explanations for every rating; do not grade charisma, accent, or similarity to the interviewer. |
| Interviewers should act as partners rather than gatekeepers, offer encouragement, and provide a conversational experience. | Current interviewer-training guide, “Best practices for interviewers.” [2] | Claude should be supportive while recording any help it provides; hostile behavior is not needed for realism. |
| Technical hires solve engineering problems as work samples, showing both skills and how they attack problems. Structured interviews have clear response criteria. | Google Online Hiring and Insights Team post, June 19, 2015. Historical first-party explanation, not confirmation of every 2026 process detail. [4] | Evaluate both the artifact and the reasoning that produced it. |
| A Google lead engineering recruiter recommends refreshing algorithms and complexity theory, practicing coding problems, explaining past algorithms and implementations, and recalling difficult bugs and fixes. He says to disclose a previously seen question so the interviewer can substitute another. | Jeff Moore, October 27, 2011. Officially published recruiter advice, but old and partly about technical interviews across software companies. [3] | Practice algorithmic fundamentals and explanation; ask whether a mock question is already familiar. Do not use it as proof of current numerical weights. |
| A former intern's Google-published advice says conversational practice matters, asking for help is fine, and interviewers want to see thinking rather than just a correct answer. | Christian Johnson, October 18, 2012. **Personal experience on a first-party publication**, weaker evidence than an institutional policy. [5] | Reasoning and help-seeking are useful practice behaviors; this does not establish that hints have zero scoring cost. |

## How ratings work: established versus unconfirmed

**Established:** Google publicly advocates behaviorally anchored rubrics—illustrative descriptions of different quality levels—plus detailed notes and interviewer calibration. Its current guide supplies four qualitative response labels. [1][2]

**Not established by the reviewed first-party sources:**

- Exact coding-specific dimensions, subcriteria, relative weights, or numeric score range.
- A universal relationship between the four response anchors and a final hiring recommendation.
- Exact penalties for hints, syntax mistakes, unfinished code, or missed edge cases.
- A universal requirement to solve a fixed number of questions, reach an optimal solution in a specified number of minutes, or use one particular tool/language.
- Level-specific coding thresholds or a formula that turns one mock into an offer probability.

These are limits of this research, **not proof that internal scorecards do not exist**. A current recruiter-provided guide could narrow the gap; it should be versioned and distinguished from general public guidance.

### Third-party claims kept separate

IGotAnOffer's SWE guide (updated June 15, 2026) says feedback forms contain recommendations such as **Strong no hire, No hire, Leaning no hire, Leaning hire, Hire, Strong hire**. It also lists four broad hiring attributes—GCA, role-related knowledge, leadership, Googleyness—and makes coding-specific claims about communication, accurate/fast code, and interview formats. These are **third-party reports**, even when informed by former interviewers; this research did not verify their exact current applicability against a first-party coding scorecard. [6, §§2.3, 3.1, 4]

Do not conflate that six-label hiring-recommendation claim with re:Work's four answer-quality anchors. Nor should the four-attribute third-party list overwrite the current re:Work page's three suggested categories. The scopes and wording differ; the evidence does not establish whether Google's internal taxonomy changed or which applies to a particular interview. [1][6]

## Recommended `study:mock` contract — local design, not Google policy

### Before interviewing

1. State the practice level, language, timebox, permitted tools, and whether assistance is allowed. Ask if the learner already knows the problem; substitute an original equivalent if so. The familiarity check is consistent with the older recruiter advice. [3]
2. Prepare a question-specific assessment: required constraints, acceptable approaches, expected complexity with justification, test cases, follow-ups, and concrete examples for the four bands. This applies the structured-rubric method rather than pretending Google supplied these coding anchors. [1]
3. Freeze that assessment for the attempt. Keep teaching/explanation until the debrief; distinguish neutral clarifications from substantive hints in the transcript.

### Proposed coding dimensions and a “solid” anchor

| Local dimension | Example of solid performance for a suitably scoped question |
|---|---|
| Problem framing | Restates the task, clarifies consequential ambiguities, and identifies relevant input constraints. |
| Algorithmic reasoning | Chooses a correct approach, explains why it works, and justifies time/space complexity and important trade-offs. |
| Implementation | Produces coherent code that implements the chosen approach correctly under the agreed assumptions. |
| Validation and debugging | Checks representative and boundary cases, traces failures, and fixes defects without the interviewer supplying the fix. |
| Communication and collaboration | Makes reasoning understandable, responds to questions, incorporates new constraints, and distinguishes assumptions from facts. |

**All rows above are proposed operational definitions.** Algorithms/complexity/explanation/debugging have historical recruiter-prep support [3]; observing problem-solving and using clear evidence have stronger institutional support [1][2][4]. The exact five-way split, edge-case expectations, and independence criteria are ours.

### Proposed four-band anchors

Use the same band names Google publishes, but label the coding definitions **study rubric v1**:

- **Poor:** Major unresolved gaps prevent a viable solution; cannot explain or repair the central issue even after substantive help.
- **Borderline:** Some meaningful progress, but important correctness/reasoning/validation gaps remain, or substantive help supplies a key missing step.
- **Solid:** Meets the question's predefined expectations; explains and validates the approach, with at most minor self-corrected mistakes.
- **Outstanding:** Meets “solid” and demonstrates the question's predefined stretch evidence, such as a justified improvement, strong generalization, or a well-reasoned follow-up—not merely faster typing or memorized tricks.
- **Not observed:** Separate from the four bands. The interview did not elicit enough evidence; do not treat missing evidence as failure.

Apply bands per dimension using question-specific examples, not a single impression. Record assistance separately (`none`, `clarification`, `nudge`, `substantive hint`) with the actual hint and subsequent response; these categories are also local. Avoid a numerical average or “Google hire” verdict: neither a weighting formula nor a mapping to hiring outcomes was verified.

### Debrief record

For each dimension, save: **band → observed evidence → remaining gap → next drill**. Include submitted code, tests actually run versus merely discussed, transcript references, elapsed time if measured, assistance, and uncertainty. Summarize readiness for the **next practice task**, not employability. A follow-up drill can target the weakest observed dimension; a later independent attempt can show whether the gap is resolved.

This implements the map's Claude-interviewer/Claude-grader goal without claiming proprietary evaluation knowledge. Evidence-based feedback follows Google's published guidance; the study progression is our recommendation. [1][2]

## Sources and retrieval limitations

All sources accessed 2026-09-30.

1. **Google re:Work Editorial Team, “A guide to structured interviewing for better hiring practices,” updated March 2026.** [Official guide](https://rework.withgoogle.com/intl/en/guides/a-guide-to-structured-interviewing-for-better-hiring-practices). Main source for current public rubric mechanics and attribute descriptions.
2. **Google re:Work Editorial Team, “Effective interviewer training for better candidate experiences,” updated March 2026.** [Official guide](https://rework.withgoogle.com/intl/en/guides/effective-interviewer-training-for-better-candidate-experiences). Main source for evidence-based feedback and interviewer behavior.
3. **Jeff Moore, Lead Engineering Recruiter, “Recruiter Tips & Tricks: Rocking the technical interview,” October 27, 2011.** [Official post](https://students.googleblog.com/2011/10/recruiter-tips-tricks-rocking-technical.html); [official full-content feed entry](https://students.googleblog.com/feeds/posts/default/8306696799083275405?alt=json). Historical technical preparation advice.
4. **Steven Claunch, Online Hiring and Insights Team, “How are interviews at Google different?”, June 19, 2015.** [Official post](https://students.googleblog.com/2015/06/how-are-interviews-at-google-different.html); [official full-content feed entry](https://students.googleblog.com/feeds/posts/default/7854247496435129876?alt=json). Historical institutional account of engineering work samples and structured interviewing.
5. **Christian Johnson, former Google intern, “Four tips towards a successful technical interview,” October 18, 2012.** [Official post](https://students.googleblog.com/2012/10/four-tips-towards-successful-technical.html); [official full-content feed entry](https://students.googleblog.com/feeds/posts/default/921055508236629989?alt=json). Personal advice, explicitly not a scorecard.
6. **IGotAnOffer, “Google Software Engineer Interview (questions, process, prep),” updated June 15, 2026.** [Third-party guide](https://igotanoffer.com/blogs/tech/google-software-engineer-interview). Used only to identify and label third-party claims, not to establish official Google policy.

The older Student Blog pages returned titles/navigation without article bodies in the text extractor. The complete bodies were read from Google's own [Blogger feed query](https://students.googleblog.com/feeds/posts/default?q=technical%20interview&alt=json&max-results=100), matching each entry to its permalink and post ID. These are first-party hosted texts, not third-party reproductions.

Current [Careers “How we hire”](https://www.google.com/about/careers/applications/how-we-hire/) and [Build Your Future resources](https://www.google.com/about/careers/applications/buildyourfuture/resources/) yielded only a navigation/footer shell in this environment. The former Tech Dev Guide interview URL redirected to the latter. The built-in browser was disconnected, so rendered Careers content and official video transcripts could not be verified. Search also returned no useful results. Accordingly, this report does not attribute a detailed modern coding rubric to inaccessible prep materials or claim an exhaustive search of all Google resources.
