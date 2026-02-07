import { createContext, useContext, useState, useEffect, ReactNode, useMemo, useCallback } from 'react'
import { authApi, User, LoginRequest, GoogleAuthRequest } from '@/api/authApi'

interface AuthContextType {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (credentials: LoginRequest) => Promise<void>
  googleLogin: (data: GoogleAuthRequest) => Promise<void>
  logout: () => void
  checkAuth: () => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null)
  const [token, setToken] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  const isAuthenticated = useMemo(() => !!token && !!user, [token, user])

  // Check authentication status on mount
  const checkAuth = useCallback(async () => {
    setIsLoading(true)
    try {
      const storedToken = localStorage.getItem('hrms_token')
      const storedUser = localStorage.getItem('hrms_user')

      if (storedToken && storedUser) {
        setToken(storedToken)
        setUser(JSON.parse(storedUser))

        // Validate token by fetching current user
        try {
          const currentUser = await authApi.getCurrentUser()
          setUser(currentUser)
          localStorage.setItem('hrms_user', JSON.stringify(currentUser))
        } catch (error) {
          // Token is invalid, clear auth
          localStorage.removeItem('hrms_token')
          localStorage.removeItem('hrms_user')
          setToken(null)
          setUser(null)
        }
      }
    } catch (error) {
      console.error('Auth check failed:', error)
    } finally {
      setIsLoading(false)
    }
  }, [])

  useEffect(() => {
    checkAuth()
  }, [checkAuth])

  const login = useCallback(async (credentials: LoginRequest) => {
    const response = await authApi.login(credentials)
    setToken(response.access_token)
    setUser(response.user)
    localStorage.setItem('hrms_token', response.access_token)
    localStorage.setItem('hrms_user', JSON.stringify(response.user))
  }, [])

  const googleLogin = useCallback(async (data: GoogleAuthRequest) => {
    const response = await authApi.googleLogin(data)
    setToken(response.access_token)
    setUser(response.user)
    localStorage.setItem('hrms_token', response.access_token)
    localStorage.setItem('hrms_user', JSON.stringify(response.user))
  }, [])

  const logout = useCallback(() => {
    setToken(null)
    setUser(null)
    localStorage.removeItem('hrms_token')
    localStorage.removeItem('hrms_user')
  }, [])

  const value = useMemo(
    () => ({
      user,
      token,
      isAuthenticated,
      isLoading,
      login,
      googleLogin,
      logout,
      checkAuth,
    }),
    [user, token, isAuthenticated, isLoading, login, googleLogin, logout, checkAuth]
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
