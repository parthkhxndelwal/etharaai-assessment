import apiClient from './client'

export interface LoginRequest {
  email: string
  password: string
}

export interface TokenResponse {
  success: boolean
  access_token: string
  token_type: string
  user: User
}

export interface User {
  email: string
  full_name: string
  role: string
  is_active: boolean
}

export const authApi = {
  /**
   * Login with email and password
   */
  login: async (credentials: LoginRequest): Promise<TokenResponse> => {
    const response = await apiClient.post('/api/v1/auth/login', credentials)
    return response.data
  },

  /**
   * Get current user info
   */
  getCurrentUser: async (): Promise<User> => {
    const response = await apiClient.get('/api/v1/auth/me')
    return response.data
  },
}
