import { createBrowserRouter } from 'react-router-dom'
import { lazy, Suspense } from 'react'
import { PageLoader } from './components/ui/PageLoader'
import { ProtectedRoute } from './components/auth/ProtectedRoute'
import { AppLayout } from './components/layout/AppLayout'

// Lazy load all pages for code splitting
const LandingPage = lazy(() => import('./pages/LandingPage'))
const workspacePages = () => import('./pages/WorkspacePages')
const LoginPage = lazy(() => workspacePages().then((pages) => ({ default: pages.LoginPage })))
const RegisterPage = lazy(() => workspacePages().then((pages) => ({ default: pages.RegisterPage })))
const OnboardingPage = lazy(() => workspacePages().then((pages) => ({ default: pages.OnboardingPage })))
const ForgotPasswordPage = lazy(() => workspacePages().then((pages) => ({ default: pages.ForgotPasswordPage })))
const DashboardPage = lazy(() => workspacePages().then((pages) => ({ default: pages.DashboardPage })))
const LearningPathsPage = lazy(() => workspacePages().then((pages) => ({ default: pages.LearningPathsPage })))
const PathDetailPage = lazy(() => workspacePages().then((pages) => ({ default: pages.PathDetailPage })))
const LessonPage = lazy(() => workspacePages().then((pages) => ({ default: pages.LessonPage })))
const PlaygroundPage = lazy(() => workspacePages().then((pages) => ({ default: pages.PlaygroundPage })))
const MentorPage = lazy(() => workspacePages().then((pages) => ({ default: pages.MentorPage })))
const QuestsPage = lazy(() => workspacePages().then((pages) => ({ default: pages.QuestsPage })))
const AchievementsPage = lazy(() => workspacePages().then((pages) => ({ default: pages.AchievementsPage })))
const LeaderboardPage = lazy(() => workspacePages().then((pages) => ({ default: pages.LeaderboardPage })))
const ProjectsPage = lazy(() => workspacePages().then((pages) => ({ default: pages.ProjectsPage })))
const ProjectDetailPage = lazy(() => workspacePages().then((pages) => ({ default: pages.ProjectDetailPage })))
const ProfilePage = lazy(() => workspacePages().then((pages) => ({ default: pages.ProfilePage })))
const AnalyticsPage = lazy(() => workspacePages().then((pages) => ({ default: pages.AnalyticsPage })))
const AdminPage = lazy(() => workspacePages().then((pages) => ({ default: pages.AdminPage })))
const NotFoundPage = lazy(() => workspacePages().then((pages) => ({ default: pages.NotFoundPage })))

function withSuspense(Component: React.ComponentType) {
  return (
    <Suspense fallback={<PageLoader />}>
      <Component />
    </Suspense>
  )
}

function protectedPage(Component: React.ComponentType, adminOnly = false) {
  return (
    <ProtectedRoute adminOnly={adminOnly}>
      <AppLayout>{withSuspense(Component)}</AppLayout>
    </ProtectedRoute>
  )
}

export const router = createBrowserRouter([
  { path: '/', element: withSuspense(LandingPage) },
  { path: '/login', element: withSuspense(LoginPage) },
  { path: '/register', element: withSuspense(RegisterPage) },
  { path: '/forgot-password', element: withSuspense(ForgotPasswordPage) },
  { path: '/onboarding', element: protectedPage(OnboardingPage) },
  { path: '/dashboard', element: protectedPage(DashboardPage) },
  { path: '/paths', element: protectedPage(LearningPathsPage) },
  { path: '/paths/:slug', element: protectedPage(PathDetailPage) },
  { path: '/lessons/:lessonId', element: protectedPage(LessonPage) },
  { path: '/playground', element: protectedPage(PlaygroundPage) },
  { path: '/mentor', element: protectedPage(MentorPage) },
  { path: '/quests', element: protectedPage(QuestsPage) },
  { path: '/achievements', element: protectedPage(AchievementsPage) },
  { path: '/leaderboard', element: protectedPage(LeaderboardPage) },
  { path: '/projects', element: protectedPage(ProjectsPage) },
  { path: '/projects/:projectId', element: protectedPage(ProjectDetailPage) },
  { path: '/profile', element: protectedPage(ProfilePage) },
  { path: '/analytics', element: protectedPage(AnalyticsPage) },
  { path: '/admin', element: protectedPage(AdminPage, true) },
  { path: '*', element: withSuspense(NotFoundPage) },
])
