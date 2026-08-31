-- PRISM PostgreSQL / TimescaleDB Migration 001: Core Relational Schema

CREATE TABLE IF NOT EXISTS regions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    country VARCHAR(100) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS subscribers (
    id SERIAL PRIMARY KEY,
    region_id INTEGER REFERENCES regions(id) ON DELETE CASCADE,
    org_name VARCHAR(255) NOT NULL,
    contact_phone VARCHAR(55) NOT NULL,
    subscriber_type VARCHAR(50) NOT NULL CHECK (subscriber_type IN ('disaster_response', 'agriculture', 'telecom', 'aviation')),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS scintillation_readings (
    time TIMESTAMPTZ NOT NULL,
    region_id INTEGER NOT NULL REFERENCES regions(id),
    s4_index DOUBLE PRECISION NOT NULL,
    kp_index DOUBLE PRECISION NOT NULL,
    risk_tier VARCHAR(20) NOT NULL CHECK (risk_tier IN ('LOW', 'MODERATE', 'SEVERE'))
);

CREATE TABLE IF NOT EXISTS alerts_sent (
    id SERIAL PRIMARY KEY,
    time TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    subscriber_id INTEGER REFERENCES subscribers(id),
    risk_tier VARCHAR(20) NOT NULL,
    delivery_status VARCHAR(50) NOT NULL
);
