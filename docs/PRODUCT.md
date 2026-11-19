# CouchPilot product brief

## Decision and audience
Test whether adults watching instructional content on a television can find, understand and retain a useful segment with less interaction burden. This is a product hypothesis, not a user-research finding. The first release is a browser prototype with one original two-minute lesson and four bounded capabilities: seek, explain, prepare a companion card, and combined seek/card.

The first priority is intent fulfillment and viewer control. A smart answer that seeks to the wrong moment is a product failure. Ship the public rules-based exploration as a labeled work sample; hold any claim of production-ready voice AI until independent evaluation and real-user task research exist.

## Context and differentiation
YouTube already offers Ask YouTube on TVs and supports mobile companion interactions. CouchPilot is an independent task-completion and evaluation study, not a claim that these capabilities are new or absent from YouTube. Its narrow contribution is an inspectable voice/text-to-action loop, source-constrained outputs, consent before playback changes, and recorded local-model failures. It does not use YouTube branding, private APIs, scraped transcripts or actual YouTube account actions.

Official references checked November 18, 2026:
- https://blog.youtube/news-and-events/ask-youtube-web-mobile-tv/
- https://blog.youtube/news-and-events/youtube-conversational-ai-tool-available-smart-tvs/
- https://support.google.com/youtube/answer/7640706
- https://developers.google.com/youtube/iframe_api_reference
- https://developers.google.com/youtube/v3/docs/captions/download
- Related role: https://www.google.com/about/careers/applications/jobs/results/134050378411844294-product-manager-ii-living-room-tv-voice-experiences-youtube

## User journey
A viewer submits a typed request, or reviews an optional browser speech transcript first. The planner identifies retrieval terms, reads retrieved source segments, and chooses a bounded action. The UI displays the proposed timestamp and action. Only explicit approval changes playback or creates a card. Undo restores the previous playhead. Missing evidence, ambiguity, cancellation and inference failures are visible; model failures never silently switch to rules.

## Priorities and exclusions
P0: correct timestamp, source attribution, action validation, keyboard access, confirmation, cancellation, no unauthorized side effects. P1: explanation and phone handoff. P2: voice convenience and telemetry export. The implementation prioritizes the first-party lesson over catalog breadth to make provenance and expected outcomes auditable.

Excluded: autonomous purchases/comments/subscriptions, personal recommendations, account linking, live-stream analysis, child profiles, native Google TV/Roku/LG/Samsung integration, and any claim of deployment to real YouTube viewers. Screen-reader and actual television hardware testing remain necessary.

## Alternatives and trade-offs
| Option | Strength | Weakness / cost |
|---|---|---|
| Chapter buttons | Fast, predictable, private | Viewer needs to know which chapter contains the answer |
| Rules retrieval baseline | Negligible inference cost; reproducible | Brittle intent understanding and ambiguity handling |
| Small local model | Flexible phrasing; no paid inference API | CPU latency, download and memory costs; nonzero errors |
| Cloud model | Potential quality and latency improvements | Ongoing spend, processing consent and service dependence; not used |

The local-model approach preserves a free inference path but hardware, electricity, bandwidth and setup remain real costs. We do not assume AI is better than the baseline. Benchmark and viewer-task evidence must justify its friction.

## Success and economics
Primary proposed measure: verified task completion per eligible initiated task. Confirmations, abandoned requests, wrong seeks and undo count against an unqualified success claim. Secondary measures: median/p95 completion time, clarification completion, repeat use and phone-card completion. Guardrails: wrong actions, unsupported explanations, privacy incidents and playback interruption.

Cost per successful task = total inference/serving cost divided by verified completed tasks. A local zero-API-bill run is not zero resource cost. No ad revenue, retention uplift or user adoption is imputed. A browser demo cannot prove household retention or monetization.

## Experiment and release plan — not run with people
First recruit consenting adults using instructional videos. Use counterbalanced tasks and unseen lesson content to compare chapter controls, simple retrieval and AI assistance. Separate text input from speech transcription effects. Record completions, errors and task duration; do not fabricate interviews or represent model-generated personas as users. Determine sample size from a pilot variance estimate and an explicitly agreed minimum effect before a confirmatory study.

For an eventual online rollout, assign consistently by viewer or household where shared-TV interference matters. Use fixed observation windows, a primary metric, predeclared guardrails, SRM checks and a missing-telemetry policy. Account for repeated tasks within users and device strata. Define stopping/rollback and multiplicity before exposure; do not peek until significance. Ramp only after review.

Prototype release: runnable, attributed and reproducible. Production AI release: HOLD. Required next evidence includes unseen task success, acceptable p95 on target devices, consented usability observations, transcription/accent evaluation, complete privacy design and device partner constraints. Thresholds should be agreed before evaluation, not moved after seeing failures.
