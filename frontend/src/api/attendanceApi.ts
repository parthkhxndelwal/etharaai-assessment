import apiClient from './client'

export interface AttendanceRecord {
  id: string
  employee_id: string
  employee_name?: string
  date: string
  status: string
  notes?: string
  created_at: string
}

export interface AttendanceCreate {
  employee_id: string
  date: string
  status: string
  notes?: string
}

export interface AttendanceUpdate {
  status?: string
  notes?: string
}

export interface AttendanceListResponse {
  success: boolean
  data: AttendanceRecord[]
  total: number
}

export interface AttendanceResponse {
  success: boolean
  data: AttendanceRecord
  message?: string
}

export const attendanceApi = {
  /**
   * Get all attendance records with optional filters
   */
  getAttendance: async (params?: {
    employee_id?: string
    date?: string
    start_date?: string
    end_date?: string
    status?: string
  }): Promise<AttendanceListResponse> => {
    const response = await apiClient.get('/api/v1/attendance', { params })
    return response.data
  },

  /**
   * Get attendance records for specific employee
   */
  getEmployeeAttendance: async (
    employeeId: string,
    params?: {
      start_date?: string
      end_date?: string
    }
  ): Promise<AttendanceListResponse> => {
    const response = await apiClient.get(`/api/v1/attendance/${employeeId}`, { params })
    return response.data
  },

  /**
   * Mark attendance for an employee
   */
  markAttendance: async (data: AttendanceCreate): Promise<AttendanceResponse> => {
    const response = await apiClient.post('/api/v1/attendance', data)
    return response.data
  },

  /**
   * Update attendance record
   */
  updateAttendance: async (
    recordId: string,
    data: AttendanceUpdate
  ): Promise<AttendanceResponse> => {
    const response = await apiClient.put(`/api/v1/attendance/${recordId}`, data)
    return response.data
  },

  /**
   * Delete attendance record
   */
  deleteAttendance: async (recordId: string): Promise<{ success: boolean; message: string }> => {
    const response = await apiClient.delete(`/api/v1/attendance/${recordId}`)
    return response.data
  },
}
