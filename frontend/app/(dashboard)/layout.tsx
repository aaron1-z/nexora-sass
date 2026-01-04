'use client'

import { useEffect, useState } from 'react'
import { useRouter, usePathname } from 'next/navigation'
import { supabase } from '@/lib/supabase/client'
import Link from 'next/link'
import NexoraLogo from '@/components/NexoraLogo'

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const router = useRouter()
  const pathname = usePathname()
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

    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, session) => {
      if (!session) {
        router.push('/login')
      } else {
        setUser(session.user)
      }
    })

    return () => subscription.unsubscribe()
  }, [router])

  const handleSignOut = async () => {
    await supabase.auth.signOut()
    router.push('/login')
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-white">Loading...</div>
      </div>
    )
  }

  const navItems = [
    { href: '/dashboard', label: 'Dashboard' },
    { href: '/briefs', label: 'Briefs' },
    { href: '/billing', label: 'Billing' },
    { href: '/settings', label: 'Settings' },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 via-gray-900 to-black text-white">
      <nav className="bg-gray-800/50 backdrop-blur-sm border-b border-gray-700/50 sticky top-0 z-50">
        <div className="container mx-auto px-4">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-8">
              <Link href="/dashboard" className="flex items-center gap-2 text-xl font-bold">
                <NexoraLogo className="w-6 h-6 text-blue-400" />
                <span className="bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">Nexora</span>
              </Link>
              {navItems.map((item) => (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`${
                    pathname === item.href
                      ? 'text-blue-400 border-b-2 border-blue-400'
                      : 'text-gray-300 hover:text-white'
                  } px-3 py-2 transition-colors font-medium`}
                >
                  {item.label}
                </Link>
              ))}
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-400 hidden sm:block">{user?.email}</span>
              <button
                onClick={handleSignOut}
                className="text-gray-300 hover:text-white text-sm px-3 py-2 rounded-lg hover:bg-gray-700/50 transition-colors"
              >
                Sign Out
              </button>
            </div>
          </div>
        </div>
      </nav>
      <main className="container mx-auto px-4 py-8">{children}</main>
    </div>
  )
}

