-- FabPulse — Core Database Schema + RLS Policies
-- Apply this in Supabase SQL Editor before first deploy
-- Version: 1.0.0
--
-- Run this file once. It creates all tables, enables RLS on each one,
-- and defines the plant-isolation policies in a single pass.

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ─────────────────────────────────────────────────────────────
-- plants
-- ─────────────────────────────────────────────────────────────
CREATE TABLE plants (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  company_name TEXT NOT NULL,
  timezone TEXT NOT NULL DEFAULT 'America/Toronto',
  created_at TIMESTAMPTZ DEFAULT NOW()
);
ALTER TABLE plants ENABLE ROW LEVEL SECURITY;
CREATE POLICY "plant_isolation" ON plants
  USING (id::TEXT = auth.jwt() -> 'app_metadata' ->> 'plant_id');

-- ─────────────────────────────────────────────────────────────
-- divisions
-- ─────────────────────────────────────────────────────────────
CREATE TABLE divisions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  plant_id UUID REFERENCES plants(id) ON DELETE CASCADE NOT NULL,
  name TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
ALTER TABLE divisions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "plant_isolation" ON divisions
  USING (plant_id::TEXT = auth.jwt() -> 'app_metadata' ->> 'plant_id');

-- ─────────────────────────────────────────────────────────────
-- stations
-- ─────────────────────────────────────────────────────────────
CREATE TABLE stations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  division_id UUID REFERENCES divisions(id) ON DELETE CASCADE NOT NULL,
  plant_id UUID REFERENCES plants(id) ON DELETE CASCADE NOT NULL,
  name TEXT NOT NULL,
  kiosk_token TEXT UNIQUE,
  is_active BOOLEAN DEFAULT TRUE
);
ALTER TABLE stations ENABLE ROW LEVEL SECURITY;
CREATE POLICY "plant_isolation" ON stations
  USING (plant_id::TEXT = auth.jwt() -> 'app_metadata' ->> 'plant_id');

-- ─────────────────────────────────────────────────────────────
-- workers
-- ─────────────────────────────────────────────────────────────
CREATE TABLE workers (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  plant_id UUID REFERENCES plants(id) ON DELETE CASCADE NOT NULL,
  name TEXT NOT NULL,
  employee_id TEXT,
  pin_hash TEXT,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
ALTER TABLE workers ENABLE ROW LEVEL SECURITY;
CREATE POLICY "plant_isolation" ON workers
  USING (plant_id::TEXT = auth.jwt() -> 'app_metadata' ->> 'plant_id');

-- ─────────────────────────────────────────────────────────────
-- jobs
-- ─────────────────────────────────────────────────────────────
CREATE TABLE jobs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  plant_id UUID REFERENCES plants(id) ON DELETE CASCADE NOT NULL,
  division_id UUID REFERENCES divisions(id),
  job_number TEXT NOT NULL,
  customer_name TEXT,
  description TEXT,
  engineering_hours NUMERIC,
  status TEXT DEFAULT 'pending',
  priority INTEGER DEFAULT 0,
  due_date DATE,
  started_at TIMESTAMPTZ,
  completed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
ALTER TABLE jobs ENABLE ROW LEVEL SECURITY;
CREATE POLICY "plant_isolation" ON jobs
  USING (plant_id::TEXT = auth.jwt() -> 'app_metadata' ->> 'plant_id');

-- ─────────────────────────────────────────────────────────────
-- task_logs
-- ─────────────────────────────────────────────────────────────
CREATE TABLE task_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  plant_id UUID REFERENCES plants(id) ON DELETE CASCADE NOT NULL,
  job_id UUID REFERENCES jobs(id) ON DELETE CASCADE NOT NULL,
  station_id UUID REFERENCES stations(id),
  worker_id UUID REFERENCES workers(id),
  started_at TIMESTAMPTZ NOT NULL,
  completed_at TIMESTAMPTZ,
  duration_minutes NUMERIC GENERATED ALWAYS AS (
    EXTRACT(EPOCH FROM (completed_at - started_at)) / 60
  ) STORED,
  synced_at TIMESTAMPTZ DEFAULT NOW(),
  offline_created BOOLEAN DEFAULT FALSE,
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
ALTER TABLE task_logs ENABLE ROW LEVEL SECURITY;
CREATE POLICY "plant_isolation" ON task_logs
  USING (plant_id::TEXT = auth.jwt() -> 'app_metadata' ->> 'plant_id');

-- ─────────────────────────────────────────────────────────────
-- simulation_runs
-- ─────────────────────────────────────────────────────────────
CREATE TABLE simulation_runs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  plant_id UUID REFERENCES plants(id) NOT NULL,
  job_id UUID REFERENCES jobs(id) NOT NULL,
  input_params JSONB,
  output_p50 DATE,
  output_p70 DATE,
  output_p95 DATE,
  iterations INTEGER DEFAULT 1000,
  vertex_ai_request_id TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
ALTER TABLE simulation_runs ENABLE ROW LEVEL SECURITY;
CREATE POLICY "plant_isolation" ON simulation_runs
  USING (plant_id::TEXT = auth.jwt() -> 'app_metadata' ->> 'plant_id');

-- ─────────────────────────────────────────────────────────────
-- subscriptions
-- ─────────────────────────────────────────────────────────────
CREATE TABLE subscriptions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  plant_id UUID REFERENCES plants(id) NOT NULL,
  stripe_customer_id TEXT,
  stripe_subscription_id TEXT,
  tier TEXT,
  status TEXT,
  current_period_end TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
ALTER TABLE subscriptions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "plant_isolation" ON subscriptions
  USING (plant_id::TEXT = auth.jwt() -> 'app_metadata' ->> 'plant_id');

-- ─────────────────────────────────────────────────────────────
-- Indexes
-- ─────────────────────────────────────────────────────────────
CREATE INDEX idx_jobs_plant_status ON jobs(plant_id, status);
CREATE INDEX idx_task_logs_job ON task_logs(job_id);
CREATE INDEX idx_task_logs_plant_started ON task_logs(plant_id, started_at DESC);
CREATE INDEX idx_stations_kiosk_token ON stations(kiosk_token);
CREATE INDEX idx_workers_plant ON workers(plant_id);
CREATE INDEX idx_simulation_runs_job ON simulation_runs(job_id);
