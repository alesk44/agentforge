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

## Authentication preview

- `auth.html` uses Supabase Auth for email/password sign-up, sign-in, password reset and Google OAuth.
- `dashboard.html` requires a signed-in session and allows a user to create/list their own business workspace through RLS.
- The Supabase publishable key is intentionally public; database access must remain protected by RLS. Never put a service-role key in browser code.
- Before testing on GitHub Pages, configure Supabase Auth URL settings: Site URL `https://alesk44.github.io/agentforge/` and allowed redirect URLs `https://alesk44.github.io/agentforge/**`. Enable Google provider and enter Google OAuth credentials only in Supabase Dashboard. Email confirmation delivery may require configuring SMTP.
- These flows have been implemented in code but still require end-to-end browser testing after Pages is live and Auth providers/redirects are configured.

## Next milestones

1. Enable GitHub Pages and configure Supabase Auth redirect/provider settings.
2. Test sign-up, email confirmation, sign-in, Google OAuth, password reset and sign-out.
3. Test tenant isolation with two separate accounts.
4. Add server-side AI provider adapters, usage limits and human approval.
5. Add billing only after pricing, terms and service scope are finalised.

## Self-hosted stack review

See [`docs/SELF_HOSTED_STACK_REVIEW.md`](docs/SELF_HOSTED_STACK_REVIEW.md) for the shortlist, licence cautions, hosting constraints and phased adoption plan.

## Zero-budget note

The current prototype has no paid runtime dependencies. Hosting availability and free-tier limits are controlled by the hosting provider and may change. A production AI service may incur model, database, email or automation costs.

## Licence

MIT. See LICENSE.