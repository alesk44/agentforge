# Alesk Hub (preview)

A separate mobile-first PWA shell for organizing email, cloud drives, calendars and work follow-ups.

## Current honest status
- UI and navigation are local/static.
- No provider is connected; no OAuth client or secure backend is configured.
- No email is fetched or sent; no files are read, moved, uploaded or deleted.
- Calendar items are not fetched or created.
- Drafts and follow-ups are session-only.
- Assistant prompts are a UI preview, not live AI.

## Deploy without Replit
This folder is served as a subpath by the existing GitHub Pages deployment for AgentForge, when that repository's Pages workflow is enabled. Expected path: `https://alesk44.github.io/agentforge/hub/`.

## Before connecting real accounts
1. Configure a separate secure backend and OAuth applications for each provider.
2. Use server-side authorization-code flow with PKCE/state validation and least-privilege scopes.
3. Store refresh tokens only in encrypted server-side storage; never in browser code or Git.
4. Implement per-user access controls, revocation, audit logging and explicit confirmation for send/delete/share/calendar writes.
5. Complete provider verification and test with dedicated accounts.

## Install
Open the HTTPS page on Android Chrome, menu ⋮ → Add to Home screen / Install app. iPhone Safari: Share → Add to Home Screen.
