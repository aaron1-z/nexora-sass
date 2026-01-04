# Nexora SaaS - Production-Ready Intelligence Engine Platform

Complete B2B SaaS application for AI-powered intelligence briefs.

## 🏗️ Architecture

- **Frontend**: Next.js 14 (App Router) + Tailwind CSS → Deployed on Vercel
- **Backend**: FastAPI (Python) → Deployed on Fly.io
- **Database & Auth**: Supabase (PostgreSQL + Auth)
- **Payments**: Dodo Payments
- **Domains**: nexora.io (frontend), api.nexora.io (backend)

## 📁 Project Structure

```
nexora-saas/
├── backend/           # FastAPI application
│   ├── app/
│   │   ├── api/      # API endpoints
│   │   ├── services/ # Business logic
│   │   ├── models/   # Pydantic models
│   │   └── main.py   # FastAPI app
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/          # Next.js application
│   ├── app/          # Pages and routes
│   ├── lib/          # Utilities and API clients
│   └── types/        # TypeScript types
│
├── infra/
│   ├── supabase/     # Database migrations and RLS
│   ├── fly/          # Fly.io configuration
│   └── vercel.json   # Vercel configuration
│
└── DEPLOYMENT.md     # Complete deployment guide
```

## 🚀 Quick Start

See [DEPLOYMENT.md](./DEPLOYMENT.md) for complete deployment instructions.

### Prerequisites

1. Supabase project
2. Dodo Payments account
3. Fly.io account
4. Vercel account
5. Domain name (optional)

### Deployment Steps

1. **Setup Supabase**: Run migrations and configure auth
2. **Setup Dodo Payments**: Create products and configure webhooks
3. **Deploy Backend**: Deploy to Fly.io
4. **Deploy Frontend**: Deploy to Vercel
5. **Configure DNS**: Point domains
6. **Test**: Verify all functionality

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed steps.

## 🔑 Key Features

- ✅ Multi-tenant organizations with role-based access
- ✅ Dodo Payments subscription billing with webhooks
- ✅ Usage tracking and limits per plan
- ✅ AI-powered brief generation
- ✅ Complete authentication (email + Google OAuth)
- ✅ Row-level security in database
- ✅ Production-ready error handling
- ✅ Audit logging
- ✅ Admin metrics

## 📊 Database Schema

- `organizations` - Organization/tenant data
- `org_members` - User-org relationships with roles
- `subscriptions` - Dodo Payments subscription tracking
- `briefs` - Generated intelligence briefs
- `usage_events` - Usage tracking for billing
- `audit_logs` - Compliance and security logs

## 🔐 Security

- JWT authentication via Supabase
- Row-level security (RLS) policies
- Role-based access control (admin, analyst, viewer)
- Organization isolation
- Secure API endpoints
- HTTPS enforced

## 💳 Billing Plans

- **Starter**: Free, 10 briefs/month
- **Pro**: $99/month, 100 briefs/month
- **Enterprise**: Custom pricing, unlimited

## 📝 API Endpoints

- `POST /briefs/generate` - Generate new brief
- `GET /briefs` - List briefs
- `GET /briefs/{id}` - Get brief details
- `GET /usage` - Get usage statistics
- `POST /dodo/create-checkout` - Create checkout session
- `POST /dodo/webhook` - Handle Dodo Payments webhooks
- `GET /admin/metrics` - Admin metrics

## 🛠️ Development

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## 📄 License

Copyright © 2025 Nexora Intelligence. All rights reserved.

## 🆘 Support

For deployment help, see [DEPLOYMENT.md](./DEPLOYMENT.md).

