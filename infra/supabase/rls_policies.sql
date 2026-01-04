-- Row Level Security Policies for Nexora SaaS
-- Run this after creating the schema

-- Enable RLS on all tables
ALTER TABLE organizations ENABLE ROW LEVEL SECURITY;
ALTER TABLE org_members ENABLE ROW LEVEL SECURITY;
-- Subscriptions table removed for pay-per-brief model
ALTER TABLE briefs ENABLE ROW LEVEL SECURITY;
ALTER TABLE usage_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;

-- Helper function to get user's org_ids
CREATE OR REPLACE FUNCTION get_user_org_ids(user_uuid UUID)
RETURNS SETOF UUID AS $$
    SELECT org_id FROM org_members WHERE user_id = user_uuid;
$$ LANGUAGE sql SECURITY DEFINER;

-- Helper function to get user's role in org
CREATE OR REPLACE FUNCTION get_user_role(user_uuid UUID, org_uuid UUID)
RETURNS TEXT AS $$
    SELECT role FROM org_members WHERE user_id = user_uuid AND org_id = org_uuid;
$$ LANGUAGE sql SECURITY DEFINER;

-- Organizations policies
CREATE POLICY "Users can view their own organizations"
    ON organizations FOR SELECT
    USING (id IN (SELECT get_user_org_ids(auth.uid())));

CREATE POLICY "Admins can update their organizations"
    ON organizations FOR UPDATE
    USING (
        id IN (SELECT get_user_org_ids(auth.uid()))
        AND get_user_role(auth.uid(), id) IN ('admin')
    );

-- Org members policies
CREATE POLICY "Users can view members of their orgs"
    ON org_members FOR SELECT
    USING (org_id IN (SELECT get_user_org_ids(auth.uid())));

CREATE POLICY "Admins can manage members in their orgs"
    ON org_members FOR ALL
    USING (
        org_id IN (SELECT get_user_org_ids(auth.uid()))
        AND get_user_role(auth.uid(), org_id) IN ('admin')
    );

-- Subscriptions table removed for pay-per-brief model
-- Payment tracking is done via usage_events with event_type='brief_payment_completed'

-- Briefs policies
CREATE POLICY "Users can view briefs in their orgs"
    ON briefs FOR SELECT
    USING (org_id IN (SELECT get_user_org_ids(auth.uid())));

CREATE POLICY "Analysts and admins can create briefs"
    ON briefs FOR INSERT
    WITH CHECK (
        org_id IN (SELECT get_user_org_ids(auth.uid()))
        AND get_user_role(auth.uid(), org_id) IN ('admin', 'analyst')
    );

CREATE POLICY "Admins can delete briefs in their orgs"
    ON briefs FOR DELETE
    USING (
        org_id IN (SELECT get_user_org_ids(auth.uid()))
        AND get_user_role(auth.uid(), org_id) IN ('admin')
    );

-- Usage events policies
CREATE POLICY "Users can view usage events for their orgs"
    ON usage_events FOR SELECT
    USING (org_id IN (SELECT get_user_org_ids(auth.uid())));

CREATE POLICY "Analysts and admins can create usage events"
    ON usage_events FOR INSERT
    WITH CHECK (
        org_id IN (SELECT get_user_org_ids(auth.uid()))
        AND get_user_role(auth.uid(), org_id) IN ('admin', 'analyst')
    );

-- Audit logs policies
CREATE POLICY "Users can view audit logs for their orgs"
    ON audit_logs FOR SELECT
    USING (org_id IN (SELECT get_user_org_ids(auth.uid())));

CREATE POLICY "System can create audit logs"
    ON audit_logs FOR INSERT
    WITH CHECK (true); -- Service role will insert

-- Note: check_usage_limits function is not needed for pay-per-brief model
-- Credit checking is done via check_payment_credit in backend
