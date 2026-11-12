# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 1.3.x   | Yes |
| 1.2.x   | Yes (security fixes only) |
| < 1.2   | No |

## Reporting a vulnerability

Do **not** open a public GitHub issue for security vulnerabilities.

Please report privately via one of:

1. [GitHub Security Advisories](https://github.com/Pollax-ai/Pollax-SDK/security/advisories/new) for this repository
2. Email: **security@pollax.ai**

Include:

- Affected package (`pollax` npm / PyPI) and version
- Description of the issue and impact
- Reproduction steps or proof of concept (if safe to share)
- Any suggested fix

We aim to acknowledge reports within **2 business days** and to provide a remediation timeline after triage.

## Safe usage

- Never commit API keys (`sk_live_…`, `sk_test_…`) to source control
- Prefer environment variables or a secrets manager
- Rotate keys immediately if exposure is suspected
- Verify webhook signatures with `Pollax.verifyWebhookSignature` / `Pollax.verify_webhook_signature` before trusting event payloads
