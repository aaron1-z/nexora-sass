# Deploy Nexora to nexora.io - Step by Step Guide

This guide will help you deploy Nexora to your custom domain `nexora.io`.

## 📋 Prerequisites Checklist

- [ ] GitHub account (free)
- [ ] Supabase account (free tier works)
- [ ] Dodo Payments account
- [ ] Fly.io account (free tier available) - Sign up at https://fly.io
- [ ] Vercel account (free tier available) - Sign up at https://vercel.com
- [ ] Domain `nexora.io` (you need to own this domain)

---

## Part 1: Backend Deployment (API at api.nexora.io)

### Step 1.1: Install Fly CLI

**Windows (PowerShell):**
```powershell
# Using PowerShell
iwr https://fly.io/install.ps1 -useb | iex
```

**Or download from:** https://fly.io/docs/hands-on/install-flyctl/

### Step 1.2: Login to Fly.io

```bash
fly auth login
```

This will open a browser to authenticate.

### Step 1.3: Create Fly.io App

From your project root directory:

```bash
cd C:\Users\KIIT01\Nexora-Intelligence-Engine-2
fly apps create nexora-api
```

### Step 1.4: Set Environment Variables

**⚠️ IMPORTANT:** Run this from your project root directory:

```bash
fly secrets set --app nexora-api \
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

### Step 1.5: Deploy Backend

From your project root directory:

```bash
fly deploy --config infra/fly/fly.toml
```

Wait for deployment to complete (this takes a few minutes).

### Step 1.6: Verify Backend is Running

```bash
fly open --app nexora-api
```

You should see: `{"status":"ok","app":"Nexora API","version":"1.0.0"}`

### Step 1.7: Add Custom Domain (api.nexora.io)

```bash
fly certs add api.nexora.io --app nexora-api
```

Follow the instructions to add DNS records to your domain provider.

**DNS Record to Add:**
- **Type**: CNAME
- **Name**: api
- **Value**: `nexora-api.fly.dev` (or whatever Fly.io tells you)

---

## Part 2: Frontend Deployment (Website at nexora.io)

### Step 2.1: Push Code to GitHub

1. Create a new repository on GitHub (e.g., `nexora-saas`)
2. Push your code:

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/nexora-saas.git
git push -u origin main
```

### Step 2.2: Deploy to Vercel

1. Go to https://vercel.com
2. Click "Add New Project"
3. Import your GitHub repository
4. **IMPORTANT**: Configure project:
   - **Root Directory**: `frontend` (click "Edit" and set to `frontend`)
   - **Framework Preset**: Next.js
   - **Build Command**: `npm run build` (or leave default)
   - **Output Directory**: `.next` (or leave default)

### Step 2.3: Add Environment Variables in Vercel

In Vercel project settings → Environment Variables, add:

```
NEXT_PUBLIC_SUPABASE_URL=https://cghypsnfylxvazkdilxc.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=sb_publishable_gGPtbYgZm7jsMVpt3iPuAA_l67eIsGK
NEXT_PUBLIC_API_URL=https://api.nexora.io
```

### Step 2.4: Deploy

Click "Deploy" in Vercel. Wait for deployment to complete.

### Step 2.5: Add Custom Domain (nexora.io)

1. In Vercel dashboard → Your Project → Settings → Domains
2. Click "Add Domain"
3. Enter: `nexora.io`
4. Also add: `www.nexora.io`
5. Follow DNS instructions to add records:

**DNS Records to Add:**
- For `nexora.io`: Add A record pointing to Vercel IP (Vercel will show you)
- For `www.nexora.io`: Add CNAME record pointing to `cname.vercel-dns.com`

---

## Part 3: DNS Configuration

You need to configure DNS at your domain registrar (where you bought nexora.io):

### DNS Records Needed:

1. **For Frontend (nexora.io):**
   - **A Record**: `@` → Vercel IP address (Vercel will provide)
   - **CNAME Record**: `www` → `cname.vercel-dns.com`

2. **For Backend API (api.nexora.io):**
   - **CNAME Record**: `api` → `nexora-api.fly.dev` (or what Fly.io provided)

### Where to Add DNS Records:

- Go to your domain registrar (GoDaddy, Namecheap, Cloudflare, etc.)
- Find DNS Management / DNS Settings
- Add the records above
- **Wait 5-60 minutes** for DNS to propagate

---

## Part 4: Final Configuration

### Step 4.1: Update Supabase Redirect URLs

1. Go to Supabase Dashboard → Authentication → URL Configuration
2. Add to "Redirect URLs":
   ```
   https://nexora.io/api/auth/callback
   https://www.nexora.io/api/auth/callback
   ```

### Step 4.2: Update Dodo Payments Webhook

1. Go to Dodo Payments Dashboard → Developer → Webhooks
2. Update webhook endpoint to: `https://api.nexora.io/dodo/webhook`
3. Verify webhook secret: `whsec_UrlJ54pwV3+JyuVswZlGkGxkDe1rNBKz`

### Step 4.3: Verify Everything Works

1. Visit https://nexora.io
2. Sign up for an account
3. Go to Billing → Purchase credit
4. Test brief generation

---

## 🔧 Troubleshooting

### Backend Not Working?

```bash
# Check logs
fly logs --app nexora-api

# Check environment variables
fly secrets list --app nexora-api

# Restart app
fly apps restart nexora-api
```

### Frontend Not Working?

- Check Vercel deployment logs
- Verify environment variables are set
- Check browser console for errors

### DNS Issues?

- Use https://dnschecker.org to verify DNS propagation
- Wait up to 24 hours for DNS to fully propagate
- Make sure DNS records are exactly as provided

### Payment Not Working?

- Check Fly.io logs: `fly logs --app nexora-api`
- Verify Dodo Payments webhook is configured
- Check webhook delivery in Dodo Payments dashboard

---

## ✅ Deployment Checklist

- [ ] Backend deployed to Fly.io
- [ ] Frontend deployed to Vercel
- [ ] DNS records added
- [ ] api.nexora.io is accessible
- [ ] nexora.io is accessible
- [ ] Supabase redirect URLs updated
- [ ] Dodo Payments webhook configured
- [ ] Test signup works
- [ ] Test payment works
- [ ] Test brief generation works

---

## 🎉 You're Live!

Once everything is working:
- **Frontend**: https://nexora.io
- **Backend API**: https://api.nexora.io
- **API Docs**: https://api.nexora.io/docs

---

## 💰 Costs (Free Tier)

- **Fly.io**: Free tier includes 3 shared-cpu VMs
- **Vercel**: Free tier includes unlimited deployments
- **Supabase**: Free tier includes 500MB database
- **Domain**: Depends on your registrar (usually $10-15/year)

All free tiers should be sufficient for starting out! 🚀

