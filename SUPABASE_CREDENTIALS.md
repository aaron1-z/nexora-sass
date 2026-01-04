# Supabase Credentials - Nexora SaaS

## ✅ Setup Complete

Your Supabase project is configured and ready to use.

## Credentials

**Project URL**: `https://cghypsnfylxvazkdilxc.supabase.co`

**Anon/Public Key**: `sb_publishable_gGPtbYgZm7jsMVpt3iPuAA_l67eIsGK`

**Service Role Key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNnaHlwc25meWx4dmF6a2RpbHhjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzMyMzE4NiwiZXhwIjoyMDgyODk5MTg2fQ.ZBbeLj5fZTTba29I08lZkv7srcbOgGjPEYhrsn1CCaw`

## Environment Variables

### Backend (.env.local)

```bash
SUPABASE_URL=https://cghypsnfylxvazkdilxc.supabase.co
SUPABASE_KEY=sb_publishable_gGPtbYgZm7jsMVpt3iPuAA_l67eIsGK
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNnaHlwc25meWx4dmF6a2RpbHhjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzMyMzE4NiwiZXhwIjoyMDgyODk5MTg2fQ.ZBbeLj5fZTTba29I08lZkv7srcbOgGjPEYhrsn1CCaw
```

### Frontend (.env.local)

```bash
NEXT_PUBLIC_SUPABASE_URL=https://cghypsnfylxvazkdilxc.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=sb_publishable_gGPtbYgZm7jsMVpt3iPuAA_l67eIsGK
```

## Next Steps

1. ✅ Database migrations - Run `infra/supabase/migrations/001_initial_schema.sql`
2. ✅ RLS policies - Run `infra/supabase/rls_policies.sql`
3. ✅ Configure authentication providers in Supabase dashboard
4. ✅ Set up Dodo Payments (see DODO_PAYMENTS_SETUP.md)
5. ✅ Deploy backend and frontend

## Dashboard Links

- **Project Dashboard**: https://supabase.com/dashboard/project/cghypsnfylxvazkdilxc
- **SQL Editor**: https://cghypsnfylxvazkdilxc.supabase.co/project/default/sql
- **API Settings**: https://cghypsnfylxvazkdilxc.supabase.co/project/settings/api
- **Authentication Settings**: https://cghypsnfylxvazkdilxc.supabase.co/project/auth/providers

## Security Notes

⚠️ **Important**:
- Service Role Key has full database access - keep it secret!
- Never commit `.env` files to git
- Only use Service Role Key in backend/server code
- Anon key is safe to use in frontend (it's public)

---

✅ Supabase setup complete! Ready for database migrations and deployment.

