# Pollax SDK

Official TypeScript and Python client libraries for the [Pollax](https://pollax.ai) AI Voice Platform.

[![npm version](https://img.shields.io/npm/v/pollax.svg)](https://www.npmjs.com/package/pollax)
[![PyPI version](https://img.shields.io/pypi/v/pollax.svg)](https://pypi.org/project/pollax/)
[![CI](https://github.com/Pollax-ai/Pollax-SDK/actions/workflows/ci.yml/badge.svg)](https://github.com/Pollax-ai/Pollax-SDK/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

## Install

```bash
# TypeScript / JavaScript
npm install pollax

# Python 3.8+
pip install pollax
```

Go SDK: **coming soon** (not published yet).

## Auth

Create an API key in the Pollax dashboard, then:

```typescript
import { Pollax } from 'pollax';

const pollax = new Pollax({
  apiKey: process.env.POLLAX_API_KEY!, // e.g. sk_test_...
});
```

```python
import os
from pollax import Pollax

pollax = Pollax(api_key=os.environ['POLLAX_API_KEY'])
```

Never commit live keys. See [SECURITY.md](./SECURITY.md).

## Quick start

### TypeScript

```typescript
import { Pollax } from 'pollax';

const pollax = new Pollax({ apiKey: process.env.POLLAX_API_KEY! });

const agent = await pollax.agents.create({
  name: 'Customer Support Agent',
  system_prompt: 'You are a helpful customer support agent.',
  voice_id: 'alloy',
  model: 'gpt-4',
});

const call = await pollax.calls.create({
  agent_id: agent.id,
  to_number: '+1234567890',
});

console.log('Call initiated:', call.call_sid);
```

### Python

```python
import os
from pollax import Pollax

pollax = Pollax(api_key=os.environ['POLLAX_API_KEY'])

agent = pollax.agents.create(
    name='Customer Support Agent',
    system_prompt='You are a helpful customer support agent.',
    voice_id='alloy',
    model='gpt-4',
)

call = pollax.calls.create(
    agent_id=agent.id,
    to_number='+1234567890',
)

print(f'Call initiated: {call.call_sid}')
```

## Resources (1.3+)

| Resource | Examples |
|----------|----------|
| `agents` | create, list, update, `setKnowledgeBaseIds` |
| `calls` | create, list, listPage, transfer, `listTransfers`, `broadcastHistory`, `getAnalysis` |
| `campaigns` | create, list, start/pause/resume/complete, `listCallLines`, `rerun`, `previewContacts` |
| `knowledge` | create (text), upload, `uploadFile`, `addUrl`, search, stats |
| `phoneNumbers` | list, search, purchase, assign/unassign, provision/deprovision, number request |
| `wallet` | get balance, ledger |
| `tts` | `broadcastPreview` |
| `webhooks` | subscriptions + `Pollax.verifyWebhookSignature` |

## Personalizing calls with variables

```typescript
const call = await pollax.calls.create({
  agent_id: agent.id,
  to_number: '+1234567890',
  variables: {
    contact_name: 'Alex',
    amount_due: '120',
    due_date: '2025-07-01',
  },
});
```

Use `{{contact_name}}` in agent system prompts / welcome messages. Use `{contact_name}` in one-way `announcement_message`.

## Versioning

This project follows [Semantic Versioning](https://semver.org/):

- **MAJOR** — breaking API or type changes
- **MINOR** — new methods / endpoints (backward compatible)
- **PATCH** — bug fixes and docs

See [CHANGELOG.md](./CHANGELOG.md) and [docs/migration.md](./docs/migration.md).

## Documentation

- [Quick start](./docs/quickstart.md)
- [API reference](./docs/api-reference.md)
- [Migration (1.2 → 1.3)](./docs/migration.md)
- [Best practices](./docs/best-practices.md)
- [Examples](./examples)
- [Contributing](./CONTRIBUTING.md)
- [Security](./SECURITY.md)
- [Code of Conduct](./CODE_OF_CONDUCT.md)

## Support

- Email: [support@pollax.ai](mailto:support@pollax.ai)
- Issues: [github.com/Pollax-ai/Pollax-SDK/issues](https://github.com/Pollax-ai/Pollax-SDK/issues)

## License

MIT — see [LICENSE](./LICENSE).
