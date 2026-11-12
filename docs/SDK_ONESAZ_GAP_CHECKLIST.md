# Pollax SDK gap checklist (Onesaz path B)

Goal: Onesaz `admin-server` voice layer can drop raw axios and call **SDK only**.
Baseline: SDK **1.2.0**. Target: **1.3.0** (this expansion).

Status: `DONE` = shipped in 1.3.0 · `PARTIAL` = method existed but incomplete · `N/A` = Onesaz-only (no SDK needed)

---

## Legend

| Column | Meaning |
|--------|---------|
| Onesaz | Function / call site in `admin-server/app/voice/voice.service.js` |
| HTTP | Pollax API path (relative to `/api/v1`) |
| SDK 1.2 | Prior coverage |
| SDK 1.3 | Method to use after expansion |

---

## 1. Wallet (was missing entirely)

| Onesaz | HTTP | SDK 1.2 | SDK 1.3 method | Status |
|--------|------|---------|----------------|--------|
| `getWalletBalance` | `GET /wallet` | — | `wallet.get()` / `wallet.retrieve()` | DONE |
| `getWalletLedger` | `GET /wallet/ledger?limit=` | — | `wallet.ledger({ limit })` | DONE |

---

## 2. Phone numbers

| Onesaz | HTTP | SDK 1.2 | SDK 1.3 method | Status |
|--------|------|---------|----------------|--------|
| `listPhoneNumbers` | `GET /phone-numbers` | `phoneNumbers.list` | same | DONE (already) |
| `searchPhoneNumbers` | `GET /phone-numbers/search` | `phoneNumbers.search` | same (+ unwrap `{ numbers }`) | DONE |
| `purchasePhoneNumber` | `POST /phone-numbers` | `phoneNumbers.purchase` | same | DONE (already) |
| release | `DELETE /phone-numbers/:id` | `phoneNumbers.release` | same | DONE (already) |
| `getNumberRequest` | `GET /phone-numbers/number-request` | — | `phoneNumbers.getNumberRequest()` | DONE |
| `requestNumber` | `POST /phone-numbers/number-request` | — | `phoneNumbers.requestNumber(body)` | DONE |
| `setNumberAutoRenew` | `PUT /phone-numbers/:id` `{ auto_renew }` | — | `phoneNumbers.update(id, { auto_renew })` | DONE |
| `assignPhoneNumber` | `POST /phone-numbers/:id/assign` | — | `phoneNumbers.assign(id, { agent_id })` | DONE |
| unassign | `POST /phone-numbers/:id/unassign` | — | `phoneNumbers.unassign(id)` | DONE |
| `setInboundProvisioning` on | `POST /phone-numbers/:id/provision` | — | `phoneNumbers.provision(id, body?)` | DONE |
| `setInboundProvisioning` off | `POST /phone-numbers/:id/deprovision` | — | `phoneNumbers.deprovision(id)` | DONE |

---

## 3. Knowledge

| Onesaz | HTTP | SDK 1.2 | SDK 1.3 method | Status |
|--------|------|---------|----------------|--------|
| `listKnowledge` | `GET /knowledge` | `knowledge.list` | same | DONE (already) |
| `getKnowledge` | `GET /knowledge/:id` | `knowledge.retrieve` | same (returns `content`) | DONE (already) |
| `deleteKnowledge` | `DELETE /knowledge/:id` | `knowledge.delete` | same | DONE (already) |
| `searchKnowledge` | `POST /knowledge/search` | `knowledge.search` | same | DONE (already) |
| `addKnowledgeText` | `POST /knowledge` JSON `{ name, content, type }` | upload only (multipart) | `knowledge.create({ name, content, type, agent_id? })` | DONE |
| multipart text fallback | `POST /knowledge` multipart | `knowledge.upload` | same | DONE (already) |
| `uploadKnowledgeFile` | `POST /knowledge/upload` | wrong path (`/knowledge`) | `knowledge.uploadFile(file, { agent_id?, name? })` | DONE |
| `addKnowledgeUrl` | `POST /knowledge/url` | — | `knowledge.addUrl({ url, name?, agent_id? })` | DONE |
| `getKnowledgeStats` | `GET /knowledge/stats` | — | `knowledge.stats()` | DONE |

---

## 4. Agents

| Onesaz | HTTP | SDK 1.2 | SDK 1.3 method | Status |
|--------|------|---------|----------------|--------|
| `listAgents` | `GET /agents?is_active=` | `agents.list` | same | DONE (already) |
| `getAgent` | `GET /agents/:id` | `agents.retrieve` | same | DONE (already) |
| bind KB ids | `PUT /agents/:id` `{ knowledge_base_ids }` | `agents.update` (types lacked field) | `agents.update` + `agents.setKnowledgeBaseIds(id, ids)` | DONE |

---

## 5. Calls

| Onesaz | HTTP | SDK 1.2 | SDK 1.3 method | Status |
|--------|------|---------|----------------|--------|
| `createCall` | `POST /calls` | `calls.create` | same | DONE (already) |
| `listCalls` / live logs | `GET /calls` | `calls.list` / `listPage` | same | DONE (already) |
| `getCallDetail` | `GET /calls/:sid` | `calls.retrieve` | same | DONE (already) |
| optional analysis | `GET /calls/:sid/analytics` \| `/analysis` | — | `calls.getAnalysis(sid)` | DONE |
| `listTransfers` | `GET /calls/transfers` | — | `calls.listTransfers(params?)` | DONE |
| `getBroadcastHistory` | `GET /calls/broadcast-history` | — | `calls.broadcastHistory({ limit? })` | DONE |
| end / transfer / transcript / recording | existing | existing | same | DONE (already) |

---

## 6. Campaigns

| Onesaz | HTTP | SDK 1.2 | SDK 1.3 method | Status |
|--------|------|---------|----------------|--------|
| `createCampaign` | `POST /campaigns` | `campaigns.create` | same | DONE (already) |
| `listCampaigns` | `GET /campaigns?status=` | `campaigns.list` (no status) | `campaigns.list({ status? })` | DONE |
| `getCampaignDetail` | `GET /campaigns/:id` | `campaigns.retrieve` | same | DONE (already) |
| call lines | `GET /campaigns/:id/call-lines` | — | `campaigns.listCallLines(id, { limit? })` | DONE |
| `previewCampaignRerun` | `GET /campaigns/:id/rerun-preview` | — | `campaigns.rerunPreview(id, params?)` | DONE |
| `createCampaignRerun` | `POST /campaigns/:id/rerun` | — | `campaigns.rerun(id, body)` | DONE |
| `campaignAction` | `POST /campaigns/:id/{start\|pause\|resume\|complete}` | start/pause/resume/complete | same | DONE (already) |
| contacts preview | `POST /campaigns/contacts/preview` | — | `campaigns.previewContacts(file)` | DONE |
| upload contacts | `POST /campaigns/:id/upload` | `campaigns.uploadContacts` | same | DONE (already) |

---

## 7. TTS / broadcast

| Onesaz | HTTP | SDK 1.2 | SDK 1.3 method | Status |
|--------|------|---------|----------------|--------|
| `previewBroadcast` | `POST /tts/broadcast-preview` | — | `tts.broadcastPreview({ text, language?, speed?, resolved? })` | DONE |

---

## 8. Out of SDK scope (keep in Onesaz)

| Concern | Why N/A |
|---------|---------|
| Per-institute key resolution / Provider Config | CRM multi-tenant store, not Pollax API |
| `VoiceCallModel` persistence / CRM lead notify | Onesaz DB + CRM |
| Cost stripping (`withoutPollaxCost`) | Onesaz product policy |
| Local CSV parse fallback when preview fails | Onesaz resilience |
| Notification-service proxy path | Ops bridge; SDK always uses direct API key |

---

## Onesaz migration map (after publish 1.3.0)

```text
axios GET  /wallet                    →  pollax.wallet.get()
axios GET  /wallet/ledger             →  pollax.wallet.ledger({ limit })
axios GET  /phone-numbers/number-request → pollax.phoneNumbers.getNumberRequest()
axios POST /phone-numbers/number-request → pollax.phoneNumbers.requestNumber(body)
axios PUT  /phone-numbers/:id         →  pollax.phoneNumbers.update(id, { auto_renew })
axios POST /phone-numbers/:id/assign  →  pollax.phoneNumbers.assign(id, { agent_id })
axios POST /phone-numbers/:id/unassign→  pollax.phoneNumbers.unassign(id)
axios POST /phone-numbers/:id/provision → pollax.phoneNumbers.provision(id, body?)
axios POST /phone-numbers/:id/deprovision → pollax.phoneNumbers.deprovision(id)
axios POST /knowledge                 →  pollax.knowledge.create({ name, content, type })
axios POST /knowledge/upload          →  pollax.knowledge.uploadFile(file, opts)
axios POST /knowledge/url             →  pollax.knowledge.addUrl({ url, name?, agent_id? })
axios GET  /knowledge/stats           →  pollax.knowledge.stats()
axios PUT  /agents/:id knowledge_base_ids → pollax.agents.setKnowledgeBaseIds(id, ids)
axios GET  /calls/transfers           →  pollax.calls.listTransfers(params)
axios GET  /calls/broadcast-history   →  pollax.calls.broadcastHistory({ limit })
axios GET  /calls/:sid/analytics|analysis → pollax.calls.getAnalysis(sid)
axios GET  /campaigns/:id/call-lines  →  pollax.campaigns.listCallLines(id, { limit })
axios GET  /campaigns/:id/rerun-preview → pollax.campaigns.rerunPreview(id, params)
axios POST /campaigns/:id/rerun       →  pollax.campaigns.rerun(id, body)
axios POST /campaigns/contacts/preview→  pollax.campaigns.previewContacts(file)
axios POST /tts/broadcast-preview     →  pollax.tts.broadcastPreview(params)
```

Python names are snake_case (`phone_numbers`, `set_knowledge_base_ids`, `list_call_lines`, `broadcast_preview`, etc.).

---

## Acceptance for path B (Onesaz)

1. Publish / consume `pollax@1.3.0` (npm) and `pollax==1.3.0` (PyPI) — or git pin until publish.
2. Replace every `pollaxClient*` axios call in `voice.service.js` with SDK methods above.
3. Keep institute key resolution + DB/CRM side-effects outside the SDK.
4. Smoke: wallet, number request/assign/provision, knowledge text+file+url+stats, campaign lines/rerun, transfers, broadcast preview.
