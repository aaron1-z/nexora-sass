'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { supabase } from '@/lib/supabase/client'

export default function SettingsPage() {
  const router = useRouter()
  const [user, setUser] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      if (!session) {
        router.push('/login')
      } else {
        setUser(session.user)
        setLoading(false)
      }
    })
  }, [router])

  if (loading) {
    return <div className="text-white">Loading...</div>
  }

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Settings</h1>
        <p className="text-gray-400">Manage your account settings</p>
      </div>

      <div className="bg-gray-800 rounded-lg p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">Account Information</h2>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">Email</label>
            <div className="bg-gray-700 border border-gray-600 rounded px-4 py-2">
              {user?.email}
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium mb-2">User ID</label>
            <div className="bg-gray-700 border border-gray-600 rounded px-4 py-2 text-sm text-gray-400 font-mono">
              {user?.id}
            </div>
          </div>
        </div>
      </div>

      <div className="bg-gray-800 rounded-lg p-6">
        <h2 className="text-xl font-semibold mb-4">Danger Zone</h2>
        <button
          onClick={async () => {
            if (confirm('Are you sure you want to sign out?')) {
              await supabase.auth.signOut()
              router.push('/login')
            }
          }}
          className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
        >
          Sign Out
        </button>
      </div>
    </div>
  )
}

