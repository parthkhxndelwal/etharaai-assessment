import { format, parseISO, isValid } from 'date-fns'

export const formatDate = (date: string | Date, formatStr: string = 'MMM d, yyyy'): string => {
  try {
    const dateObj = typeof date === 'string' ? parseISO(date) : date
    if (!isValid(dateObj)) return 'Invalid date'
    return format(dateObj, formatStr)
  } catch (error) {
    return 'Invalid date'
  }
}

export const formatDateTime = (date: string | Date): string => {
  return formatDate(date, 'MMM d, yyyy h:mm a')
}

export const formatDateISO = (date: Date): string => {
  return format(date, 'yyyy-MM-dd')
}

export const formatPercentage = (value: number): string => {
  return `${value.toFixed(1)}%`
}

export const capitalizeFirst = (str: string): string => {
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase()
}

export const getInitials = (name: string): string => {
  return name
    .split(' ')
    .map(part => part[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
}
