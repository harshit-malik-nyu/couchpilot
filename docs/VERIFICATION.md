# Published prototype verification

Verified November 18, 2026 (America/New_York), on the public Chrome desktop experience.

- Application revision: `25862d7a9fba26924a01e671c1541eef101beb82`.
- [Repository CI passed](https://github.com/harshit-malik-nyu/couchpilot/actions/runs/44439026189): 20 Python tests and 7 JavaScript tests, across Python 3.11–3.13; JavaScript syntax, SQL funnel reconciliation and generated-asset consistency checks.
- Portfolio deployment includes the project as the first selected-work card and in the role evidence page.
- [Live experience](https://portfolio-lac-five-10.vercel.app/projects/couchpilot).

## Observed browser results

| Journey | Result |
|---|---|
| Open from the portfolio's CouchPilot card | Published page, chapter controls and evaluation loaded |
| Start the original lesson | Video played; duration 120 seconds; no media error |
| Request assignment check plus phone card | Review showed two actions sourced to 00:40; playback stayed unchanged until approval |
| Apply reviewed actions | Player moved to 40 seconds and the assignment companion card appeared |
| Undo the jump | Player returned to its previous position, 0 seconds |
| Open companion link | Assignment excerpt and 40–60 second source range appeared |
| Return from the companion | Player initialized at 40 seconds |
| Inspect public evaluation | Displayed rules 11/12, local model 9/12 and one wrong-seek proposal |

The screenshot is an unedited capture of the deployed page, not a design mockup.

## Limits of this verification

These observations are a desktop browser smoke check, not a cross-device usability study. No physical TV, phone camera scan, screen reader or microphone permission was exercised. The companion hyperlink was tested; QR decoding on physical devices remains unverified. The deployed app uses the deterministic rules baseline. The local-model evaluation and its failures are recorded separately in `evaluation/`. Passing engineering tests does not establish model quality, user value or production readiness.
