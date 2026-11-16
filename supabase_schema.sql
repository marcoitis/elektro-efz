-- Elektroinstallateur EFZ v0.6 – optionales persönliches Cloud-Backend
-- Ausführen im SQL-Editor des EIGENEN Supabase-Projekts.
-- WICHTIG: Den öffentlichen Key (Publishable/Anon) in der App verwenden.
-- Niemals den service_role-Key in die HTML-App übernehmen.

create table if not exists public.efz_progress (
  user_id uuid primary key references auth.users(id) on delete cascade,
  revision bigint not null default 1 check (revision >= 1),
  progress jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now()
);

alter table public.efz_progress enable row level security;
revoke all on public.efz_progress from anon;
grant select, insert, update on public.efz_progress to authenticated;

drop policy if exists efz_select_own on public.efz_progress;
create policy efz_select_own on public.efz_progress
  for select to authenticated using ((select auth.uid())=user_id);

drop policy if exists efz_insert_own on public.efz_progress;
create policy efz_insert_own on public.efz_progress
  for insert to authenticated with check ((select auth.uid())=user_id);

drop policy if exists efz_update_own on public.efz_progress;
create policy efz_update_own on public.efz_progress
  for update to authenticated using ((select auth.uid())=user_id)
  with check ((select auth.uid())=user_id);

create or replace function public.efz_progress_set_updated_at()
returns trigger language plpgsql set search_path = '' as $$
begin
  new.updated_at=now();
  return new;
end;
$$;

drop trigger if exists efz_progress_timestamp on public.efz_progress;
create trigger efz_progress_timestamp
  before insert or update on public.efz_progress
  for each row execute function public.efz_progress_set_updated_at();

-- Die App verwendet Revisionen per bedingtem PATCH (Optimistic Locking):
-- update ... where user_id = auth.uid() AND revision = expectedRevision
-- Sind keine Zeilen aktualisiert, STOPPT der Client die Automatik und verlangt
-- eine ausdrückliche Entscheidung: Cloud / lokal / zusammenführen.
-- Audio-Dateien werden NIE in dieses Backend hochgeladen.
