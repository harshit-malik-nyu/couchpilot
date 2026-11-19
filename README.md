# CouchPilot

**A connected-TV AI product lab: find the right moment, understand it, and take it with you.**

[Try the experience](https://portfolio-lac-five-10.vercel.app/projects/couchpilot/) · [Product brief](docs/PRODUCT.md) · [Architecture](docs/ARCHITECTURE.md) · [Evaluation](docs/EVALUATION.md) · [Limitations](docs/LIMITATIONS.md)

An independent work sample by Harshit Malik for consumer AI product work. No affiliation with Google or YouTube. One original two-minute visual lesson makes every source excerpt and timestamp inspectable. No scraped video or fabricated customer evidence.

![Published CouchPilot experience](docs/live-demo.jpg)

[Deployment verification](docs/VERIFICATION.md) records the browser checks and exact tested revision.

## What works

- Play an original silent lesson and navigate six chapters with keyboard or pointer.
- Request a jump, explanation, phone card, or combined jump/card.
- Review source-backed action proposals before changing playback; undo a jump.
- Scan a QR to open the selected public lesson card on a phone and return to its timestamp.
- Inspect measured local-model traces and failures alongside the deterministic baseline.
- Run a bounded two-call local AI workflow with Ollama. It chooses retrieval terms, reads the results, selects actions, and returns a validated proposal. No paid inference API required.
- Exercise a separate loopback-only handoff API with 120-second expiry, one-time consumption and owner revocation.

**The public page runs the rules baseline. Its language-model results are recorded, not live inference.** Optional browser speech recognition requires user permission and may use the browser provider's service. Text input always works; no speech accuracy claim is made.

## Measured result and product decision

| Run | Correct authored tasks | Wrong seek proposals | Scope |
|---|---:|---:|---|
| Rules baseline | 11 / 12 | 0 | Deterministic reference |
| Local Qwen2.5 3B, v1 | 2 / 12 | 1 | Initial action contract |
| Local Qwen2.5 3B, v2 | 9 / 12 | 1 | Development rerun after simplifying the contract |

**Hold production AI rollout.** The model did not beat the baseline on this small, narrow suite. V2 failed two unsupported/ambiguous requests safely and proposed an unwanted seek on a card-only task. Model median measured task latency was 3.63 seconds; p95 was 13.14 seconds in this CPU run, including both model calls and possible first-request loading. These are authored acceptance cases, not independent held-out performance or human task timings. All failures and source/model hashes are retained. The public prototype is a reviewable work sample, not a claim of model readiness.

## Run without inference

Python 3.11+ and Node 20+; no runtime packages required for the prepared static app.

```sh
python -m unittest discover -s tests -v
node --test tests/test_engine.mjs
python scripts/verify_analytics.py
python scripts/build_web.py
python -m couchpilot.server
```

Open `http://127.0.0.1:8787`. The default experience uses rules. Server binds to loopback, so it is not a public or LAN service. The public QR works on a phone because it opens the published companion card; the local single-use API is separate.

## Run actual local AI

Install Ollama from its official source, start its local service and download the model. Model weights are separate and subject to their own license. Hardware, memory, electricity and downloads are resources even without an API bill.

```sh
ollama pull qwen2.5:3b
python -m couchpilot.server --model qwen2.5:3b
# Enable “Use local Ollama model” in the local app.
python -m couchpilot.evaluate --model qwen2.5:3b --output evaluation/my-local-run.json
```

The application calls only `127.0.0.1:11434`. Model unavailability produces a visible error; it never silently substitutes the rules policy. The evaluator writes progress after each case. Use a fresh filename for a new trial; the command does not resume interrupted runs. Tests use explicit model doubles and do not count as model-quality measurements.

## Contents

- `couchpilot/core.py`: retrieval, local model adapter, action validation and reference policy.
- `couchpilot/server.py`, `pairing.py`: loopback API and bounded single-use handoff.
- `web/`: static TV interface, original video, companion and recorded evidence.
- `evaluation/`: task definitions, v1 failure report, v2 report and v1 source snapshot.
- `analytics/`: task-level SQL funnel; verification uses labeled synthetic rows.
- `docs/`: strategy, experiment plan, traceability, risks and release decision.

Rebuild the original media with Pillow and ffmpeg using `python scripts/build_media.py`. Rebuild QR assets with qrcode 8.2 using `python scripts/build_qr.py`. These are optional asset-build dependencies, not app runtime requirements. Media generation is not byte-identical across encoder versions.

## Evidence boundaries

No native YouTube integration, device/OEM launch, real customer research, production-scale serving, guaranteed privacy on shared TVs, measured adoption or revenue impact. The public card contains only original public content; it is shareable and has no expiry. The original lesson and transcripts are released under CC0-1.0; code is MIT. Third-party runtimes/models retain their own licenses and are not redistributed.
