create or replace function public.set_updated_at()
returns trigger
language plpgsql
set search_path = ''
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

drop policy if exists profiles_read_own on public.profiles;
create policy profiles_read_own on public.profiles
for select to authenticated using (id = (select auth.uid()));
drop policy if exists profiles_insert_own on public.profiles;
create policy profiles_insert_own on public.profiles
for insert to authenticated with check (id = (select auth.uid()));
drop policy if exists profiles_update_own on public.profiles;
create policy profiles_update_own on public.profiles
for update to authenticated using (id = (select auth.uid()))
with check (id = (select auth.uid()));

drop policy if exists businesses_owner_all on public.businesses;
create policy businesses_owner_all on public.businesses
for all to authenticated using (owner_id = (select auth.uid()))
with check (owner_id = (select auth.uid()));

drop policy if exists agent_runs_owner_read on public.agent_runs;
create policy agent_runs_owner_read on public.agent_runs
for select to authenticated using (
  exists (select 1 from public.businesses b
          where b.id = business_id and b.owner_id = (select auth.uid()))
);
drop policy if exists service_requests_owner_all on public.service_requests;
create policy service_requests_owner_all on public.service_requests
for all to authenticated using (
  exists (select 1 from public.businesses b
          where b.id = business_id and b.owner_id = (select auth.uid()))
)
with check (
  exists (select 1 from public.businesses b
          where b.id = business_id and b.owner_id = (select auth.uid()))
);
drop policy if exists usage_events_owner_read on public.usage_events;
create policy usage_events_owner_read on public.usage_events
for select to authenticated using (
  exists (select 1 from public.businesses b
          where b.id = business_id and b.owner_id = (select auth.uid()))
);