-- Fix Signup Trigger for Pay-Per-Brief Model
-- Run this in Supabase SQL Editor: https://cghypsnfylxvazkdilxc.supabase.co/project/default/sql

-- Step 1: Ensure brief_credits column exists
ALTER TABLE organizations 
ADD COLUMN IF NOT EXISTS brief_credits INTEGER DEFAULT 0;

-- Step 2: Update the handle_new_user function
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
    VALUES (
        COALESCE(NEW.raw_user_meta_data->>'full_name', split_part(NEW.email, '@', 1)), 
        org_slug, 
        'pay_as_you_go', 
        0
    )
    RETURNING id INTO new_org_id;
    
    -- Add user as admin
    INSERT INTO org_members (org_id, user_id, role)
    VALUES (new_org_id, NEW.id, 'admin');
    
    RETURN NEW;
EXCEPTION
    WHEN others THEN
        -- Log error but don't fail signup (allows user creation even if org creation fails)
        RAISE WARNING 'Error in handle_new_user for user %: %', NEW.id, SQLERRM;
        RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Step 3: Ensure trigger exists
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION handle_new_user();

-- Step 4: Verify function and trigger were created
SELECT 
    'Function created' as status,
    proname as name
FROM pg_proc 
WHERE proname = 'handle_new_user';

SELECT 
    'Trigger created' as status,
    tgname as name
FROM pg_trigger 
WHERE tgname = 'on_auth_user_created';

-- Done! Try signing up again.

