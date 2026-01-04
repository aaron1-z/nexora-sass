# Backend Environment Variables Template

Copy this to `backend/.env.local` and fill in the values:

```bash
# Supabase Configuration
SUPABASE_URL=https://cghypsnfylxvazkdilxc.supabase.co
SUPABASE_KEY=sb_publishable_gGPtbYgZm7jsMVpt3iPuAA_l67eIsGK
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNnaHlwc25meWx4dmF6a2RpbHhjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzMyMzE4NiwiZXhwIjoyMDgyODk5MTg2fQ.ZBbeLj5fZTTba29I08lZkv7srcbOgGjPEYhrsn1CCaw

# Dodo Payments Configuration
DODO_API_KEY=ad5Bx5vArOtTPea1.1T9XxL9p2aQ3d3VEcUjy6yubrfkSyGxveXjEkb9onx3QQndt
DODO_WEBHOOK_SECRET=whsec_UrlJ54pwV3+JyuVswZlGkGxkDe1rNBKz
DODO_PRODUCT_BRIEF=pdt_0NVOawMXoMB75Xo8Dbmbo
DODO_ENVIRONMENT=live_mode
DODO_API_URL=https://api.dodopayments.com
BRIEF_PRICE_USD=3.00

# App Configuration
ENVIRONMENT=development
DEBUG=true
API_URL=http://localhost:8000

# CORS (comma-separated, no spaces)
CORS_ORIGINS=http://localhost:3000
```

## Quick Setup

1. Create `backend/.env.local` file
2. Copy the template above
3. Replace `pdt_0NVOaw...` with your actual Product ID from Dodo Payments dashboard
4. Save the file

## Production Environment

For production deployment (Fly.io), set these as secrets:

```bash
fly secrets set \
  DODO_API_KEY=ad5Bx5vArOtTPea1.1T9XxL9p2aQ3d3VEcUjy6yubrfkSyGxveXjEkb9onx3QQndt \
  DODO_WEBHOOK_SECRET=whsec_UrlJ54pwV3+JyuVswZlGkGxkDe1rNBKz \
  DODO_PRODUCT_BRIEF=your_product_id \
  # ... other variables
```

## Getting Product ID

1. Go to Dodo Payments Dashboard
2. Navigate to Products
3. Find "Nexora Briefs" product
4. Copy the Product ID (starts with `pdt_`)
5. Replace `pdt_0NVOaw...` in your `.env.local` file

---

**Remember**: Never commit `.env.local` files to git!

