import { motion } from 'framer-motion'

export function PageLoader() {
  return (
    <div className="fixed inset-0 flex items-center justify-center bg-slate-50 z-50">
      <div className="text-center">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
          className="w-10 h-10 border-4 border-brand-200 border-t-brand-600 rounded-full mx-auto mb-4"
        />
        <p className="text-slate-500 text-sm font-medium">Loading Learnova…</p>
      </div>
    </div>
  )
}

export function Skeleton({ className = '' }: { className?: string }) {
  return <div className={`animate-pulse bg-slate-200 rounded-lg ${className}`} />
}

export function CardSkeleton() {
  return (
    <div className="card p-6 space-y-3">
      <Skeleton className="h-5 w-2/3" />
      <Skeleton className="h-4 w-full" />
      <Skeleton className="h-4 w-4/5" />
    </div>
  )
}
