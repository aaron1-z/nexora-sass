'use client'

import { useEffect, useState } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { supabase } from '@/lib/supabase/client'
import { briefsApi, dodoApi, devApi } from '@/lib/api'
import Link from 'next/link'
import type { Brief } from '@/types'

interface PaymentStatus {
  has_credit: boolean
  available_credits: number
  price_per_brief: number
  total_paid: number
  total_used: number
}

export default function BriefsPage() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const [orgId, setOrgId] = useState<string | null>(null)
  const [briefs, setBriefs] = useState<Brief[]>([])
  const [query, setQuery] = useState('')
  const [generating, setGenerating] = useState(false)
  const [loading, setLoading] = useState(true)
  const [page, setPage] = useState(1)
  const [total, setTotal] = useState(0)
  const [paymentStatus, setPaymentStatus] = useState<PaymentStatus | null>(null)
  const [processingPayment, setProcessingPayment] = useState(false)

  useEffect(() => {
    loadData()
    
    // Check for payment success
    if (searchParams?.get('payment') === 'success') {
      setTimeout(() => {
        loadData()
      }, 2000) // Wait for webhook to process
    }
  }, [page, searchParams])

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

        // Load payment status
        try {
          const status = await briefsApi.checkPaymentStatus()
          setPaymentStatus(status)
        } catch (error) {
          console.error('Error loading payment status:', error)
        }

        // Load briefs
        const data = await briefsApi.list(org, page, 20)
        setBriefs(data.briefs || [])
        setTotal(data.total || 0)
      }
    } catch (error) {
      console.error('Error loading briefs:', error)
    } finally {
      setLoading(false)
    }
  }

  const handlePurchaseCredit = async () => {
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

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!query.trim() || !orgId) return

    if (!paymentStatus?.has_credit) {
      if (confirm(`You need to purchase a credit ($${paymentStatus?.price_per_brief || 3.00}) to generate a brief. Proceed to payment?`)) {
        await handlePurchaseCredit()
      }
      return
    }

    setGenerating(true)
    try {
      await briefsApi.generate(query, orgId)
      setQuery('')
      await loadData() // Reload to refresh credits and briefs
    } catch (error: any) {
      if (error.response?.status === 402) {
        // Payment required
        if (confirm('Payment required to generate brief. Purchase credit?')) {
          await handlePurchaseCredit()
        }
      } else {
        alert(error.response?.data?.detail || 'Failed to generate brief')
      }
    } finally {
      setGenerating(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-white text-lg">Loading...</div>
      </div>
    )
  }

  const hasCredit = paymentStatus?.has_credit ?? false

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
          Intelligence Briefs
        </h1>
        <p className="text-gray-400 text-lg">Generate comprehensive strategic intelligence reports</p>
      </div>

      {/* Credit Status Banner */}
      {paymentStatus && (
        <div className={`rounded-xl p-6 mb-8 border-2 ${
          hasCredit 
            ? 'bg-gradient-to-r from-green-900/30 to-emerald-900/30 border-green-700/50' 
            : 'bg-gradient-to-r from-yellow-900/30 to-amber-900/30 border-yellow-700/50'
        }`}>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className={`p-3 rounded-full ${hasCredit ? 'bg-green-500/20' : 'bg-yellow-500/20'}`}>
                {hasCredit ? (
                  <svg className="w-6 h-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                ) : (
                  <svg className="w-6 h-6 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                  </svg>
                )}
              </div>
              <div>
                <h3 className={`text-xl font-semibold mb-1 ${hasCredit ? 'text-green-200' : 'text-yellow-200'}`}>
                  {hasCredit ? 'Credits Available' : 'No Credits Available'}
                </h3>
                <p className={`text-sm ${hasCredit ? 'text-green-300' : 'text-yellow-300'}`}>
                  {hasCredit 
                    ? `${paymentStatus.available_credits} credit${paymentStatus.available_credits !== 1 ? 's' : ''} available • $${paymentStatus.price_per_brief} per brief`
                    : `Purchase a credit ($${paymentStatus.price_per_brief}) to generate your first brief`
                  }
                </p>
              </div>
            </div>
            {!hasCredit && (
              <div className="flex gap-2">
                {/* Always show in development - check if localhost */}
                {(typeof window !== 'undefined' && window.location.hostname === 'localhost') && (
                  <button
                    onClick={async () => {
                      try {
                        await devApi.grantCredit()
                        await loadData()
                        alert('✅ Test credit granted! You can now generate a brief.')
                      } catch (error: any) {
                        const errorMessage = error.response?.data?.detail || error.response?.data?.message || error.message || 'Failed to grant test credit'
                        const errorString = typeof errorMessage === 'string' ? errorMessage : JSON.stringify(errorMessage)
                        alert(errorString)
                        console.error('Grant credit error:', error)
                      }
                    }}
                    className="bg-green-600 text-white px-4 py-3 rounded-lg font-semibold hover:bg-green-700 transition-all shadow-lg hover:shadow-xl text-sm"
                    title="Dev only: Grant test credit"
                  >
                    🧪 Grant Test Credit
                  </button>
                )}
                <button
                  onClick={handlePurchaseCredit}
                  disabled={processingPayment}
                  className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-3 rounded-lg font-semibold hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg hover:shadow-xl"
                >
                  {processingPayment ? 'Processing...' : `Purchase Credit - $${paymentStatus.price_per_brief}`}
                </button>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Generation Form */}
      <form onSubmit={handleGenerate} className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 mb-8 border border-gray-700/50 shadow-xl">
        <div className="flex gap-4">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Enter topic or query (e.g., 'AI chips market trends', 'Q4 economic outlook')"
            className="flex-1 bg-gray-900/50 border border-gray-700 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            required
            disabled={generating || !hasCredit}
          />
          <button
            type="submit"
            disabled={generating || !query.trim() || !hasCredit}
            className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 py-3 rounded-lg font-semibold hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg hover:shadow-xl disabled:hover:shadow-lg"
          >
            {generating ? (
              <span className="flex items-center gap-2">
                <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Generating...
              </span>
            ) : (
              `Generate Brief${paymentStatus ? ` ($${paymentStatus.price_per_brief})` : ''}`
            )}
          </button>
        </div>
        {!hasCredit && (
          <p className="text-sm text-gray-400 mt-3">
            <Link href="/billing" className="text-blue-400 hover:text-blue-300 underline">
              Purchase a credit
            </Link>
            {' '}to generate briefs
          </p>
        )}
      </form>

      {/* Briefs List */}
      {briefs.length === 0 ? (
        <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-12 text-center border border-gray-700/50">
          <div className="max-w-md mx-auto">
            <svg className="w-16 h-16 text-gray-600 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <p className="text-gray-400 text-lg mb-2">No briefs yet</p>
            <p className="text-gray-500 mb-6">
              {hasCredit 
                ? "Generate your first intelligence brief above"
                : "Purchase a credit to generate your first brief"
              }
            </p>
            {!hasCredit && (
              <button
                onClick={handlePurchaseCredit}
                className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-3 rounded-lg font-semibold hover:from-blue-700 hover:to-purple-700 transition-all shadow-lg hover:shadow-xl"
              >
                Purchase Credit for ${paymentStatus?.price_per_brief || 3.00}
              </button>
            )}
          </div>
        </div>
      ) : (
        <>
          <div className="space-y-4 mb-8">
            {briefs.map((brief) => (
              <Link
                key={brief.id}
                href={`/briefs/${brief.id}`}
                className="block bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 hover:bg-gray-800/70 border border-gray-700/50 hover:border-blue-500/50 transition-all shadow-lg hover:shadow-xl"
              >
                <div className="flex items-start justify-between mb-3">
                  <h3 className="text-xl font-semibold text-white flex-1">{brief.title}</h3>
                  <div className="flex items-center gap-2 ml-4">
                    {brief.confidence && (
                      <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                        brief.confidence === 'High' ? 'bg-green-500/20 text-green-400' :
                        brief.confidence === 'Medium' ? 'bg-yellow-500/20 text-yellow-400' :
                        'bg-gray-500/20 text-gray-400'
                      }`}>
                        {brief.confidence}
                      </span>
                    )}
                    <span className="px-3 py-1 rounded-full bg-blue-500/20 text-blue-400 text-xs font-semibold">
                      {brief.status}
                    </span>
                  </div>
                </div>
                <p className="text-gray-400 text-sm mb-4 line-clamp-2">
                  {brief.output_data.executive_summary?.substring(0, 200) || 'No summary available'}...
                </p>
                <div className="flex justify-between text-sm text-gray-500">
                  <span>{new Date(brief.created_at).toLocaleDateString('en-US', { 
                    year: 'numeric', 
                    month: 'long', 
                    day: 'numeric' 
                  })}</span>
                  <span className="text-blue-400 hover:text-blue-300">View details →</span>
                </div>
              </Link>
            ))}
          </div>

          {total > 20 && (
            <div className="flex justify-center items-center gap-4">
              <button
                onClick={() => setPage(p => Math.max(1, p - 1))}
                disabled={page === 1}
                className="bg-gray-800 text-white px-6 py-2 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-700 transition-all"
              >
                Previous
              </button>
              <span className="text-gray-400">
                Page {page} of {Math.ceil(total / 20)}
              </span>
              <button
                onClick={() => setPage(p => p + 1)}
                disabled={page * 20 >= total}
                className="bg-gray-800 text-white px-6 py-2 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-700 transition-all"
              >
                Next
              </button>
            </div>
          )}
        </>
      )}
    </div>
  )
}
