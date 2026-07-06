# Legal-Docs RAG — Document Sync Specification

## Goal

Keep a vector store in sync with the firm's SharePoint document library so the legal
research assistant answers from current documents.

## Corpus

- ~50,000 documents at launch (PDF, DOCX), single SharePoint site, 6 document libraries
- Growth: ~200 new/updated documents per business day, spread across the day
- Deletes are rare (~10/month) but must eventually disappear from search results
- Average document: 15 pages; largest: 400 pages

## Freshness requirement

- Lawyers expect a document uploaded in the morning to be searchable **the same
  business day**. Nobody has asked for minutes-level freshness.
- Deletions must propagate within 7 days (compliance).

## Infrastructure (fixed)

- Self-hosted n8n, **single instance** (no queue mode), shared with 11 other production
  automations — long-running executions have caused missed webhook triggers before
- Azure OpenAI `text-embedding-3-small`, capacity cap **100 requests/min** (shared with
  other projects; raising the cap requires a quota request with unknown lead time)
- SharePoint Online via Microsoft Graph:
  - Graph API throttling: per-app limits, 429s observed during business hours
  - Change notifications (webhooks) require a **public HTTPS endpoint** and
    subscriptions that **expire every ~30 days** and must be renewed
  - Delta query API available per drive (`/delta` endpoint, returns change tokens)
- Vector store: Qdrant, self-hosted on the same VM as n8n (8 GB RAM total)

## Team & operations

- One person (Romuald) builds and operates this alongside client work
- No on-call: if sync breaks Friday night, it may not be noticed until Monday
- Budget-sensitive: Azure credits are sponsored and finite

## Options under consideration

1. **Event-driven**: Graph change notifications → n8n webhook → per-document
   fetch/parse/embed/upsert as changes happen
2. **Nightly batch**: scheduled n8n workflow at 03:00 → delta query per library →
   process changed documents in batches → upsert

## Out of scope

- Chunking strategy and retrieval tuning (decided separately)
- Access control / permission trimming (phase 2)
