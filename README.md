> Publication update: the project owner has approved uploading this handoff to GitHub ndthanh/sentimeter on main. Earlier review gates below describe the package review stage. Hosted-site deployment is unchanged.

# Sentimeter — review package

Frontend demo for human-agent collaboration: English UI, Vietnamese audio/transcript, structured AG-UI integration boundary. Includes standalone case investigation and audio-driven call playback.

**Review-only handoff. No GitHub push authorized yet.**

Start here: [HANDOFF.md](HANDOFF.md) (Vietnamese), then [integration/README.md](integration/README.md) and [REVIEW-CHECKLIST.md](REVIEW-CHECKLIST.md).

```sh
python3 -m http.server 4173 --directory dist
# http://localhost:4173
npm test
```

No installation/build or ElevenLabs API key is needed to play the included audio. Python 3 serves files; Node 18+ runs the tests. Only `dist` should be web-served. No live bank or STT connection is included.
