# Improvement record: request control, evidence and interaction

## Problem
V2 scored 9/12 on narrow authored development tasks. It proposed a jump on a card-only request, failed to clarify an unspecified step and selected unverified evidence for an unrelated question. The browser also needed stronger protection against an edited request leaving a stale proposal available. These are specific reliability issues, not reasons to assign an arbitrary new portfolio score.

## Frozen evaluation design
`evaluation/robustness-design.json` records the hash and target criteria for 54 authored tasks written before the v3 changes. Cases include the original 12 plus navigation, card-only requests, all six current-chapter contexts, scoped negation, combined actions, relative chapters, ambiguous/out-of-scope requests, adversarial requests and paraphrases. The cases remained visible during development. This is an expanded development suite, not an independent test set or a sample of real viewer behavior.

Exact task success requires the expected status, exact tool set, correct segment and exact canonical source fields. A safe refusal to a valid task is a failure, not a successful safety result. All 54 cases remain in each denominator.

## Interventions and observed results

| Version | Change | Exact tasks | Failure interpretation |
|---|---|---:|---|
| v3 | Request boundary, source checks, consent critic and one repair | 42/54 | Ten blocked failures plus two wrong excerpt selections; prompt instructions did not reliably constrain tools |
| v4 | Compile consented actions and retrieved IDs into the decoding schema | 52/54 | No contract errors; two general introductions selected instead of specific excerpts |
| v5 | Remove irrelevant playhead cue and simplify evidence selection prompt | 54/54 | No observed error on these same known development cases |
| Current rules | Same request boundaries; highest-ranked source | 54/54 | This suite does not demonstrate incremental AI value |

V5 made 76 model calls across 38 tasks. Sixteen tasks were handled by deterministic boundary checks without invoking a model. Model output restrictions are enforced by the host. A chapter-specific request can have only one permissible action and source; this does not demonstrate open-ended reasoning. The model still plans retrieval terms and chooses evidence where several candidates remain. Validators and consent do not establish semantic correctness; the v4 errors demonstrate that distinction.

## Interaction and analysis changes
- Editing text, choosing a new chapter, changing engine or cancelling invalidates the pending request. Revision checks discard late responses; approval consumes the proposal once.
- Relative context is captured at submission. A chapter change requires a fresh review instead of silently retargeting an old request.
- Ambiguous requests offer explicit chapter choices. Selection prepares a new proposal and preserves the requested action type; execution still requires approval.
- TV focus mode enlarges controls and moves focus spatially with arrow keys. Native text editing retains normal keyboard behavior. It is a browser layout, not a certified TV application.
- The complete transcript is readable without watching the silent lesson. Reduced-motion and forced-colors styles remain supported.
- Task IDs are independent of cancellation revisions. Undo is attributed to the task that initiated its jump, even if a subsequent request was cancelled.
- The evidence explorer exposes historical runs, failures, categories and full recorded traces. Policy-only tasks are labeled separately from model latency.

## Reproduction and boundaries
`python scripts/verify_reports.py` checks report completeness, the frozen case hash, arithmetic, model-call budgets and exact current-source hashes. `python scripts/verify_qr.py` renders shipped SVG assets on the same white background used by the app and decodes every resulting URL. Optional decoder packages are pinned in CI. Software QR decoding is not a physical camera compatibility test.

The model files record Python, platform, Ollama version/model digest, hashes and task-level latencies. Model latency excludes speech, real device interaction and human approval. Historical source snapshots are under `evaluation/archive/`; v3 and v4 use the preserved `policy-v3.py.txt`. V2 is a self-contained core snapshot. Never overwrite the recorded reports when testing new changes.

## Product decision
Publish the transparent, reproducible work sample. Keep public interaction on the deterministic path and keep the local model optional. No incremental viewer value, ASR accuracy, native TV support, client adoption or production-scale serving has been established. A perfect observed score on these authored tasks is one bounded engineering result, not a universal product rating.

The 54-case suite contains 53 unique request/context pairs: “Explain this part” at the uncertainty chapter appears once in the original suite and once in the expanded context sweep. Both recorded cases remain visible; they are not independent observations.
