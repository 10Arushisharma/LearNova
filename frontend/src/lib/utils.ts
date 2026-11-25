import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatXP(xp: number): string {
  if (xp >= 1000) return `${(xp / 1000).toFixed(1)}k`
  return xp.toString()
}

export function getLevelColor(level: number): string {
  const colors = [
    'text-slate-600', 'text-blue-600', 'text-green-600', 'text-teal-600',
    'text-purple-600', 'text-indigo-600', 'text-violet-600', 'text-pink-600',
    'text-rose-600', 'text-amber-600',
  ]
  return colors[Math.min(level - 1, colors.length - 1)]
}

export function getDifficultyColor(difficulty: string): string {
  const map: Record<string, string> = {
    beginner: 'text-green-700 bg-green-50 border-green-200',
    easy: 'text-green-700 bg-green-50 border-green-200',
    intermediate: 'text-amber-700 bg-amber-50 border-amber-200',
    medium: 'text-amber-700 bg-amber-50 border-amber-200',
    advanced: 'text-red-700 bg-red-50 border-red-200',
    hard: 'text-red-700 bg-red-50 border-red-200',
  }
  return map[difficulty] || 'text-slate-700 bg-slate-50 border-slate-200'
}

export function timeAgo(dateStr: string): string {
  const diff = Date.now() - new Date(dateStr).getTime()
  const mins = Math.floor(diff / 60000)
  if (mins < 1) return 'just now'
  if (mins < 60) return `${mins}m ago`
  const hrs = Math.floor(mins / 60)
  if (hrs < 24) return `${hrs}h ago`
  return `${Math.floor(hrs / 24)}d ago`
}

export function formatDate(dateStr: string): string {
  return new Date(dateStr).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })
}
