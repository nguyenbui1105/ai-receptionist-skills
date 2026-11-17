# Contributing to ReceptionistOS

Thank you for helping make voice agents more dependable.

## Development workflow

1. Fork and create a focused feature branch.
2. Use Python 3.11+, run `python -m unittest discover -s tests -v`.
3. Keep each skill's `SKILL.md` self-contained: trigger, inputs, instructions, fallback and acceptance checks.
4. Write a regression test for any new business action or failure scenario.
5. Submit a PR summarizing impact, tests and any legal/security concerns.

## Project principles

- No real customer PII, recordings, tokens or VINs in commits, issues or tests.
- Do not confuse an offline prototype with a production telephony integration.
- Preserve explicit caller confirmation and truthful result reporting.
- Cite official provider docs for integration-specific assumptions.
- Treat recording, AI disclosure, SMS and outbound-calling regulations as deployment-dependent.

Good first issues: calendar concurrency, signed webhooks, interruption tests, multi-language evaluations, and a consent-gated SMS mock.

Contributions are licensed under MIT.
