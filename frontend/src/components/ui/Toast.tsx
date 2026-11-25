import { motion, AnimatePresence } from 'framer-motion'
import { CheckCircle, AlertCircle, Info, AlertTriangle, X } from 'lucide-react'
import { useUIStore } from '@/store/uiStore'

const icons = {
  success: CheckCircle,
  error: AlertCircle,
  info: Info,
  warning: AlertTriangle,
}
const colors = {
  success: 'border-green-200 bg-green-50 text-green-800',
  error: 'border-red-200 bg-red-50 text-red-800',
  info: 'border-blue-200 bg-blue-50 text-blue-800',
  warning: 'border-amber-200 bg-amber-50 text-amber-800',
}

export function ToastContainer() {
  const { toasts, removeToast } = useUIStore()
  return (
    <div className="fixed bottom-6 right-6 z-50 flex flex-col gap-3 max-w-sm w-full pointer-events-none">
      <AnimatePresence>
        {toasts.map((t) => {
          const Icon = icons[t.type]
          return (
            <motion.div
              key={t.id}
              initial={{ opacity: 0, y: 20, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: 20, scale: 0.95 }}
              className={`card border pointer-events-auto p-4 flex items-start gap-3 ${colors[t.type]}`}
            >
              <Icon className="shrink-0 mt-0.5" size={18} />
              <div className="flex-1 min-w-0">
                <p className="font-semibold text-sm">{t.title}</p>
                {t.message && <p className="text-xs mt-0.5 opacity-80">{t.message}</p>}
              </div>
              <button onClick={() => removeToast(t.id)} className="shrink-0 opacity-60 hover:opacity-100 transition-opacity">
                <X size={14} />
              </button>
            </motion.div>
          )
        })}
      </AnimatePresence>
    </div>
  )
}

export function XPPopup() {
  const { xpPopup } = useUIStore()
  return (
    <AnimatePresence>
      {xpPopup.visible && (
        <motion.div
          initial={{ opacity: 0, y: 20, scale: 0.8 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, y: -30, scale: 0.8 }}
          className="fixed bottom-24 right-6 z-50 xp-pill text-base shadow-lg pointer-events-none"
        >
          ⚡ +{xpPopup.amount} XP
        </motion.div>
      )}
    </AnimatePresence>
  )
}

export function LevelUpModal() {
  const { levelUpModal, hideLevelUp } = useUIStore()
  return (
    <AnimatePresence>
      {levelUpModal.visible && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm"
          onClick={hideLevelUp}
        >
          <motion.div
            initial={{ scale: 0.5, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.8, opacity: 0 }}
            className="card p-10 text-center max-w-sm mx-4"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="text-6xl mb-4">🎉</div>
            <h2 className="text-2xl font-bold gradient-text">Level Up!</h2>
            <p className="text-slate-600 mt-2">You reached</p>
            <p className="text-xl font-bold text-brand-600 mt-1">Level {levelUpModal.level} — {levelUpModal.title}</p>
            <button className="btn-primary mt-6 w-full justify-center" onClick={hideLevelUp}>
              Awesome! 🚀
            </button>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}
