# Voice authorization demo

Use a speaker-authorized provider voice only after the backend has verified consent and vendor eligibility.

```python
from datetime import datetime, timezone
from receptionist.voices import VoiceGrant, VoiceRegistry

approved = VoiceGrant(
    business_id="demo-florist",
    speaker_id="speaker-demo",
    provider="example-provider",
    voice_id="voice-demo",
    purpose="inbound_receptionist",
    consent_reference="private-consent-record",
    consent_verified=True,
    provider_verified=True,
)
registry = VoiceRegistry((approved,))
print(registry.select(
    business_id="demo-florist",
    voice_id="voice-demo",
    purpose="inbound_receptionist",
    now=datetime.now(timezone.utc),
))
```

**This is only a policy demonstration.** A production service must prevent untrusted callers from setting the verified fields, persist status in a secure database, review voice-owner proof and use provider APIs to manage actual custom voices.
