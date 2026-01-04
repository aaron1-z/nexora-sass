# Nexora SaaS - Complete Project Structure

## Directory Layout

```
nexora-saas/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py            # FastAPI application entry point
│   │   ├── config.py          # Configuration and settings
│   │   ├── dependencies.py    # Auth middleware and dependencies
│   │   │
│   │   ├── api/               # API endpoints
│   │   │   ├── __init__.py
│   │   │   ├── briefs.py      # Brief generation and management
│   │   │   ├── usage.py       # Usage statistics
│   │   │   ├── stripe.py      # Stripe billing endpoints
│   │   │   └── admin.py       # Admin metrics
│   │   │
│   │   ├── models/            # Pydantic models
│   │   │   ├── __init__.py
│   │   │   ├── brief.py       # Brief request/response models
│   │   │   └── subscription.py # Subscription models
│   │   │
│   │   ├── services/          # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── engine.py      # AI engine wrapper
│   │   │   ├── supabase.py    # Supabase helpers
│   │   │   ├── stripe.py      # Stripe integration
│   │   │   └── usage.py       # Usage tracking
│   │   │
│   │   └── utils/             # Utilities
│   │       ├── __init__.py
│   │       └── logging.py     # Logging configuration
│   │
│   ├── engine/                # AI Engine (copy or symlink from existing)
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile             # Docker configuration for Fly.io
│   └── .env.example           # Environment variables template
│
├── frontend/                   # Next.js Frontend
│   ├── app/
│   │   ├── layout.tsx         # Root layout
│   │   ├── page.tsx           # Landing page
│   │   ├── globals.css        # Global styles
│   │   │
│   │   ├── (auth)/            # Auth routes (login/signup)
│   │   │   ├── login/
│   │   │   │   └── page.tsx
│   │   │   └── signup/
│   │   │       └── page.tsx
│   │   │
│   │   ├── (dashboard)/       # Protected dashboard routes
│   │   │   ├── layout.tsx     # Dashboard layout with nav
│   │   │   ├── dashboard/
│   │   │   │   └── page.tsx   # Dashboard home
│   │   │   ├── briefs/
│   │   │   │   ├── page.tsx   # Briefs list
│   │   │   │   └── [id]/
│   │   │   │       └── page.tsx # Brief detail
│   │   │   ├── billing/
│   │   │   │   └── page.tsx   # Billing and plans
│   │   │   └── settings/
│   │   │       └── page.tsx   # User settings
│   │   │
│   │   ├── pricing/
│   │   │   └── page.tsx       # Public pricing page
│   │   │
│   │   └── api/
│   │       └── auth/
│   │           └── callback/
│   │               └── route.ts # OAuth callback
│   │
│   ├── lib/
│   │   ├── supabase/
│   │   │   └── client.ts      # Supabase client
│   │   ├── api.ts             # API client functions
│   │   └── utils.ts           # Utility functions
│   │
│   ├── types/
│   │   └── index.ts           # TypeScript types
│   │
│   ├── package.json           # NPM dependencies
│   ├── next.config.js         # Next.js configuration
│   ├── tailwind.config.ts     # Tailwind CSS configuration
│   ├── tsconfig.json          # TypeScript configuration
│   └── .env.example           # Environment variables template
│
├── infra/
│   ├── supabase/
│   │   ├── migrations/
│   │   │   └── 001_initial_schema.sql  # Database schema
│   │   └── rls_policies.sql            # Row-level security policies
│   │
│   ├── fly/
│   │   └── fly.toml           # Fly.io configuration
│   │
│   └── vercel.json            # Vercel configuration
│
├── scripts/
│   └── setup-env.sh           # Environment setup helper
│
├── DEPLOYMENT.md              # Complete deployment guide
├── README.md                  # Project overview
└── PROJECT_STRUCTURE.md       # This file
```

## File Descriptions

### Backend

#### Core Files
- `app/main.py` - FastAPI application setup, CORS, route registration
- `app/config.py` - Settings management using pydantic-settings
- `app/dependencies.py` - Authentication middleware, org resolution, role checks

#### API Endpoints
- `app/api/briefs.py` - Brief generation, listing, retrieval
- `app/api/usage.py` - Usage statistics endpoint
- `app/api/dodo.py` - Dodo Payments checkout and webhook handling
- `app/api/admin.py` - Admin metrics endpoint

#### Services
- `app/services/engine.py` - Wraps AI engine with async execution, timeouts, error handling
- `app/services/supabase.py` - Supabase database helpers, usage checks, audit logging
- `app/services/dodo.py` - Dodo Payments integration (checkout, webhooks, customer management)
- `app/services/usage.py` - Usage tracking and statistics

#### Models
- `app/models/brief.py` - Brief request/response schemas
- `app/models/subscription.py` - Subscription and usage schemas

### Frontend

#### Pages
- `app/page.tsx` - Landing page with hero, features, CTA
- `app/(auth)/login/page.tsx` - Email + Google login
- `app/(auth)/signup/page.tsx` - Email + Google signup
- `app/(dashboard)/dashboard/page.tsx` - Dashboard with usage stats and recent briefs
- `app/(dashboard)/briefs/page.tsx` - Briefs list with generation form
- `app/(dashboard)/briefs/[id]/page.tsx` - Brief detail view
- `app/(dashboard)/billing/page.tsx` - Billing, plans, upgrade flow
- `app/(dashboard)/settings/page.tsx` - User settings
- `app/pricing/page.tsx` - Public pricing page

#### Utilities
- `lib/supabase/client.ts` - Supabase client initialization
- `lib/api.ts` - API client with auth interceptors
- `lib/utils.ts` - Helper functions (cn, formatDate, etc.)
- `types/index.ts` - TypeScript type definitions

### Infrastructure

#### Database
- `infra/supabase/migrations/001_initial_schema.sql` - Complete database schema
  - Tables: organizations, org_members, subscriptions, briefs, usage_events, audit_logs
  - Indexes, triggers, functions
  - Auto-org creation on signup

- `infra/supabase/rls_policies.sql` - Row-level security policies
  - Org isolation
  - Role-based access (admin, analyst, viewer)
  - Usage limit checking function

#### Deployment
- `infra/fly/fly.toml` - Fly.io configuration
- `infra/vercel.json` - Vercel configuration

## Key Design Decisions

1. **Multi-tenancy**: Organizations with role-based access control
2. **Authentication**: Supabase Auth with JWT tokens
3. **Billing**: Dodo Payments subscriptions with webhook-based updates
4. **Usage Tracking**: Event-based system with plan limits
5. **Security**: RLS policies, org isolation, role enforcement
6. **Error Handling**: Comprehensive error handling at all layers
7. **Logging**: Audit logs for compliance
8. **Scalability**: Async execution, timeouts, connection pooling

## Next Steps After Deployment

1. Set up monitoring (Sentry, Datadog, etc.)
2. Configure analytics (PostHog, Mixpanel)
3. Set up backups (Supabase daily backups)
4. Configure email notifications
5. Set up rate limiting
6. Create admin dashboard
7. Add CI/CD pipelines
8. Set up staging environment

