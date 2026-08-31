-- PRISM TimescaleDB Migration 002: Hypertable Definitions

-- Enable TimescaleDB extension if available
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

-- Convert scintillation_readings into a time-series hypertable partitioned by time
SELECT create_hypertable('scintillation_readings', 'time', if_not_exists => TRUE);

-- Create optimized index for fast spatial-temporal region queries
CREATE INDEX IF NOT EXISTS idx_scintillation_region_time ON scintillation_readings (region_id, time DESC);
