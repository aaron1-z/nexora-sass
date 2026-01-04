export interface Brief {
  id: string
  org_id: string
  user_id: string
  title: string
  query: string
  output_data: {
    executive_summary?: string
    immediate_impact?: string
    scenarios?: Array<{
      name: string
      prob: number
      path: string[]
      signals: string[]
    }>
    actions?: Array<{
      title: string
      rationale?: string
      steps: string[]
      impact_score: number
    }>
    watch_triggers?: string[]
    confidence?: string
  }
  confidence?: string
  execution_time_ms?: number
  cost_usd?: number
  status: string
  created_at: string
}

export interface Usage {
  org_id: string
  plan: string
  current_period_start?: string
  briefs_used: number
  briefs_limit: number
  usage_percentage: number
}

export interface Organization {
  id: string
  name: string
  slug: string
  plan: string
  subscription_status: string
}

