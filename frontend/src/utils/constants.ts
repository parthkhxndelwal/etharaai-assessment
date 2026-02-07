export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
export const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID || ''
export const APP_NAME = import.meta.env.VITE_APP_NAME || 'Sutra HRMS'

export const DEPARTMENTS = [
  'Engineering',
  'Sales',
  'Marketing',
  'HR',
  'Finance',
  'Operations',
  'Product',
  'Customer Support'
]

export const ATTENDANCE_STATUS = {
  PRESENT: 'Present',
  ABSENT: 'Absent',
  HALF_DAY: 'Half Day',
  LEAVE: 'Leave',
} as const

export const ROUTES = {
  HOME: '/',
  LOGIN: '/login',
  DASHBOARD: '/dashboard',
  EMPLOYEES: '/employees',
  EMPLOYEE_DETAIL: '/employees/:id',
  ATTENDANCE: '/attendance',
} as const
