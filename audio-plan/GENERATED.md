# Generated trial audio

Three dialogue blocks generated from the user-approved script using Quynh (operator) and Chi (customer). Both have Vietnamese, northern, young, female library labels. Key never copied into project source or output.

Audio durations: verification 36.362s; request 35.318s; resolution 70.609s. Total 142.289s, excluding hold. 19 timed turns validated, no timestamp overlaps or out-of-range turns. Perceptual accuracy/accent not yet verified by listening.

Use generated/playback-manifest.json and the numbered MP3 files. Dispatch ui_cues only; turn on_end arrays are cleared to avoid duplicates. Verification cues are located using character alignment at the end of the operator confirmation sentence: DOB 16.96s; National ID and identity complete 31.68s (relative to verification.mp3). Hold enabled at request 33.76s. Follow-up enabled at resolution 50.8s; pause before the next turn until the operator registers it.

Use HTMLAudioElement.currentTime with requestAnimationFrame while playing, plus ended/seek handling and an exactly-once ledger. Do not drive cues with setTimeout or the old 4x demo clock. Browser scheduling and alignment quality must be measured, not assumed. The clips are wired into the UI. Runtime copies are in dist/audio/quynh-chi; the second pair is in dist/audio/oanh-thao-linh.

One 20-second hold gives approximately 12.3% of the final 162.3-second call. The maximum based solely on generated speech duration is 35.57 seconds for a 20% final ratio; actual operator waiting affects the denominator. Check the in-call ratio too.
