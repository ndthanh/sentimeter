> Historical planning document. Current behavior and integration limits are documented in ../HANDOFF.md. Audio has been generated and integrated.

# Audio-driven call demo — pending script approval

UI remains English. Spoken dialogue is Vietnamese, with two female voices selected by the user: a calm, clear operator and a natural customer who is initially concerned. The script contains fictional DOB/ID values matching the customer profile. No API calls or audio generation have been performed.

## Interaction state machine
1. Incoming call: customer-profile ring animation, name/registered number and Accept call. Optional synthesized local ringtone; browser audio starts only after a user gesture. No verification or investigation yet.
2. Accept call: stop ringing and play `verification`. The customer’s statement alone does not verify identity. At the end of the operator’s explicit DOB confirmation, show DOB Verified. At the end of her national-ID confirmation, show ID Verified and identity complete.
3. Play `request`. On completion of the customer’s request, populate business labels sequentially: 12 Techcombank Rewards, 11 Points enquiry support, supplied L3 reversal/cancellation label; L4 remains not supplied. Show a classification note that L3 needs confirmation for this failed-transaction case. Do not invent an Item/code.
4. After the customer agrees to wait, enable Hold call and pause conversation. Wait for the operator click; do not automatically hold.
5. Hold click: start hold timer and agent run. Execute T24 → FIMI → Programme Terms → MCC Reference → IDO → Rewards Portal. Cards update from AG-UI events. No investigations occur before this point in the new flow.
6. Once all required checks succeed: display recommended answer and follow-up solution; enable Resume call. If a lookup fails, show retry/incomplete state and do not manufacture a recommendation.
7. Resume click: stop hold timer and play `resolution`. After the customer authorizes a follow-up, enable Register follow-up and pause before the operator’s next statement until the operator registers the mock request. The UI must not say an actual external request succeeded unless the backend confirms it.
8. End of closing line: call completed; permit reset/replay. Reset cancels audio, cues, lookup timers and pending run; late events must be ignored.

## Synchronization
Use generated `voice_segments[].dialogue_input_index` to map transcript turns to audio times. Drive highlights and cue dispatch from HTMLAudioElement.currentTime, seeking/ended events and an exactly-once cue ledger. Do not keep the old 4× wall-clock playback for spoken audio. Gate transitions wait for actual operator actions. Process the final cue on ended even if timeupdate skipped it. Prevent duplicate playback/Accept/Hold clicks and duplicate events. Keep media time separate from actual call/hold time. Pause all demo clocks during presenter pause or buffering; preserve the current audio position. Verify generated dialogue has no unwanted overlap at action boundaries; split the affected audio block if needed.

Only validated observable agent state should drive UI. Verification indicator in this mock is an operator-confirmation event, not a voice biometric check. Real verification remains server-authoritative.

## Hold budget
Do not retain the old 45-second hold by assumption: the new recorded conversation will have a different length. After generation, measure the non-hold dialogue duration D. To meet H/(D+H) <= 20%, choose H <= D/4, also <=60 seconds and max 2 holds. Target one short 15–25-second mock investigation only if the measured duration permits it. Actual presenter delays on hold count; show warnings and allow Resume even if analysis is still running rather than trapping the customer on hold. UI should distinguish current ratio from projected final ratio. Do not pad dialogue just to make a metric pass.

## Delivery phases
A. Approve Vietnamese script and settle classification note/L4.
B. Select two female Vietnamese voice IDs. Store key in local environment only; never add it to browser JS or a repository.
C. Generate three timestamped dialogue blocks with the provided script, then review pronunciation of Trip.com, dates, ID digits, amounts and points.
D. Wire ring/Accept/Hold/Resume controls and the cue engine. Replace old automatic lookup timing with hold-gated AG-UI mock runs.
E. Load audio and manifest as static assets; no ElevenLabs API key or API calls from the published frontend. Update transcript UI for Vietnamese speech, with optional English translation separately labelled.
F. Verify accept gate, both verification cues, ordered breadcrumb updates, no lookup before Hold, full checklist before answer, no resolution audio before Resume, follow-up confirmation, buffering, replay, late-event rejection and hold policy. Publish updated interaction after review.

## Generator
Python 3 standard library only. Offline preview:

    python3 audio-plan/generate_audio.py

It prints the exact SHA256 and request sizes; it does not access ElevenLabs. After human approval of that exact script, configure these environment variables securely on the local machine:

- ELEVENLABS_API_KEY
- ELEVENLABS_OPERATOR_VOICE_ID
- ELEVENLABS_CUSTOMER_VOICE_ID

Then run (replace placeholder with approved SHA printed by the dry run):

    python3 audio-plan/generate_audio.py --generate --approved-sha256 APPROVED_SCRIPT_SHA256

Output: MP3 blocks, raw timestamp metadata and `generated/manifest.json`. Existing matching generations are reused. There are no automatic paid retries. The hash option is a guard against accidentally generating a changed script, not a substitute for human approval. Two female Vietnamese voices must be selected by listening to samples; a voice ID alone does not validate gender/language quality.

Endpoint: https://api.elevenlabs.io/v1/text-to-dialogue/with-timestamps
Documentation: https://elevenlabs.io/docs/api-reference/text-to-dialogue/convert-with-timestamps
Model: eleven_v3; language_code vi; two voice IDs; each request kept below 2,000 characters. Response contains audio_base64 and voice_segments with input indices and time ranges. Generation and timing quality are not yet API-tested.
