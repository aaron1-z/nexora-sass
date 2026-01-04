# Deploy Nexora to nexora.io using Railway

This guide will help you deploy Nexora backend to Railway and frontend to Vercel.

## 📋 Prerequisites Checklist

- [ ] GitHub account (free)
- [ ] Supabase account (free tier works)
- [ ] Dodo Payments account
- [ ] Railway account (free tier available) - Sign up at https://railway.app
- [ ] Vercel account (free tier available) - Sign up at https://vercel.com
- [ ] Domain `nexora.io` (you need to own this domain)

---

## Part 1: Backend Deployment (API at api.nexora.io) - Railway

### Step 1.1: Push Code to GitHub

1. Create a new repository on GitHub (e.g., `nexora-saas`)
2. Push your code:

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/nexora-saas.git
git push -u origin main
```

### Step 1.2: Create Railway Account

1. Go to https://railway.app
2. Sign up with GitHub (recommended - easier integration)
3. Complete the setup

### Step 1.3: Create New Project

1. In Railway dashboard, click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your `nexora-saas` repository
4. Railway will detect the Dockerfile automatically

### Step 1.4: Configure Build Settings

1. Railway should auto-detect `backend/Dockerfile`
2. If not, go to Settings → Build:
   - **Root Directory**: Leave empty (project root)
   - **Dockerfile Path**: `backend/Dockerfile`
   - **Build Command**: Leave default
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Step 1.5: Set Environment Variables

In Railway dashboard → Your Service → Variables, add these:

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
PORT=8000
```

**Note**: Railway automatically sets `PORT` variable, but we include it just in case.

### Step 1.6: Deploy

1. Railway will automatically start deploying when you connect the repo
2. Watch the build logs in Railway dashboard
3. Wait for deployment to complete (takes 3-5 minutes)

### Step 1.7: Get Railway URL

1. After deployment, Railway will give you a URL like: `nexora-api-production.up.railway.app`
2. Click on your service → Settings → Generate Domain
3. Railway will provide a domain (you can use this for testing)

### Step 1.8: Add Custom Domain (api.nexora.io)

1. In Railway dashboard → Your Service → Settings → Domains
2. Click "Custom Domain"
3. Enter: `api.nexora.io`
4. Railway will provide DNS instructions

**DNS Record to Add:**
- Go to your domain registrar
- Add **CNAME record**:
  - **Name**: `api`
  - **Value**: Railway will provide (something like `cname.railway.app`)

---

## Part 2: Frontend Deployment (Website at nexora.io) - Vercel

### Step 2.1: Deploy to Vercel

1. Go to https://vercel.com
2. Click "Add New Project"
3. Import your GitHub repository
4. **IMPORTANT**: Configure project:
   - **Root Directory**: `frontend` (click "Edit" and set to `frontend`)
   - **Framework Preset**: Next.js
   - **Build Command**: `npm run build` (or leave default)
   - **Output Directory**: `.next` (or leave default)

### Step 2.2: Add Environment Variables in Vercel

In Vercel project settings → Environment Variables, add:

```
NEXT_PUBLIC_SUPABASE_URL=https://cghypsnfylxvazkdilxc.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=sb_publishable_gGPtbYgZm7jsMVpt3iPuAA_l67eIsGK
NEXT_PUBLIC_API_URL=https://api.nexora.io
```

### Step 2.3: Deploy

Click "Deploy" in Vercel. Wait for deployment to complete.

### Step 2.4: Add Custom Domain (nexora.io)

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
   - **CNAME Record**: `api` → Railway CNAME (Railway will provide in domain settings)

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

1. Check Railway logs:
   - Go to Railway dashboard → Your Service → Deployments → Click latest deployment → View logs

2. Check environment variables:
   - Railway dashboard → Your Service → Variables
   - Make sure all variables are set correctly

3. Restart service:
   - Railway dashboard → Your Service → Settings → Restart

### Frontend Not Working?

- Check Vercel deployment logs
- Verify environment variables are set
- Check browser console for errors
- Make sure `NEXT_PUBLIC_API_URL=https://api.nexora.io` is set

### DNS Issues?

- Use https://dnschecker.org to verify DNS propagation
- Wait up to 24 hours for DNS to fully propagate
- Make sure DNS records are exactly as provided
- Check Railway domain settings for the correct CNAME value

### Payment Not Working?

- Check Railway logs for backend errors
- Verify Dodo Payments webhook is configured to `https://api.nexora.io/dodo/webhook`
- Check webhook delivery in Dodo Payments dashboard
- Verify `DODO_API_URL=https://api.dodopayments.com` is set correctly

---

## ✅ Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Railway project created
- [ ] Backend deployed to Railway
- [ ] Environment variables set in Railway
- [ ] Custom domain `api.nexora.io` added to Railway
- [ ] Frontend deployed to Vercel
- [ ] Environment variables set in Vercel
- [ ] Custom domain `nexora.io` added to Vercel
- [ ] DNS records added at domain registrar
- [ ] DNS propagated (check with dnschecker.org)
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

- **Railway**: Free tier includes $5 credit/month (enough for small apps)
- **Vercel**: Free tier includes unlimited deployments
- **Supabase**: Free tier includes 500MB database
- **Domain**: Depends on your registrar (usually $10-15/year)

All free tiers should be sufficient for starting out! 🚀

---

## 🚀 Quick Deploy Commands

### Railway CLI (Optional - you can use the web dashboard instead)

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link to project
railway link

# Deploy
railway up
```

But the web dashboard is easier! Just connect your GitHub repo and Railway handles everything.

