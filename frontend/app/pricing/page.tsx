'use client'

import Link from 'next/link'
import { useEffect, useState } from 'react'
import { supabase } from '@/lib/supabase/client'
import { useRouter } from 'next/navigation'

export default function PricingPage() {
  const router = useRouter()
  const [scrolled, setScrolled] = useState(false)

  useEffect(() => {
    // Handle scroll for navbar
    const handleScroll = () => {
      setScrolled(window.scrollY > 20)
    }
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-black text-white">
      <div className="container mx-auto px-4 py-32">
        <nav className="flex justify-between items-center mb-16">
          <Link href="/" className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
            Nexora
          </Link>
          <div className="space-x-4">
            <Link href="/login" className="text-gray-300 hover:text-white">
              Sign In
            </Link>
            <Link
              href="/signup"
              className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-all"
            >
              Get Started
            </Link>
          </div>
        </nav>

        <div className="text-center max-w-4xl mx-auto mb-20">
          <h1 className="text-5xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
            Simple, Transparent Pricing
          </h1>
          <p className="text-xl text-gray-300 mb-4">
            Pay per brief. No subscriptions. No hidden fees.
          </p>
          <p className="text-lg text-gray-400">
            Generate intelligence briefs on-demand at $3.00 each
          </p>
        </div>

        {/* Pricing Card */}
        <div className="max-w-2xl mx-auto">
          <div className="bg-gradient-to-br from-gray-800/50 to-gray-900/50 backdrop-blur-sm rounded-2xl p-10 border-2 border-blue-500/50 shadow-2xl">
            <div className="text-center mb-8">
              <div className="inline-block bg-blue-500/20 px-4 py-2 rounded-full mb-4">
                <span className="text-blue-400 font-semibold">Pay Per Brief</span>
              </div>
              <div className="mb-4">
                <span className="text-6xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
                  $3.00
                </span>
              </div>
              <p className="text-xl text-gray-300 mb-2">per intelligence brief</p>
              <p className="text-gray-400">One-time payment • No subscription required</p>
            </div>

            <div className="bg-gray-900/50 rounded-xl p-6 mb-8 border border-gray-700/50">
              <h3 className="font-semibold text-lg mb-4 text-center">What's included:</h3>
              <div className="space-y-4">
                <div className="flex items-start gap-3">
                  <svg className="w-6 h-6 text-green-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <div>
                    <div className="font-semibold text-white">Comprehensive Intelligence Brief</div>
                    <div className="text-sm text-gray-400">Full strategic analysis with executive summary</div>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <svg className="w-6 h-6 text-green-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <div>
                    <div className="font-semibold text-white">Scenario Analysis</div>
                    <div className="text-sm text-gray-400">Multiple outcome scenarios with probability assessments</div>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <svg className="w-6 h-6 text-green-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <div>
                    <div className="font-semibold text-white">Action Plans</div>
                    <div className="text-sm text-gray-400">Strategic recommendations with step-by-step guidance</div>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <svg className="w-6 h-6 text-green-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <div>
                    <div className="font-semibold text-white">Watch Triggers</div>
                    <div className="text-sm text-gray-400">Key signals and indicators to monitor</div>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <svg className="w-6 h-6 text-green-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <div>
                    <div className="font-semibold text-white">Lifetime Access</div>
                    <div className="text-sm text-gray-400">Full access to your generated brief forever</div>
                  </div>
                </div>
              </div>
            </div>

            <div className="text-center">
              <Link
                href="/signup"
                className="inline-block w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 py-4 rounded-xl text-lg font-semibold hover:from-blue-700 hover:to-purple-700 transition-all shadow-2xl hover:shadow-blue-500/50 mb-4"
              >
                Get Started
              </Link>
              <p className="text-sm text-gray-400">
                Secure payment via Dodo Payments • No credit card required to sign up
              </p>
            </div>
          </div>

          {/* FAQ Section */}
          <div className="mt-16">
            <h2 className="text-3xl font-bold text-center mb-12">Frequently Asked Questions</h2>
            <div className="space-y-6">
              <div className="bg-gray-800/30 rounded-xl p-6 border border-gray-700/50">
                <h3 className="font-semibold text-lg mb-2">How does pay-per-brief work?</h3>
                <p className="text-gray-400">
                  You purchase credits for $3.00 each. Each credit allows you to generate one intelligence brief. 
                  Credits don't expire and can be used anytime.
                </p>
              </div>
              <div className="bg-gray-800/30 rounded-xl p-6 border border-gray-700/50">
                <h3 className="font-semibold text-lg mb-2">Do I need a subscription?</h3>
                <p className="text-gray-400">
                  No! We use a pay-per-brief model. You only pay when you need a brief. No monthly fees, 
                  no subscriptions, no commitments.
                </p>
              </div>
              <div className="bg-gray-800/30 rounded-xl p-6 border border-gray-700/50">
                <h3 className="font-semibold text-lg mb-2">Can I purchase multiple credits at once?</h3>
                <p className="text-gray-400">
                  Currently, each purchase is for one credit ($3.00). You can purchase as many credits as you need, 
                  whenever you need them.
                </p>
              </div>
              <div className="bg-gray-800/30 rounded-xl p-6 border border-gray-700/50">
                <h3 className="font-semibold text-lg mb-2">What payment methods do you accept?</h3>
                <p className="text-gray-400">
                  We accept all major payment methods through Dodo Payments, including credit cards, debit cards, 
                  and other secure payment options.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
