import unittest
from dataclasses import replace
from datetime import datetime, timedelta, timezone

from receptionist.voices import VoiceAccessError, VoiceGrant, VoiceRegistry


NOW = datetime(2030, 1, 1, tzinfo=timezone.utc)


class VoiceRegistryTests(unittest.TestCase):
    def setUp(self):
        self.grant = VoiceGrant(
            business_id="demo-florist", speaker_id="speaker-1",
            provider="approved-provider", voice_id="voice-opaque-1",
            purpose="inbound_receptionist", consent_reference="consent-record-1",
            consent_verified=True, provider_verified=True,
            expires_at=NOW + timedelta(days=30),
        )
        self.registry = VoiceRegistry((self.grant,))

    def select(self, **kwargs):
        values = dict(business_id="demo-florist", voice_id="voice-opaque-1",
                      purpose="inbound_receptionist", now=NOW)
        values.update(kwargs)
        return self.registry.select(**values)

    def test_approved_voice(self):
        self.assertEqual(self.select(), "voice-opaque-1")

    def test_wrong_business_denied(self):
        with self.assertRaises(VoiceAccessError):
            self.select(business_id="another-shop")

    def test_wrong_purpose_denied(self):
        with self.assertRaises(VoiceAccessError):
            self.select(purpose="outbound_sales")

    def test_unknown_voice_denied(self):
        with self.assertRaises(VoiceAccessError):
            self.select(voice_id="unknown")

    def test_without_consent_denied(self):
        self.registry.add_from_trusted_backend(replace(self.grant, consent_verified=False))
        with self.assertRaises(VoiceAccessError):
            self.select()

    def test_without_vendor_verification_denied(self):
        self.registry.add_from_trusted_backend(replace(self.grant, provider_verified=False))
        with self.assertRaises(VoiceAccessError):
            self.select()

    def test_without_consent_reference_denied(self):
        self.registry.add_from_trusted_backend(replace(self.grant, consent_reference=""))
        with self.assertRaises(VoiceAccessError):
            self.select()

    def test_revoked_denied(self):
        self.registry.revoke("voice-opaque-1")
        with self.assertRaises(VoiceAccessError):
            self.select()

    def test_expired_denied(self):
        with self.assertRaises(VoiceAccessError):
            self.select(now=NOW + timedelta(days=31))

    def test_naive_expiration_rejected(self):
        with self.assertRaises(ValueError):
            replace(self.grant, expires_at=datetime(2030, 1, 2))

    def test_naive_now_rejected(self):
        with self.assertRaises(VoiceAccessError):
            self.select(now=datetime(2030, 1, 1))


if __name__ == "__main__":
    unittest.main()
