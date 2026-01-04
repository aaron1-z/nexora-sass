#!/bin/bash
# Setup script for Nexora SaaS
# This script helps set up environment variables

echo "Nexora SaaS - Environment Setup"
echo "================================"
echo ""

# Check if .env files exist
if [ ! -f "backend/.env" ]; then
    echo "Creating backend/.env from template..."
    cp backend/.env.example backend/.env 2>/dev/null || echo "Backend .env.example not found"
    echo "⚠️  Please edit backend/.env with your actual values"
fi

if [ ! -f "frontend/.env.local" ]; then
    echo "Creating frontend/.env.local from template..."
    cp frontend/.env.example frontend/.env.local 2>/dev/null || echo "Frontend .env.example not found"
    echo "⚠️  Please edit frontend/.env.local with your actual values"
fi

echo ""
echo "Next steps:"
echo "1. Edit backend/.env with your Supabase and Stripe keys"
echo "2. Edit frontend/.env.local with your Supabase and Stripe keys"
echo "3. Run database migrations in Supabase"
echo "4. Deploy backend to Fly.io"
echo "5. Deploy frontend to Vercel"
echo ""
echo "See DEPLOYMENT.md for complete instructions"

