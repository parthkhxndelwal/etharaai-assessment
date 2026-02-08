import { createContext, useContext, useState, useCallback, ReactNode, useMemo } from 'react'
import { employeeApi, Employee, EmployeeCreate, EmployeeUpdate } from '../api/employeeApi'

interface EmployeeContextType {
  employees: Employee[]
  loading: boolean
  error: string | null
  fetchEmployees: (filters?: { department?: string; search?: string }) => Promise<void>
  getEmployee: (employeeId: string) => Promise<Employee | null>
  addEmployee: (data: EmployeeCreate) => Promise<void>
  updateEmployee: (employeeId: string, data: EmployeeUpdate) => Promise<void>
  removeEmployee: (employeeId: string) => Promise<void>
  refreshEmployees: () => Promise<void>
}

const EmployeeContext = createContext<EmployeeContextType | undefined>(undefined)

export const EmployeeProvider = ({ children }: { children: ReactNode }) => {
  const [employees, setEmployees] = useState<Employee[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const fetchEmployees = useCallback(async (filters?: { department?: string; search?: string }) => {
    setLoading(true)
    setError(null)
    try {
      const response = await employeeApi.getEmployees(filters)
      setEmployees(response.data)
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to fetch employees'
      setError(message)
      throw err
    } finally {
      setLoading(false)
    }
  }, [])

  const getEmployee = useCallback(async (employeeId: string): Promise<Employee | null> => {
    setError(null)
    try {
      const response = await employeeApi.getEmployee(employeeId)
      return response.data
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to fetch employee'
      setError(message)
      return null
    }  
  }, [])

  const addEmployee = useCallback(async (data: EmployeeCreate) => {
    setError(null)
    try {
      await employeeApi.createEmployee(data)
      // Refresh the list
      await fetchEmployees()
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to create employee'
      setError(message)
      throw err
    }
  }, [fetchEmployees])

  const updateEmployee = useCallback(async (employeeId: string, data: EmployeeUpdate) => {
    setError(null)
    try {
      await employeeApi.updateEmployee(employeeId, data)
      // Refresh the list
      await fetchEmployees()
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to update employee'
      setError(message)
      throw err
    }
  }, [fetchEmployees])

  const removeEmployee = useCallback(async (employeeId: string) => {
    setError(null)
    try {
      await employeeApi.deleteEmployee(employeeId)
      // Remove from local state
      setEmployees((prev) => prev.filter((emp) => emp.employee_id !== employeeId))
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to delete employee'
      setError(message)
      throw err
    }
  }, [])

  const refreshEmployees = useCallback(async () => {
    await fetchEmployees()
  }, [fetchEmployees])

  const value = useMemo(
    () => ({
      employees,
      loading,
      error,
      fetchEmployees,
      getEmployee,
      addEmployee,
      updateEmployee,
      removeEmployee,
      refreshEmployees,
    }),
    [employees, loading, error, fetchEmployees, getEmployee, addEmployee, updateEmployee, removeEmployee, refreshEmployees]
  )

  return <EmployeeContext.Provider value={value}>{children}</EmployeeContext.Provider>
}

export const useEmployees = () => {
  const context = useContext(EmployeeContext)
  if (context === undefined) {
    throw new Error('useEmployees must be used within an EmployeeProvider')
  }
  return context
}
