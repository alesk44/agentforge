# Security notes

- Treat this repository as a public client application: never commit API keys, passwords, service-role keys or private tokens.
- Keep AI provider credentials and privileged Supabase credentials in server-side environment secrets only.
- Enforce tenant ownership with Supabase Row Level Security (RLS); never rely on hidden UI controls as authorization.
- Outbound email, messages, purchases and other external actions require explicit human review.
- Validate and rate-limit all public endpoints; add spam protection before enabling lead capture.
- The current website is a static prototype. Its sample agent responses are illustrative and no personal data is submitted or persisted.
- Do not connect this schema to the existing Marée Jersey database. AgentForge requires its own project/database.

Before production: review policies, add auth flows, test cross-tenant isolation, configure backups/retention, and complete privacy/terms disclosures.