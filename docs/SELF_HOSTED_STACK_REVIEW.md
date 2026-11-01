# AgentForge — revue Awesome Selfhosted

Date de revue : 2026-11-01

## Périmètre et méthode

Revue ciblée des catégories pertinentes du catalogue Awesome Selfhosted : GenAI, Automation, CRM, Ticketing, Search Engines, Email/Newsletters, Low Code, CI/CD, Testing, Monitoring, Authentication, Booking/Scheduling, Analytics et Resource Planning. Le catalogue est un index communautaire très vaste, pas une garantie de sécurité, de maintenance, de coût nul ni de compatibilité commerciale. Cette note n'affirme pas que chaque entrée du catalogue a été auditée individuellement.

Sources de départ :
- https://awesome-selfhosted.net/
- https://awesome-selfhosted.net/tags/generative-artificial-intelligence-genai.html
- https://awesome-selfhosted.net/tags/automation.html
- https://awesome-selfhosted.net/tags/customer-relationship-management-crm.html
- https://awesome-selfhosted.net/tags/ticketing.html
- https://awesome-selfhosted.net/tags/search-engines.html
- https://awesome-selfhosted.net/tags/software-development---low-code.html
- https://awesome-selfhosted.net/tags/software-development---testing.html
- https://sysadmin.awesome-selfhosted.net/tags/continuous-integration--continuous-deployment.html

## Décision d'architecture

AgentForge doit rester le produit principal (interface, comptes, abonnements, données clients, autorisations et expérience des agents). Les logiciels tiers sont des moteurs/adaptateurs facultatifs, pas des dépendances qui remplacent le produit.

Socle actuel conservé :
- Frontend statique du dépôt GitHub Pages tant que le déploiement est validé.
- Supabase indépendant `agentforge` pour Auth, PostgreSQL et RLS.
- API/Edge Functions côté serveur pour les opérations privilégiées et les appels aux modèles.
- Secrets exclusivement côté serveur. Ne jamais publier de service-role key, jeton fournisseur ou mot de passe dans le navigateur ou Git.

## Shortlist

| Domaine | Projet | Licence listée | Décision |
|---|---|---|---|
| Agents/RAG | AnythingLLM | MIT | POC local plus tard; candidat moteur documentaire/agent, pas une dépendance immédiate |
| Inférence locale | Ollama | MIT | Option pour machine dédiée; pas une API publique gratuite sans matériel/serveur |
| Inférence locale | LocalAI | MIT | Alternative à évaluer seulement si besoin concret |
| Automatisation | Activepieces | MIT pour le core; fonctionnalités Enterprise sous licence commerciale | Candidat pour workflows internes; vérifier chaque fonctionnalité et licence avant toute intégration SaaS multi-tenant |
| Surveillance web | changedetection.io | Apache-2.0 | Bon candidat pour un agent de veille/alertes, sous réserve des conditions des sites surveillés |
| Recherche plein texte | Meilisearch | MIT | Plus tard, seulement si PostgreSQL full-text ne suffit plus |
| CRM externe | Twenty | AGPL-3.0 | Ne pas intégrer au lancement; préférer le CRM minimal interne |
| CRM externe | EspoCRM | AGPL-3.0 | Alternative, même réserve licence/intégration |
| Support | Zammad | AGPL-3.0 | Phase ultérieure; pas nécessaire au MVP |
| Support | Libredesk | AGPL-3.0 | À comparer à Zammad si le volume le justifie |
| Email marketing | Listmonk | AGPL-3.0 | Plus tard; nécessite un fournisseur SMTP et gestion du consentement/désinscription |
| Marketing automation | Mautic | GPL-3.0 | Trop lourd pour le MVP |
| Admin interne | Appsmith | Apache-2.0 | Option pour outils d'administration internes, non requis |
| CI/CD | Woodpecker | Apache-2.0 | Pas nécessaire tant que GitHub Actions suffit |
| Tests | WebHook Tester / Request Inbox | MIT / Apache-2.0 listées | Outils ponctuels de QA, pas une dépendance de production |
| Statut/monitoring | Uptime Kuma | MIT | Option utile lorsque l'app a un endpoint public et un hébergement stable |
| Recherche web | SearXNG | AGPL-3.0, anti-features signalées dans le catalogue | Ne pas l'utiliser sans examen de ses anti-features, de la fiabilité et des conditions des moteurs sources |

Les licences ci-dessus sont celles affichées par le catalogue ou la documentation consultée; il faut contrôler le dépôt, les dépendances, les modules Enterprise et les conditions d'hébergement au moment de chaque adoption. AGPL/GPL n'interdisent pas automatiquement une activité commerciale, mais imposent des obligations qui nécessitent une revue juridique adaptée.

## Attention aux licences et au modèle SaaS

- Activepieces indique que son core est MIT, mais que les fonctions Enterprise/Cloud sont sous licence commerciale. Les fonctionnalités Enterprise incluent notamment multi-tenancy, SSO, rôles avancés, audit logs, secret managers et builder intégrable. Ne pas bâtir le multi-tenant AgentForge sur ces fonctions sans licence écrite.
- AnythingLLM est annoncé MIT et peut être auto-hébergé avec Docker; un modèle externe peut cependant générer des coûts. Le mode multi-utilisateur nécessite un service serveur Docker.
- Ollama peut fonctionner localement, mais les performances et la concurrence dépendent de la RAM/VRAM et du matériel. Le service public multi-client requiert une machine toujours disponible et sécurisée.
- Les outils Docker ci-dessus ne sont pas déployables directement sur GitHub Pages. Cloudflare Workers gratuits ont des limites de CPU, mémoire, requêtes et temps d'exécution; ce n'est pas un VPS Docker.

## Plan de livraison recommandé

### Maintenant — MVP à coût minimal
1. Terminer l'authentification Supabase (email/mot de passe, vérification d'email, réinitialisation, Google uniquement après configuration OAuth correcte).
2. Mettre les tables métiers derrière RLS et tester avec deux comptes/entreprises distincts.
3. Ajouter des Edge Functions pour créer/exécuter les jobs et appeler un fournisseur IA via une interface d'adaptateur.
4. Enregistrer chaque exécution, statut, consommation et erreur; quotas appliqués côté serveur.
5. Ajouter validation, rate limiting, anti-spam, journaux d'audit et approbation humaine avant toute action externe.
6. Garder les agents démo explicitement étiquetés; pas de fausse exécution réelle.
7. Garder GitHub Actions pour tests et déploiement statique.

### Ensuite — après validation de la demande
1. Tester AnythingLLM et Ollama localement pour comparer qualité/coût sur les cas d'usage AgentForge.
2. Évaluer Activepieces Community pour quelques automatisations internes seulement, sans fonctions Enterprise.
3. Ajouter changedetection.io pour un agent de veille si les sources autorisent l'accès et la fréquence de consultation.
4. Ajouter Uptime Kuma, support client et outil CRM externe seulement lorsque le volume le justifie.
5. Comparer le coût réel d'un petit VPS, sauvegardes, stockage, egress, modèles et maintenance avant toute mise en production.

## Règles de sécurité et d'exploitation

- Aucun conteneur tiers n'a accès directement à la base de production sans rôle dédié et droits minimaux.
- Pas de service-role key dans le frontend.
- Toute donnée client est cloisonnée par utilisateur/entreprise et vérifiée par RLS côté base.
- Webhooks signés, idempotence, limites de fréquence, délais, reprises contrôlées et journalisation.
- Les actions qui envoient un message, modifient un CRM, publient ou dépensent de l'argent exigent une autorisation explicite.
- Vérifier maintenance récente, CVE, images Docker, dépendances, sauvegardes, export et procédure de suppression avant d'héberger un outil.
- « Open source » et « self-hosted » ne signifient pas « gratuit à exploiter » : calcul, stockage, réseau, domaine, e-mail, sauvegardes et temps d'administration restent des coûts.

## Liens de vérification des licences/limites

- Activepieces license: https://www.activepieces.com/docs/about/license
- Activepieces Enterprise license: https://github.com/activepieces/activepieces/blob/main/packages/ee/LICENSE
- AnythingLLM Docker: https://docs.anythingllm.com/installation-docker/overview
- Ollama FAQ: https://github.com/ollama/ollama/blob/main/docs/faq.mdx
- Cloudflare Workers pricing: https://developers.cloudflare.com/workers/platform/pricing/
- Cloudflare Workers limits: https://developers.cloudflare.com/workers/platform/limits/
