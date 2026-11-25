import { Link, useNavigate } from 'react-router-dom'
import { Bell, Search, Zap, Flame, LogOut, User, Settings, ChevronDown, BookOpen, LayoutDashboard } from 'lucide-react'
import { useState } from 'react'
import { useAuthStore } from '@/store/authStore'
import { api } from '@/lib/api'
import { useUIStore } from '@/store/uiStore'
import { formatXP } from '@/lib/utils'
import { motion, AnimatePresence } from 'framer-motion'

export function Navbar() {
  const { user, setUser } = useAuthStore()
  const { addToast } = useUIStore()
  const navigate = useNavigate()
  const [dropdownOpen, setDropdownOpen] = useState(false)
  const [searchOpen, setSearchOpen] = useState(false)

  const handleLogout = async () => {
    await api.post('/auth/logout')
    setUser(null)
    addToast({ type: 'info', title: 'Logged out', message: 'See you next time!' })
    navigate('/login')
  }

  const totalXP = user?.level_info?.total_xp ?? 0
  const streak = user?.streak?.current_streak ?? 0

  return (
    <header className="sticky top-0 z-40 bg-white/80 backdrop-blur-md border-b border-slate-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/dashboard" className="flex items-center gap-2 font-bold text-xl">
            <div className="w-8 h-8 gradient-brand rounded-lg flex items-center justify-center">
              <Zap size={16} className="text-white" />
            </div>
            <span className="gradient-text">Learnova</span>
          </Link>

          {/* Nav links — desktop */}
          <nav className="hidden md:flex items-center gap-1">
            <NavLink to="/dashboard" icon={<LayoutDashboard size={15} />}>Dashboard</NavLink>
            <NavLink to="/paths" icon={<BookOpen size={15} />}>Paths</NavLink>
            <NavLink to="/playground" icon={<span className="text-xs font-mono">{'{}'}</span>}>Playground</NavLink>
            <NavLink to="/mentor" icon={<span className="text-xs">🤖</span>}>AI Mentor</NavLink>
            <NavLink to="/leaderboard" icon={<span className="text-xs">🏆</span>}>Leaderboard</NavLink>
          </nav>

          {/* Right section */}
          <div className="flex items-center gap-3">
            {/* XP */}
            <div className="xp-pill hidden sm:flex">
              <Zap size={12} className="text-amber-500" />
              {formatXP(totalXP)} XP
            </div>

            {/* Streak */}
            {streak > 0 && (
              <div className="streak-pill hidden sm:flex">
                <Flame size={12} className="text-orange-500" />
                {streak}d
              </div>
            )}

            {/* Search */}
            <button onClick={() => setSearchOpen(!searchOpen)} className="btn-ghost p-2 rounded-lg">
              <Search size={18} />
            </button>

            {/* Notifications */}
            <Link to="/dashboard#notifications" className="btn-ghost p-2 rounded-lg relative">
              <Bell size={18} />
            </Link>

            {/* Avatar dropdown */}
            <div className="relative">
              <button
                onClick={() => setDropdownOpen(!dropdownOpen)}
                className="flex items-center gap-2 p-1.5 rounded-xl hover:bg-slate-100 transition-colors"
              >
                <div className="w-8 h-8 gradient-brand rounded-full flex items-center justify-center text-white text-sm font-bold">
                  {user?.full_name?.[0] ?? '?'}
                </div>
                <ChevronDown size={14} className="text-slate-500 hidden sm:block" />
              </button>
              <AnimatePresence>
                {dropdownOpen && (
                  <motion.div
                    initial={{ opacity: 0, y: 8, scale: 0.95 }}
                    animate={{ opacity: 1, y: 0, scale: 1 }}
                    exit={{ opacity: 0, y: 8, scale: 0.95 }}
                    className="absolute right-0 mt-2 w-56 card shadow-lg py-1 z-50"
                  >
                    <div className="px-4 py-3 border-b border-slate-100">
                      <p className="font-semibold text-sm">{user?.full_name}</p>
                      <p className="text-xs text-slate-500">{user?.email}</p>
                      <p className="text-xs text-brand-600 font-medium mt-0.5">
                        Level {user?.level_info?.level} — {user?.level_info?.title}
                      </p>
                    </div>
                    <DropdownItem to="/profile" icon={<User size={14} />}>My Profile</DropdownItem>
                    <DropdownItem to="/quests" icon={<span className="text-xs">⚡</span>}>Daily Quests</DropdownItem>
                    <DropdownItem to="/achievements" icon={<span className="text-xs">🏅</span>}>Achievements</DropdownItem>
                    <DropdownItem to="/analytics" icon={<span className="text-xs">📊</span>}>Analytics</DropdownItem>
                    {user?.role === 'admin' && (
                      <DropdownItem to="/admin" icon={<Settings size={14} />}>Admin Panel</DropdownItem>
                    )}
                    <div className="border-t border-slate-100 mt-1 pt-1">
                      <button
                        onClick={handleLogout}
                        className="w-full flex items-center gap-2 px-4 py-2.5 text-sm text-red-600 hover:bg-red-50 transition-colors"
                      >
                        <LogOut size={14} />
                        Sign out
                      </button>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </div>
        </div>
      </div>
    </header>
  )
}

function NavLink({ to, icon, children }: { to: string; icon: React.ReactNode; children: React.ReactNode }) {
  return (
    <Link to={to} className="flex items-center gap-1.5 px-3 py-2 rounded-lg text-sm font-medium text-slate-600 hover:text-brand-600 hover:bg-brand-50 transition-colors">
      {icon}
      {children}
    </Link>
  )
}

function DropdownItem({ to, icon, children }: { to: string; icon: React.ReactNode; children: React.ReactNode }) {
  return (
    <Link
      to={to}
      className="flex items-center gap-2 px-4 py-2.5 text-sm text-slate-700 hover:bg-slate-50 transition-colors"
    >
      {icon}
      {children}
    </Link>
  )
}
