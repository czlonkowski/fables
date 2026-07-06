# DRAFT — n8n migration: SQLite → Postgres

Production instance: n8n.example-client.pl (Docker Compose, Caddy proxy).
~200 active workflows (client automations: invoicing, CRM sync, alerting).
Window: Saturday 02:00–04:00 (agreed with client, max 2h downtime).

## Steps

1. **01:45** — Announce maintenance in the client Slack channel.
2. **02:00** — Pull the new images:
   `docker compose pull`
3. **02:05** — Export the SQLite data:
   `docker compose exec n8n n8n export:workflow --all --output=/backup/workflows.json`
   `docker compose exec n8n n8n export:credentials --all --output=/backup/credentials.json`
4. **02:15** — Provision Postgres:
   - Add `postgres:16` service to docker-compose.yml (volume `pgdata`)
   - Create DB `n8n`, user `n8n`, strong password in `.env`
5. **02:25** — Point n8n at Postgres:
   - Set `DB_TYPE=postgresdb`, `DB_POSTGRESDB_HOST=postgres`, etc. in `.env`
6. **02:30** — Start the stack:
   `docker compose up -d` (n8n runs its schema migrations on first boot)
7. **02:40** — Import the data:
   `docker compose exec n8n n8n import:workflow --input=/backup/workflows.json`
   `docker compose exec n8n n8n import:credentials --input=/backup/credentials.json`
8. **02:50** — Smoke test: open the UI, check the workflow list loads, run one
   manual test execution of the invoicing workflow.
9. **03:00** — Announce completion in Slack. Done — one hour of buffer to spare.

## Notes

- The old SQLite file stays inside the old volume, so we can always look at it later
  if something seems off.
- Execution history doesn't migrate with export/import — acceptable, client agreed
  history can start fresh.
