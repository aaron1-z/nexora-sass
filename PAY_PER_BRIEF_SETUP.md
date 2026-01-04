# Pay-Per-Brief Model Setup

## Overview

Nexora now uses a **pay-per-brief** model instead of subscriptions:
- **Price**: $3.00 per brief
- **Payment Type**: One-time payment via Dodo Payments
- **Product**: Use your existing "Nexora Briefs" product (Product ID: `pdt_0NVOaw...`)

## Configuration

### Backend Environment Variables

Update `backend/.env.local`:

```bash
# Dodo Payments
DODO_API_KEY=ad5Bx5vArOtTPea1.1T9XxL9p2aQ3d3VEcUjy6yubrfkSyGxveXjEkb9onx3QQndt
DODO_WEBHOOK_SECRET=whsec_UrlJ54pwV3+JyuVswZlGkGxkDe1rNBKz
DODO_PRODUCT_BRIEF=pdt_0NVOawMXoMB75Xo8Dbmbo
DODO_ENVIRONMENT=live_mode
DODO_API_URL=https://api.dodopayments.com
BRIEF_PRICE_USD=3.00
```

**Note**: Get your Product ID from Dodo Payments dashboard → Products → "Nexora Briefs" → Copy Product ID

### Frontend Environment Variables

Update `frontend/.env.local`:

```bash
# No product IDs needed for frontend - payment is handled server-side
NEXT_PUBLIC_SUPABASE_URL=https://cghypsnfylxvazkdilxc.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=sb_publishable_gGPtbYgZm7jsMVpt3iPuAA_l67eIsGK
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## How It Works

1. **User clicks "Purchase Credit"** → Creates Dodo Payments checkout session for $3.00
2. **User completes payment** → Webhook records payment in `usage_events` table
3. **User generates brief** → System checks for available credit, generates brief, uses one credit
4. **Process repeats** → User purchases new credit for each brief

## Database Flow

1. Payment webhook → Creates `usage_events` record with `event_type="brief_payment_completed"`
2. Brief generation → Creates `briefs` record and `usage_events` record with `event_type="brief_generated"`
3. Credit calculation → `available_credits = payments - briefs_generated`

## API Endpoints

### Create Payment Checkout
```
POST /dodo/create-checkout
Returns: { checkout_url, session_id }
```

### Check Payment Status
```
GET /briefs/payment-status
Returns: {
  has_credit: boolean,
  available_credits: number,
  price_per_brief: 3.00,
  total_paid: number,
  total_used: number
}
```

### Generate Brief (requires credit)
```
POST /briefs/generate
Body: { query, org_id, metadata }
Returns: BriefResponse
Error 402 if no credit available
```

## Webhook Events

Dodo Payments webhook handles:
- `checkout.session.completed` / `payment.success`
  - Creates `usage_events` record with payment details
  - Grants credit for one brief

## Frontend Flow

1. **Billing Page**: Shows available credits, "Purchase Credit" button
2. **Briefs Page**: 
   - Shows credit status
   - "Generate Brief" button disabled if no credit
   - Prompts user to purchase if they try to generate without credit

## Testing

1. Start backend and frontend
2. Sign in to application
3. Go to Billing page → Purchase credit
4. Complete payment in Dodo Payments
5. Go to Briefs page → Generate brief (should work now)
6. Generate another brief (should require new payment)

## Notes

- Credits are tracked per organization
- One payment = one brief credit
- Credits don't expire (can be used anytime)
- Payment is one-time, no recurring subscription
- Product ID from Dodo Payments dashboard: Use the "Nexora Briefs" product ID

