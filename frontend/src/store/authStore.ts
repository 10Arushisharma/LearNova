import { create } from 'zustand'

export interface User {
  id: number
  email: string
  username: string
  full_name: string
  role: string
  onboarding_completed: boolean
  profile?: {
    avatar_url: string
    bio: string
    timezone: string
    streak_freezes: number
    github_url?: string
    public_profile?: boolean
    show_on_leaderboard?: boolean
  }
  preferences?: {
    experience_level: string
    interests: string[]
    daily_minutes_goal: number
    recommended_path_slug: string
  }
  level_info?: {
    level: number
    title: string
    total_xp: number
    next_level_xp: number
    xp_to_next_level: number
    progress_percentage: number
    is_max_level: boolean
  }
  streak?: {
    current_streak: number
    longest_streak: number
    last_active_date: string | null
  }
}

interface AuthState {
  user: User | null
  isLoading: boolean
  setUser: (user: User | null) => void
  setLoading: (v: boolean) => void
  updateUser: (partial: Partial<User>) => void
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isLoading: true,
  setUser: (user) => set({ user, isLoading: false }),
  setLoading: (isLoading) => set({ isLoading }),
  updateUser: (partial) => set((s) => ({ user: s.user ? { ...s.user, ...partial } : null })),
}))
