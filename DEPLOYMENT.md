# Nexora SaaS - Complete Deployment Guide

This guide walks you through deploying the complete Nexora SaaS application.

## Prerequisites

- GitHub account
- Supabase account (free tier works)
- Dodo Payments account
- Fly.io account (free tier available)
- Vercel account (free tier available)
- Domain name (optional but recommended)

---

## Step 1: Supabase Setup

### 1.1 Create Supabase Project

1. Go to https://supabase.com
2. Create a new project
3. Note your:
   - Project URL (e.g., `https://xxxxx.supabase.co`)
   - Anon/Public key
   - Service role key (keep secret!)

### 1.2 Run Database Migrations

1. Go to SQL Editor in Supabase dashboard
2. Run `infra/supabase/migrations/001_initial_schema.sql`
3. Run `infra/supabase/rls_policies.sql`
4. Verify tables are created (check Table Editor)

### 1.3 Configure Authentication

1. Go to Authentication → Providers
2. Enable Email provider
3. Enable Google provider (optional but recommended)
4. Add your domain to allowed redirect URLs:
   - `https://nexora.io/api/auth/callback`
   - `http://localhost:3000/api/auth/callback` (for development)

---

## Step 2: Dodo Payments Setup

### 2.1 Create Product

1. Go to Dodo Payments Dashboard → Products
2. Create product "Nexora Briefs"
   - Price: $3.00 (one-time payment)
   - Type: One-time payment (not subscription)
   - Note the Product ID (starts with `pdt_`)

### 2.2 Get API Keys

✅ **Your Credentials**:
- API Key: `ad5Bx5vArOtTPea1.1T9XxL9p2aQ3d3VEcUjy6yubrfkSyGxveXjEkb9onx3QQndt`
- Webhook Secret: `whsec_UrlJ54pwV3+JyuVswZlGkGxkDe1rNBKz`

### 2.3 Setup Webhooks

1. Go to Developer → Webhooks
2. Add endpoint: `https://api.nexora.io/dodo/webhook`
3. Select events:
   - `checkout.session.completed` or `payment.success`
4. Webhook secret: `whsec_UrlJ54pwV3+JyuVswZlGkGxkDe1rNBKz`

---

## Step 3: Backend Deployment (Fly.io)

### 3.1 Prepare Backend

```bash
cd backend

# Copy engine directory to backend (or use symlink)
# The engine code should be accessible from backend/app/services/engine.py
```

### 3.2 Install Fly CLI

```bash
# macOS
brew install flyctl

# Or download from https://fly.io/docs/hands-on/install-flyctl/
```

### 3.3 Login and Create App

```bash
fly auth login
fly apps create nexora-api
```

### 3.4 Set Environment Variables

```bash
fly secrets set \
  SUPABASE_URL=https://cghypsnfylxvazkdilxc.supabase.co \
  SUPABASE_KEY=sb_publishable_gGPtbYgZm7jsMVpt3iPuAA_l67eIsGK \
  SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNnaHlwc25meWx4dmF6a2RpbHhjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzMyMzE4NiwiZXhwIjoyMDgyODk5MTg2fQ.ZBbeLj5fZTTba29I08lZkv7srcbOgGjPEYhrsn1CCaw \
  DODO_API_KEY=ad5Bx5vArOtTPea1.1T9XxL9p2aQ3d3VEcUjy6yubrfkSyGxveXjEkb9onx3QQndt \
  DODO_WEBHOOK_SECRET=whsec_UrlJ54pwV3+JyuVswZlGkGxkDe1rNBKz \
  DODO_PRODUCT_BRIEF=pdt_0NVOawMXoMB75Xo8Dbmbo \
  DODO_ENVIRONMENT=live_mode \
  DODO_API_URL=https://api.dodopayments.com \
  BRIEF_PRICE_USD=3.00 \
  ENVIRONMENT=production \
  API_URL=https://api.nexora.io \
  CORS_ORIGINS=https://nexora.io,https://www.nexora.io
```

**Note**: Replace `your_product_id` with your actual Product ID from Dodo Payments dashboard.

### 3.5 Deploy

```bash
# Copy fly.toml to backend directory
cp infra/fly/fly.toml backend/

cd backend
fly deploy
```

### 3.6 Verify Deployment

```bash
fly open
# Should show {"status":"ok","app":"Nexora API","version":"1.0.0"}
```

---

## Step 4: Frontend Deployment (Vercel)

### 4.1 Prepare Frontend

1. Push code to GitHub (create repository if needed)

### 4.2 Deploy to Vercel

1. Go to https://vercel.com
2. Import your GitHub repository
3. Select the `frontend` directory as root
4. Add environment variables:
   ```
   NEXT_PUBLIC_SUPABASE_URL=https://cghypsnfylxvazkdilxc.supabase.co
   NEXT_PUBLIC_SUPABASE_ANON_KEY=sb_publishable_gGPtbYgZm7jsMVpt3iPuAA_l67eIsGK
   NEXT_PUBLIC_API_URL=https://api.nexora.io
   ```
5. Deploy

### 4.3 Update Supabase Redirect URLs

1. Add Vercel URL to allowed redirect URLs in Supabase:
   - `https://your-app.vercel.app/api/auth/callback`

---

## Step 5: DNS Configuration

### 5.1 Point Domain to Vercel

1. In Vercel dashboard → Settings → Domains
2. Add `nexora.io` and `www.nexora.io`
3. Follow DNS instructions (add CNAME/A records)

### 5.2 Point API Subdomain to Fly.io

1. In Fly.io dashboard → Apps → nexora-api → Settings
2. Add custom domain: `api.nexora.io`
3. Follow DNS instructions (add CNAME record)

---

## Step 6: Final Configuration

### 6.1 Update CORS Origins

In Fly.io, update `CORS_ORIGINS` to include your actual domain:
```bash
fly secrets set CORS_ORIGINS=https://nexora.io,https://www.nexora.io
```

### 6.2 Update Dodo Payments Webhook URL

1. In Dodo Payments Dashboard → Developer → Webhooks
2. Update endpoint URL to: `https://api.nexora.io/dodo/webhook`
3. Verify webhook secret matches: `whsec_UrlJ54pwV3+JyuVswZlGkGxkDe1rNBKz`

### 6.3 Test the Application

1. Visit https://nexora.io
2. Sign up for an account
3. Go to Billing page → Purchase credit for $3.00
4. Complete payment in Dodo Payments
5. Generate a brief
6. Verify webhook delivery in Dodo Payments dashboard

---

## Step 7: Go-Live Checklist

- [ ] Supabase database migrations run successfully
- [ ] Supabase auth providers configured
- [ ] Dodo Payments product created
- [ ] Dodo Payments webhook endpoint configured
- [ ] Backend deployed to Fly.io and accessible
- [ ] Frontend deployed to Vercel
- [ ] DNS configured and propagated
- [ ] Environment variables set correctly
- [ ] Test signup flow works
- [ ] Test payment flow works
- [ ] Test brief generation works
- [ ] Test webhook delivery
- [ ] Monitor error logs

---

## Environment Variables Reference

### Backend (Fly.io)

```
SUPABASE_URL=https://cghypsnfylxvazkdilxc.supabase.co
SUPABASE_KEY=sb_publishable_gGPtbYgZm7jsMVpt3iPuAA_l67eIsGK
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNnaHlwc25meWx4dmF6a2RpbHhjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzMyMzE4NiwiZXhwIjoyMDgyODk5MTg2fQ.ZBbeLj5fZTTba29I08lZkv7srcbOgGjPEYhrsn1CCaw
DODO_API_KEY=ad5Bx5vArOtTPea1.1T9XxL9p2aQ3d3VEcUjy6yubrfkSyGxveXjEkb9onx3QQndt
DODO_WEBHOOK_SECRET=whsec_UrlJ54pwV3+JyuVswZlGkGxkDe1rNBKz
DODO_PRODUCT_BRIEF=pdt_0NVOawMXoMB75Xo8Dbmbo
DODO_ENVIRONMENT=live_mode
DODO_API_URL=https://api.dodopayments.com
BRIEF_PRICE_USD=3.00
ENVIRONMENT=production
API_URL=https://api.nexora.io
CORS_ORIGINS=https://nexora.io,https://www.nexora.io
```

### Frontend (Vercel)

```
NEXT_PUBLIC_SUPABASE_URL=https://cghypsnfylxvazkdilxc.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=sb_publishable_gGPtbYgZm7jsMVpt3iPuAA_l67eIsGK
NEXT_PUBLIC_API_URL=https://api.nexora.io
```

---

## Troubleshooting

### Backend Issues

- Check Fly.io logs: `fly logs`
- Verify environment variables: `fly secrets list`
- Test API directly: `curl https://api.nexora.io/health`

### Frontend Issues

- Check Vercel build logs
- Verify environment variables in Vercel dashboard
- Check browser console for errors

### Database Issues

- Check Supabase logs in dashboard
- Verify RLS policies are enabled
- Test queries in SQL Editor

### Dodo Payments Issues

- Check webhook delivery in Dodo Payments dashboard
- Verify webhook secret matches: `whsec_UrlJ54pwV3+JyuVswZlGkGxkDe1rNBKz`
- Check backend logs for webhook errors
- Verify API key has correct permissions

---

## Support

For issues or questions:
- Check logs in Fly.io, Vercel, and Supabase dashboards
- Review error messages carefully
- Ensure all environment variables are set correctly
- Verify DNS propagation completed (can take up to 48 hours)

---

## Next Steps After Deployment

1. Set up monitoring (Sentry, LogRocket, etc.)
2. Configure analytics (PostHog, Mixpanel, etc.)
3. Set up backup strategy for database
4. Configure CDN for static assets
5. Set up CI/CD pipelines
6. Create admin dashboard for metrics
7. Set up email notifications
8. Configure rate limiting
9. Set up error tracking
10. Create user documentation

---

**You're ready to collect revenue!** 🚀
