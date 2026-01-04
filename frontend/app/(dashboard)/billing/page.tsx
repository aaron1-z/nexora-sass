'use client'

import { useEffect, useState } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { supabase } from '@/lib/supabase/client'
import { dodoApi, usageApi } from '@/lib/api'
import type { Usage } from '@/types'
import Link from 'next/link'

export default function BillingPage() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const [orgId, setOrgId] = useState<string | null>(null)
  const [usage, setUsage] = useState<Usage | null>(null)
  const [loading, setLoading] = useState(true)
  const [processingPayment, setProcessingPayment] = useState(false)
  const [pricePerBrief, setPricePerBrief] = useState(3.00)

  useEffect(() => {
    const loadData = async () => {
      try {
        const {
          data: { session },
        } = await supabase.auth.getSession()
        if (!session) {
          router.push('/login')
          return
        }

        const { data: memberships } = await supabase
          .from('org_members')
          .select('org_id')
          .eq('user_id', session.user.id)
          .limit(1)
          .single()

        if (memberships) {
          const org = memberships.org_id
          setOrgId(org)

          const usageData = await usageApi.get(org)
          setUsage(usageData)
        }
      } catch (error) {
        console.error('Error loading billing:', error)
      } finally {
        setLoading(false)
      }
    }

    loadData()
    
    // Check for payment success redirect
    if (searchParams?.get('payment') === 'success') {
      // Reload data after a delay to allow webhook to process
      setTimeout(() => {
        loadData()
      }, 2000)
    }
  }, [searchParams, router])

  useEffect(() => {
    const fetchPrice = async () => {
      try {
        const { briefsApi } = await import('@/lib/api')
        const status = await briefsApi.checkPaymentStatus()
        if (status.price_per_brief) {
          setPricePerBrief(status.price_per_brief)
        }
      } catch (error) {
        console.error('Failed to fetch price:', error)
        // Default to 3.00 if fetch fails
      }
    }
    if (orgId) {
      fetchPrice()
    }
  }, [orgId])


  const handlePurchaseBrief = async () => {
    if (!orgId) return

    setProcessingPayment(true)
    try {
      const { checkout_url } = await dodoApi.createCheckout()
      window.location.href = checkout_url
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || error.response?.data?.message || error.message || 'Failed to create checkout session'
      const errorString = typeof errorMessage === 'string' ? errorMessage : JSON.stringify(errorMessage)
      alert(errorString)
      console.error('Checkout error:', error)
      setProcessingPayment(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-white text-lg">Loading...</div>
      </div>
    )
  }

  const availableCredits = usage ? (usage.briefs_limit - usage.briefs_used) : 0

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
          Billing & Credits
        </h1>
        <p className="text-gray-400 text-lg">Purchase credits to generate intelligence briefs</p>
      </div>

      {/* Credit Status Card */}
      {usage && (
        <div className="bg-gradient-to-br from-gray-800/50 to-gray-900/50 backdrop-blur-sm rounded-2xl p-8 mb-8 border border-gray-700/50 shadow-xl">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h2 className="text-2xl font-semibold mb-2">Your Credits</h2>
              <p className="text-gray-400">Pay-per-brief model • One-time payments</p>
            </div>
            <div className="text-right">
              <div className="text-5xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
                {availableCredits}
              </div>
              <div className="text-gray-400 text-sm mt-1">
                {availableCredits === 1 ? 'Credit' : 'Credits'} Available
              </div>
            </div>
          </div>

          <div className="grid md:grid-cols-3 gap-6 mb-6">
            <div className="bg-gray-900/50 rounded-lg p-4 border border-gray-700/50">
              <div className="text-sm text-gray-400 mb-1">Total Purchased</div>
              <div className="text-2xl font-bold text-white">{usage.briefs_limit}</div>
            </div>
            <div className="bg-gray-900/50 rounded-lg p-4 border border-gray-700/50">
              <div className="text-sm text-gray-400 mb-1">Briefs Generated</div>
              <div className="text-2xl font-bold text-white">{usage.briefs_used}</div>
            </div>
            <div className="bg-gray-900/50 rounded-lg p-4 border border-gray-700/50">
              <div className="text-sm text-gray-400 mb-1">Price per Brief</div>
              <div className="text-2xl font-bold text-green-400">${pricePerBrief}</div>
            </div>
          </div>

          {usage.briefs_limit > 0 && (
            <div>
              <div className="flex justify-between text-sm mb-2">
                <span className="text-gray-400">Usage Progress</span>
                <span className="text-gray-400">{Math.round(usage.usage_percentage)}%</span>
              </div>
              <div className="w-full bg-gray-700/50 rounded-full h-3 overflow-hidden">
                <div
                  className="bg-gradient-to-r from-blue-500 to-purple-500 h-3 rounded-full transition-all duration-300"
                  style={{ width: `${Math.min(usage.usage_percentage, 100)}%` }}
                ></div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Purchase Card */}
      <div className="bg-gradient-to-br from-gray-800/50 to-gray-900/50 backdrop-blur-sm rounded-2xl p-10 border border-gray-700/50 shadow-xl">
        <div className="text-center max-w-2xl mx-auto">
          <div className="mb-6">
            <h2 className="text-3xl font-bold mb-2">Purchase Brief Credit</h2>
            <p className="text-gray-400">One-time payment • No subscription required</p>
          </div>

          <div className="mb-8">
            <div className="inline-block bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-8 mb-6 shadow-2xl">
              <div className="text-6xl font-bold text-white mb-2">${pricePerBrief}</div>
              <div className="text-gray-200 text-lg">per intelligence brief</div>
            </div>
          </div>

          <div className="bg-gray-900/50 rounded-xl p-8 mb-8 text-left border border-gray-700/50">
            <h3 className="text-xl font-semibold mb-6 text-center">What you get:</h3>
            <div className="grid md:grid-cols-2 gap-4">
              <div className="flex items-start gap-3">
                <svg className="w-6 h-6 text-green-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                <div>
                  <div className="font-semibold text-white">Comprehensive Intelligence Brief</div>
                  <div className="text-sm text-gray-400">Full strategic analysis and insights</div>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <svg className="w-6 h-6 text-green-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                <div>
                  <div className="font-semibold text-white">Scenario Analysis</div>
                  <div className="text-sm text-gray-400">Multiple outcome scenarios with probabilities</div>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <svg className="w-6 h-6 text-green-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                <div>
                  <div className="font-semibold text-white">Action Plans</div>
                  <div className="text-sm text-gray-400">Strategic recommendations and next steps</div>
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
              <div className="flex items-start gap-3 md:col-span-2">
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

          <button
            onClick={handlePurchaseBrief}
            disabled={processingPayment}
            className="w-full md:w-auto bg-gradient-to-r from-blue-600 to-purple-600 text-white px-12 py-4 rounded-xl text-lg font-semibold hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-2xl hover:shadow-blue-500/50 mb-4"
          >
            {processingPayment ? (
              <span className="flex items-center justify-center gap-2">
                <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Processing...
              </span>
            ) : (
              `Purchase Credit - $${pricePerBrief}`
            )}
          </button>

          <div className="flex items-center justify-center gap-2 text-sm text-gray-500 mt-4">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
            <span>Secure payment via Dodo Payments • One-time payment • No subscription</span>
          </div>
        </div>
      </div>

      {/* Quick Links */}
      {availableCredits > 0 && (
        <div className="mt-8 text-center">
          <Link
            href="/briefs"
            className="inline-flex items-center gap-2 text-blue-400 hover:text-blue-300 font-semibold"
          >
            <span>Generate a brief with your credits</span>
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </Link>
        </div>
      )}
    </div>
  )
}
