import { create } from 'zustand'

interface Toast {
  id: string
  type: 'success' | 'error' | 'info' | 'warning'
  title: string
  message?: string
  duration?: number
}

interface UIState {
  toasts: Toast[]
  addToast: (t: Omit<Toast, 'id'>) => void
  removeToast: (id: string) => void
  xpPopup: { amount: number; visible: boolean }
  showXPPopup: (amount: number) => void
  hideXPPopup: () => void
  levelUpModal: { level: number; title: string; visible: boolean }
  showLevelUp: (level: number, title: string) => void
  hideLevelUp: () => void
}

export const useUIStore = create<UIState>((set) => ({
  toasts: [],
  addToast: (t) => {
    const id = Math.random().toString(36).slice(2)
    set((s) => ({ toasts: [...s.toasts, { ...t, id }] }))
    setTimeout(() => set((s) => ({ toasts: s.toasts.filter((x) => x.id !== id) })), t.duration ?? 4000)
  },
  removeToast: (id) => set((s) => ({ toasts: s.toasts.filter((t) => t.id !== id) })),
  xpPopup: { amount: 0, visible: false },
  showXPPopup: (amount) => {
    set({ xpPopup: { amount, visible: true } })
    setTimeout(() => set({ xpPopup: { amount: 0, visible: false } }), 2500)
  },
  hideXPPopup: () => set({ xpPopup: { amount: 0, visible: false } }),
  levelUpModal: { level: 0, title: '', visible: false },
  showLevelUp: (level, title) => set({ levelUpModal: { level, title, visible: true } }),
  hideLevelUp: () => set({ levelUpModal: { level: 0, title: '', visible: false } }),
}))
