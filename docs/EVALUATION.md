# Evaluation record and release decision

## Current result — November 19, 2026

The frozen 54-case authored robustness suite is recorded in `robustness-cases.json` and `robustness-design.json`. Rules pass 54/54. The current constrained local AI workflow (v5) also passes 54/54, with zero wrong validated seek proposals, zero source-fidelity failures and zero inference errors in this run. **38 tasks invoked the model; 16 were deterministic boundary decisions.** This is a full-system development result, not unconstrained model accuracy or unseen validation.

The same author wrote the cases and changed the implementation with those cases visible. The v3 42/54 and v4 52/54 reports remain available alongside the v5 report; no case was removed or relabeled. See [the improvement record](UPGRADE.md) for the interventions and failure analysis.

Model-invoked tasks had a descriptive median of 3.35 seconds and nearest-rank p95 of 4.83 seconds; the maximum was 9.94 seconds, including possible initial model loading. These CPU measurements exclude speech recognition, real devices and human task completion. The report's overall latency summary also includes the 16 near-instant policy-only decisions; use the model-invoked subset when assessing inference latency.

The JSON output schema limits generation to consented tools and retrieved IDs. Exact source copying prevents fabricated excerpts, but source relevance still requires measurement. No AI advantage over rules has been demonstrated on this suite. Production AI remains on hold.

## Historical v1–v2 protocol
Twelve authored text tasks cover direct navigation, explanation, compound actions, current-playhead context, negation, unrelated requests, disallowed actions, ambiguity, a phone-only card, reasoning questions, instruction override and timestamp retrieval. The fixture, source and expected task results were written in the same development process. They are not independent or permanently held out.

Success requires the expected status, exact action set and correct target segment. A wrong seek is any proposed seek with an incorrect target or when no seek was requested. Human approval can block a bad proposal, but it does not make the model proposal correct. Exact copied excerpts establish source fidelity only; they do not establish relevance or comprehension.

All cases are counted once, including inference/schema failures. Reports preserve per-task latency, trace, source/case hashes, Python/platform and Ollama model metadata, including the model digest. p95 is nearest-rank: with 12 observations it is the maximum, so treat it as an unstable descriptive measure. First request includes possible model loading; the reports do not isolate a warm-service SLO.

## Iterations
V1 (preserved in `model-v1.json` and `core-v1.py.txt`): 2/12, seven contract errors. The planner frequently mixed clarification status with executable actions. Those proposals were blocked.

V2 (`model-run.json`): action selection simplified to one intent and a source identifier, with a JSON schema and explicit mapping to bounded tools. This is a development rerun on the same known tasks, not unseen validation. Result: 9/12, two blocked unverified-source errors, one unwanted seek. Rules baseline: 11/12, ambiguity failure. No superiority claim is justified.

## Failure analysis
| Task | Observed v2 failure | Product consequence | Candidate next experiment |
|---|---|---|---|
| Unrelated baking question | Proposed an explanation with no retrieved evidence | Validator blocks; error is less helpful than clear unsupported response | Compare no-evidence routing with model abstention on a frozen new task family |
| Unspecified step | Proposed a segment absent from retrieval | No execution; viewer must restate request | Evaluate a clarification policy using true ambiguity labels |
| Card-only request | Proposed both seek and card | Unwanted playback change if approved | Separate playback authorization from semantic source selection, then evaluate negation/implicit-action cases |

Do not fix a benchmark by relabeling these expected outcomes or discarding failures. Any tuning needs a versioned new report and an explicitly labeled development/holdout split. Generated requests from the same author are still limited evidence.

## Decision
Release the prototype as an inspectable independent work sample. Hold production AI. The model has not demonstrated better task success than a cheap baseline, satisfactory low-latency TV interaction, real ASR robustness or household usefulness. Proposed release gates should be set before a new evaluation and include a zero-wrong-action sample criterion with uncertainty, task success targets, device-specific latency and consented user-task results. Even zero observed failures cannot prove zero risk.

Next external validation would be real adult viewers, unseen lessons, varied accents/background audio, device/network strata and privacy comprehension. None is claimed as completed. No human completion-time comparison with remote-only navigation is available; chapter controls provide the implemented manual baseline for that future study.
