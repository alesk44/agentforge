create extension if not exists pgcrypto;

create or replace function public.set_updated_at()
returns trigger language plpgsql as $$
begin new.updated_at = now(); return new; end;
$$;

create table if not exists public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  display_name text,
  preferred_language text not null default 'en' check (preferred_language in ('en','fr')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.businesses (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null references auth.users(id) on delete cascade,
  name text not null check (char_length(name) between 1 and 160),
  industry text,
  country_code text not null default 'JE',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.plans (
  id text primary key,
  name text not null,
  monthly_price_gbp numeric(8,2) not null check (monthly_price_gbp >= 0),
  workflow_limit integer not null check (workflow_limit >= 0),
  active boolean not null default true,
  created_at timestamptz not null default now()
);

create table if not exists public.agent_runs (
  id uuid primary key default gen_random_uuid(),
  business_id uuid not null references public.businesses(id) on delete cascade,
  agent_key text not null,
  status text not null default 'queued' check (status in ('queued','running','succeeded','failed','cancelled')),
  input_summary text,
  output_summary text,
  model_provider text,
  started_at timestamptz,
  completed_at timestamptz,
  created_at timestamptz not null default now()
);

create table if not exists public.service_requests (
  id uuid primary key default gen_random_uuid(),
  business_id uuid not null references public.businesses(id) on delete cascade,
  request_type text not null,
  description text not null check (char_length(description) between 1 and 5000),
  status text not null default 'new' check (status in ('new','reviewing','in_progress','completed','closed')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.usage_events (
  id uuid primary key default gen_random_uuid(),
  business_id uuid not null references public.businesses(id) on delete cascade,
  event_type text not null,
  quantity numeric(12,3) not null default 1 check (quantity >= 0),
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create index if not exists businesses_owner_id_idx on public.businesses(owner_id);
create index if not exists agent_runs_business_created_idx on public.agent_runs(business_id, created_at desc);
create index if not exists service_requests_business_created_idx on public.service_requests(business_id, created_at desc);
create index if not exists usage_events_business_created_idx on public.usage_events(business_id, created_at desc);

drop trigger if exists profiles_set_updated_at on public.profiles;
create trigger profiles_set_updated_at before update on public.profiles for each row execute function public.set_updated_at();
drop trigger if exists businesses_set_updated_at on public.businesses;
create trigger businesses_set_updated_at before update on public.businesses for each row execute function public.set_updated_at();
drop trigger if exists service_requests_set_updated_at on public.service_requests;
create trigger service_requests_set_updated_at before update on public.service_requests for each row execute function public.set_updated_at();

alter table public.profiles enable row level security;
alter table public.businesses enable row level security;
alter table public.plans enable row level security;
alter table public.agent_runs enable row level security;
alter table public.service_requests enable row level security;
alter table public.usage_events enable row level security;

drop policy if exists profiles_read_own on public.profiles;
create policy profiles_read_own on public.profiles for select to authenticated using (id = auth.uid());
drop policy if exists profiles_insert_own on public.profiles;
create policy profiles_insert_own on public.profiles for insert to authenticated with check (id = auth.uid());
drop policy if exists profiles_update_own on public.profiles;
create policy profiles_update_own on public.profiles for update to authenticated using (id = auth.uid()) with check (id = auth.uid());

drop policy if exists businesses_owner_all on public.businesses;
create policy businesses_owner_all on public.businesses for all to authenticated using (owner_id = auth.uid()) with check (owner_id = auth.uid());
drop policy if exists plans_read_active on public.plans;
create policy plans_read_active on public.plans for select to anon, authenticated using (active = true);

drop policy if exists agent_runs_owner_read on public.agent_runs;
create policy agent_runs_owner_read on public.agent_runs for select to authenticated using (exists (select 1 from public.businesses b where b.id = business_id and b.owner_id = auth.uid()));
drop policy if exists service_requests_owner_all on public.service_requests;
create policy service_requests_owner_all on public.service_requests for all to authenticated using (exists (select 1 from public.businesses b where b.id = business_id and b.owner_id = auth.uid())) with check (exists (select 1 from public.businesses b where b.id = business_id and b.owner_id = auth.uid()));
drop policy if exists usage_events_owner_read on public.usage_events;
create policy usage_events_owner_read on public.usage_events for select to authenticated using (exists (select 1 from public.businesses b where b.id = business_id and b.owner_id = auth.uid()));

-- Agent run creation, status updates and usage writes must go through a trusted server/Edge Function.
-- Do not expose service-role keys in the browser.