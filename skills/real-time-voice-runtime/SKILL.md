---
name: real-time-voice-runtime
description: Integrate an approved voice into a low-latency AI receptionist call with interruption handling, backpressure, fallback, and tool execution.
---
# Real-time voice runtime

**Trigger:** Incoming phone/SIP/WebRTC call after business routing is configured and a provider adapter has been implemented.

## Responsibilities

- Connect transport (PSTN/SIP/WebRTC) to either an end-to-end speech-to-speech model **or** ASR → LLM/tool gateway → streaming TTS. These are alternative pipelines.
- Stream media without leaking API keys to browsers or telephone clients.
- Disclose AI identity in the first response before normal business actions; manage any separate recording notice and consent.
- Select the configured catalog or **approved** custom voice at session creation via the server-side voice registry.
- Support barge-in and cancellation: stop queued audio, truncate interrupted responses where supported, and resume from the latest confirmed state. Don't double-book on retries.
- Route tools to the authenticated, deterministic domain API. Natural language output cannot stand in for calendar/SMS/transfer results.
- Support jitter buffers, timeouts, media reconnect, bounded queues and independent call cancellation.
- Avoid storing raw recordings/transcripts unless explicitly enabled under an approved retention/consent policy.

## Inputs

`call_id`, `business_id`, `language`, approved voice registry selection, authorized backend session token, transport capabilities and policy profile.

## Architecture

```text
Caller ⇄ PSTN / SIP ⇄ Voice transport
                         ⇅ audio + events
                      Runtime adapter
                     /             \
      Speech-to-speech model    ASR→LLM→TTS
                     \             /
                   Policy + tool gateway
                        ⇅
           Verified business tools + handoff
```

## State machine

`NEW → DISCLOSING → ACTIVE → (INTERRUPTED | WAITING_TOOL | ESCALATING) → ENDING → CLOSED`

`CLOSED` is terminal; cancelled audio must never restart. Handle provider-specific transcripts as provisional until final. Voice changes may require new sessions.

## Practical acceptance gates

- First audio contains truthful AI disclosure; separate consent gate applied if recording.
- Every booking is committed through confirmed, idempotent backend action, not speech generation.
- Interruptions suppress old speech chunks; obsolete tool responses do not trigger unwanted actions.
- Invalid voice license / revoked consent → no cloned audio.
- p50/p95 time-to-first-audio, end-to-end turn latency, dropped frames, interruptions, handoff completion and quality are measured in a consented pilot. **No target is claimed measured by this repository.**
- Webhook signatures, replay protection, tenant authorization and transfer allowlist all implemented before live deployment.

## Provider-specific notes

- [ElevenLabs streaming TTS](https://elevenlabs.io/docs/eleven-api/guides/how-to/websockets/realtime-tts): select supported model for the WebSocket endpoint; not all models support `stream-input`.
- [OpenAI Realtime voice events](https://developers.openai.com/api/docs/guides/realtime-conversations): builtin voices and eligible custom voices are configured at session initialization. Treat provider availability as versioned.
- Never hardcode any provider-specific voice ID or production credential in these portable skills.
