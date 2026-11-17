---
name: voice-cloning
description: Create and manage a custom receptionist voice only when the speaker has authorized its exact business use; enforce provider verification, revocation and honest AI disclosure.
---
# Voice cloning — consent-gated

**Trigger:** A business owner asks to use a distinctive, custom voice for the receptionist. **Not** required for the standard synthetic-voice path.

## Safety and authorization contract

- Never clone a voice from a customer call, social clip, voicemail, celebrity recording, or scraped audio without the actual speaker's explicit permission and provider-compliant identity verification.
- The person whose voice is being replicated must authorize **the exact voice likeness, business, purpose, providers and deployment context**. A business owner's permission is not sufficient when another person owns the voice.
- A verified consent record is required **before** enabling a cloned voice. Keep evidence privately, not in GitHub or prompts. Verify that the vendor allows the intended voice and usage.
- **ElevenLabs Professional Voice Cloning:** The voice owner must create and verify their own PVC; third-party cloning is not available via this mode, even with consent. For a business, ask the owner to share it through provider-supported sharing.
- **OpenAI recorded custom voices:** Requires eligible project access, a consent recording and sample recording from the same speaker; do not assume availability. Prompt-generated voices are a separate non-cloning path.
- Do not deploy voice likenesses for deception, impersonation, fraud, or claims of a human operator. Receptionist must introduce itself as AI.
- Honor withdrawal of consent immediately: stop using the voice, disable its binding, and initiate vendor-specific deletion/retention requests.

## Inputs

`business_id`, `speaker_id` (pseudonymous), `provider`, `voice_id`, `purpose`, `consent_reference`, `consent_status`, `provider_verification_status`, `expires_at` (optional).

**Never require raw audio, biometric evidence, IDs or API keys in model prompt/tool arguments.** Save them only to an access-controlled service consistent with provider policy.

## Workflow

1. Ask whether an ordinary catalog voice is sufficient. Prefer it when the business does not need a distinct identity.
2. Verify that the intended speaker and provider policy permit this creation method and commercial use; verify the participant's identity using the vendor's official process.
3. Collect *purpose-specific*, informed authorization via a secure mechanism; capture evidence reference, time and withdrawal path.
4. Review sample quality: one speaker, no music, consistent microphone distance, normal pitch/prosody, no confidential information.
5. Submit samples only via the approved provider's current authenticated workflow. Never bypass a verification step.
6. Evaluate language coverage, pronunciation, sound quality, stability, and latency on **consented** samples.
7. Register an opaque provider `voice_id` with consent/verification metadata, enforce tenant scope, then allow a session to select it.
8. Revalidate at session start; select default catalog voice or human handoff if inactive, expired, revoked, missing, or vendor unavailable.
9. On revocation: fail closed; revoke the voice binding, disable active use, and execute documented provider deletion procedures.

## Output

`{voice_id, provider, speaker_id, business_id, consent_reference, status: approved|revoked|expired}`; no raw audio.

## Tests / acceptance criteria

- Missing consent, pending provider verification, mismatched tenant/purpose, expired or revoked status → **no custom voice**.
- No ability to authorize using only a model-generated `consent=true` field.
- Caller hears upfront AI disclosure; caller can request a human.
- Provider outage → documented default synthetic voice (if approved), otherwise human fallback.
- Voice quality and similarity measured with permission; never label a synthetic voice as a human staff member.

## References

- [ElevenLabs voice cloning](https://elevenlabs.io/docs/eleven-creative/voices/voice-cloning/)
- [ElevenLabs PVC verification](https://elevenlabs.io/docs/eleven-api/guides/how-to/voices/professional-voice-cloning)
- [OpenAI custom voices](https://developers.openai.com/api/docs/guides/custom-voices)
