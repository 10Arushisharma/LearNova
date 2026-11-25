import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Brain, Zap, Trophy, Code2, Rocket, Users, Star, ChevronDown,
  Play, CheckCircle2, ArrowRight, Flame, Target, BookOpen,
  BarChart3, MessageSquare, Award, Lock, Unlock, Terminal,
  GitBranch, Layers, Cpu, Sparkles, GraduationCap, TrendingUp,
  Shield, Clock, Globe, Menu, X
} from 'lucide-react';
import { cn } from '@/lib/utils';

const features = [
  {
    icon: <BookOpen className="w-6 h-6" />,
    title: 'Interactive Lessons',
    desc: 'Learn through hands-on coding exercises, not just videos. Every concept has an interactive challenge.',
    color: 'from-blue-500 to-cyan-500',
  },
  {
    icon: <Brain className="w-6 h-6" />,
    title: 'AI Mentor',
    desc: 'Your personal AI tutor guides you with Socratic questioning, hints, and deep explanations.',
    color: 'from-purple-500 to-pink-500',
  },
  {
    icon: <Zap className="w-6 h-6" />,
    title: 'Gamified XP',
    desc: 'Earn XP, level up, unlock achievements, and maintain streaks to stay motivated every day.',
    color: 'from-yellow-500 to-orange-500',
  },
  {
    icon: <Terminal className="w-6 h-6" />,
    title: 'Python Playground',
    desc: 'Run Python code directly in your browser with our secure sandboxed execution environment.',
    color: 'from-green-500 to-emerald-500',
  },
  {
    icon: <Rocket className="w-6 h-6" />,
    title: 'Real Projects',
    desc: 'Build portfolio-worthy projects with guided milestones and real datasets to solve real problems.',
    color: 'from-orange-500 to-red-500',
  },
  {
    icon: <Trophy className="w-6 h-6" />,
    title: 'Leaderboards',
    desc: 'Compete globally and locally, see weekly rankings, and climb to the top of your cohort.',
    color: 'from-indigo-500 to-purple-500',
  },
];

const paths = [
  { title: 'Python Foundations', sub: 'Variables to OOP', diff: 'Beginner', hours: 24, color: 'from-blue-600 to-blue-400', icon: '🐍' },
  { title: 'Data Science', sub: 'Pandas, NumPy, Viz', diff: 'Intermediate', hours: 40, color: 'from-green-600 to-emerald-400', icon: '📊' },
  { title: 'Machine Learning', sub: 'Scikit-learn & Models', diff: 'Intermediate', hours: 50, color: 'from-purple-600 to-purple-400', icon: '🤖' },
  { title: 'Deep Learning', sub: 'Neural Nets & PyTorch', diff: 'Advanced', hours: 60, color: 'from-orange-600 to-orange-400', icon: '🧠' },
  { title: 'Generative AI', sub: 'LLMs, Prompting, RAG', diff: 'Advanced', hours: 45, color: 'from-violet-600 to-violet-400', icon: '✨' },
  { title: 'AI Engineering', sub: 'Deploy & Scale AI Apps', diff: 'Expert', hours: 55, color: 'from-indigo-600 to-indigo-400', icon: '⚙️' },
];

const modes = [
  {
    title: 'Write & Run',
    desc: 'Write Python from scratch and execute instantly',
    code: `def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

print(list(fibonacci(8)))
# [0, 1, 1, 2, 3, 5, 8, 13]`,
    color: 'from-blue-500 to-cyan-500',
    icon: <Play className="w-5 h-5" />,
  },
  {
    title: 'Debug Code',
    desc: 'Find and fix bugs with AI-guided hints',
    code: `# BUG: Fix the binary search!
def binary_search(arr, target):
    lo, hi = 0, len(arr)  # ← bug here
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] == target: return mid
        elif arr[mid] < target: lo = mid
        else: hi = mid - 1`,
    color: 'from-red-500 to-orange-500',
    icon: <Code2 className="w-5 h-5" />,
  },
  {
    title: 'Predict Output',
    desc: 'Test your mental model before running',
    code: `x = [1, 2, 3, 4, 5]
result = [i**2 for i in x if i % 2 != 0]
print(result)

# What do you think prints?
# A) [1, 9, 25]
# B) [1, 4, 9, 16, 25]
# C) [2, 4]
# D) Error`,
    color: 'from-purple-500 to-pink-500',
    icon: <Target className="w-5 h-5" />,
  },
];

const mentorConvo = [
  { role: 'user', text: 'Why does my list comprehension produce wrong results?' },
  { role: 'assistant', text: "Great question! Before I explain, let me ask: what do you *expect* the comprehension to produce, and what does it actually give you? 🤔" },
  { role: 'user', text: 'I expected [1,4,9] but got [1,2,3]' },
  { role: 'assistant', text: "Interesting! It looks like the squaring part might be missing. Can you share your code? A common mistake is writing `[x for x in lst]` instead of `[x**2 for x in lst]`. What does yours look like?" },
];

const xpTable = [
  { level: 1, name: 'Novice', xp: '0 – 500', perks: 'Basic lessons unlocked' },
  { level: 5, name: 'Apprentice', xp: '2,000 – 4,000', perks: 'Playground + Projects' },
  { level: 10, name: 'Practitioner', xp: '8,000 – 12,000', perks: 'Advanced paths unlock' },
  { level: 20, name: 'Expert', xp: '30,000 – 50,000', perks: 'Mentor mode + Badges' },
  { level: 30, name: 'Master', xp: '80,000+', perks: 'Leaderboard hall of fame' },
];

const achievements = [
  { icon: '🔥', name: 'On Fire', desc: '7-day streak' },
  { icon: '🏆', name: 'Top 10', desc: 'Weekly leaderboard' },
  { icon: '🧠', name: 'Deep Thinker', desc: 'Complete Deep Learning path' },
  { icon: '⚡', name: 'Speed Coder', desc: 'Solve in under 60s' },
  { icon: '🎯', name: 'Perfect Score', desc: '100% on quiz' },
  { icon: '🌟', name: 'First Star', desc: 'Earn 1000 XP' },
];

const testimonials = [
  {
    name: 'Sarah K.',
    role: 'Data Scientist @ Google',
    avatar: 'SK',
    text: 'Learnova\'s AI Mentor helped me understand backpropagation in a way no YouTube video ever did. The Socratic approach is brilliant.',
    stars: 5,
  },
  {
    name: 'Marcus T.',
    role: 'ML Engineer @ Startup',
    avatar: 'MT',
    text: 'I went from "what is a variable" to deploying my first ML model in 3 months. The gamification kept me hooked every single day.',
    stars: 5,
  },
  {
    name: 'Priya M.',
    role: 'CS Student, IIT',
    avatar: 'PM',
    text: 'The Python Playground is insanely fast. No setup, no fuss. I just open Learnova and start coding. My grades improved massively.',
    stars: 5,
  },
];

const faqs = [
  {
    q: 'Is Learnova free?',
    a: 'Yes! You can start for free and access Python Foundations and core features. Premium paths unlock with a Pro subscription.',
  },
  {
    q: 'Do I need any prior coding experience?',
    a: 'Not at all. Our Python Foundations path starts from absolute zero — no experience needed.',
  },
  {
    q: 'How is the AI Mentor different from ChatGPT?',
    a: 'Our AI Mentor uses a Socratic method — it asks guiding questions rather than giving direct answers, which dramatically improves retention.',
  },
  {
    q: 'Can I run Python code without installing anything?',
    a: 'Yes! Our cloud-based Python Playground runs your code securely in the browser. No installation required.',
  },
  {
    q: 'What certificates do I get?',
    a: 'You earn digital certificates for each completed path that you can share on LinkedIn and your portfolio.',
  },
];

const FAQItem: React.FC<{ q: string; a: string; index: number }> = ({ q, a, index }) => {
  const [open, setOpen] = useState(false);
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1 }}
      viewport={{ once: true }}
      className="border border-white/10 rounded-xl overflow-hidden"
    >
      <button
        className="w-full flex items-center justify-between p-5 text-left bg-white/5 hover:bg-white/10 transition-colors"
        onClick={() => setOpen(!open)}
      >
        <span className="font-semibold text-white">{q}</span>
        <ChevronDown className={cn('w-5 h-5 text-gray-400 transition-transform', open && 'rotate-180')} />
      </button>
      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="overflow-hidden"
          >
            <div className="p-5 bg-white/[0.02] text-gray-400 leading-relaxed">{a}</div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
};

const LandingPage: React.FC = () => {
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <div className="min-h-screen bg-[#030712] text-white overflow-x-hidden">
      {/* ── NAVBAR ── */}
      <header className="fixed top-0 inset-x-0 z-50 border-b border-white/5 bg-[#030712]/80 backdrop-blur-xl">
        <nav className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2 font-bold text-xl">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-purple-500 to-blue-500 flex items-center justify-center">
              <Brain className="w-5 h-5 text-white" />
            </div>
            <span className="bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">Learnova</span>
          </Link>

          <div className="hidden md:flex items-center gap-6 text-sm font-medium text-gray-400">
            {['Paths', 'Playground', 'Mentor', 'Leaderboard'].map((item) => (
              <Link key={item} to={`/${item.toLowerCase()}`} className="hover:text-white transition-colors">
                {item}
              </Link>
            ))}
          </div>

          <div className="hidden md:flex items-center gap-3">
            <Link to="/login" className="px-4 py-2 text-sm font-medium text-gray-300 hover:text-white transition-colors">
              Login
            </Link>
            <Link
              to="/register"
              className="px-4 py-2 text-sm font-semibold rounded-lg bg-gradient-to-r from-purple-500 to-blue-500 hover:opacity-90 transition-opacity"
            >
              Start Free
            </Link>
          </div>

          <button className="md:hidden p-2 text-gray-400" onClick={() => setMobileOpen(!mobileOpen)}>
            {mobileOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </nav>

        <AnimatePresence>
          {mobileOpen && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="md:hidden border-t border-white/5 bg-[#030712] px-4 py-4 space-y-3"
            >
              {['Paths', 'Playground', 'Mentor', 'Leaderboard'].map((item) => (
                <Link key={item} to={`/${item.toLowerCase()}`} className="block py-2 text-gray-300 hover:text-white">
                  {item}
                </Link>
              ))}
              <Link to="/login" className="block py-2 text-gray-300 hover:text-white">Login</Link>
              <Link to="/register" className="block py-2 px-4 text-center rounded-lg bg-gradient-to-r from-purple-500 to-blue-500 font-semibold">
                Start Free
              </Link>
            </motion.div>
          )}
        </AnimatePresence>
      </header>

      {/* ── HERO ── */}
      <section className="relative pt-32 pb-24 px-4 overflow-hidden">
        {/* Background blobs */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute -top-40 -right-40 w-[600px] h-[600px] rounded-full bg-purple-500/10 blur-3xl" />
          <div className="absolute top-20 -left-40 w-[500px] h-[500px] rounded-full bg-blue-500/10 blur-3xl" />
          <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-[800px] h-[300px] rounded-full bg-indigo-500/5 blur-3xl" />
        </div>

        <div className="relative max-w-7xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-purple-500/10 border border-purple-500/20 text-purple-400 text-sm font-medium mb-6">
              <Sparkles className="w-3.5 h-3.5" />
              The AI-Powered Python Learning Platform
            </div>
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="text-5xl md:text-7xl font-black leading-tight mb-6"
          >
            Don't Just Learn AI.
            <br />
            <span className="bg-gradient-to-r from-purple-400 via-pink-400 to-blue-400 bg-clip-text text-transparent">
              Build With It.
            </span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="text-xl text-gray-400 max-w-2xl mx-auto mb-10"
          >
            Master Python, Data Science, and AI through interactive lessons, an AI mentor, real projects,
            and gamified XP — all in your browser. No setup required.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16"
          >
            <Link
              to="/register"
              className="group flex items-center gap-2 px-8 py-4 rounded-xl bg-gradient-to-r from-purple-500 to-blue-500 font-bold text-lg hover:opacity-90 transition-all hover:scale-105"
            >
              Start Learning Free
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </Link>
            <Link
              to="/paths"
              className="flex items-center gap-2 px-8 py-4 rounded-xl border border-white/20 font-semibold text-lg hover:bg-white/5 transition-all"
            >
              <Play className="w-5 h-5 text-purple-400" />
              Explore Paths
            </Link>
          </motion.div>

          {/* Dashboard preview card */}
          <motion.div
            initial={{ opacity: 0, y: 60, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="relative max-w-4xl mx-auto"
          >
            <div className="absolute inset-0 bg-gradient-to-t from-purple-500/20 to-blue-500/20 rounded-2xl blur-2xl" />
            <div className="relative rounded-2xl border border-white/10 bg-[#0d1117] overflow-hidden shadow-2xl">
              <div className="flex items-center gap-2 px-4 py-3 border-b border-white/5 bg-white/5">
                <div className="w-3 h-3 rounded-full bg-red-400" />
                <div className="w-3 h-3 rounded-full bg-yellow-400" />
                <div className="w-3 h-3 rounded-full bg-green-400" />
                <span className="ml-3 text-xs text-gray-500 font-mono">learnova.app/dashboard</span>
              </div>
              <div className="p-6 grid grid-cols-2 md:grid-cols-4 gap-4">
                {[
                  { label: 'Total XP', value: '12,450', icon: <Zap className="w-4 h-4 text-yellow-400" />, sub: '+320 today' },
                  { label: 'Level', value: '14', icon: <Star className="w-4 h-4 text-purple-400" />, sub: 'Practitioner' },
                  { label: 'Streak', value: '21 days', icon: <Flame className="w-4 h-4 text-orange-400" />, sub: 'Keep it up! 🔥' },
                  { label: 'Lessons', value: '89', icon: <CheckCircle2 className="w-4 h-4 text-green-400" />, sub: 'Completed' },
                ].map((stat) => (
                  <div key={stat.label} className="bg-white/5 rounded-xl p-4 text-left">
                    <div className="flex items-center gap-2 text-xs text-gray-500 mb-2">
                      {stat.icon}
                      {stat.label}
                    </div>
                    <div className="text-2xl font-bold text-white mb-1">{stat.value}</div>
                    <div className="text-xs text-gray-500">{stat.sub}</div>
                  </div>
                ))}
              </div>
              <div className="px-6 pb-6">
                <div className="bg-white/5 rounded-xl p-4">
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-sm font-semibold text-white">Machine Learning Path</span>
                    <span className="text-xs text-gray-500">62% complete</span>
                  </div>
                  <div className="h-2 bg-white/10 rounded-full overflow-hidden">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: '62%' }}
                      transition={{ duration: 1.5, delay: 1 }}
                      className="h-full rounded-full bg-gradient-to-r from-purple-500 to-blue-500"
                    />
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* ── WHY LEARNOVA ── */}
      <section className="py-24 px-4">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-black mb-4">Why Learnova?</h2>
            <p className="text-xl text-gray-400 max-w-2xl mx-auto">
              We combine the best of structured learning, AI tutoring, and gamification to make you actually stick with it.
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((f, i) => (
              <motion.div
                key={f.title}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                whileHover={{ y: -4 }}
                className="group relative p-6 rounded-2xl border border-white/10 bg-white/5 hover:bg-white/10 transition-all"
              >
                <div className={cn('inline-flex p-3 rounded-xl bg-gradient-to-br mb-4 text-white', f.color)}>
                  {f.icon}
                </div>
                <h3 className="text-xl font-bold mb-2">{f.title}</h3>
                <p className="text-gray-400 leading-relaxed">{f.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* ── LEARNING PATHS ── */}
      <section className="py-24 px-4 bg-white/[0.02]">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-black mb-4">Learning Paths</h2>
            <p className="text-xl text-gray-400 max-w-2xl mx-auto">
              From zero to AI engineer. Structured paths with clear milestones.
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {paths.map((p, i) => (
              <motion.div
                key={p.title}
                initial={{ opacity: 0, scale: 0.95 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.08 }}
                whileHover={{ scale: 1.02 }}
                className="relative overflow-hidden rounded-2xl border border-white/10 bg-[#0d1117] p-6 cursor-pointer group"
              >
                <div className={cn('absolute inset-0 bg-gradient-to-br opacity-5 group-hover:opacity-10 transition-opacity', p.color)} />
                <div className="relative">
                  <div className="text-4xl mb-4">{p.icon}</div>
                  <h3 className="text-xl font-bold mb-1">{p.title}</h3>
                  <p className="text-gray-400 text-sm mb-4">{p.sub}</p>
                  <div className="flex items-center justify-between">
                    <span className={cn(
                      'text-xs font-semibold px-2.5 py-1 rounded-full',
                      p.diff === 'Beginner' ? 'bg-green-500/20 text-green-400' :
                      p.diff === 'Intermediate' ? 'bg-yellow-500/20 text-yellow-400' :
                      p.diff === 'Advanced' ? 'bg-orange-500/20 text-orange-400' :
                      'bg-red-500/20 text-red-400'
                    )}>
                      {p.diff}
                    </span>
                    <span className="text-xs text-gray-500 flex items-center gap-1">
                      <Clock className="w-3.5 h-3.5" />
                      {p.hours}h
                    </span>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>

          <div className="text-center mt-10">
            <Link to="/paths" className="inline-flex items-center gap-2 px-6 py-3 rounded-xl border border-white/20 font-semibold hover:bg-white/5 transition-all">
              View All Paths <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </section>

      {/* ── LEARN BY DOING ── */}
      <section className="py-24 px-4">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-black mb-4">Learn by Doing</h2>
            <p className="text-xl text-gray-400 max-w-2xl mx-auto">
              Three powerful modes to sharpen your Python skills through active practice.
            </p>
          </motion.div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {modes.map((mode, i) => (
              <motion.div
                key={mode.title}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.15 }}
                className="rounded-2xl border border-white/10 overflow-hidden"
              >
                <div className={cn('p-4 bg-gradient-to-r text-white flex items-center gap-3', mode.color)}>
                  {mode.icon}
                  <div>
                    <div className="font-bold">{mode.title}</div>
                    <div className="text-sm opacity-90">{mode.desc}</div>
                  </div>
                </div>
                <pre className="p-4 bg-[#0d1117] text-sm text-green-300 font-mono leading-relaxed overflow-x-auto">
                  <code>{mode.code}</code>
                </pre>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* ── AI MENTOR ── */}
      <section className="py-24 px-4 bg-white/[0.02]">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            <motion.div
              initial={{ opacity: 0, x: -30 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
            >
              <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-purple-500/10 border border-purple-500/20 text-purple-400 text-sm font-medium mb-6">
                <Brain className="w-3.5 h-3.5" />
                AI-Powered Mentorship
              </div>
              <h2 className="text-4xl md:text-5xl font-black mb-6">
                Your Personal
                <br />
                <span className="bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">AI Mentor</span>
              </h2>
              <p className="text-xl text-gray-400 mb-6">
                Unlike a search engine, our AI mentor <strong className="text-white">guides you to the answer</strong> using
                Socratic questioning. You'll remember it because you discovered it yourself.
              </p>
              <ul className="space-y-3">
                {[
                  'Personalized hints based on your code',
                  'Explain concepts at your level',
                  '7 interaction modes (beginner, debug, interview…)',
                  'Available 24/7, no waiting',
                ].map((item) => (
                  <li key={item} className="flex items-center gap-3 text-gray-300">
                    <CheckCircle2 className="w-5 h-5 text-green-400 shrink-0" />
                    {item}
                  </li>
                ))}
              </ul>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 30 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="rounded-2xl border border-white/10 bg-[#0d1117] overflow-hidden"
            >
              <div className="flex items-center gap-2 px-4 py-3 border-b border-white/5 bg-white/5">
                <Brain className="w-4 h-4 text-purple-400" />
                <span className="text-sm font-semibold text-white">AI Mentor</span>
                <span className="ml-auto text-xs text-purple-400 bg-purple-500/10 px-2 py-0.5 rounded-full">Socratic Mode</span>
              </div>
              <div className="p-4 space-y-4">
                {mentorConvo.map((msg, i) => (
                  <motion.div
                    key={i}
                    initial={{ opacity: 0, y: 10 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: i * 0.2 }}
                    className={cn('flex', msg.role === 'user' ? 'justify-end' : 'justify-start')}
                  >
                    <div className={cn(
                      'max-w-[85%] rounded-xl px-4 py-3 text-sm leading-relaxed',
                      msg.role === 'user'
                        ? 'bg-purple-500/20 text-purple-100'
                        : 'bg-white/5 text-gray-300'
                    )}>
                      {msg.text}
                    </div>
                  </motion.div>
                ))}
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* ── GAMIFICATION ── */}
      <section className="py-24 px-4">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-black mb-4">Level Up as You Learn</h2>
            <p className="text-xl text-gray-400">
              Every lesson, challenge, and project earns you XP. Watch your rank climb.
            </p>
          </motion.div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
            {/* XP Table */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="rounded-2xl border border-white/10 bg-white/5 overflow-hidden"
            >
              <div className="p-4 border-b border-white/5 font-semibold">Level Progression</div>
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-white/5 text-gray-500 text-xs uppercase">
                    <th className="py-3 px-4 text-left">Lvl</th>
                    <th className="py-3 px-4 text-left">Title</th>
                    <th className="py-3 px-4 text-left">XP Range</th>
                    <th className="py-3 px-4 text-left">Perks</th>
                  </tr>
                </thead>
                <tbody>
                  {xpTable.map((row) => (
                    <tr key={row.level} className="border-b border-white/5 hover:bg-white/5 transition-colors">
                      <td className="py-3 px-4 font-bold text-purple-400">{row.level}</td>
                      <td className="py-3 px-4 font-semibold text-white">{row.name}</td>
                      <td className="py-3 px-4 text-gray-400 font-mono text-xs">{row.xp}</td>
                      <td className="py-3 px-4 text-gray-400">{row.perks}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </motion.div>

            {/* Achievements */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
            >
              <h3 className="text-xl font-bold mb-4">Achievements</h3>
              <div className="grid grid-cols-2 gap-4">
                {achievements.map((a, i) => (
                  <motion.div
                    key={a.name}
                    initial={{ opacity: 0, scale: 0.9 }}
                    whileInView={{ opacity: 1, scale: 1 }}
                    viewport={{ once: true }}
                    transition={{ delay: i * 0.08 }}
                    whileHover={{ scale: 1.03 }}
                    className="p-4 rounded-xl border border-white/10 bg-white/5 flex items-center gap-3"
                  >
                    <span className="text-3xl">{a.icon}</span>
                    <div>
                      <div className="font-semibold text-sm">{a.name}</div>
                      <div className="text-xs text-gray-500">{a.desc}</div>
                    </div>
                  </motion.div>
                ))}
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* ── TESTIMONIALS ── */}
      <section className="py-24 px-4 bg-white/[0.02]">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-black mb-4">Loved by Learners</h2>
            <p className="text-gray-400 text-sm italic">(Demo testimonials for illustration purposes)</p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {testimonials.map((t, i) => (
              <motion.div
                key={t.name}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.15 }}
                className="p-6 rounded-2xl border border-white/10 bg-white/5"
              >
                <div className="flex gap-1 mb-4">
                  {Array.from({ length: t.stars }).map((_, j) => (
                    <Star key={j} className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                  ))}
                </div>
                <p className="text-gray-300 leading-relaxed mb-6">"{t.text}"</p>
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-gradient-to-br from-purple-500 to-blue-500 flex items-center justify-center font-bold text-sm">
                    {t.avatar}
                  </div>
                  <div>
                    <div className="font-semibold text-sm">{t.name}</div>
                    <div className="text-xs text-gray-500">{t.role}</div>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* ── FAQ ── */}
      <section className="py-24 px-4">
        <div className="max-w-3xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-12"
          >
            <h2 className="text-4xl md:text-5xl font-black mb-4">FAQ</h2>
          </motion.div>
          <div className="space-y-3">
            {faqs.map((faq, i) => (
              <FAQItem key={i} q={faq.q} a={faq.a} index={i} />
            ))}
          </div>
        </div>
      </section>

      {/* ── FINAL CTA ── */}
      <section className="py-24 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            className="relative p-12 rounded-3xl overflow-hidden border border-white/10"
          >
            <div className="absolute inset-0 bg-gradient-to-br from-purple-500/20 via-blue-500/10 to-indigo-500/20" />
            <div className="relative">
              <Rocket className="w-12 h-12 text-purple-400 mx-auto mb-6" />
              <h2 className="text-4xl md:text-5xl font-black mb-4">
                Ready to Start Your
                <br />
                AI Journey?
              </h2>
              <p className="text-xl text-gray-400 mb-8 max-w-xl mx-auto">
                Join thousands of learners mastering Python and AI. Free to start, no credit card required.
              </p>
              <Link
                to="/register"
                className="inline-flex items-center gap-2 px-10 py-4 rounded-xl bg-gradient-to-r from-purple-500 to-blue-500 font-bold text-lg hover:opacity-90 transition-all hover:scale-105"
              >
                Get Started Free
                <ArrowRight className="w-5 h-5" />
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      {/* ── FOOTER ── */}
      <footer className="border-t border-white/5 py-12 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mb-10">
            <div className="col-span-2 md:col-span-1">
              <div className="flex items-center gap-2 font-bold text-xl mb-4">
                <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-purple-500 to-blue-500 flex items-center justify-center">
                  <Brain className="w-5 h-5 text-white" />
                </div>
                <span className="bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">Learnova</span>
              </div>
              <p className="text-gray-500 text-sm">The AI-powered platform to master Python and AI development.</p>
            </div>
            {[
              { title: 'Learn', links: ['Paths', 'Playground', 'Projects'] },
              { title: 'Community', links: ['Leaderboard', 'Achievements', 'Mentor'] },
              { title: 'Company', links: ['About', 'Privacy', 'Terms'] },
            ].map((col) => (
              <div key={col.title}>
                <h4 className="font-semibold mb-4 text-sm text-gray-300">{col.title}</h4>
                <ul className="space-y-2">
                  {col.links.map((link) => (
                    <li key={link}>
                      <Link to={`/${link.toLowerCase()}`} className="text-sm text-gray-500 hover:text-white transition-colors">
                        {link}
                      </Link>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
          <div className="border-t border-white/5 pt-6 text-center text-sm text-gray-600">
            © {new Date().getFullYear()} Learnova. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;
