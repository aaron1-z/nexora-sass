/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  env: {
    NEXT_PUBLIC_SUPABASE_URL: process.env.NEXT_PUBLIC_SUPABASE_URL,
    NEXT_PUBLIC_SUPABASE_ANON_KEY: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY,
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'https://api.nexora.io',
    NEXT_PUBLIC_DODO_PRODUCT_STARTER: process.env.NEXT_PUBLIC_DODO_PRODUCT_STARTER,
    NEXT_PUBLIC_DODO_PRODUCT_PRO: process.env.NEXT_PUBLIC_DODO_PRODUCT_PRO,
  },
}

module.exports = nextConfig

