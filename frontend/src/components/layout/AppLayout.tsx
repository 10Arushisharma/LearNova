import { Navbar } from './Navbar'
import { ToastContainer, XPPopup, LevelUpModal } from '../ui/Toast'
import { useEffect } from 'react'
import { useAuthStore } from '@/store/authStore'
import { api } from '@/lib/api'

interface Props { children: React.ReactNode }

export function AppLayout({ children }: Props) {
  const { user, setUser, isLoading } = useAuthStore()

  useEffect(() => {
    if (!user && isLoading) {
      api.get('/users/me').then((r) => setUser(r.data)).catch(() => setUser(null))
    }
  }, [])

  return (
    <div className="min-h-screen bg-slate-50">
      <Navbar />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>
      <ToastContainer />
      <XPPopup />
      <LevelUpModal />
    </div>
  )
}
