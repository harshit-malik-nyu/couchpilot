# Acceptance and traceability

| Need | Implementation | Verification |
|---|---|---|
| Retrieve relevant source | keyword search plus model query planner | retrieval tests and task benchmark |
| Ground action coordinates | canonical segment resolver | unknown/unretrieved source tests |
| No hidden side effects | allowlisted action proposal + UI confirmation | purchase/extra-field rejection; browser review flow |
| Recover from wrong navigation | stored previous playhead | browser undo check |
| Model outage is visible | error status with no rules fallback | injected connection-error test |
| Cancel pending result | request generation and AbortController | browser cancel check; server may finish inference but UI discards response |
| Share selected source | public companion link + QR | browser card and return-to-timestamp check |
| Test one-time exchange | local pairing store | HTTP, expiry, owner and concurrent-consume tests |
| Compare alternatives | frozen authored cases and reports | recorded v1 failure retained; development iteration labeled |
| Keep prompts private | session events omit raw text | inspect event export schema |

Release-owner and stakeholder assignments are proposed responsibilities, not completed approvals. Real interviews and device acceptance remain outstanding.
