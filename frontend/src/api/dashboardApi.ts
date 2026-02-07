import apiClient from './client'

export interface DashboardSummary {
  total_employees: number
  present_today: number
  absent_today: number
  department_counts: Record<string, number>
}

export interface EmployeeAttendanceSummary {
  employee_id: string
  full_name: string
  department: string
  present_days: number
  absent_days: number
  total_days: number
  attendance_percentage: number
}

export interface DashboardResponse {
  success: boolean
  data: DashboardSummary
}

export interface AttendanceSummaryResponse {
  success: boolean
  data: EmployeeAttendanceSummary[]
  message?: string
}

export const dashboardApi = {
  /**
   * Get dashboard summary statistics
   */
  getSummary: async (): Promise<DashboardResponse> => {
    const response = await apiClient.get('/api/v1/dashboard/summary')
    return response.data
  },

  /**
   * Get attendance summary per employee
   */
  getAttendanceSummary: async (): Promise<AttendanceSummaryResponse> => {
    const response = await apiClient.get('/api/v1/dashboard/attendance-summary')
    return response.data
  },
}
