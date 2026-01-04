# Supabase Setup - Quick Reference

## Your Supabase Credentials

✅ **Project URL**: `https://cghypsnfylxvazkdilxc.supabase.co`
✅ **Anon/Public Key**: `sb_publishable_gGPtbYgZm7jsMVpt3iPuAA_l67eIsGK`
✅ **Service Role Key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNnaHlwc25meWx4dmF6a2RpbHhjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzMyMzE4NiwiZXhwIjoyMDgyODk5MTg2fQ.ZBbeLj5fZTTba29I08lZkv7srcbOgGjPEYhrsn1CCaw`

## ✅ Setup Complete!

All credentials have been obtained. You can now proceed with database migrations and deployment.

## Environment Variables Setup

### Backend (.env.local)

Create `backend/.env.local` with:

```bash
SUPABASE_URL=https://cghypsnfylxvazkdilxc.supabase.co
SUPABASE_KEY=sb_publishable_gGPtbYgZm7jsMVpt3iPuAA_l67eIsGK
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNnaHlwc25meWx4dmF6a2RpbHhjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzMyMzE4NiwiZXhwIjoyMDgyODk5MTg2fQ.ZBbeLj5fZTTba29I08lZkv7srcbOgGjPEYhrsn1CCaw
```

### Frontend (.env.local)

Create `frontend/.env.local` with:

```bash
NEXT_PUBLIC_SUPABASE_URL=https://cghypsnfylxvazkdilxc.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=sb_publishable_gGPtbYgZm7jsMVpt3iPuAA_l67eIsGK
```

## Next Steps

1. ✅ All credentials obtained
2. ✅ Run database migrations (see DEPLOYMENT.md Step 1.2)
3. ✅ Configure authentication providers in Supabase
4. ✅ Test the connection
5. ✅ Set up Dodo Payments (see DODO_PAYMENTS_SETUP.md)

## Database Migrations

Run these SQL files in Supabase SQL Editor (in order):

1. Go to: https://cghypsnfylxvazkdilxc.supabase.co/project/default/sql
2. Run `infra/supabase/migrations/001_initial_schema.sql`
3. Run `infra/supabase/rls_policies.sql`
4. Verify tables were created (check Table Editor)

## Security Notes

- ⚠️ **Never commit `.env.local` files to git** (they're in .gitignore)
- ⚠️ **Service Role Key has full database access** - keep it secret
- ✅ The anon key is safe to use in frontend (it's public)
- ✅ Service role key should ONLY be used in backend/server

## Quick Test

Test your connection:

```bash
# Backend
cd backend
python -c "from app.config import settings; print('Supabase URL:', settings.supabase_url)"

# Frontend
cd frontend
npm run dev
# Check browser console for connection errors
```

## Dashboard Links

- **Project Dashboard**: https://supabase.com/dashboard/project/cghypsnfylxvazkdilxc
- **SQL Editor**: https://cghypsnfylxvazkdilxc.supabase.co/project/default/sql
- **API Settings**: https://cghypsnfylxvazkdilxc.supabase.co/project/settings/api
- **Authentication**: https://cghypsnfylxvazkdilxc.supabase.co/project/auth/providers

---

✅ **Supabase setup complete!** Ready for database migrations and deployment.
