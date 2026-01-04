import axios from 'axios'
import { supabase } from './supabase/client'

const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'https://api.nexora.io'

const api = axios.create({
  baseURL: apiUrl,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add auth token to requests
api.interceptors.request.use(async (config) => {
  const { data: { session } } = await supabase.auth.getSession()
  if (session?.access_token) {
    config.headers.Authorization = `Bearer ${session.access_token}`
  }
  return config
})

export default api

export const briefsApi = {
  generate: async (query: string, orgId: string, metadata?: any) => {
    // org_id is optional in backend (comes from auth context)
    const response = await api.post('/briefs/generate', {
      query,
      metadata,
    })
    return response.data
  },
  
  list: async (orgId: string, page = 1, pageSize = 20) => {
    // org_id comes from auth context, not query param
    const response = await api.get('/briefs', {
      params: { page, page_size: pageSize },
    })
    return response.data
  },
  
  get: async (briefId: string) => {
    const response = await api.get(`/briefs/${briefId}`)
    return response.data
  },
  
  checkPaymentStatus: async () => {
    const response = await api.get('/briefs/payment-status')
    return response.data
  },
}

export const usageApi = {
  get: async (orgId: string) => {
    // org_id comes from auth context, not query param
    const response = await api.get('/usage')
    return response.data
  },
}

export const dodoApi = {
  createCheckout: async () => {
    const response = await api.post('/dodo/create-checkout')
    return response.data
  },
}

export const adminApi = {
  getMetrics: async () => {
    const response = await api.get('/admin/metrics')
    return response.data
  },
}

export const devApi = {
  grantCredit: async () => {
    const response = await api.post('/dev/grant-credit')
    return response.data
  },
  clearCredits: async () => {
    const response = await api.post('/dev/clear-credits')
    return response.data
  },
}

