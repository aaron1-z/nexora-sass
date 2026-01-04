'use client'

import { useEffect, useState } from 'react'
import { useRouter, useParams } from 'next/navigation'
import { briefsApi } from '@/lib/api'
import type { Brief } from '@/types'
import Link from 'next/link'

export default function BriefDetailPage() {
  const router = useRouter()
  const params = useParams()
  const [brief, setBrief] = useState<Brief | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadBrief()
  }, [params.id])

  const loadBrief = async () => {
    try {
      const data = await briefsApi.get(params.id as string)
      setBrief(data)
    } catch (error) {
      console.error('Error loading brief:', error)
      router.push('/briefs')
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

  if (!brief) {
    return (
      <div className="text-center py-12">
        <div className="text-white text-lg mb-4">Brief not found</div>
        <Link href="/briefs" className="text-blue-400 hover:text-blue-300">
          ← Back to Briefs
        </Link>
      </div>
    )
  }

  const { output_data } = brief

  return (
    <div className="max-w-5xl mx-auto">
      <Link
        href="/briefs"
        className="inline-flex items-center gap-2 text-blue-400 hover:text-blue-300 mb-6 transition-colors"
      >
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        Back to Briefs
      </Link>

      <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-8 border border-gray-700/50 shadow-xl">
        <div className="mb-6 pb-6 border-b border-gray-700/50">
          <div className="flex items-start justify-between mb-4">
            <h1 className="text-4xl font-bold text-white flex-1 pr-4">{brief.title}</h1>
            <div className="flex items-center gap-2 flex-shrink-0">
              {brief.confidence && (
                <span className={`px-4 py-2 rounded-full text-sm font-semibold ${
                  brief.confidence === 'High' ? 'bg-green-500/20 text-green-400 border border-green-500/30' :
                  brief.confidence === 'Medium' ? 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/30' :
                  'bg-gray-500/20 text-gray-400 border border-gray-500/30'
                }`}>
                  {brief.confidence} Confidence
                </span>
              )}
              <span className="px-4 py-2 rounded-full bg-blue-500/20 text-blue-400 text-sm font-semibold border border-blue-500/30">
                {brief.status}
              </span>
            </div>
          </div>
          <div className="flex items-center gap-4 text-sm text-gray-400">
            <span>{new Date(brief.created_at).toLocaleDateString('en-US', { 
              year: 'numeric', 
              month: 'long', 
              day: 'numeric',
              hour: '2-digit',
              minute: '2-digit'
            })}</span>
            {brief.execution_time_ms && (
              <span>• Generated in {(brief.execution_time_ms / 1000).toFixed(1)}s</span>
            )}
            {brief.cost_usd && (
              <span>• ${brief.cost_usd.toFixed(2)}</span>
            )}
          </div>
        </div>

        {output_data.executive_summary && (
          <section className="mb-10">
            <h2 className="text-2xl font-semibold mb-4 text-white">Executive Summary</h2>
            <div className="bg-gray-900/50 rounded-lg p-6 border border-gray-700/50">
              <p className="text-gray-300 leading-relaxed text-lg whitespace-pre-wrap">{output_data.executive_summary}</p>
            </div>
          </section>
        )}

        {output_data.immediate_impact && (
          <section className="mb-10">
            <h2 className="text-2xl font-semibold mb-4 text-white">Immediate Impact</h2>
            <div className="bg-gray-900/50 rounded-lg p-6 border border-gray-700/50">
              <p className="text-gray-300 leading-relaxed text-lg whitespace-pre-wrap">{output_data.immediate_impact}</p>
            </div>
          </section>
        )}

        {output_data.scenarios && output_data.scenarios.length > 0 && (
          <section className="mb-10">
            <h2 className="text-2xl font-semibold mb-6 text-white">Scenario Analysis</h2>
            <div className="space-y-6">
              {output_data.scenarios.map((scenario, idx) => (
                <div key={idx} className="bg-gray-900/50 rounded-xl p-6 border border-gray-700/50">
                  <div className="flex justify-between items-start mb-4">
                    <h3 className="text-xl font-semibold text-white">{scenario.name}</h3>
                    <span className="px-4 py-2 bg-blue-500/20 text-blue-400 rounded-full text-sm font-semibold border border-blue-500/30">
                    {scenario.prob}% probability
                    </span>
                  </div>
                  {scenario.path && scenario.path.length > 0 && (
                    <div className="mb-4">
                      <h4 className="font-semibold mb-3 text-gray-300">Path:</h4>
                      <ul className="space-y-2">
                        {scenario.path.map((step, i) => (
                          <li key={i} className="flex items-start gap-3 text-gray-300">
                            <span className="text-blue-400 mt-1">→</span>
                            <span>{step}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                  {scenario.signals && scenario.signals.length > 0 && (
                    <div>
                      <h4 className="font-semibold mb-3 text-gray-300">Key Signals:</h4>
                      <div className="flex flex-wrap gap-2">
                        {scenario.signals.map((signal, i) => (
                          <span key={i} className="px-3 py-1 bg-purple-500/20 text-purple-300 rounded-full text-sm border border-purple-500/30">
                            {signal}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </section>
        )}

        {output_data.actions && output_data.actions.length > 0 && (
          <section className="mb-10">
            <h2 className="text-2xl font-semibold mb-6 text-white">Action Plans</h2>
            <div className="space-y-6">
              {output_data.actions.map((action, idx) => (
                <div key={idx} className="bg-gray-900/50 rounded-xl p-6 border border-gray-700/50">
                  <div className="flex justify-between items-start mb-4">
                    <h3 className="text-xl font-semibold text-white">{action.title}</h3>
                    <div className="flex items-center gap-2">
                      <span className="px-4 py-2 bg-green-500/20 text-green-400 rounded-full text-sm font-semibold border border-green-500/30">
                        Impact: {action.impact_score}/5
                      </span>
                    </div>
                  </div>
                  {action.rationale && (
                    <p className="text-gray-300 mb-4 leading-relaxed">{action.rationale}</p>
                  )}
                  {action.steps && action.steps.length > 0 && (
                    <div>
                      <h4 className="font-semibold mb-3 text-gray-300">Steps:</h4>
                      <ol className="space-y-3">
                        {action.steps.map((step, i) => (
                          <li key={i} className="flex items-start gap-3 text-gray-300">
                            <span className="flex-shrink-0 w-6 h-6 bg-blue-500/20 text-blue-400 rounded-full flex items-center justify-center text-sm font-semibold border border-blue-500/30">
                              {i + 1}
                            </span>
                            <span className="pt-0.5">{step}</span>
                          </li>
                        ))}
                      </ol>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </section>
        )}

        {output_data.watch_triggers && output_data.watch_triggers.length > 0 && (
          <section>
            <h2 className="text-2xl font-semibold mb-6 text-white">Watch Triggers</h2>
            <div className="bg-gray-900/50 rounded-xl p-6 border border-gray-700/50">
              <ul className="space-y-3">
                {output_data.watch_triggers.map((trigger, idx) => (
                  <li key={idx} className="flex items-start gap-3 text-gray-300">
                    <svg className="w-5 h-5 text-yellow-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                    </svg>
                    <span className="pt-0.5">{trigger}</span>
                  </li>
                ))}
              </ul>
            </div>
          </section>
        )}
      </div>
    </div>
  )
}
