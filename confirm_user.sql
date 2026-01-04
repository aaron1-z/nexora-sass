-- Quick SQL fix to confirm your user email
-- Run this in Supabase SQL Editor if you prefer SQL over dashboard

-- Replace 'adityakittu2773@gmail.com' with your actual email
UPDATE auth.users
SET email_confirmed_at = NOW()
WHERE email = 'adityakittu2773@gmail.com'
AND email_confirmed_at IS NULL;

-- Verify it worked
SELECT email, email_confirmed_at, created_at 
FROM auth.users 
WHERE email = 'adityakittu2773@gmail.com';

