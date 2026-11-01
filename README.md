# AgentForge

A lightweight, responsive landing page and interactive prototype for an AI workflow service aimed at small businesses.

## Current status

**Prototype / preview only.** The agent cards show deterministic sample outputs. They do not call an AI model, browse the web, send messages, store leads, or trigger external actions. The enquiry form validates in the browser but does not transmit or retain submissions.

## Run locally

Open index.html in a browser. No package installation or build step is required.

## Deploy free with GitHub Pages

1. In the repository, open **Settings → Pages**.
2. Under **Build and deployment**, choose **GitHub Actions**.
3. Push to main. The included workflow publishes the static site.
4. The project URL will be https://alesk44.github.io/agentforge/ once Pages is enabled and the workflow succeeds.

## Product direction

- English-first with a French language toggle.
- GBP indicative pricing; no checkout is connected.
- Human review before external communications or actions.
- Integration adapters should be added only after the relevant service and credentials are configured.
- Never expose API keys in browser code.

## Next milestones

1. Verify GitHub Pages deployment and mobile layout.
2. Add a secure backend and authentication.
3. Add tenant-scoped data, consent, rate limits and audit logs.
4. Connect one real AI workflow behind a server-side adapter.
5. Add billing only after pricing, terms and service scope are finalised.

## Zero-budget note

The current prototype has no paid runtime dependencies. Hosting availability and free-tier limits are controlled by the hosting provider and may change. A production AI service may incur model, database, email or automation costs.

## Licence

MIT. See LICENSE.