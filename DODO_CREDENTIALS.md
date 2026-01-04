# Dodo Payments Credentials - Nexora SaaS

## ✅ Your Dodo Payments Credentials

**API Key**: `ad5Bx5vArOtTPea1.1T9XxL9p2aQ3d3VEcUjy6yubrfkSyGxveXjEkb9onx3QQndt`

**Webhook Secret**: `whsec_UrlJ54pwV3+JyuVswZlGkGxkDe1rNBKz`

**Product ID**: `pdt_0NVOawMXoMB75Xo8Dbmbo` (Nexora Briefs)

## Environment Variables Setup

### Backend (.env.local)

Create or update `backend/.env.local`:

```bash
# Dodo Payments Configuration
DODO_API_KEY=ad5Bx5vArOtTPea1.1T9XxL9p2aQ3d3VEcUjy6yubrfkSyGxveXjEkb9onx3QQndt
DODO_WEBHOOK_SECRET=whsec_UrlJ54pwV3+JyuVswZlGkGxkDe1rNBKz
DODO_PRODUCT_BRIEF=pdt_0NVOawMXoMB75Xo8Dbmbo
DODO_ENVIRONMENT=live_mode  # or "test_mode" for testing
DODO_API_URL=https://api.dodopayments.com
BRIEF_PRICE_USD=3.00
```

### Frontend

No Dodo Payments credentials needed in frontend - payment is handled server-side.

## Webhook Configuration

1. Go to Dodo Payments Dashboard → Developer → Webhooks
2. Add webhook endpoint: `https://api.nexora.io/dodo/webhook`
3. Select events:
   - `checkout.session.completed` or `payment.success`
4. Use webhook secret: `whsec_UrlJ54pwV3+JyuVswZlGkGxkDe1rNBKz`

## Product Setup

Make sure you have a product in Dodo Payments:
- **Product Name**: "Nexora Briefs" (or similar)
- **Price**: $3.00
- **Type**: One-time payment
- **Product ID**: Copy this and use as `DODO_PRODUCT_BRIEF`

## Security Notes

⚠️ **Important**:
- Never commit `.env.local` files to git (they're in .gitignore)
- Keep API key and webhook secret secure
- Use `live_mode` for production, `test_mode` for testing
- Webhook secret is used to verify incoming webhook requests

## Testing

For testing, you can set:
```bash
DODO_ENVIRONMENT=test_mode
```

This uses Dodo Payments' test environment.

## Next Steps

1. ✅ API credentials obtained
2. ✅ Add credentials to `backend/.env.local`
3. ✅ Get Product ID from Dodo Payments dashboard
4. ✅ Configure webhook endpoint in Dodo Payments
5. ✅ Test payment flow

---

✅ **Dodo Payments credentials ready!** Update your `.env` files and configure the webhook.

