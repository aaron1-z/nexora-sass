-- Nexora SaaS - Initial Schema
-- Run this in Supabase SQL Editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Organizations table
CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    plan TEXT NOT NULL DEFAULT 'pay_as_you_go', -- pay_as_you_go for per-brief model
    dodo_customer_id TEXT,
    brief_credits INTEGER DEFAULT 0, -- Credits available for brief generation
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Organization members (junction table with roles)
CREATE TABLE org_members (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    org_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    role TEXT NOT NULL DEFAULT 'viewer', -- admin, analyst, viewer
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(org_id, user_id)
);

-- Subscriptions table removed for pay-per-brief model
-- Payments are tracked via usage_events with event_type='brief_payment_completed'

-- Briefs table
CREATE TABLE briefs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    org_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE SET NULL,
    title TEXT NOT NULL,
    query TEXT NOT NULL,
    input_data JSONB,
    output_data JSONB NOT NULL,
    confidence TEXT,
    execution_time_ms INTEGER,
    cost_usd DECIMAL(10, 6) DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'completed', -- pending, processing, completed, failed
    error_message TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Usage events for tracking and billing
CREATE TABLE usage_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    org_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    user_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
    event_type TEXT NOT NULL, -- brief_generated, api_call, etc.
    metadata JSONB,
    cost_usd DECIMAL(10, 6) DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Audit logs for compliance
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    org_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    user_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
    action TEXT NOT NULL,
    resource_type TEXT,
    resource_id UUID,
    metadata JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_org_members_org_id ON org_members(org_id);
CREATE INDEX idx_org_members_user_id ON org_members(user_id);
CREATE INDEX idx_briefs_org_id ON briefs(org_id);
CREATE INDEX idx_briefs_user_id ON briefs(user_id);
CREATE INDEX idx_briefs_created_at ON briefs(created_at DESC);
CREATE INDEX idx_usage_events_org_id ON usage_events(org_id);
CREATE INDEX idx_usage_events_created_at ON usage_events(created_at DESC);
CREATE INDEX idx_audit_logs_org_id ON audit_logs(org_id);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at DESC);
-- Subscription indexes removed for pay-per-brief model

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers for updated_at
CREATE TRIGGER update_organizations_updated_at BEFORE UPDATE ON organizations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Subscriptions table removed for pay-per-brief model

CREATE TRIGGER update_briefs_updated_at BEFORE UPDATE ON briefs
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Function to auto-create org on user signup
CREATE OR REPLACE FUNCTION handle_new_user()
RETURNS TRIGGER AS $$
DECLARE
    new_org_id UUID;
    org_slug TEXT;
BEGIN
    -- Generate org slug from email
    org_slug := lower(regexp_replace(NEW.email, '[^a-z0-9]+', '-', 'g'));
    org_slug := left(org_slug || '-' || substr(md5(random()::text), 1, 8), 50);
    
    -- Create organization with pay-as-you-go plan
    INSERT INTO organizations (name, slug, plan, brief_credits)
    VALUES (COALESCE(NEW.raw_user_meta_data->>'full_name', split_part(NEW.email, '@', 1)), org_slug, 'pay_as_you_go', 0)
    RETURNING id INTO new_org_id;
    
    -- Add user as admin
    INSERT INTO org_members (org_id, user_id, role)
    VALUES (new_org_id, NEW.id, 'admin');
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger for new user signup
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION handle_new_user();
