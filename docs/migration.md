# Migration guide: 1.2 → 1.3

Pollax SDK **1.3.0** expands the client so integrators (including Onesaz) can call the public API without raw HTTP for wallet, phone ops, knowledge ingest, campaign reruns, transfers, and TTS preview.

## Install

```bash
npm install pollax@^1.3.0
# or
pip install "pollax>=1.3.0"
```

## New resources

### Wallet

```ts
const bal = await pollax.wallet.get();
const ledger = await pollax.wallet.ledger({ limit: 50 });
```

```python
bal = pollax.wallet.get()
ledger = pollax.wallet.ledger(limit=50)
```

### TTS

```ts
await pollax.tts.broadcastPreview({ text: 'Hello', language: 'hi', speed: 1 });
```

```python
pollax.tts.broadcast_preview(text='Hello', language='hi', speed=1)
```

## Expanded methods

| Area | New methods (TS) | Python |
|------|------------------|--------|
| Phone | `getNumberRequest`, `requestNumber`, `update`, `assign`, `unassign`, `provision`, `deprovision` | snake_case equivalents |
| Knowledge | `create`, `uploadFile`, `addUrl`, `stats` | `create`, `upload_file`, `add_url`, `stats` |
| Agents | `setKnowledgeBaseIds` | `set_knowledge_base_ids` |
| Calls | `listTransfers`, `broadcastHistory`, `getAnalysis` | `list_transfers`, `broadcast_history`, `get_analysis` |
| Campaigns | `list({ status })`, `listCallLines`, `rerunPreview`, `rerun`, `previewContacts` | snake_case equivalents |

## Breaking changes

None intended for 1.3.0. Existing 1.2 call sites (`agents`, `calls.create`, `campaigns.create`, `knowledge.upload` → `POST /knowledge`) keep working.

Note: prefer `knowledge.uploadFile` for the binary `POST /knowledge/upload` path; `knowledge.upload` still posts multipart to `/knowledge`.

## Onesaz / multi-tenant apps

Keep institute API-key resolution and CRM/DB side-effects outside the SDK. Construct one client per request:

```ts
const pollax = new Pollax({
  apiKey: instituteKey,
  baseURL: process.env.POLLAX_API_URL || 'https://api.pollax.ai',
});
```

See [SDK_ONESAZ_GAP_CHECKLIST.md](./SDK_ONESAZ_GAP_CHECKLIST.md) for the full method ↔ endpoint map.
