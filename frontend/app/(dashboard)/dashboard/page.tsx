'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { supabase } from '@/lib/supabase/client'
import { briefsApi, usageApi } from '@/lib/api'
import Link from 'next/link'
import type { Brief, Usage } from '@/types'

export default function DashboardPage() {
  const router = useRouter()
  const [orgId, setOrgId] = useState<string | null>(null)
  const [briefs, setBriefs] = useState<Brief[]>([])
  const [usage, setUsage] = useState<Usage | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadData()
  }, [])

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

        // Load briefs
        const briefsData = await briefsApi.list(org, 1, 5)
        setBriefs(briefsData.briefs || [])

        // Load usage
        const usageData = await usageApi.get(org)
        setUsage(usageData)
      }
    } catch (error) {
      console.error('Error loading dashboard:', error)
    } finally {
      setLoading(false)
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
          Dashboard
        </h1>
        <p className="text-gray-400 text-lg">Welcome back! Here's your overview.</p>
      </div>

      {/* Stats Grid */}
      <div className="grid md:grid-cols-3 gap-6 mb-8">
        {/* Available Credits */}
        <div className="bg-gradient-to-br from-blue-900/30 to-blue-800/30 backdrop-blur-sm rounded-xl p-6 border border-blue-700/50 shadow-xl">
          <div className="flex items-center justify-between mb-4">
            <div className="p-3 bg-blue-500/20 rounded-lg">
              <svg className="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
          <div className="text-3xl font-bold text-white mb-1">{availableCredits}</div>
          <div className="text-gray-400 text-sm">Available Credits</div>
          {availableCredits === 0 && (
            <Link href="/billing" className="text-blue-400 hover:text-blue-300 text-sm mt-2 inline-block">
              Purchase credits →
            </Link>
          )}
        </div>

        {/* Briefs Generated */}
        <div className="bg-gradient-to-br from-purple-900/30 to-purple-800/30 backdrop-blur-sm rounded-xl p-6 border border-purple-700/50 shadow-xl">
          <div className="flex items-center justify-between mb-4">
            <div className="p-3 bg-purple-500/20 rounded-lg">
              <svg className="w-6 h-6 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
          </div>
          <div className="text-3xl font-bold text-white mb-1">{usage?.briefs_used || 0}</div>
          <div className="text-gray-400 text-sm">Briefs Generated</div>
        </div>

        {/* Total Purchased */}
        <div className="bg-gradient-to-br from-green-900/30 to-green-800/30 backdrop-blur-sm rounded-xl p-6 border border-green-700/50 shadow-xl">
          <div className="flex items-center justify-between mb-4">
            <div className="p-3 bg-green-500/20 rounded-lg">
              <svg className="w-6 h-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
          <div className="text-3xl font-bold text-white mb-1">{usage?.briefs_limit || 0}</div>
          <div className="text-gray-400 text-sm">Total Purchased</div>
        </div>
      </div>

      {/* Usage Progress */}
      {usage && usage.briefs_limit > 0 && (
        <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 mb-8 border border-gray-700/50 shadow-xl">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold">Credit Usage</h2>
            <span className="text-sm text-gray-400">
              {usage.briefs_used} of {usage.briefs_limit} used
            </span>
          </div>
          <div className="w-full bg-gray-700/50 rounded-full h-4 overflow-hidden">
            <div
              className="bg-gradient-to-r from-blue-500 to-purple-500 h-4 rounded-full transition-all duration-300"
              style={{ width: `${Math.min(usage.usage_percentage, 100)}%` }}
            ></div>
          </div>
          <div className="mt-2 text-sm text-gray-400">
            {availableCredits} credit{availableCredits !== 1 ? 's' : ''} remaining
          </div>
        </div>
      )}

      {/* Recent Briefs */}
      <div className="mb-8">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-semibold">Recent Briefs</h2>
          <Link
            href="/briefs"
            className="text-blue-400 hover:text-blue-300 font-semibold flex items-center gap-1"
          >
            View All
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </Link>
        </div>

        {briefs.length === 0 ? (
          <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-12 text-center border border-gray-700/50">
            <svg className="w-16 h-16 text-gray-600 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <p className="text-gray-400 mb-4 text-lg">No briefs yet</p>
            <p className="text-gray-500 mb-6">Generate your first intelligence brief to get started</p>
            <Link
              href="/briefs"
              className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-3 rounded-lg font-semibold hover:from-blue-700 hover:to-purple-700 inline-block transition-all shadow-lg hover:shadow-xl"
            >
              Generate Your First Brief
            </Link>
          </div>
        ) : (
          <div className="space-y-4">
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
                  </div>
                </div>
                <p className="text-gray-400 text-sm mb-4 line-clamp-2">
                  {brief.output_data.executive_summary?.substring(0, 150) || 'No summary available'}...
                </p>
                <div className="flex justify-between text-sm text-gray-500">
                  <span>{new Date(brief.created_at).toLocaleDateString('en-US', { 
                    year: 'numeric', 
                    month: 'short', 
                    day: 'numeric' 
                  })}</span>
                  <span className="text-blue-400 hover:text-blue-300">View details →</span>
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>

      {/* Quick Actions */}
      <div className="grid md:grid-cols-2 gap-6">
        <Link
          href="/briefs"
          className="bg-gradient-to-r from-blue-600/20 to-purple-600/20 backdrop-blur-sm rounded-xl p-6 border border-blue-700/50 hover:border-blue-500/50 transition-all group"
        >
          <div className="flex items-center gap-4">
            <div className="p-3 bg-blue-500/20 rounded-lg group-hover:bg-blue-500/30 transition-all">
              <svg className="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
              </svg>
            </div>
            <div>
              <h3 className="font-semibold text-white mb-1">Generate New Brief</h3>
              <p className="text-sm text-gray-400">Create a new intelligence brief</p>
            </div>
          </div>
        </Link>

        <Link
          href="/billing"
          className="bg-gradient-to-r from-purple-600/20 to-pink-600/20 backdrop-blur-sm rounded-xl p-6 border border-purple-700/50 hover:border-purple-500/50 transition-all group"
        >
          <div className="flex items-center gap-4">
            <div className="p-3 bg-purple-500/20 rounded-lg group-hover:bg-purple-500/30 transition-all">
              <svg className="w-6 h-6 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
              </svg>
            </div>
            <div>
              <h3 className="font-semibold text-white mb-1">Purchase Credits</h3>
              <p className="text-sm text-gray-400">Buy credits to generate briefs</p>
            </div>
          </div>
        </Link>
      </div>
    </div>
  )
}
