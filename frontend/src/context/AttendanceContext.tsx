import { createContext, useContext, useState, useCallback, ReactNode, useMemo } from 'react'
import { attendanceApi, AttendanceRecord, AttendanceCreate, AttendanceUpdate } from '../api/attendanceApi'

interface AttendanceContextType {
  records: AttendanceRecord[]
  loading: boolean
  error: string | null
  fetchAttendance: (filters?: {
    employee_id?: string
    date?: string
    start_date?: string
    end_date?: string
    status?: string
  }) => Promise<void>
  fetchEmployeeAttendance: (employeeId: string, filters?: {
    start_date?: string
    end_date?: string
  }) => Promise<void>
  markAttendance: (data: AttendanceCreate) => Promise<void>
  updateAttendance: (recordId: string, data: AttendanceUpdate) => Promise<void>
  removeAttendance: (recordId: string) => Promise<void>
  refreshAttendance: () => Promise<void>
}

const AttendanceContext = createContext<AttendanceContextType | undefined>(undefined)

export const AttendanceProvider = ({ children }: { children: ReactNode }) => {
  const [records, setRecords] = useState<AttendanceRecord[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const fetchAttendance = useCallback(async (filters?: {
    employee_id?: string
    date?: string
    start_date?: string
    end_date?: string
    status?: string
  }) => {
    setLoading(true)
    setError(null)
    try {
      const response = await attendanceApi.getAttendance(filters)
      setRecords(response.data)
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to fetch attendance'
      setError(message)
      throw err
    } finally {
      setLoading(false)
    }
  }, [])

  const fetchEmployeeAttendance = useCallback(async (
    employeeId: string,
    filters?: { start_date?: string; end_date?: string }
  ) => {
    setLoading(true)
    setError(null)
    try {
      const response = await attendanceApi.getEmployeeAttendance(employeeId, filters)
      setRecords(response.data)
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to fetch employee attendance'
      setError(message)
      throw err
    } finally {
      setLoading(false)
    }
  }, [])

  const markAttendance = useCallback(async (data: AttendanceCreate) => {
    setError(null)
    try {
      await attendanceApi.markAttendance(data)
      // Refresh the list
      await fetchAttendance()
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to mark attendance'
      setError(message)
      throw err
    }
  }, [fetchAttendance])

  const updateAttendance = useCallback(async (recordId: string, data: AttendanceUpdate) => {
    setError(null)
    try {
      await attendanceApi.updateAttendance(recordId, data)
      // Refresh the list
      await fetchAttendance()
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to update attendance'
      setError(message)
      throw err
    }
  }, [fetchAttendance])

  const removeAttendance = useCallback(async (recordId: string) => {
    setError(null)
    try {
      await attendanceApi.deleteAttendance(recordId)
      // Remove from local state
      setRecords((prev) => prev.filter((record) => record.id !== recordId))
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to delete attendance'
      setError(message)
      throw err
    }
  }, [])

  const refreshAttendance = useCallback(async () => {
    await fetchAttendance()
  }, [fetchAttendance])

  const value = useMemo(
    () => ({
      records,
      loading,
      error,
      fetchAttendance,
      fetchEmployeeAttendance,
      markAttendance,
      updateAttendance,
      removeAttendance,
      refreshAttendance,
    }),
    [records, loading, error, fetchAttendance, fetchEmployeeAttendance, markAttendance, updateAttendance, removeAttendance, refreshAttendance]
  )

  return <AttendanceContext.Provider value={value}>{children}</AttendanceContext.Provider>
}

export const useAttendance = () => {
  const context = useContext(AttendanceContext)
  if (context === undefined) {
    throw new Error('useAttendance must be used within an AttendanceProvider')
  }
  return context
}
