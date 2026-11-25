import { useRef, useState, type FormEvent, type ReactNode } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import axios from 'axios'
import Editor from '@monaco-editor/react'
import { api } from '@/lib/api'
import { useAuthStore, type User } from '@/store/authStore'
import { useUIStore } from '@/store/uiStore'

type PathSummary = {
  id: number
  slug: string
  title: string
  subtitle: string
  description: string
  difficulty: string
  estimated_hours: number
  total_lessons: number
  completed_lessons: number
  progress_percentage: number
}

type LessonSummary = {
  id: number
  title: string
  summary: string
  status: string
  estimated_minutes: number
  xp_reward: number
}

type LearningPath = PathSummary & {
  modules: Array<{ id: number; title: string; description: string; lessons: LessonSummary[] }>
}

function useApiData<T>(key: string, url: string) {
  return useQuery<T>({
    queryKey: [key, url],
    queryFn: async () => (await api.get<T>(url)).data,
  })
}

function getErrorMessage(error: unknown, fallback: string) {
  if (axios.isAxiosError<{ detail?: string }>(error)) {
    return error.response?.data?.detail ?? fallback
  }
  return fallback
}

function Page({ title, subtitle, children }: { title: string; subtitle?: string; children: ReactNode }) {
  return (
    <section className="space-y-6">
      <header>
        <h1 className="text-3xl font-bold text-slate-900">{title}</h1>
        {subtitle && <p className="mt-2 text-slate-600">{subtitle}</p>}
      </header>
      {children}
    </section>
  )
}

function QueryState({ loading, error, children }: { loading: boolean; error: unknown; children: ReactNode }) {
  if (loading) return <p className="text-slate-500">Loading…</p>
  if (error) return <div role="alert" className="card p-5 text-red-700">Could not load this information. Please try again.</div>
  return <>{children}</>
}

function AuthFrame({ title, children }: { title: string; children: ReactNode }) {
  return (
    <main className="min-h-screen flex items-center justify-center px-4 py-12">
      <div className="card w-full max-w-md p-8">
        <Link to="/" className="gradient-text font-bold text-lg">Learnova</Link>
        <h1 className="mt-6 text-2xl font-bold">{title}</h1>
        {children}
      </div>
    </main>
  )
}

function AuthForm({ mode }: { mode: 'login' | 'register' }) {
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)
  const navigate = useNavigate()
  const setUser = useAuthStore((state) => state.setUser)

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError('')
    setBusy(true)
    const form = new FormData(event.currentTarget)
    const payload = Object.fromEntries(form.entries())
    try {
      const { data } = await api.post<User>(`/auth/${mode}`, payload)
      setUser(data)
      navigate(mode === 'register' || !data.onboarding_completed ? '/onboarding' : '/dashboard')
    } catch (requestError: unknown) {
      setError(getErrorMessage(requestError, 'Unable to continue. Check your details and try again.'))
    } finally {
      setBusy(false)
    }
  }

  return (
    <AuthFrame title={mode === 'login' ? 'Welcome back' : 'Create your account'}>
      <form className="mt-6 space-y-4" onSubmit={submit}>
        {mode === 'register' && <>
          <label className="block text-sm font-medium">Full name<input className="input-field mt-1" name="full_name" required autoComplete="name" /></label>
          <label className="block text-sm font-medium">Username<input className="input-field mt-1" name="username" required autoComplete="username" /></label>
        </>}
        <label className="block text-sm font-medium">Email<input className="input-field mt-1" name="email" type="email" required autoComplete="email" /></label>
        <label className="block text-sm font-medium">Password<input className="input-field mt-1" name="password" type="password" minLength={8} required autoComplete={mode === 'login' ? 'current-password' : 'new-password'} /></label>
        {error && <p role="alert" className="text-sm text-red-700">{error}</p>}
        <button className="btn-primary w-full justify-center" disabled={busy}>{busy ? 'Please wait…' : mode === 'login' ? 'Sign in' : 'Create account'}</button>
      </form>
      <div className="mt-5 flex justify-between text-sm">
        {mode === 'login' ? <Link className="text-brand-600" to="/forgot-password">Forgot password?</Link> : <span />}
        <Link className="text-brand-600" to={mode === 'login' ? '/register' : '/login'}>{mode === 'login' ? 'Create account' : 'Sign in'}</Link>
      </div>
    </AuthFrame>
  )
}

export function LoginPage() { return <AuthForm mode="login" /> }
export function RegisterPage() { return <AuthForm mode="register" /> }

export function ForgotPasswordPage() {
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const [token, setToken] = useState(() => new URLSearchParams(window.location.search).get('token') ?? '')
  const [resetComplete, setResetComplete] = useState(false)
  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setMessage('')
    setError('')
    try {
      const form = new FormData(event.currentTarget)
      const { data } = await api.post('/auth/forgot-password', { email: form.get('email') })
      setMessage(data.detail)
      if (data.dev_token) setToken(data.dev_token)
    } catch (e: unknown) {
      setError(getErrorMessage(e, 'Unable to request a reset link.'))
    }
  }
  async function reset(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setMessage('')
    setError('')
    try {
      const form = new FormData(event.currentTarget)
      await api.post('/auth/reset-password', { token, new_password: form.get('new_password') })
      setResetComplete(true)
      setMessage('Password reset successfully. You can now sign in.')
    } catch (requestError: unknown) {
      setError(getErrorMessage(requestError, 'Unable to reset your password.'))
    }
  }
  return <AuthFrame title="Reset your password">
    {!token ? <form className="mt-6 space-y-4" onSubmit={(event) => void submit(event)}>
      <label className="block text-sm font-medium">Email<input className="input-field mt-1" type="email" name="email" required /></label>
      {message && <p role="status" className="text-sm text-green-700 break-all">{message}</p>}
      {error && <p role="alert" className="text-sm text-red-700">{error}</p>}
      <button className="btn-primary w-full justify-center">Send reset instructions</button>
    </form> : <form className="mt-6 space-y-4" onSubmit={(event) => void reset(event)}>
      <label className="block text-sm font-medium">New password<input className="input-field mt-1" type="password" name="new_password" minLength={8} required autoComplete="new-password" /></label>
      {message && <p role="status" className="text-sm text-green-700">{message}</p>}
      {error && <p role="alert" className="text-sm text-red-700">{error}</p>}
      {!resetComplete && <button className="btn-primary w-full justify-center">Set new password</button>}
    </form>}
    <Link className="mt-5 block text-sm text-brand-600" to="/login">Back to sign in</Link>
  </AuthFrame>
}

export function OnboardingPage() {
  const [step, setStep] = useState(0)
  const [experience, setExperience] = useState('complete_beginner')
  const [interests, setInterests] = useState<string[]>(['python'])
  const [goal, setGoal] = useState('')
  const [minutes, setMinutes] = useState(30)
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)
  const setUser = useAuthStore((state) => state.setUser)
  const navigate = useNavigate()
  const options = ['python', 'data science', 'machine learning', 'deep learning', 'generative ai', 'ai engineering']

  async function finish() {
    setBusy(true)
    setError('')
    try {
      await api.post('/auth/onboarding', { experience_level: experience, interests, learning_goal: goal, daily_minutes: minutes })
      const { data } = await api.get<User>('/users/me')
      setUser(data)
      navigate('/dashboard')
    } catch (e: unknown) {
      setError(getErrorMessage(e, 'Unable to save your learning plan.'))
    } finally {
      setBusy(false)
    }
  }

  return <AuthFrame title={`Set up your learning plan · ${step + 1}/4`}>
    <div className="mt-6 space-y-5">
      {step === 0 && <label className="block text-sm font-medium">How much Python or AI experience do you have?
        <select className="input-field mt-2" value={experience} onChange={(e) => setExperience(e.target.value)}>
          <option value="complete_beginner">I’m a complete beginner</option><option value="beginner">Some basics</option><option value="intermediate">Comfortable coding</option><option value="advanced">Experienced</option>
        </select>
      </label>}
      {step === 1 && <fieldset><legend className="text-sm font-medium">Choose the topics you’re interested in</legend><div className="mt-3 grid grid-cols-2 gap-2">
        {options.map((item) => <label key={item} className="card p-3 text-sm flex gap-2 items-center"><input type="checkbox" checked={interests.includes(item)} onChange={(e) => setInterests((old) => e.target.checked ? [...old, item] : old.filter((x) => x !== item))} />{item}</label>)}
      </div></fieldset>}
      {step === 2 && <label className="block text-sm font-medium">What do you want to achieve?
        <textarea className="input-field mt-2 min-h-28" value={goal} onChange={(e) => setGoal(e.target.value)} placeholder="e.g. Build my first machine learning project" />
      </label>}
      {step === 3 && <label className="block text-sm font-medium">Daily learning goal: {minutes} minutes
        <input className="mt-4 w-full" type="range" min="10" max="120" step="10" value={minutes} onChange={(e) => setMinutes(Number(e.target.value))} />
      </label>}
      {error && <p role="alert" className="text-sm text-red-700">{error}</p>}
      <div className="flex justify-between">
        <button className="btn-secondary" disabled={step === 0 || busy} onClick={() => setStep(step - 1)}>Back</button>
        {step < 3 ? <button className="btn-primary" onClick={() => setStep(step + 1)}>Continue</button> : <button className="btn-primary" disabled={busy || interests.length === 0} onClick={finish}>{busy ? 'Saving…' : 'Start learning'}</button>}
      </div>
    </div>
  </AuthFrame>
}

export function DashboardPage() {
  const stats = useApiData<Record<string, any>>('stats', '/users/me/stats')
  const paths = useApiData<PathSummary[]>('paths', '/learning/paths')
  const user = useAuthStore((state) => state.user)
  return <Page title={`Welcome back${user?.full_name ? `, ${user.full_name.split(' ')[0]}` : ''}!`} subtitle="Your learning journey, all in one place.">
    <QueryState loading={stats.isLoading || paths.isLoading} error={stats.error || paths.error}>
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {[['Total XP', stats.data?.total_xp ?? 0], ['Lessons completed', stats.data?.lessons_completed ?? 0], ['Current streak', `${stats.data?.current_streak ?? 0} days`], ['Learning time', `${stats.data?.total_learning_minutes ?? 0} min`]].map(([label, value]) => <div key={String(label)} className="card p-5"><p className="text-sm text-slate-500">{label}</p><p className="mt-2 text-2xl font-bold">{value}</p></div>)}
      </div>
      <div><h2 className="text-xl font-bold mb-3">Continue learning</h2><PathCards paths={(paths.data ?? []).slice(0, 3)} /></div>
      <div className="flex flex-wrap gap-3"><Link className="btn-secondary" to="/quests">View quests</Link><Link className="btn-secondary" to="/mentor">Ask the AI mentor</Link><Link className="btn-secondary" to="/projects">Explore projects</Link></div>
    </QueryState>
  </Page>
}

function PathCards({ paths }: { paths: PathSummary[] }) {
  if (!paths.length) return <p className="text-slate-500">No learning paths are available yet.</p>
  return <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">{paths.map((path) => <Link className="card-hover p-5" key={path.id} to={`/paths/${path.slug}`}>
    <div className="flex justify-between"><span className="badge bg-brand-50 text-brand-700">{path.difficulty}</span><span className="text-sm text-slate-500">{path.estimated_hours} hours</span></div>
    <h3 className="mt-4 text-lg font-bold">{path.title}</h3><p className="mt-1 text-sm text-slate-600">{path.subtitle}</p>
    <div className="mt-4 h-2 rounded-full bg-slate-100"><div className="h-full rounded-full bg-brand-600" style={{ width: `${path.progress_percentage}%` }} /></div>
    <p className="mt-2 text-xs text-slate-500">{path.completed_lessons}/{path.total_lessons} lessons · {path.progress_percentage}%</p>
  </Link>)}</div>
}

export function LearningPathsPage() {
  const query = useApiData<PathSummary[]>('paths', '/learning/paths')
  return <Page title="Learning paths" subtitle="Structured roadmaps from fundamentals to production AI.">
    <QueryState loading={query.isLoading} error={query.error}><PathCards paths={query.data ?? []} /></QueryState>
  </Page>
}

export function PathDetailPage() {
  const { slug = '' } = useParams()
  const query = useApiData<LearningPath>('path', `/learning/paths/${slug}`)
  return <Page title={query.data?.title ?? 'Learning path'} subtitle={query.data?.description}>
    <QueryState loading={query.isLoading} error={query.error}>
      <div className="space-y-5">{query.data?.modules.map((module) => <section key={module.id} className="card p-5">
        <h2 className="text-xl font-bold">{module.title}</h2><p className="mt-1 text-sm text-slate-600">{module.description}</p>
        <ul className="mt-4 divide-y divide-slate-100">{module.lessons.map((lesson) => <li key={lesson.id} className="py-3 flex items-center justify-between gap-4">
          <div><Link className="font-semibold hover:text-brand-600" to={`/lessons/${lesson.id}`}>{lesson.title}</Link><p className="text-sm text-slate-500">{lesson.summary}</p></div><span className="text-xs text-slate-500 whitespace-nowrap">{lesson.status} · {lesson.xp_reward} XP</span>
        </li>)}</ul>
      </section>)}</div>
    </QueryState>
  </Page>
}

type LessonData = LessonSummary & {
  learning_objectives: string[]
  content_blocks: Array<{ type: string; content: string; language?: string; variant?: string }>
  key_terms: string[]
  common_mistakes: string[]
  starter_code: string
  quiz?: {
    id: number
    title: string
    questions: Array<{ id: number; prompt: string; question_type: string; code_snippet?: string; options?: string[] }>
  } | null
}

export function LessonPage() {
  const { lessonId = '' } = useParams()
  const query = useApiData<LessonData>('lesson', `/learning/lessons/${lessonId}`)
  const [notice, setNotice] = useState('')
  const [actionError, setActionError] = useState('')
  const [answers, setAnswers] = useState<Record<string, string>>({})
  const [quizResult, setQuizResult] = useState<Record<string, any> | null>(null)
  const [quizError, setQuizError] = useState('')
  const quizStartedAt = useRef(Date.now())
  const { showXPPopup } = useUIStore()
  async function complete() {
    setActionError('')
    try {
      const { data } = await api.post(`/learning/lessons/${lessonId}/complete`)
      showXPPopup(data.xp_result?.xp_added ?? 0)
      setNotice(data.already_completed ? 'This lesson is already complete.' : 'Lesson complete — XP added!')
    } catch (error: unknown) {
      setActionError(getErrorMessage(error, 'Could not complete this lesson.'))
    }
  }
  async function submitQuiz(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (!query.data?.quiz) return
    setQuizError('')
    setQuizResult(null)
    try {
      const { data } = await api.post(`/learning/quizzes/${query.data.quiz.id}/submit`, {
        answers,
        duration_seconds: Math.floor((Date.now() - quizStartedAt.current) / 1000),
      })
      setQuizResult(data)
      if (data.xp_result?.xp_added) showXPPopup(data.xp_result.xp_added)
    } catch (error: unknown) {
      setQuizError(getErrorMessage(error, 'Could not submit this quiz.'))
    }
  }
  return <Page title={query.data?.title ?? 'Lesson'} subtitle={query.data?.summary}>
    <QueryState loading={query.isLoading} error={query.error}>
      <div className="grid gap-6 lg:grid-cols-[minmax(0,1fr)_280px]">
        <article className="card p-6 space-y-5">{query.data?.content_blocks.map((block, i) => <div key={i} className={block.type === 'code' ? 'rounded-xl bg-slate-950 p-4 text-sm text-slate-100 whitespace-pre-wrap font-mono' : block.type === 'callout' ? 'rounded-xl bg-blue-50 p-4 text-blue-900' : 'leading-7 whitespace-pre-wrap text-slate-700'}>{block.content}</div>)}
          {query.data?.quiz && <form className="rounded-xl border border-slate-200 p-5 space-y-5" onSubmit={(event) => void submitQuiz(event)}>
            <header><h2 className="text-lg font-bold">{query.data.quiz.title}</h2><p className="mt-1 text-sm text-slate-600">{query.data.quiz.questions.length} questions</p></header>
            {query.data.quiz.questions.map((question, index) => <fieldset key={question.id} className="space-y-2">
              <legend className="font-medium">{index + 1}. {question.prompt}</legend>
              {question.code_snippet && <pre className="rounded-lg bg-slate-950 p-3 text-sm text-white whitespace-pre-wrap">{question.code_snippet}</pre>}
              {question.options?.length ? <div className="grid gap-2 sm:grid-cols-2">{question.options.map((option) => <label key={option} className="flex items-start gap-2 rounded-lg border p-3 text-sm"><input type="radio" name={`question-${question.id}`} value={option} checked={answers[String(question.id)] === option} onChange={(event) => setAnswers((current) => ({ ...current, [String(question.id)]: event.target.value }))} required />{option}</label>)}</div>
                : <input className="input-field" aria-label={`Answer question ${index + 1}`} value={answers[String(question.id)] ?? ''} onChange={(event) => setAnswers((current) => ({ ...current, [String(question.id)]: event.target.value }))} required />}
              {quizResult?.results?.[index] && <p className={quizResult.results[index].correct ? 'text-sm text-green-700' : 'text-sm text-red-700'}>
                {quizResult.results[index].correct ? 'Correct.' : `Answer: ${quizResult.results[index].correct_answer}.`} {quizResult.results[index].explanation}
              </p>}
            </fieldset>)}
            {quizError && <p role="alert" className="text-sm text-red-700">{quizError}</p>}
            {quizResult && <p role="status" className="font-semibold">{quizResult.passed ? 'Quiz passed' : 'Try again'} · {quizResult.score_percentage}% · {quizResult.xp_result?.xp_added ?? 0} XP earned</p>}
            <button className="btn-primary" disabled={Object.keys(answers).length !== query.data.quiz.questions.length}>Submit quiz</button>
          </form>}
          {notice && <p role="status" className="text-green-700">{notice}</p>}
          {actionError && <p role="alert" className="text-red-700">{actionError}</p>}
          <button className="btn-primary" onClick={() => void complete()}>Mark lesson complete</button>
        </article>
        <aside className="card h-fit p-5"><h2 className="font-bold">Lesson guide</h2><p className="mt-2 text-sm text-slate-600">{query.data?.estimated_minutes} min · {query.data?.xp_reward} XP</p><h3 className="mt-5 font-semibold">Learning objectives</h3><ul className="mt-2 list-disc pl-5 text-sm text-slate-600">{query.data?.learning_objectives?.map((item) => <li key={item}>{item}</li>)}</ul></aside>
      </div>
    </QueryState>
  </Page>
}

export function PlaygroundPage() {
  const [code, setCode] = useState("print('Hello, Learnova!')")
  const [output, setOutput] = useState('')
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  async function run() {
    setBusy(true); setError(''); setOutput('')
    try {
      const { data } = await api.post('/sandbox/execute', { code })
      setOutput(data.stdout || data.output || '')
      if (data.stderr) setError(data.stderr)
    } catch (e: unknown) {
      setError(getErrorMessage(e, 'Code execution failed.'))
    } finally { setBusy(false) }
  }
  return <Page title="Python playground" subtitle="Experiment in a restricted server-side Python sandbox.">
    <div className="card overflow-hidden"><div className="h-[420px]"><Editor language="python" theme="vs-dark" value={code} onChange={(value) => setCode(value ?? '')} options={{ minimap: { enabled: false }, fontSize: 14 }} /></div>
      <div className="flex items-center justify-between border-t p-4"><span className="text-sm text-slate-500">Python · isolated runner</span><button className="btn-primary" disabled={busy} onClick={() => void run()}>{busy ? 'Running…' : 'Run code'}</button></div>
      {(output || error) && <pre className={`border-t p-4 text-sm whitespace-pre-wrap ${error ? 'text-red-700' : 'text-slate-800'}`}>{error || output}</pre>}
    </div>
  </Page>
}

type ChatMessage = { role: 'user' | 'assistant'; content: string }
type ConversationSummary = { id: number; title: string; mode: string; updated_at: string }
export function MentorPage() {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [message, setMessage] = useState('')
  const [mode, setMode] = useState('hint')
  const [conversationId, setConversationId] = useState<number | null>(null)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const conversations = useApiData<ConversationSummary[]>('mentor-conversations', '/mentor/conversations')

  async function openConversation(id: number) {
    setError('')
    try {
      const { data } = await api.get<{ id: number; mode: string; messages: ChatMessage[] }>(`/mentor/conversations/${id}`)
      setConversationId(data.id)
      setMode(data.mode)
      setMessages(data.messages)
    } catch (requestError: unknown) {
      setError(getErrorMessage(requestError, 'Could not load this conversation.'))
    }
  }

  async function send(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (!message.trim()) return
    const text = message.trim()
    setMessages((old) => [...old, { role: 'user', content: text }])
    setMessage(''); setBusy(true); setError('')
    try {
      const { data } = await api.post('/mentor/chat', { message: text, mode, conversation_id: conversationId })
      setConversationId(data.conversation_id)
      setMessages((old) => [...old, { role: 'assistant', content: data.reply }])
      await conversations.refetch()
    } catch (e: unknown) {
      setError(getErrorMessage(e, 'The mentor could not respond. Please try again.'))
    } finally { setBusy(false) }
  }
  return <Page title="Socratic AI mentor" subtitle="Ask for a hint, explore a concept, or debug a problem together.">
    <div className="grid gap-4 lg:grid-cols-[240px_minmax(0,1fr)]">
      <aside className="card p-4"><div className="flex items-center justify-between gap-2"><h2 className="font-semibold">Conversations</h2><button className="text-sm text-brand-600" onClick={() => { setConversationId(null); setMessages([]); setError('') }}>New</button></div>
        <div className="mt-3 space-y-1">{(conversations.data ?? []).map((conversation) => <button key={conversation.id} className={`w-full rounded-lg px-3 py-2 text-left text-sm hover:bg-slate-50 ${conversationId === conversation.id ? 'bg-brand-50 text-brand-800' : 'text-slate-600'}`} onClick={() => void openConversation(conversation.id)}>{conversation.title}</button>)}
          {!conversations.isLoading && !conversations.data?.length && <p className="text-xs text-slate-500">Your conversations will appear here.</p>}
        </div>
      </aside>
    <div className="card flex min-h-[480px] flex-col p-5">
      <label className="mb-4 text-sm font-medium">Teaching mode<select className="input-field mt-1" value={mode} onChange={(e) => setMode(e.target.value)}>{['hint', 'beginner', 'deep_technical', 'debug', 'test_me', 'interview', 'example'].map((m) => <option key={m} value={m}>{m.replace(/_/g, ' ')}</option>)}</select></label>
      <div className="flex-1 space-y-3 overflow-y-auto">{messages.length === 0 && <p className="text-sm text-slate-500">What are you learning today?</p>}{messages.map((item, index) => <div key={index} className={`max-w-[85%] whitespace-pre-wrap rounded-xl p-3 text-sm ${item.role === 'user' ? 'ml-auto bg-brand-50 text-brand-950' : 'bg-slate-100 text-slate-800'}`}><strong className="block mb-1">{item.role === 'user' ? 'You' : 'Mentor'}</strong>{item.content}</div>)}</div>
      {error && <p role="alert" className="mt-3 text-sm text-red-700">{error}</p>}
      <form className="mt-4 flex gap-2" onSubmit={(e) => void send(e)}><input className="input-field" value={message} onChange={(e) => setMessage(e.target.value)} maxLength={4000} placeholder="Ask your question…" /><button className="btn-primary" disabled={busy || !message.trim()}>{busy ? 'Thinking…' : 'Ask'}</button></form>
    </div>
    </div>
  </Page>
}

function DataListPage({ title, subtitle, endpoint }: { title: string; subtitle: string; endpoint: string }) {
  const query = useApiData<unknown>('listing', endpoint)
  return <Page title={title} subtitle={subtitle}><QueryState loading={query.isLoading} error={query.error}>
    {Array.isArray(query.data) && query.data.length > 0 ? <div className="grid gap-3 md:grid-cols-2">{query.data.map((item: any, i) => <div key={item.id ?? item.code ?? i} className="card p-5"><h2 className="font-semibold">{item.title ?? item.name ?? item.username ?? item.code ?? `${title} ${i + 1}`}</h2><p className="mt-1 text-sm text-slate-600">{item.description ?? item.subtitle ?? item.status ?? ''}</p>{item.xp_reward != null && <span className="mt-3 inline-block badge bg-amber-50 text-amber-800">{item.xp_reward} XP</span>}</div>)}</div>
      : <div className="card p-6 text-slate-600">Nothing to show yet. Keep learning and check back soon.</div>}
  </QueryState></Page>
}

type QuestData = { id: number; quest_id: number; title: string; description: string; xp_reward: number; target_count: number; progress_count: number; completed: boolean; claimed: boolean }
export function QuestsPage() {
  const query = useApiData<QuestData[]>('quests', '/quests/all')
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  async function claim(questId: number) {
    setMessage(''); setError('')
    try {
      await api.post(`/quests/${questId}/claim`)
      setMessage('Reward claimed! Refresh to see updated progress.')
      await query.refetch()
    } catch (requestError: unknown) {
      setError(getErrorMessage(requestError, 'Could not claim this reward.'))
    }
  }
  return <Page title="Quests" subtitle="Complete activities and claim rewards.">
    <QueryState loading={query.isLoading} error={query.error}>
      {message && <p role="status" className="text-green-700">{message}</p>}
      {error && <p role="alert" className="text-red-700">{error}</p>}
      <div className="grid gap-3 md:grid-cols-2">{(query.data ?? []).map((quest) => <div key={quest.id} className="card p-5">
        <div className="flex items-start justify-between gap-3"><h2 className="font-semibold">{quest.title}</h2><span className="badge bg-amber-50 text-amber-800">{quest.xp_reward} XP</span></div>
        <p className="mt-2 text-sm text-slate-600">{quest.description}</p>
        <div className="mt-4 h-2 rounded-full bg-slate-100"><div className="h-full rounded-full bg-brand-600" style={{ width: `${Math.min(100, quest.progress_count / quest.target_count * 100)}%` }} /></div>
        <div className="mt-2 flex items-center justify-between text-xs text-slate-500"><span>{quest.progress_count}/{quest.target_count}</span>
          {quest.completed && !quest.claimed ? <button className="btn-primary px-3 py-1.5" onClick={() => void claim(quest.quest_id ?? quest.id)}>Claim reward</button> : <span>{quest.claimed ? 'Claimed' : quest.completed ? 'Complete' : 'In progress'}</span>}
        </div>
      </div>)}</div>
    </QueryState>
  </Page>
}
export function AchievementsPage() { return <DataListPage title="Achievements" subtitle="Milestones earned throughout your learning journey." endpoint="/gamification/achievements" /> }
export function LeaderboardPage() { return <DataListPage title="Leaderboard" subtitle="Compare progress with the Learnova community." endpoint="/leaderboard/global" /> }
export function ProjectsPage() {
  const query = useApiData<Array<{ id: number; title: string; summary: string; difficulty: string; technologies: string[]; completed: boolean }>>('projects', '/projects')
  return <Page title="Project lab" subtitle="Apply your skills to real-world AI projects.">
    <QueryState loading={query.isLoading} error={query.error}><div className="grid gap-4 md:grid-cols-2">
      {(query.data ?? []).map((project) => <Link className="card-hover p-5" key={project.id} to={`/projects/${project.id}`}>
        <div className="flex items-start justify-between gap-3"><h2 className="text-lg font-bold">{project.title}</h2><span className="badge bg-brand-50 text-brand-700">{project.completed ? 'Completed' : project.difficulty}</span></div>
        <p className="mt-2 text-sm text-slate-600">{project.summary}</p>
        <p className="mt-4 text-xs text-slate-500">{project.technologies?.join(' · ')}</p>
      </Link>)}
      {!query.data?.length && <div className="card p-6 text-slate-600">No projects are available yet.</div>}
    </div></QueryState>
  </Page>
}

export function ProjectDetailPage() {
  const { projectId = '' } = useParams()
  const query = useApiData<Record<string, any>>('project', `/projects/${projectId}`)
  const [submission, setSubmission] = useState('')
  const [result, setResult] = useState('')
  const [error, setError] = useState('')
  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); setError(''); setResult('')
    try {
      const { data } = await api.post(`/projects/${projectId}/submit`, { code: submission })
      setResult(data.feedback ?? data.message ?? 'Submission received.')
    } catch (e: unknown) { setError(getErrorMessage(e, 'Submission failed.')) }
  }
  return <Page title={query.data?.title ?? 'Project'} subtitle={query.data?.description}>
    <QueryState loading={query.isLoading} error={query.error}><div className="card p-5"><h2 className="text-xl font-bold">Project workspace</h2><p className="mt-2 text-sm text-slate-600">Describe your approach or include a code submission for backend evaluation.</p>
      <form className="mt-4 space-y-3" onSubmit={(e) => void submit(e)}><textarea className="input-field min-h-48 font-mono" value={submission} onChange={(e) => setSubmission(e.target.value)} required placeholder="Write your solution or project notes…" /><button className="btn-primary">Submit for evaluation</button></form>
      {result && <p role="status" className="mt-4 text-green-700">{result}</p>}{error && <p role="alert" className="mt-4 text-red-700">{error}</p>}
    </div></QueryState>
  </Page>
}

export function ProfilePage() {
  const user = useAuthStore((state) => state.user)
  const updateUser = useAuthStore((state) => state.updateUser)
  const [notice, setNotice] = useState('')
  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); setNotice('')
    const form = new FormData(event.currentTarget)
    const payload = Object.fromEntries(form.entries())
    try {
      await api.patch('/users/me', payload)
      updateUser({ full_name: String(payload.full_name) })
      setNotice('Profile saved.')
    } catch (e: unknown) { setNotice(getErrorMessage(e, 'Could not save your profile.')) }
  }
  return <Page title="Profile & settings" subtitle="Keep your learner profile up to date.">
    <form className="card max-w-2xl space-y-4 p-6" onSubmit={(e) => void submit(e)}>
      <label className="block text-sm font-medium">Full name<input name="full_name" className="input-field mt-1" defaultValue={user?.full_name} required /></label>
      <label className="block text-sm font-medium">Bio<textarea name="bio" className="input-field mt-1" defaultValue={user?.profile?.bio} /></label>
      <label className="block text-sm font-medium">Timezone<input name="timezone" className="input-field mt-1" defaultValue={user?.profile?.timezone ?? 'UTC'} /></label>
      <label className="block text-sm font-medium">GitHub profile<input name="github_url" type="url" className="input-field mt-1" defaultValue={user?.profile?.github_url} /></label>
      {notice && <p role="status" className="text-sm">{notice}</p>}<button className="btn-primary">Save profile</button>
    </form>
  </Page>
}

export function AnalyticsPage() {
  const query = useApiData<Record<string, any>>('analytics', '/users/me/stats')
  return <Page title="Learning analytics" subtitle="Review your recent activity and learning progress.">
    <QueryState loading={query.isLoading} error={query.error}><div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
      {Object.entries({ 'Lessons completed': query.data?.lessons_completed, 'Challenges solved': query.data?.challenges_solved, 'Learning minutes': query.data?.total_learning_minutes, 'Average quiz score': query.data?.avg_quiz_score }).map(([label, value]) => <div className="card p-5" key={label}><p className="text-sm text-slate-500">{label}</p><p className="mt-2 text-2xl font-bold">{value ?? 0}</p></div>)}
    </div><div className="card mt-5 p-5"><h2 className="font-bold">Weekly activity</h2><div className="mt-4 grid grid-cols-7 gap-2">{(query.data?.weekly_activity ?? []).map((day: any) => <div key={day.date} className="rounded-lg bg-brand-50 p-3 text-center"><div className="text-xs text-slate-500">{day.date.slice(5)}</div><div className="mt-1 font-bold">{day.xp_earned} XP</div><div className="text-xs text-slate-500">{day.minutes_learned} min</div></div>)}</div></div></QueryState>
  </Page>
}

export function AdminPage() {
  const query = useApiData<Record<string, any>>('admin', '/admin/stats')
  return <Page title="Admin console" subtitle="Platform overview and user management.">
    <QueryState loading={query.isLoading} error={query.error}><div className="card p-5"><h2 className="font-bold">Platform metrics</h2><pre className="mt-3 overflow-auto text-sm">{JSON.stringify(query.data, null, 2)}</pre></div><div className="mt-5"><DataListPage title="Users" subtitle="Registered learners." endpoint="/admin/users" /></div></QueryState>
  </Page>
}

export function NotFoundPage() {
  return <main className="min-h-screen grid place-items-center px-6 text-center"><div><p className="text-sm font-semibold text-brand-600">404</p><h1 className="mt-2 text-3xl font-bold">Page not found</h1><p className="mt-3 text-slate-600">This page may have moved or does not exist.</p><Link className="btn-primary mt-6" to="/dashboard">Back to dashboard</Link></div></main>
}
