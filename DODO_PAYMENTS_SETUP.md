# Dodo Payments Integration Guide

## Overview

This application uses Dodo Payments for **pay-per-brief** billing model:
- **Price**: $3.00 per brief
- **Payment Type**: One-time payment
- **Product**: "Nexora Briefs" ($3.00)

## ✅ Your Credentials

- **API Key**: `ad5Bx5vArOtTPea1.1T9XxL9p2aQ3d3VEcUjy6yubrfkSyGxveXjEkb9onx3QQndt`
- **Webhook Secret**: `whsec_UrlJ54pwV3+JyuVswZlGkGxkDe1rNBKz`
- **Product**: "Nexora Briefs" (get Product ID from dashboard)

## Setup Instructions

### 1. Create Dodo Payments Account

✅ Already done - you have an account.

### 2. Get API Credentials

✅ **Already obtained**:
- API Key: `ad5Bx5vArOtTPea1.1T9XxL9p2aQ3d3VEcUjy6yubrfkSyGxveXjEkb9onx3QQndt`
- Webhook Secret: `whsec_UrlJ54pwV3+JyuVswZlGkGxkDe1rNBKz`

Store these securely in your `.env` files.

### 3. Get Product ID

1. Go to Dodo Payments Dashboard → Products
2. Find "Nexora Briefs" product
3. Copy the Product ID (starts with `pdt_`)
4. Use this as `DODO_PRODUCT_BRIEF` in your environment variables

### 4. Configure Webhooks

1. Go to Developer → Webhooks
2. Create new webhook endpoint: `https://api.nexora.io/dodo/webhook`
3. Select events to listen for:
   - `checkout.session.completed` or `payment.success`
4. Webhook secret: `whsec_UrlJ54pwV3+JyuVswZlGkGxkDe1rNBKz`
5. Save the webhook

### 5. Environment Variables

**Backend (.env.local)**:
```bash
DODO_API_KEY=ad5Bx5vArOtTPea1.1T9XxL9p2aQ3d3VEcUjy6yubrfkSyGxveXjEkb9onx3QQndt
DODO_WEBHOOK_SECRET=whsec_UrlJ54pwV3+JyuVswZlGkGxkDe1rNBKz
DODO_PRODUCT_BRIEF=pdt_0NVOawMXoMB75Xo8Dbmbo
DODO_ENVIRONMENT=live_mode  # or "test_mode" for testing
DODO_API_URL=https://api.dodopayments.com
BRIEF_PRICE_USD=3.00
```

**Frontend (.env.local)**:
```bash
# No Dodo Payments credentials needed - payment handled server-side
NEXT_PUBLIC_SUPABASE_URL=https://cghypsnfylxvazkdilxc.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=sb_publishable_gGPtbYgZm7jsMVpt3iPuAA_l67eIsGK
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 6. Install SDK

The backend uses the Dodo Payments Python SDK:

```bash
cd backend
pip install dodopayments
```

If the SDK is not available, the code includes a fallback using `requests` library.

### 7. Test Mode

For testing, set:
```bash
DODO_ENVIRONMENT=test_mode
```

This uses Dodo Payments' test environment.

## API Endpoints

### Create Checkout Session (Pay-Per-Brief)
```
POST /dodo/create-checkout
Returns: { checkout_url, session_id }
```

### Webhook Handler
```
POST /dodo/webhook
Headers: x-dodo-signature
Body: webhook event JSON
```

## Webhook Events

The application handles the following webhook events:

1. **checkout.session.completed** / **payment.success**
   - Records payment in `usage_events` table
   - Grants credit for one brief generation

## How Pay-Per-Brief Works

1. User clicks "Purchase Credit" → Creates checkout session for $3.00
2. User completes payment → Webhook receives `payment.success` event
3. System records payment → Grants one credit to user's organization
4. User generates brief → System checks for credit, generates brief, uses credit
5. User needs another brief → Must purchase another credit

## Database Flow

- Payments tracked in `usage_events` with `event_type="brief_payment_completed"`
- Briefs tracked in `briefs` table
- Credit calculation: `available_credits = payments - briefs_generated`

## Troubleshooting

### Webhook Not Receiving Events

1. Verify webhook URL is correct and accessible: `https://api.nexora.io/dodo/webhook`
2. Check webhook secret matches: `whsec_UrlJ54pwV3+JyuVswZlGkGxkDe1rNBKz`
3. Verify events are enabled in Dodo Payments dashboard
4. Check backend logs for webhook errors

### API Authentication Errors

1. Verify API key is correct: `ad5Bx5vArOtTPea1.1T9XxL9p2aQ3d3VEcUjy6yubrfkSyGxveXjEkb9onx3QQndt`
2. Check API key has necessary permissions
3. Verify environment (test_mode vs live_mode) matches your account

### Checkout Session Creation Fails

1. Verify product ID is correct (get from Dodo Payments dashboard)
2. Check API key permissions
3. Review backend logs for detailed error messages

### Payment Not Granting Credit

1. Check webhook is receiving events
2. Verify webhook secret matches
3. Check database `usage_events` table for payment records
4. Review backend logs for webhook processing errors

## SDK Documentation

For more details, refer to:
- Dodo Payments API Docs: https://docs.dodopayments.com
- Python SDK: https://docs.dodopayments.com/api-reference/dodo-payments-sdks

## Support

For Dodo Payments support:
- Documentation: https://docs.dodopayments.com
- Support: Contact Dodo Payments support team

---

**Setup complete!** Just need to:
1. Get Product ID from dashboard
2. Configure webhook endpoint
3. Add credentials to `.env` files
