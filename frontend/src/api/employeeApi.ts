import apiClient from './client'

export interface Employee {
  id: string
  employee_id: string
  full_name: string
  email: string
  department: string
  position: string
  created_at: string
  updated_at: string
}

export interface EmployeeCreate {
  employee_id: string
  full_name: string
  email: string
  department: string
  position: string
}

export interface EmployeeUpdate {
  full_name?: string
  email?: string
  department?: string
  position?: string
}

export interface EmployeeListResponse {
  success: boolean
  data: Employee[]
  total: number
}

export interface EmployeeResponse {
  success: boolean
  data: Employee
  message?: string
}

export const employeeApi = {
  /**
   * Get all employees with optional filters
   */
  getEmployees: async (params?: {
    department?: string
    search?: string
  }): Promise<EmployeeListResponse> => {
    const response = await apiClient.get('/api/v1/employees', { params })
    return response.data
  },

  /**
   * Get single employee by ID
   */
  getEmployee: async (employeeId: string): Promise<EmployeeResponse> => {
    const response = await apiClient.get(`/api/v1/employees/${employeeId}`)
    return response.data
  },

  /**
   * Create new employee
   */
  createEmployee: async (data: EmployeeCreate): Promise<EmployeeResponse> => {
    const response = await apiClient.post('/api/v1/employees', data)
    return response.data
  },

  /**
   * Update existing employee
   */
  updateEmployee: async (
    employeeId: string,
    data: EmployeeUpdate
  ): Promise<EmployeeResponse> => {
    const response = await apiClient.put(`/api/v1/employees/${employeeId}`, data)
    return response.data
  },

  /**
   * Delete employee
   */
  deleteEmployee: async (employeeId: string): Promise<{ success: boolean; message: string }> => {
    const response = await apiClient.delete(`/api/v1/employees/${employeeId}`)
    return response.data
  },
}
