// @vitest-environment jsdom
import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { describe, expect, it } from 'vitest'
import { ForgotPasswordPage, LoginPage, RegisterPage } from './WorkspacePages'

function renderInRouter(ui: React.ReactNode) {
  return render(<MemoryRouter>{ui}</MemoryRouter>)
}

describe('authentication pages', () => {
  it('renders the login form', () => {
    renderInRouter(<LoginPage />)
    expect(screen.getByRole('heading', { name: 'Welcome back' })).toBeTruthy()
    expect(screen.getByLabelText('Email')).toBeTruthy()
    expect(screen.getByLabelText('Password')).toBeTruthy()
  })

  it('renders registration identity fields', () => {
    renderInRouter(<RegisterPage />)
    expect(screen.getByRole('heading', { name: 'Create your account' })).toBeTruthy()
    expect(screen.getByLabelText('Full name')).toBeTruthy()
    expect(screen.getByLabelText('Username')).toBeTruthy()
  })

  it('renders the new-password form for a reset token', () => {
    window.history.replaceState({}, '', '/forgot-password?token=sample-token')
    renderInRouter(<ForgotPasswordPage />)
    expect(screen.getByLabelText('New password')).toBeTruthy()
    window.history.replaceState({}, '', '/')
  })
})
