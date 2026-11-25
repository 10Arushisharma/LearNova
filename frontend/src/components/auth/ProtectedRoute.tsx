import { Navigate } from 'react-router-dom'
import { useAuthStore } from '@/store/authStore'
import { useEffect } from 'react'
import { api } from '@/lib/api'

interface Props {
  children: React.ReactNode
  adminOnly?: boolean
}

export function ProtectedRoute({ children, adminOnly }: Props) {
  const { user, isLoading, setUser, setLoading } = useAuthStore()

  useEffect(() => {
    if (!user) {
      api.get('/users/me').then((res) => setUser(res.data)).catch(() => setUser(null))
    }
  }, [])

  if (isLoading && !user) return null

  if (!user) return <Navigate to="/login" replace />
  if (adminOnly && user.role !== 'admin') return <Navigate to="/dashboard" replace />
  if (user && !user.onboarding_completed && window.location.pathname !== '/onboarding') {
    return <Navigate to="/onboarding" replace />
  }

  return <>{children}</>
}
