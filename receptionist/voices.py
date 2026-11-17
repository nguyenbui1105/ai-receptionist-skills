"""Consent-aware selection of synthetic/clone voice IDs.

Reference domain gate only: does not authenticate speakers, create clones, play
audio, contact providers, or permanently persist an audit trail. A trusted
backend MUST populate records after real verification and approval.
"""
from dataclasses import dataclass
from datetime import datetime, timezone


class VoiceAccessError(ValueError):
    """Voice cannot be selected for this tenant and purpose."""


@dataclass(frozen=True)
class VoiceGrant:
    business_id: str
    speaker_id: str
    provider: str
    voice_id: str
    purpose: str
    consent_reference: str
    consent_verified: bool
    provider_verified: bool
    revoked: bool = False
    expires_at: datetime | None = None

    def __post_init__(self):
        if self.expires_at is not None and (
            self.expires_at.tzinfo is None or self.expires_at.utcoffset() is None
        ):
            raise ValueError("expires_at must be timezone aware")


class VoiceRegistry:
    """Fail-closed in-memory authorization checker. Not a production database."""

    def __init__(self, grants=()):
        self._grants = {g.voice_id: g for g in grants}

    def add_from_trusted_backend(self, grant: VoiceGrant) -> None:
        """Only a verified backend should call this function."""
        if not grant.voice_id or not grant.business_id:
            raise VoiceAccessError("Voice ID and business are required")
        self._grants[grant.voice_id] = grant

    def revoke(self, voice_id: str) -> None:
        from dataclasses import replace
        if voice_id in self._grants:
            self._grants[voice_id] = replace(self._grants[voice_id], revoked=True)

    def select(self, *, business_id: str, voice_id: str, purpose: str,
               now: datetime | None = None) -> str:
        now = now or datetime.now(timezone.utc)
        if now.tzinfo is None or now.utcoffset() is None:
            raise VoiceAccessError("Current timestamp must be timezone aware")
        grant = self._grants.get(voice_id)
        if grant is None:
            raise VoiceAccessError("Unknown voice")
        if grant.business_id != business_id or grant.purpose != purpose:
            raise VoiceAccessError("Voice not authorized for this business/purpose")
        if not (grant.consent_verified and grant.provider_verified
                and grant.consent_reference and grant.speaker_id):
            raise VoiceAccessError("Verified speaker consent and provider approval required")
        if grant.revoked:
            raise VoiceAccessError("Voice access revoked")
        if grant.expires_at is not None and now >= grant.expires_at:
            raise VoiceAccessError("Voice consent expired")
        return grant.voice_id
