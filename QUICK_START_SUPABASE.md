# Quick Start - Supabase Configuration

## ✅ Already Done
- Supabase project created
- Project URL: `https://cghypsnfylxvazkdilxc.supabase.co`
- Anon key obtained: `sb_publishable_gGPtbYgZm7jsMVpt3iPuAA_l67eIsGK`
- Service role key obtained: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNnaHlwc25meWx4dmF6a2RpbHhjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzMyMzE4NiwiZXhwIjoyMDgyODk5MTg2fQ.ZBbeLj5fZTTba29I08lZkv7srcbOgGjPEYhrsn1CCaw`

## 📝 Setup Your Local Environment

### Backend

Create `backend/.env.local`:
```bash
SUPABASE_URL=https://cghypsnfylxvazkdilxc.supabase.co
SUPABASE_KEY=sb_publishable_gGPtbYgZm7jsMVpt3iPuAA_l67eIsGK
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNnaHlwc25meWx4dmF6a2RpbHhjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzMyMzE4NiwiZXhwIjoyMDgyODk5MTg2fQ.ZBbeLj5fZTTba29I08lZkv7srcbOgGjPEYhrsn1CCaw
```

### Frontend

Create `frontend/.env.local`:
```bash
NEXT_PUBLIC_SUPABASE_URL=https://cghypsnfylxvazkdilxc.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=sb_publishable_gGPtbYgZm7jsMVpt3iPuAA_l67eIsGK
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🗄️ Run Database Migrations

1. Go to Supabase SQL Editor: https://cghypsnfylxvazkdilxc.supabase.co/project/default/sql
2. Run `infra/supabase/migrations/001_initial_schema.sql`
3. Run `infra/supabase/rls_policies.sql`
4. Verify tables were created (check Table Editor)

## 🔐 Configure Authentication

1. Go to Authentication → Providers
2. Enable Email provider
3. (Optional) Enable Google OAuth
4. Add redirect URL: `http://localhost:3000/api/auth/callback`

## ✅ Test Connection

```bash
# Test backend
cd backend
python -c "from app.config import settings; print('✅ Config loaded:', settings.supabase_url)"

# Test frontend
cd frontend
npm install
npm run dev
# Visit http://localhost:3000
```

## 📚 Next Steps

See `DEPLOYMENT.md` for:
- Dodo Payments setup
- Production deployment
- DNS configuration

---

**Note**: `.env.local` files are git-ignored. Never commit them!

**✅ Supabase setup complete!** Ready for database migrations.
