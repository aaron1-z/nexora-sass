# Complete Setup Guide - Nexora SaaS

## ✅ Current Status

### Supabase - ✅ Complete
- Project URL: `https://cghypsnfylxvazkdilxc.supabase.co`
- Anon Key: `sb_publishable_gGPtbYgZm7jsMVpt3iPuAA_l67eIsGK`
- Service Role Key: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNnaHlwc25meWx4dmF6a2RpbHhjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzMyMzE4NiwiZXhwIjoyMDgyODk5MTg2fQ.ZBbeLj5fZTTba29I08lZkv7srcbOgGjPEYhrsn1CCaw`

### Dodo Payments - ✅ Complete
- API Key: `ad5Bx5vArOtTPea1.1T9XxL9p2aQ3d3VEcUjy6yubrfkSyGxveXjEkb9onx3QQndt`
- Webhook Secret: `whsec_UrlJ54pwV3+JyuVswZlGkGxkDe1rNBKz`
- Product: "Nexora Briefs" ($3.00 one-time payment)
- Product ID: Get from Dodo Payments dashboard

## Quick Setup Steps

### 1. Backend Setup

Create `backend/.env.local`:

```bash
# Supabase
SUPABASE_URL=https://cghypsnfylxvazkdilxc.supabase.co
SUPABASE_KEY=sb_publishable_gGPtbYgZm7jsMVpt3iPuAA_l67eIsGK
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNnaHlwc25meWx4dmF6a2RpbHhjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzMyMzE4NiwiZXhwIjoyMDgyODk5MTg2fQ.ZBbeLj5fZTTba29I08lZkv7srcbOgGjPEYhrsn1CCaw

# Dodo Payments
DODO_API_KEY=ad5Bx5vArOtTPea1.1T9XxL9p2aQ3d3VEcUjy6yubrfkSyGxveXjEkb9onx3QQndt
DODO_WEBHOOK_SECRET=whsec_UrlJ54pwV3+JyuVswZlGkGxkDe1rNBKz
DODO_PRODUCT_BRIEF=pdt_0NVOawMXoMB75Xo8Dbmbo
DODO_ENVIRONMENT=live_mode
DODO_API_URL=https://api.dodopayments.com
BRIEF_PRICE_USD=3.00

# App
ENVIRONMENT=development
DEBUG=true
API_URL=http://localhost:8000
CORS_ORIGINS=http://localhost:3000
```

### 2. Frontend Setup

Create `frontend/.env.local`:

```bash
NEXT_PUBLIC_SUPABASE_URL=https://cghypsnfylxvazkdilxc.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=sb_publishable_gGPtbYgZm7jsMVpt3iPuAA_l67eIsGK
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Database Migrations

1. Go to: https://cghypsnfylxvazkdilxc.supabase.co/project/default/sql
2. Run: `infra/supabase/migrations/001_initial_schema.sql`
3. Run: `infra/supabase/rls_policies.sql`

### 4. Get Product ID

1. Go to Dodo Payments Dashboard → Products
2. Find "Nexora Briefs" product
3. Copy the Product ID (starts with `pdt_`)
4. Update `DODO_PRODUCT_BRIEF` in `backend/.env.local`

### 5. Configure Webhook

1. Go to Dodo Payments Dashboard → Developer → Webhooks
2. Add endpoint: `https://api.nexora.io/dodo/webhook` (or `http://localhost:8000/dodo/webhook` for local testing)
3. Select event: `checkout.session.completed` or `payment.success`
4. Webhook secret: `whsec_UrlJ54pwV3+JyuVswZlGkGxkDe1rNBKz`

### 6. Run Application

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Testing Flow

1. Sign up / Sign in to application
2. Go to Billing page
3. Click "Purchase Credit for $3.00"
4. Complete payment in Dodo Payments
5. Go to Briefs page
6. Generate a brief (should work now!)

## Next Steps

- [ ] Set Product ID in backend `.env.local`
- [ ] Run database migrations
- [ ] Configure webhook endpoint
- [ ] Test payment flow
- [ ] Deploy to production

---

**All credentials ready!** Just need to get the Product ID and configure the webhook.

